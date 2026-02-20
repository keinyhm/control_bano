from odoo import api, models, fields

class ReportIncidencias(models.AbstractModel):
    _name = 'report.centro_incidencias_demo.informe_incidencias'
    _description = 'Informe de incidencias'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['centro.incidencia'].browse(docids)
        return {
            'doc_ids': docids,
            'doc_model': 'centro.incidencia',
            'docs': docs,
            'fields': fields,  # <-- CLAVE para que el QWeb tenga "fields"
        }
