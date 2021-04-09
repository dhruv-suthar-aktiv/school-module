from odoo.exceptions import ValidationError
from odoo import api, fields, models, _, modules


class JobDesignation(models.Model):
    _name='job.designation'
    _rec_name = "position"

    position = fields.Char(string="Position")
    applicants_ids = fields.One2many('job.application','designation_id',string="Applicants")

