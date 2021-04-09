from odoo.exceptions import ValidationError
from odoo import api, fields, models, _, modules

import base64
import re
from datetime import datetime, timedelta


class StudentStudent(models.Model):
    _name = 'student.student'
    _description = 'Student Record'
    _inherit = ['mail.thread', 'mail.activity.mixin','professor.professor']

    @api.model
    def _get_default_image(self):
        with open(modules.get_module_resource('school', 'static/description', 'user.png'), 'rb') as img:
            image = base64.b64encode(img.read())
        return image

    name = fields.Char(string='Name', required=True)
    age = fields.Integer(string='Age', compute="age_calc", store=True)
    photo = fields.Binary(string='Image', default=_get_default_image)

    gender = fields.Selection([('male', 'Male'),
                               ('female', 'Female'),
                               ('others', 'Others')],
                              string='Gender', required=True)

    student_dob = fields.Date(string='Date of birth')

    student_blood_group = fields.Selection([('A+', 'A+ve'), ('B+', 'B+ve'),
                                            ('C+', 'C+ve'), ('D+', 'D+ve'),
                                            ('A-', 'A-ve'), ('B-', 'B-ve'),
                                            ('C-', 'C-ve'), ('D-', 'D-ve')],
                                           string='Blood Group')

    state = fields.Selection([('draft', 'Draft'),
                              ('done', 'Done'),
                              ('cancel', 'Cancel'), ],
                             required=True, default='draft')

    roll_no = fields.Char(string='Roll no.',
                          required=True, copy=False,
                          readonly=True, index=True,
                          default=lambda self: _('New'))

    email = fields.Char(string='Email', required=True)

    onchange_field = fields.Char(string="Onchange gender")

    scheduler_date = fields.Date(
        required=True, string='Scheduler Date', default=datetime.today())

    def scheduler_demo(self):
        for rec in self:
            print("THIS IS REC........", rec)
            rec.scheduler_date += timedelta(days=2)

    @api.model
    def create(self, vals):
        """ Overiding create method to create the roll no sequence """
        if vals.get('name_seq', _('New')) == _('New'):
            vals['roll_no'] = self.env['ir.sequence'].next_by_code(
                'student.student.sequence') or _('New')
            result = super(StudentStudent, self).create(vals)
            return result

    def write(self, vals):
        """ Overiding write method to prevent the updation of email field """
        if vals.get('email') == None:
            vals['email'] = self.email
            result = super(StudentStudent, self).write(vals)
            return result
        else:
            raise ValidationError("Can't change the email address")

    @api.constrains('name')
    def check_name(self):
        """ Checks if the name contains only alphabets"""
        for rec in self:
            if not re.match(r"[a-zA-Z\s]+$", rec.name):
                raise ValidationError('Name should only contain alphabets')

    @api.depends('student_dob')
    def age_calc(self):
        """ Automatically calculate the age by calculating the
                difference of current date and date of birth """
        if self.student_dob is not False:
            self.age = (datetime.today().date() -
                        datetime.strptime(
                str(self.student_dob),
                '%Y-%m-%d').date()) // timedelta(days=365)

    @api.onchange('gender')
    def onchange_calc(self):
        """ Automatically calculate the age by calculating the
                difference of current date and date of birth """
        if self.gender is not False:
            self.onchange_field = self.gender

    # def button_done(self):
    #     """ Logic for the "done" button in the statusbar """
    #     order_confirmed = self.env['sale.order'].search(
    #         [('state', "=", "sale")])
    #     order_browse = self.env['sale.order'].browse(20000000000)
    #     print("CONFIRMED SALES ORDERS.......", order_confirmed)
    #     print("OBJECT USING BROWSE METHOD..........", order_browse)
    #     print("CHECKS IF OBJECT IS SINGLETON.........",
    #           order_confirmed.ensure_one())

        # rec.write({'state': 'done'})

    # def button_reset(self):
    #     """ Logic for the "reset" button in the statusbar """
    #     for rec in self:
    #         rec.state = 'draft'

    def button_done(self):
        student = self.env['student.student'].search([])
        # products = self.env['product.template'].search([('type','=','product'),
        #                                                 ('sale_ok','=',True),
        #                                                 ('purchase_ok','=',True),
        #                                               ])
        products = self.env['product.template'].search([('type','=','product'),
                                                        ('sale_ok','=',True),
                                                        ('purchase_ok','=',True),
                                                      ],limit=2,order='create_date')
        print(f"\n\n\n------products-----------{products.mapped('name')}-----\n\n\n")

        print("CHECK RETURN TYPE OF CREATE METHOD...", student)

    def button_cancel(self):
        """ Logic for the "cancel" button in the statusbar """
        for rec in self:
            rec.write({'state': 'cancel'})

    def _prepare_home_portal_values(self):
        values = super(PortalAccount, self)._prepare_home_portal_values()
        invoice_count = request.env['account.move'].search_count([
            ('type', 'in', ('out_invoice', 'in_invoice', 'out_refund', 'in_refund', 'out_receipt', 'in_receipt')),
        ])
        values['invoice_count'] = invoice_count
        return values

    @api.model
    def student_rec(self):
        list_student = self.env["student.student"].search([])
        return [student.name for student in list_student]
