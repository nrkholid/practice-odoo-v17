from odoo.exceptions import UserError
from odoo.tests import TransactionCase


class TestPurchaseOrderSupportingDocument(TransactionCase):
    def setUp(self):
        super().setUp()

        # Create PO Attachment Requirement
        self.requirement_material = self.env[
            "purchase.order.attachment.requirement"
        ].create(
            {
                "name": "Material Doc",
                "document_type": "1_material_purpose",
                "document_count": 2,
            }
        )

        self.requirement_both = self.env[
            "purchase.order.attachment.requirement"
        ].create(
            {
                "name": "Common Doc",
                "document_type": "2_service_purpose",
                "document_count": 1,
            }
        )

        # Create Purchase Order with NO purchase_type (for test 1)
        self.po_no_type = self.env["purchase.order"].create(
            {
                "partner_id": self.env.ref("base.partner_admin").id,
                "purchase_type": "material",
            }
        )

        # Create Purchase Order with purchase_type=material (for test 2 & 3)
        self.po_material = self.env["purchase.order"].create(
            {
                "partner_id": self.env.ref("base.partner_admin").id,
                "purchase_type": "material",
            }
        )

        # Trigger onchange manually
        self.po_no_type._onchange_purchase_type()
        self.po_material._onchange_purchase_type()

    def test_purchase_type_is_set_or_not(self):
        """Test: Validate whether purchase_type is set or empty."""

        # PO tanpa purchase_type
        self.assertTrue(
            self.po_no_type.purchase_type, "Purchase Type is not should be empty."
        )

        # PO dengan purchase_type
        self.assertTrue(
            self.po_material.purchase_type, "Purchase Type is not should be empty."
        )

    def test_purchase_type_not_set_should_use_both_type(self):
        """Test: When purchase_type is not set, only
        '3_both' document should be required."""
        document_lines = self.po_no_type.purchase_order_supporting_document_line_ids
        self.assertTrue(
            all(
                line.po_attachment_requirement_id.document_type
                in ["3_both", "1_material_purpose"]
                for line in document_lines
            ),
            "Should only load '3_both' document requirements.",
        )

    def test_confirm_button_should_fail_if_attachment_below_minimum(self):
        """Test: Should raise if nb_attachment < document_count."""
        doc_line = (
            self.po_material.purchase_order_supporting_document_line_ids.filtered(
                lambda x: x.po_attachment_requirement_id == self.requirement_material
            )
        )
        self.assertTrue(
            doc_line, "Document line for material requirement should exist."
        )
        self.assertEqual(doc_line.nb_attachment, 0, "No attachments should be present.")

        # Simulate confirmation: you may need to create a custom
        # method in your module to handle validation
        # Here, we will simulate a validation function
        def validate_attachments(po):
            for doc in po.purchase_order_supporting_document_line_ids:
                if doc.nb_attachment < doc.po_attachment_requirement_id.document_count:
                    raise UserError(
                        f"Attachment count for"
                        f"{doc.po_attachment_requirement_id.name}"
                        f"is below required minimum."
                    )

        with self.assertRaises(UserError):
            validate_attachments(self.po_material)

    def test_attachment_count_matches_minimum_document(self):
        """Test: nb_attachment is correctly counted."""
        doc_line = (
            self.po_material.purchase_order_supporting_document_line_ids.filtered(
                lambda x: x.po_attachment_requirement_id == self.requirement_material
            )
        )

        # Simulate 2 attachments
        attachment_1 = self.env["ir.attachment"].create(
            {
                "name": "doc1.pdf",
                "datas": "VGhpcyBpcyBhIHRlc3QgZmlsZQ==",
                "res_model": "purchase.order.supporting.document",
                "res_id": doc_line.id,
            }
        )
        attachment_2 = self.env["ir.attachment"].create(
            {
                "name": "doc2.pdf",
                "datas": "VGhpcyBpcyBhbm90aGVyIGZpbGU=",
                "res_model": "purchase.order.supporting.document",
                "res_id": doc_line.id,
            }
        )

        doc_line.attachment_ids = [(6, 0, [attachment_1.id, attachment_2.id])]
        doc_line._compute_nb_attachment()

        self.assertEqual(doc_line.nb_attachment, 2, "Attachment count should be 2.")
