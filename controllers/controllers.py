# -*- coding: utf-8 -*-
# from odoo import http


# class RentalManagment(http.Controller):
#     @http.route('/rental_managment/rental_managment', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/rental_managment/rental_managment/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('rental_managment.listing', {
#             'root': '/rental_managment/rental_managment',
#             'objects': http.request.env['rental_managment.rental_managment'].search([]),
#         })

#     @http.route('/rental_managment/rental_managment/objects/<model("rental_managment.rental_managment"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('rental_managment.object', {
#             'object': obj
#         })

