from odoo import fields, models


class AuthOAuthProviderGroupMapping(models.Model):
    _name = "auth.oauth.provider.group_mapping"
    _description = "OAuth group mapping"
    _rec_name = "role_name"
    _order = "role_name"

    oauth_provider_id = fields.Many2one(
        "auth.oauth.provider",
        "OAuth Provider",
        required=True,
        ondelete="cascade",
    )

    role_name = fields.Char(
        "Role Name",
        help=("The OAuth Role name"),
    )

    group_ids = fields.Many2many(
        comodel_name="res.groups",
        string="Odoo Groups",
        help="The Odoo groups to assign"
    )
