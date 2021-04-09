from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ManagerManager(models.Model):
    _name = "member.member"
    _description = ''

    partner_id = fields.Many2one("res.partner", string="Name")
    email = fields.Char(string="Email",default=None,related = 'partner_id.email')
    phone = fields.Char(string="Phone",default=None,related = 'partner_id.phone')
    lang = fields.Selection(string="Language",default=None,related = 'partner_id.lang')
    birthdate_date = fields.Date("Birthdate",related="partner_id.birthdate_date")
    age = fields.Integer(string="Age", readonly=True, related="partner_id.age")
