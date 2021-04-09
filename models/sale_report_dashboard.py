from odoo.exceptions import ValidationError
from odoo import api, fields, models, _, modules
from datetime import date,timedelta

class SaleOrder(models.Model):
    _name="testing.testing"

    def get_dashboard_data(self):
        """ Returns the count of confirmed orders of last month """
        sale_orders = self.env['sale.order'].search([('state', '=', 'sale')])
        invoices = self.env['account.move'].search([('invoice_payment_state', '=', 'paid')])
        confirm_count = 0
        invoice_paid_count = 0
        amount_total=0
        products =[]

        for invoice in invoices:
            if invoice.invoice_date.month == date.today().month-1:
                invoice_paid_count+=1


        for order in sale_orders:
            if order.date_order.month == date.today().month-1:
                confirm_count+=1
                amount_total+=order.amount_total
                for saleline in order.order_line:
                    for product in products:
                        if saleline.product_id.name in product_list:
                            product_list[saleline.product_id.name]['qty'] += saleline.product_uom_qty
                    else:
                        product_list[saleline.product_id.name] = {
                        'qty':saleline.product_uom_qty,
                        'uom':saleline.product_uom.name
                        }
        temp_list = []

        for i in product_list.items():
            if i[1].get('qty') > 15:
                temp_list.append({'name':i[0],'qty':i[1].get('qty'),'uom':i[1].get('uom')})



        temp = {'no_confirmed_orders':confirm_count,
                'product_list':product_list,
                'amount_total':amount_total,
                'invoice_paid_count':invoice_paid_count}

        print(f"\n\n\n --------------final dict---------------{temp}-------- \n\n\n")
        print(f"\n\n\n --------------product list---------------{product_list}-------- \n\n\n")

        return temp
