# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Bista First Module',
    'version': '1.0',
    'category': 'Tools',
    'sequence': 2,
    'author': 'Bista-Training-Team-BD-2022',
    'summary': 'Bista employee information',
    'description': "Bista employee information",
    'website': 'https://www.odoo.com/app/employees',
    'depends': [
        'base_setup',
        'sale',
    ],
    'data': [
        # 'security/hr_security.xml',
        'security/ir.model.access.csv',
        'views/bista_employee_views.xml',
        'views/job_position_views.xml',
        'views/employee_skill_views.xml',
        'views/employee_education_views.xml',
        'views/city_information_views.xml',
        'views/res_partner.xml',
        'views/sale_order_extend_view.xml',
        'report/bista_report_saleorder.xml',
        'report/bista_first_addons_reports.xml',
        'report/bista_skill_report_template.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'OPL-1',
}
