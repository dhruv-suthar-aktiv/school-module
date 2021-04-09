from odoo import fields, models, api, _


class SubjectSubject(models.Model):
    _name = 'subject.subject'

    name = fields.Char(string='Name', required=True)
    name_seq = fields.Char(string='Subject Reference',
                           required=True, copy=False,
                           readonly=True, index=True,
                           default=lambda self: _('New'))

    testing = fields.Char(string='Testing')
    professor_id = fields.Many2one(
        'professor.professor', string="Professor ID")

    _sql_constraints = [
        ('subject_uniq', 'unique(name)',
         "There cannot be multiple subjects with same name !"),
    ]

    @api.model
    def create(self, vals):
        """ Overides the create method and assigns the sequence to new record"""
        if vals.get('name_seq', _('New')) == _('New'):
            vals['name_seq'] = self.env['ir.sequence'].next_by_code(
                'subject.subject.sequence') or _('New')
            vals['testing'] = "{} The field value is assigned through overiding".format(
                vals['name_seq'])
            result = super(SubjectSubject, self).create(vals)
            return result

    def name_get(self):
        res = [(rec.id, '%s - %s' % (rec.name_seq, rec.name)) for rec in self]
        return res
