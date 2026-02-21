from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime


class BathroomVisit(models.Model):
    _name = "control_bano.visit"
    _description = "Visita al baño"
    _order = "start_dt desc, id desc"

    #student_name = fields.Char(string="Alumno/a", required=True)

    student_id = fields.Many2one('res.partner', string="Alumno/a (Contacto)", required=True)

    stage = fields.Selection(
        [
            ("eso", "ESO"),
            ("bach", "Bachillerato"),
            ("fp_basica", "FP Básica"),
            ("fp_medio", "FP Grado Medio"),
            ("fp_superior", "FP Grado Superior"),
        ],
        string="Etapa",
        required=True,
    )

    # ESO: 1º a 4º
    eso_level = fields.Selection(
        [("1", "1º"), ("2", "2º"), ("3", "3º"), ("4", "4º")],
        string="Curso ESO",
    )

    # Bach y FP: 1º o 2º
    year_12 = fields.Selection(
        [("1", "1º"), ("2", "2º")],
        string="Curso (1º/2º)",
    )

    group = fields.Selection(
        [("A", "A"), ("B", "B"), ("C", "C")],
        string="Grupo",
    )

    itinerary = fields.Selection(
        [
            ("ciencias", "Ciencias"),
            ("tecnologico", "Tecnológico"),
            ("social", "Social"),
            ("humanidades", "Humanidades"),
        ],
        string="Itinerario (Bach)",
    )

    course_display = fields.Char(
        string="Curso (texto)",
        compute="_compute_course_display",
        store=True,
        readonly=True,
    )

    start_dt = fields.Datetime(string="Salida")
    end_dt = fields.Datetime(string="Vuelta")

    # Para dashboard / graph / pivot (KPI)
    duration_minutes = fields.Float(
        string="Duración (min)",
        compute="_compute_duration_minutes",
        store=True,
        readonly=True,
    )

    state = fields.Selection(
        [
            ("draft", "Borrador"),
            ("in_progress", "En curso"),
            ("done", "Finalizada"),
            ("cancelled", "Cancelada"),
        ],
        default="draft",
        required=True,
    )

    # ----------------------------
    # COMPUTES
    # ----------------------------
    @api.depends("stage", "eso_level", "year_12", "group", "itinerary")
    def _compute_course_display(self):
        stage_label = dict(self._fields["stage"].selection)
        eso_label = dict(self._fields["eso_level"].selection)
        y12_label = dict(self._fields["year_12"].selection)
        itin_label = dict(self._fields["itinerary"].selection)

        for r in self:
            parts = []
            if r.stage:
                parts.append(stage_label.get(r.stage))

            # Nivel según etapa
            if r.stage == "eso":
                if r.eso_level:
                    parts.append(eso_label.get(r.eso_level))
            else:
                if r.year_12:
                    parts.append(y12_label.get(r.year_12))

            # Grupo
            if r.group:
                parts.append(r.group)

            # Itinerario solo en Bach
            if r.stage == "bach" and r.itinerary:
                parts.append(itin_label.get(r.itinerary))

            r.course_display = " ".join([p for p in parts if p]) or ""

    @api.depends("start_dt", "end_dt")
    def _compute_duration_minutes(self):
        for r in self:
            if r.start_dt and r.end_dt:
                delta = r.end_dt - r.start_dt
                r.duration_minutes = delta.total_seconds() / 60.0
            else:
                r.duration_minutes = 0.0

    # ----------------------------
    # ONCHANGE / CONSTRAINTS
    # ----------------------------
    @api.onchange("stage")
    def _onchange_stage(self):
        """Limpia campos que no aplican al cambiar de etapa."""
        for r in self:
            if r.stage == "eso":
                r.year_12 = False
                r.itinerary = False
            else:
                r.eso_level = False
                if r.stage != "bach":
                    r.itinerary = False

    @api.constrains("start_dt", "end_dt")
    def _check_dates(self):
        for r in self:
            if r.start_dt and r.end_dt and r.end_dt < r.start_dt:
                raise ValidationError(_("La fecha/hora de vuelta no puede ser anterior a la salida."))

    # ----------------------------
    # ACTIONS (BOTONES)
    # ----------------------------
    def action_start(self):
        for rec in self:
            if rec.state != "draft":
                raise ValidationError(_("Solo puedes iniciar desde Borrador."))
            if not rec.start_dt:
                rec.start_dt = fields.Datetime.now()
            rec.state = "in_progress"

    def action_finish(self):
        for rec in self:
            if rec.state != "in_progress":
                raise ValidationError(_("Solo puedes finalizar una visita en curso."))
            if not rec.end_dt:
                rec.end_dt = fields.Datetime.now()
            rec.state = "done"

    def action_cancel(self):
        for rec in self:
            if rec.state in ("done", "cancelled"):
                raise ValidationError(_("No puedes cancelar una visita finalizada/cancelada."))
            rec.state = "cancelled"

    # ----------------------------
    # BLOQUEO DE EDICIÓN
    # ----------------------------
    def write(self, vals):
        """
        Bloquea edición manual si ya está Finalizada/Cancelada.
        PERO permite cambios "de sistema" que solo toquen state/end_dt
        (por ejemplo al finalizar/cancelar).
        """
        protected_states = ("done", "cancelled")
        allowed_when_protected = {"state", "end_dt"}  # lo mínimo para cerrar

        for rec in self:
            if rec.state in protected_states:
                # Si intentan cambiar algo fuera de lo permitido, bloquea
                if any(k not in allowed_when_protected for k in vals.keys()):
                    raise ValidationError(_("No se puede modificar una visita finalizada o cancelada."))

        return super().write(vals)

    def unlink(self):
        for rec in self:
            if rec.state in ("done", "cancelled"):
                raise ValidationError(_("No se puede eliminar una visita finalizada o cancelada."))
        return super().unlink()


    def action_done_all(self):
            """Lógica de servidor para finalizar visitas masivamente (Fase 5)"""
            # Filtramos solo las que están 'in_progress' para no dar error de validación
            records_to_close = self.filtered(lambda r: r.state == 'in_progress')
            for record in records_to_close:
                record.write({
                    'state': 'done',
                    'end_dt': fields.Datetime.now()
                })
            return True

    @api.constrains('student_name', 'state')
    def _check_active_visit(self):
        """Integración/Lógica: Evita que un alumno tenga dos visitas abiertas a la vez"""
        for r in self:
            if r.state == 'in_progress':
                already_out = self.search([
                    ('student_name', '=', r.student_name),
                    ('state', '=', 'in_progress'),
                    ('id', '!=', r.id)
                ])
                if already_out:
                    raise ValidationError(_("El alumno %s ya tiene una visita en curso.") % r.student_name)

    def action_import_validation(self):
        """Lógica para validar datos integrados desde fuentes externas"""
        for record in self:
            if not record.student_name:
                continue
            record.student_name = record.student_name.strip().title()