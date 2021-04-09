from odoo import models


class SaleOrderReport(models.AbstractModel):
    _name = "report.school.report_saleorder"
    _description = "Sale order report"

    def _get_report_values(self, docids, data=None):
        docs = self.env['sale.order'].browse(docids)
        amount_untaxed, amount_tax, amount_total = 0.0, 0.0, 0.0

        for doc in docs:
            amount_untaxed += doc.amount_untaxed
            amount_tax += doc.amount_tax
            amount_total += doc.amount_total
        return {
            'doc_ids': docs.ids,
            'doc_model': 'sale.order',
            'docs': docs,
            'amount_untaxed': amount_untaxed,
            'amount_tax': amount_tax,
            'amount_total': amount_total,
        }
