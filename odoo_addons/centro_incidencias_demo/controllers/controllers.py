# -*- coding: utf-8 -*-
# from odoo import http


# class CentroIncidenciasDemo(http.Controller):
#     @http.route('/centro_incidencias_demo/centro_incidencias_demo', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/centro_incidencias_demo/centro_incidencias_demo/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('centro_incidencias_demo.listing', {
#             'root': '/centro_incidencias_demo/centro_incidencias_demo',
#             'objects': http.request.env['centro_incidencias_demo.centro_incidencias_demo'].search([]),
#         })

#     @http.route('/centro_incidencias_demo/centro_incidencias_demo/objects/<model("centro_incidencias_demo.centro_incidencias_demo"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('centro_incidencias_demo.object', {
#             'object': obj
#         })

