{
    "name": "Practice Odoo V17",
    "summary": """
    This module for Training Purpose Only
    """,
    "author": "PT. Arkana Solusi Digital",
    "maintainers": ["nrkholid"],
    "category": "Purchase",
    "website": "https://github.com/nrkholid/practice-odoo-v17",
    "version": "17.0.1.0.0",
    "depends": [
        "base",
        "purchase",
    ],
    "license": "LGPL-3",
    "data": [
        "security/ir.model.access.csv",
        "views/purchase_order_attachment_requirement_view.xml",
        "views/purchase_order_inherit_view.xml",
    ],
    # 'post_init_hook': 'post_init_hook',
    "application": False,
    "installable": True,
    "auto_install": False,
    "external_dependencies": {"python": []},
}
