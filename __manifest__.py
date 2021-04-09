# -*- coding: utf-8 -*-
{
    'name': "School Management",
    'version': '13.0.1.0.0',
    'summary': """ Record Student Information """,
    'category': 'Tools',
    'author': "Aktiv Software",

    'description': """
       App for School Management
    """,

    'company': 'Delhi Public School',
    'website': "http://www.aktivsoftware.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale_management', 'project', 'mail', 'contacts',
                'account', 'partner_contact_birthdate','website_event',
                'partner_contact_personal_information_page','query_deluxe',
                'website','website_sale','portal','web_tour','calendar','stock',
                'purchase','hr_attendance','hr'],

    # always loaded
        'data': [
            'views/assests.xml',
            # -----------------------------------------
            # --------------Data Files-----------------
            # -----------------------------------------
            'data/sequence.xml',
            'data/schedule.xml',
            'data/email_template.xml',
            'data/partner_data.xml',
            'data/user_data.xml',
            'data/website_menu.xml',
            # ------------------------------------------
            # --------------Security--------------------
            # ------------------------------------------
            'security/security.xml',
            'security/security_calendar.xml',
            'security/ir.model.access.csv',
            # ---------------------------------------
            # ---------------Views-------------------
            # ---------------------------------------
            'wizards/extra_classes.xml',
            'views/student_view.xml',
            'views/subject_view.xml',
            'views/professor_view.xml',
            'views/test_view.xml',
            'views/assign_class.xml',
            'views/project_views.xml',
            'views/account_view.xml',
            'views/member_view.xml',
            'views/job_designation_view.xml',
            'views/job_application_view.xml',
            'views/sale_order_view.xml',
            'views/welcome_view.xml',
            'views/sale_report_menu.xml',
            'views/product_views.xml',
            'views/purchase_view.xml',
            'views/stock_landed_cost_view.xml',
            # -----------------------------------------
            # ------------Website Templates------------
            # -----------------------------------------
            'views/student_portal_template.xml',
            'views/job_designation_template.xml',
            'views/job_application_portal_template.xml',
            'views/home_template.xml',
            'views/checkout_date_template.xml',
            # -----------------------------------------
            # ---------------Wizards-------------------
            # -----------------------------------------
            'wizards/sale_report.xml',
            # ------------------------------------------
            # ---------------Reports--------------------
            # # ------------------------------------------
            'reports/report.xml',
            'reports/professor_details.xml',
            'reports/sale_report_template.xml',
            'reports/sale_order_wizard_template.xml'
        ],

    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'qweb': [
        "static/src/xml/helloworld_template.xml",
        "static/src/xml/sales_dashboard_template.xml",
    ],
    'images': [],
    'license': 'AGPL-3',
    'installable': True,
    'application': True,
    'auto_install': False,

}
