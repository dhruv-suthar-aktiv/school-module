from odoo import models, fields


class SaleReportWizard(models.TransientModel):
    _name = "sale.report.wizard"
    _description = "Sale Report Wizard"

    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date")

    def print_sale_report_wizard(self):
        """ Fetches the sale order records between start date and end date and
        the report is generated"""


        orders = self.env['sale.order'].search(
            [('date_order', '>=', self.start_date),
             ('date_order', '<=', self.end_date)]
        )

        sale_records = [{'name': order.name,
                         'date_order': order.date_order.date(),
                         'partner_id': order.partner_id.name,
                         'amount_total': order.amount_total,
                         'state': order.state,
                         'invoice': order.invoice_status
                         } for order in orders]

        return self.env.ref(
            'school.action_report_wizard_saleorder').report_action(
            self, data={'order_list': sale_records})
