# -*- coding: utf-8 -*-
# from odoo import http


# class LogModule(http.Controller):
#     @http.route('/log_module/log_module', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/log_module/log_module/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('log_module.listing', {
#             'root': '/log_module/log_module',
#             'objects': http.request.env['log_module.log_module'].search([]),
#         })

#     @http.route('/log_module/log_module/objects/<model("log_module.log_module"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('log_module.object', {
#             'object': obj
#         })

