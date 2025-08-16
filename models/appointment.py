from odoo import models, fields, api

class Appointment(models.Model):
    _name = "clinic.appointment"
    _description = "Qabul"
    _rec_name = "title_field"

    doctor_id = fields.Many2one(comodel_name="clinic.doctor", required=True, string="Doktor")
    patient_id = fields.Many2one(comodel_name="clinic.patient", required=True, string="Bemor")
    start_time = fields.Datetime(string="Boshlanish vaqti", required=True)
    end_time = fields.Datetime(string="Tugash vaqti", required=True)
    status = fields.Selection([
        ("new", "Yangi"),
        ("treated", "Davolanmoqda"),
        ("recovered", "Sog'aygan"),
        ("canceled", "Bekor qilingan")
    ], default="new", string="Status")
    prescription_line_ids = fields.One2many(comodel_name="clinic.prescription.line", inverse_name="appointment_id")
    disease_name = fields.Char(string="Kasallik nomi")
    medicine_name = fields.Char(string="Dorilar ro'yxati", compute="_compute_medicine_name")
    title_field = fields.Char(compute="_compute_title_field")

    @api.depends('prescription_line_ids')
    def _compute_medicine_name(self):
        for record in self:
            record.medicine_name = ", ".join((record.prescription_line_ids.mapped('medicine_id.name')))

    def action_treated(self):
        for record in self:
            record.status="treated"

    def action_recovered(self):
        for record in self:
            record.status="recovered"

    def action_canceled(self):
        for record in self:
            record.status="canceled"

    @api.depends('patient_id')
    def _compute_title_field(self):
        for record in self:
            record.title_field = f"Qabul-{record.patient_id.full_name}"

    
    