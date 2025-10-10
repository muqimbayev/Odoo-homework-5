# -*- coding: utf-8 -*-
{
    'name': "rental_managment",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'data/ir_sequience.xml',
        'security/groups.xml',
        'security/ir.model.access.csv',
        'views/order_kanban_views.xml',
        'views/order_form_views.xml',
        'views/order_list_views.xml',
        'views/order_search_views.xml',
        'views/customer_kanban_views.xml',
        'views/customer_list_views.xml',
        'views/customer_form_views.xml',
        'views/product_kanban_views.xml',
        'views/product_form_views.xml',
        'views/product_list_views.xml',
        'views/category.xml',
        'views/rental_price.xml',
        'views/Report/order_report.xml',
        'views/Report/order_report_action.xml',
        'views/Report/product_rental_history_report.xml',
        'views/Report/rental_product_history_action.xml',
        'views/Report/price_list_report.xml',
        'views/Report/price_list_action.xml',














        # 'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

