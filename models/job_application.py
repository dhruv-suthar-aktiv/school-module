from odoo.exceptions import ValidationError
from odoo import api, fields, models, _, modules

class JobApplication(models.Model):
    _name = "job.application"

    name = fields.Char(string="Name")
    gender = fields.Selection([('male', 'Male'),
                               ('female', 'Female'),
                               ('others', 'Others')],
                              string='Gender', required=True)

    dob = fields.Date(string='Date of birth',required=True)
    email = fields.Char(string='Email', required=True)
    designation_id = fields.Many2one('job.designation',string="Designation")

