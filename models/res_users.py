# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging

from odoo import api, models, _
from odoo.exceptions import UserError, AccessDenied

from odoo.addons import base
base.models.res_users.USER_PRIVATE_FIELDS.append('oauth_access_token')



try:
    from jose import jwt
    from jose.exceptions import JWSError, JWTError
except ImportError:
    logging.getLogger(__name__).debug("jose library not installed")

_logger = logging.getLogger(__name__)

class ResUsers(models.Model):
    _inherit = 'res.users'

    @api.model
    def _auth_oauth_signin(self, provider, validation, params):
        user_id = super()._auth_oauth_signin(provider, validation, params)
        if not user_id: 
            return user_id
        provider_id = self.env['auth.oauth.provider'].browse(provider)
        SudoUser = self.env["res.users"].sudo().with_context(no_reset_password=True)
        user = SudoUser.search([('login', '=', user_id), ('oauth_provider_id', '=', provider)], limit=1)
        essential_groups = [
            self.env.ref("base.group_user").id,
            self.env.ref("base.group_portal").id,
            self.env.ref("base.group_public").id,
        ]
        groups = []
        if provider_id.only_oauth_groups:
            groups.append((5, False, False))
        
        access_token = user.oauth_access_token
        # Try to decode the token
        claims = jwt.get_unverified_claims(access_token)
        if not claims:
            raise AccessDenied(_("Invalid token"))
        
        # Check if the token contains client specific roles
        if not 'resource_access' in claims:
            raise AccessDenied(_("Invalid token"))
        client_roles = claims['resource_access']
        if not provider_id.client_id in client_roles:
            raise AccessDenied(_("Invalid token"))
        client_roles = client_roles[provider_id.client_id]
        if not 'roles' in client_roles:
            raise AccessDenied(_("Invalid token"))
        client_roles = client_roles['roles']
        # Check if the user has any of the roles
        if not any([role in client_roles for role in provider_id.group_mapping_ids.mapped('role_name')]):
            raise AccessDenied(_("Invalid token"))
        
        # Assign the groups
        for mapping in provider_id.group_mapping_ids:
            if mapping.role_name in client_roles:
                for group in mapping.group_ids:
                    groups.append((4, group.id, False))

        if (
            provider_id.only_oauth_groups
            and len([g[1] for g in groups if g[0] == 4 and g[1] in essential_groups])
            != 1
        ):
            raise UserError(
                _(
                    "The created user needs to have one (and only one) of the"
                    " 'User types /' groups defined."
                )
            )
        user.write({"groups_id": groups})
        return user_id
