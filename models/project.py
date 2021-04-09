from odoo import fields, models, api, _
from odoo.exceptions import ValidationError

from datetime import datetime, timedelta, date
# from dateutil.relativedelta import relativedelta


class ProjectManagement(models.Model):
    _inherit = 'project.project'

    end_date = fields.Datetime(string='Date')
    no_of_days = fields.Integer(
        string='No. of days', compute="days_calc", store=True)

    @api.depends('create_date', 'end_date')
    def days_calc(self):
        """ Calculates the difference between create date and end date"""
        for rec in self:
            if rec.create_date and rec.end_date:
                create_date = rec.create_date.date()
                end_date = rec.end_date.date()
                rec.no_of_days = (end_date - create_date).days
            else:
                rec.create_date = datetime.now()

    @api.model
    def default_get(self, fields):
        res = super(ProjectManagement, self).default_get(fields)
        res['end_date'] = datetime.now()
        return res

    @api.constrains('create_date', 'end_date')
    def check_date(self):
        for record in self:
            if record.create_date and record.end_date and record.create_date > record.end_date:
                raise ValidationError(
                    "End date cannot be less then start date")
