{'name': 'Centro - Incidencias (Demo)', 
'version': '1.0', 
'summary': 'Módulo de ejemplo para aprendizaje de Odoo', 
'depends': ['base'], 
'data': [
    'security/ir.model.access.csv', 
    'reports/accion_incidencias_report.xml', 
    'reports/action_incidencias_server.xml',
    'reports/incidencias_report.xml', 
    'views/incidencia_menu.xml', 
    'views/incidencia_list_view.xml', 
    'views/incidencia_form_view.xml'], 
    'installable': True, 
    'application': True}
