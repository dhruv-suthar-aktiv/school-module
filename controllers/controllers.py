# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request, Controller
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager
from odoo.addons.website_form.controllers.main import WebsiteForm
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.addons.website_sale.controllers.main import Website

import json
from datetime import datetime



# class WebsiteSale(WebsiteSale):

#     @http.route(['/shop/cart'], type='http', auth="public", website=True,
#                     sitemap=False)
#     def cart(self,**post):
#         print("\n\n Hello the cart method is calling \n\n")
#         res = super(WebsiteSale,self).cart(**post)
#         # print("\n\n\n\n\n This is cart  {} \n\n\n\n", res.values)
#         return res

class JobApplication(http.Controller):

    # MANDETORY_FIELD = ["name","email","dob"]

    @http.route('/my/applications', type='http', auth='public', website=True)
    def job_application_list(self, **kw):
        """ Returns The Records of the Job Applications """
        applications = request.env['job.application'].search([])
        return request.render("school.portal_my_application", {
            'applications': applications
        })


    @http.route('/designation/', type='http', auth='public', website=True)
    def job_designation_list(self, **kw):
        """ Returns the list of departments """
        job_designation = request.env['job.designation'].search([])
        return request.render("school.job_designation_view", {
            'job_designation': job_designation
        })

    @http.route(['/designation/<model("job.designation"):designation>'],
                type='http', auth="public", website=True)
    def job_application_form(self, designation, **kw):
        """ Returns the job application form for department selected for creating"""
        values = {
            'error': {},
            'error_message': [],
            'condition': True
        }
        values.update({'designation_id': designation.id})
        return request.render("school.job_application_form", values)

    @http.route(['/edit/<model("job.application"):application>'],
                type='http', auth="public", website=True)
    def edit_job_application_form(self, application, **kw):
        """ Returns the job application form for editing"""
        return request.render("school.job_application_form", {
            'designation_id': application.designation_id.id,
            'record': application
        })

# ************************************************************************************
# ****************** Edit job application records through popup **********************
# ************************************************************************************

    @http.route('/updatepopup/', type='http', auth="public",
                methods=['POST'], website=True)
    def update_job_application_save_action(self,**post):
        """ Updates the form data in the backend model(Update Action) through
            the popup """

        applicant = request.env['job.application'].browse(
            post.get('application_id'))
        applicant.write({
            'name': post.get('name'),
            'gender': post.get('gender'),
            'dob': post.get('dob'),
            'email': post.get('email'),
        })
        return request.redirect('/thanks')


# ************************************************************************************
# ******************VADIATION THROUGH "o_website_form_send****************************
# ************************************************************************************


class WebsiteForm(WebsiteForm):

    @http.route('/submit/<string:model_name>', type='http', auth="public",
                methods=['POST'], website=True)
    def submit_job_application(self, model_name, **post):
        """ Stores the application form data in the backend model(Submit Action) """
        applicant = request.env['job.application'].create({
            'name': post.get('name'),
            'gender': post.get('gender'),
            'dob': post.get('dob'),
            'email': post.get('email'),
            'designation_id': post.get('designation_id'),
        })
        return json.dumps({'id': applicant.id})

    @http.route('/update/<string:model_name>', type='http', auth="public",
                methods=['POST'], website=True)
    def update_job_application(self, model_name, **post):
        """ Updates the form data in the backend model(Update Action) """

        print("\n\n\n\n INSIDEEEEE \n\n\n\n ")
        applicant = request.env['job.application'].browse(
            post.get('application_id'))
        applicant.write({
            'name': post.get('name'),
            'gender': post.get('gender'),
            'dob': post.get('dob'),
            'email': post.get('email'),
            'designation_id': post.get('designation_id'),
        })
        return json.dumps({'id': applicant.id})

    @http.route('/thanks/', type='http', auth="public", website=True)
    def thankyou(self, **kw):
        """ Renders the success message """
        return request.render("school.page_thankyou")


# ******************************************************************************
# *************************VADIATION THROUGH PYTHON ****************************
# ******************************************************************************

    # @http.route('/submit', type='http', auth='public', website=True)
    # def submit_job_application(self, **kwargs):
    #     values = {
    #         'error': {},
    #         'error_message': [],
    #         'condition': True
    #     }

    #     if kwargs and request.httprequest.method == 'POST':
    #         error, error_message = self.details_form_validate(kwargs)
    #         values.update({'error': error, 'error_message': error_message})
    #         values.update(kwargs)
    #         values.update(
    #             {'condition': values.get('error').get('name', False)})
    #         print("\n\n\n THIS IS ERROR ...........",values.get('error_messager'))
    #         if not error:
    #             request.env['job.application'].sudo().create(kwargs)
    #             return request.render('school.page_thankyou', {})
    #         else:
    #             return request.render('school.designation_form', values)

    # def details_form_validate(self, data):
    #     """ Logic for validation of form fields """
    #     error = dict()
    #     error_message = []

    #     # Validation
    #     for field_name in self.MANDETORY_FIELD:
    #         if not data.get(field_name):
    #             print("\n\n----missing-----\n\n")
    #             error[field_name] = 'missing'
    #     if [err for err in error.values() if err == 'missing']:
    #         error_message.append(('Some required fields are empty.'))

    #     return error, error_message


# ******************************************************************************
# *************************STUDENT FORM ACTIONS ********************************
# ******************************************************************************

class StudentRecord(http.Controller):

    @http.route(['/student'], type='http', auth="user", website=True)
    def student_record(self,**kw):
        return http.request.render('school.student_form')

    @http.route('/create-student/', type='json', auth="public", website=True)
    def submit_student(self, **post):
        """ Stores student form data in the backend model(Submit Action) """
        print("\n\n\n----------post---{}------\n\n\n".format(post))
        # print("\n\n\n dob {} dob type {} \n\n\n".post.get('dob'),type(post.get('dob')))
        student = request.env['student.student'].create({
            'name': post.get('name'),
            'gender': post.get('gender'),
            'student_dob': datetime.strptime(post.get('student_dob'), '%Y-%m-%d').date(),
            'email': post.get('email'),
        })
        return True
