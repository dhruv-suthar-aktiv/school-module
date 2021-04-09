from odoo.exceptions import ValidationError
from odoo import fields,api, models, _

class Channel(models.Model):
    _inherit = 'mail.channel'

    @api.model
    def send_message(self):
        partner = 3
        odoobot_id = self.env['ir.model.data'].xmlid_to_res_id("base.partner_root")
        channel = self.with_context(mail_create_nosubscribe=True).create({
                'channel_partner_ids': [(4, odoobot_id),(4, partner)],
                'public': 'public',
                'channel_type': 'chat',
                'email_send': True,
                'name': 'Custom'
            })
        message = _("Hello Mitchell, how's you?")
        var = channel.sudo().message_post(body=message, author_id=odoobot_id, message_type="comment", subtype="mail.mt_comment")
        print(f"\n\n\n ---- var -{var}----\n\n\n")
        # self.env.user.odoobot_state = 'onboarding_emoji'
