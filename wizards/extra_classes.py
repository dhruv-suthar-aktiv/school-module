from odoo import fields, models, api, _
from odoo.exceptions import ValidationError
from datetime import datetime


class ExtraClasses(models.TransientModel):
    _name = 'extra.classes'
    professor_id = fields.Many2one('professor.professor', string='professor')
    subject_id = fields.Many2one('subject.subject', string='subject')
    class_date = fields.Date(string='Date')
    subject_code = fields.Char(
        string='Subject Code', required=True)

    def assign_class(self):
        """ Assigns the extra class to the professor """
        for rec in self:
            extra_class = self.env['assign.class'].create(
                {'professor_id': rec.professor_id.id,
                 'subject_id': rec.subject_id.id,
                 'subject_code': rec.subject_code,
                 'class_date': rec.class_date})
            print(extra_class)

    @api.constrains('class_date')
    def check_name(self):
        """ Checks if the date selected is valid """
        for rec in self:
            diff = (datetime.strptime(
                str(self.class_date), '%Y-%m-%d').date() - datetime.today().date()).days
            if diff < 0:
                raise ValidationError(
                    'Date selected should not be less then today')

    @api.onchange('professor_id')
    def onchange_professor_id(self):
        """ Subjects which a professor is assigned are only shown in dropdown """
        for rec in self:
            return {
                'domain': {
                    'subject_id': [('professor_id', "=", rec.professor_id.id)]
                }
            }

    @api.onchange('subject_id')
    def onchange_subject_id(self):
        """ Subject code is automatically selected based on subject name """
        for rec in self:
            if rec.subject_id:
                rec.subject_code = rec.subject_id.name_seq
