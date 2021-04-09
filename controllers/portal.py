from collections import OrderedDict
from operator import itemgetter

from odoo import http, _
from odoo.exceptions import AccessError, MissingError
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager
from odoo.tools import groupby as groupbyelem

from odoo.osv.expression import OR


class CustomerPortal(CustomerPortal):

    def _prepare_home_portal_values(self):
        """ Returns the count of the student and job applications """
        values = super(CustomerPortal, self)._prepare_home_portal_values()
        values['student_count'] = request.env['student.student'].search_count([
        ])
        values['application_count'] = request.env['job.application'].search_count([
        ])
        return values

    @http.route(['/my/students', '/my/students/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_students(self, page=1, sortby=None, **kw):
        """ Sortby values and pager functionality """
        values = self._prepare_portal_layout_values()
        StudentStudent = request.env['student.student']

        searchbar_sortings = {
            'date': {'label': _('Newest'), 'order': 'create_date desc'},
            'name': {'label': _('Name'), 'order': 'name'},
            'age': {'label': _('Age'), 'order': 'age'},
        }
        if not sortby:
            sortby = 'date'
        order = searchbar_sortings[sortby]['order']

        # projects count
        student_count = StudentStudent.search_count([])
        # pager
        pager = portal_pager(
            url="/my/students",
            url_args={'sortby': sortby},
            total=student_count,
            page=page,
            step=15
        )

        # content according to pager and archive selected
        students = StudentStudent.search(
            [], order=order, limit=15, offset=pager['offset'])
        # request.session['my_students_history'] = students.ids[:100]

        values.update({
            # 'date': date_begin,
            # 'date_end': date_end,
            'students': students,
            'page_name': 'Students',
            # 'archive_groups': archive_groups,
            # 'default_url': '/my/students',
            'pager': pager,
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby
        })
        return request.render("school.portal_my_students", values)

    @http.route(['/my/applications', '/my/applications/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_applications(self, page=1, sortby=None, **kw):
        """ Sortby values and pager functionality """
        values = self._prepare_portal_layout_values()
        JobApplication = request.env['job.application']
        searchbar_sortings = {
            'date': {'label': _('Newest'), 'order': 'create_date desc'},
            'dob': {'label': _('Date of birth'), 'order': 'dob'},
        }

        if not sortby:
            sortby = 'date'
        order = searchbar_sortings[sortby]['order']

        # Job Application count
        application_count = JobApplication.search_count([])

        # pager
        pager = portal_pager(
            url="/my/applications",
            url_args={'sortby': sortby},
            total=application_count,
            page=page,
            step=4
        )

        applications = JobApplication.search(
            [], order=order, limit=4, offset=pager['offset'])
        # request.session['my_students_history'] = students.ids[:100]

        values.update({
            'applications': applications,
            'page_name': 'Job Applications',
            'pager': pager,
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby
        })
        return request.render("school.portal_my_application", values)
