from odoo import fields, models, api, _, modules

from datetime import datetime, timedelta
import base64


class ProfessorProfessor(models.Model):
    _name = 'professor.professor'

    @api.model
    def _get_default_image(self):
        """ Return the default image for New records"""
        with open(modules.get_module_resource('school', 'static/description', 'user.png'), 'rb') as img:
            image = base64.b64encode(img.read())
        return image

    def get_class_count(self):
        """ Return the count of number of classes assigned to respective professor"""
        for rec in self:
            count = self.env['assign.class'].search_count(
                [('professor_id', '=', rec.id)])
            rec.extra_class_count = count

    name = fields.Char(string='Name', required=True)
    age = fields.Integer(string='Age', compute="age_calc", store=True)
    photo = fields.Binary(string='Image')
    gender = fields.Selection([('male', 'Male'),
                               ('female', 'Female'),
                               ('others', 'Others')],
                              string='Gender')

    professor_dob = fields.Date(string='Date of birth')

    professor_blood_group = fields.Selection([('A+', 'A+ve'), ('B+', 'B+ve'),
                                              ('C+', 'C+ve'), ('D+', 'D+ve'),
                                              ('A-', 'A-ve'), ('B-', 'B-ve'),
                                              ('C-', 'C-ve'), ('D-', 'D-ve')],
                                             string='Blood Group')

    name_seq = fields.Char(string='Student Reference',
                           required=True, copy=False,
                           readonly=True, index=True,
                           default=lambda self: _('New'))

    subject_ids = fields.One2many(
        'subject.subject', 'professor_id', string="Subject ID")

    extra_class_count = fields.Integer(
        string="Extra Class", compute=get_class_count)
    color = fields.Integer('Color Index')
    priority = fields.Selection(
        [('0', 'Low'),
         ('1', 'Normal'),
         ('2', 'High')],
        string='Priority', default='1')
    kanban_state = fields.Selection(
        [('Jr. Prof', 'Junior Professor'),
         ('Ast. Prof', 'Assistant Professor'),
         ('Sr. Prof', 'Senior Professor')],
        string='Position', default='Jr. Prof')
    scheduler_date = fields.Date(
        required=True, string='Scheduler Date', default=datetime.today())

    student_ids = fields.Many2many(
        'student.student', 'professor_student_rel', string="Students")

    @api.model
    def create(self, vals):
        """ Overides the create method and assigns the
            sequence to new record"""
        if vals.get('name_seq', _('New')) == _('New'):
            vals['name_seq'] = self.env['ir.sequence'].next_by_code(
                'professor.professor.sequence') or _('New')
            result = super(ProfessorProfessor, self).create(vals)
            return result

    @api.depends('professor_dob')
    def age_calc(self):
        """ Automatically calculate the age by calculating the
            difference of current date and date of birth """
        if self.professor_dob is not False:
            self.age = (datetime.today().date()-datetime.strptime(
                str(self.professor_dob), '%Y-%m-%d').date()) // timedelta(days=365)

    def scheduler_demo(self):
        professor_record = self.env['professor.professor'].search([])
        for rec in professor_record:
            print("THIS IS REC........", rec)
            rec.write({
                'scheduler_date': rec.scheduler_date+timedelta(days=2)
            })

    def open_professor_classes(self):
        """ Redirects to the Extra Classes Tree View """
        return{
            'name': _("Extra Classes"),
            'domain': [('professor_id', '=', self.id)],
            'res_model': 'assign.class',
            'context':{'default_professor_id': self.id},
            'view_id': False,
            'view_mode': 'tree,form',
            'type': 'ir.actions.act_window',
        }
