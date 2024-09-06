# Copyright 2012-2018 Therp BV <https://therp.nl>
# Copyright 2018 Brainbean Apps <https://brainbeanapps.com>
# Copyright 2021 Tecnativa - João Marques
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from logging import getLogger

from odoo import _, api, fields, models
from odoo.exceptions import UserError

_logger = getLogger(__name__)


class AuthOAuthProvider(models.Model):
    _inherit = "auth.oauth.provider"

    group_mapping_ids = fields.One2many(
        "auth.oauth.provider.group_mapping",
        "oauth_provider_id",
        "Group mappings",
        help="Define how Odoo groups are assigned to OAuth users",
    )
    only_oauth_groups = fields.Boolean(
        "Only OAuth groups",
        default=False,
        help=(
            "If this is checked, manual changes to group membership are "
            "undone on every login (so Odoo groups are always synchronous "
            "with OAuth groups). If not, manually added groups are preserved."
        ),
    )
