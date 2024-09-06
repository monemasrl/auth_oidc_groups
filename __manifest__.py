# Copyright 2024 Monema S.r.l. <https://monema.it>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "OIDC Groups assignment",
    "description": """
        Adds user accounts to groups based on rules defined by the administrator.
    """,
    "author": "Monema S.r.l.",
    "website": "https://github.com/monemasrl/auth_oidc_groups/",
    "category": "Authentication",
    "license": "AGPL-3",
    "version": "16.0.0.0.1",
    "summary": "Adds user accounts to groups based on rules defined "
    "by the administrator.",
    # any module necessary for this one to work correctly
    "depends": [
        "base",
        "auth_oauth",
        "auth_oidc",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/auth_oauth_views.xml",
    ],
    "application": False,
}
