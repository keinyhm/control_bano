from odoo import models, fields, api


class CentroIncidencia(models.Model):
    _name = 'centro.incidencia'
    _description = 'Incidencia interna (demo)'

    name = fields.Char(string='Título', required=True)
    description = fields.Text(string='Descripción')
    date = fields.Datetime(string='Fecha', default=fields.Datetime.now)
    state = fields.Selection([
        ('open', 'Abierta'),
        ('in_progress', 'En proceso'),
        ('closed', 'Cerrada')
    ], string='Estado', default='open')

    def action_in_progress(self):
        for record in self:
            record.state = 'in_progress'

    def action_close(self):
        for record in self:
            record.state = 'closed'


    def action_print_report(self):
        # Genera un informe PDF con todas las incidencias seleccionadas
        # Dominio aplicado en la vista lista
        domain = self.env.context.get('active_domain', [])
        incidencias = self.search(domain)

        # Seguridad mínima: si no hay registros, no generar informe
        if not incidencias:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Sin incidencias',
                    'message': 'El filtro actual no devuelve incidencias.',
                    'type': 'warning',
                }
            }

        # Llamamos a la acción de informe definida en XML
        return self.env.ref(
            'centro_incidencias_demo.action_report_incidencias'
        ).report_action(incidencias)


    state_label = fields.Char(
        string='Estado',
        compute='_compute_state_label',
        store=False
    )


    @api.depends('state')
    def _compute_state_label(self):
        """
        Calcula la etiqueta visible del estado
        a partir del valor almacenado.
        """
        for record in self:
            record.state_label = dict(
                self._fields['state'].selection
            ).get(record.state)

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['centro.incidencia'].browse(docids)
        return {
            'docs': docs,
            'today': fields.Datetime.now(),
        }