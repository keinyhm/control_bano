from odoo import models, fields, api
from odoo.exceptions import ValidationError


class BathroomVisit(models.Model):
    _name = "control_bano.visit"
    _description = "Visita al baño"
    _order = "start_dt desc, id desc"

    student_name = fields.Char(string="Alumno/a", required=True)

    stage = fields.Selection([
        ("eso", "ESO"),
        ("bach", "Bachillerato"),
        ("fp_basica", "FP Básica"),
        ("fp_medio", "FP Grado Medio"),
        ("fp_superior", "FP Grado Superior"),
    ], string="Etapa", required=True)

    # ESO: 1º a 4º
    eso_level = fields.Selection([
        ("1", "1º"),
        ("2", "2º"),
        ("3", "3º"),
        ("4", "4º"),
    ], string="Curso ESO")

    # Bach y FP: 1º o 2º
    year_12 = fields.Selection([
        ("1", "1º"),
        ("2", "2º"),
    ], string="Curso (1º/2º)")

    group = fields.Selection([
        ("A", "A"),
        ("B", "B"),
        ("C", "C"),
    ], string="Grupo")

    itinerary = fields.Selection([
        ("ciencias", "Ciencias"),
        ("tecnologico", "Tecnológico"),
        ("social", "Social"),
        ("humanidades", "Humanidades"),
    ], string="Itinerario (Bach)")

    course_display = fields.Char(
        string="Curso (texto)",
        compute="_compute_course_display",
        store=True
    )

    start_dt = fields.Datetime(string="Salida")
    end_dt = fields.Datetime(string="Vuelta")

    state = fields.Selection(
        [
            ("draft", "Borrador"),
            ("in_progress", "En curso"),
            ("done", "Finalizada"),
            ("cancelled", "Cancelada"),
        ],
        default="draft",
        required=True
    )

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

            # Grupo (A/B/C) 
            if r.group:
                parts.append(r.group)

            # Itinerario solo tiene sentido en Bach
            if r.stage == "bach" and r.itinerary:
                parts.append(itin_label.get(r.itinerary))

            r.course_display = " ".join([p for p in parts if p]) or ""

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


    def action_start(self):
        for rec in self:
            if rec.state != "draft":
                raise ValidationError("Solo puedes iniciar desde Borrador.")
            if not rec.start_dt:
                rec.start_dt = fields.Datetime.now()
            rec.state = "in_progress"


    def action_finish(self):
        for rec in self:
            if rec.state != "in_progress":
                raise ValidationError("Solo puedes finalizar una visita en curso.")
            if not rec.end_dt:
                rec.end_dt = fields.Datetime.now()
            rec.state = "done"


    def action_cancel(self):
        for rec in self:
            if rec.state in ("done", "cancelled"):
                raise ValidationError("No puedes cancelar una visita finalizada/cancelada.")
            rec.state = "cancelled"


    def write(self, vals):
        # Bloqueo total si está finalizada o cancelada 
        for rec in self:
            if rec.state in ("done", "cancelled"):
                raise ValidationError("No se puede modificar una visita finalizada o cancelada.")
        return super().write(vals)
