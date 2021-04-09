from odoo import fields, models, api, _, modules

from datetime import datetime, date, timedelta


class AccountInherit(models.Model):
    _inherit = 'account.move'

#******************************************************************************
#********************* SEND EMAIL THROUGH WIZARD ******************************
#*********************This one is called through button ***********************

    def action_send_email(self):
        """ Opens the wizard for composing mail with the corresponding data """
        self.ensure_one()
        ir_model_data = self.env['ir.model.data']
        try:
            template_id = ir_model_data.get_object_reference('school',
                                            'due_date_reminder_email')[1]
        except ValueError:
            template_id = False
        try:
            compose_form_id = ir_model_data.get_object_reference('mail',
                                      'email_compose_message_wizard_form')[1]
        except ValueError:
            compose_form_id = False

        ctx = {
            'default_model': 'account.move',
            'default_res_id': self.ids[0],
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
            'mark_so_as_sent': True,
            'force_email': True
        }

        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form_id, 'form')],
            'view_id': compose_form_id,
            'target': 'new',
            'context': ctx,
        }

    def date_scheduler(self):
        """ Scheduler action which will automatically send the mail whose time
            period for due date is less then two days """
        for invoice in self.search([('type', '=', 'out_invoice'),
                                    ('amount_residual', '>', 0),
                                    ('state', '=', 'posted')]):
            if(invoice.invoice_date_due - date.today()).days < 2:
                invoice.action_send_email()
                print("\n\n\n Check Email log.....")



#******************************************************************************
#*********** SEND EMAIL DIRECTLY WITHOUT OPENING THE WIZARD *******************
#********************* called through schedule action *************************
    # def action_send_email(self):
    #     """ Logic for getting email template and sending the mail """
    #     template_id = self.env.ref('school.due_date_reminder_email').id
    #     self.env['mail.template_id'].browse(
    #         template_id).send_mail(self.id, force_send=True)
