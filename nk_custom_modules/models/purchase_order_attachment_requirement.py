from odoo import fields, models


class PurchaseOrderAttachmentRequirement(models.Model):
    _name = "purchase.order.attachment.requirement"
    _description = "Purchase Order Attachment Requirement"

    name = fields.Char("Document Name", required=True, index=True)
    document_type = fields.Selection(
        [
            ("1_material_purpose", "Material Purpose"),
            ("2_service_purpose", "Service Purpose"),
            ("3_both", "Both"),
        ],
        required=True,
        index=True,
    )
    document_count = fields.Integer(
        default=1,
        help="Setup with Minimum Number of Document that need to provide",
    )
    is_mandatory = fields.Boolean("Mandatory")
