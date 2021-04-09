from odoo import fields, models, api, _
from odoo.exceptions import ValidationError

from datetime import datetime, timedelta


class SubjectLine(models.Model):
    _name = "subject.line"
    professor_id = fields.Many2one(
        'professor.professor', string="Professor id")

    subject_id = fields.Many2one(
        'subject.subject', string="Subject id")

    subject_name = fields.Char(default=None,related = 'subject_id.name')
    subject_testing = fields.Char(default=None,related = 'subject_id.testing')
    # _sql_constraints = [
    #     ('subject_unique', 'unique(professor_id, subject_id)',
    #      _("Cannot assign same subjects to multiple professor")),
    # ]


    @api.constrains('subject_id')
    def _check_unique_subjects(self):
        for rec in self:
            result = self.search(
                [('subject_id', '=', rec.subject_id.id)])
            if result:
                raise ValidationError(
                    "Subject is already assigned to professor")
