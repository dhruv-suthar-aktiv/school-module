from odoo import fields, models, api, _


class AssignClass(models.Model):
    _name = 'assign.class'
    _description = ''

    professor_id = fields.Many2one('professor.professor', string='professor')
    subject_id = fields.Many2one('subject.subject', string='subject')
    class_date = fields.Date(string='Date')
    subject_code = fields.Char(string='Subject Code')

    @api.onchange('professor_id')
    def onchange_professor_id(self):
        """ Subjects which a professor is assigned are only shown in dropdown """
        for rec in self:
            return {
                'domain': {
                    'subject_id': [('professor_id', "=", rec.professor_id.id)]
                }
            }
