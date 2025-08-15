from odoo import models, fields, api
from datetime import datetime
from odoo.exceptions import ValidationError


class ClinicPrescriptionLine(models.Model):
    _name = "clinic.prescription.line"
    _description = "Retsept qatori"
    _rec_name = "appointment_id"

    appointment_id = fields.Many2one(comodel_name="clinic.appointment", string="Retsept", required=True, ondelete="cascade")
    medicine_id = fields.Many2one(comodel_name="clinic.medicine", string="Dori", required=True)
    dosage_quantity = fields.Float(string="Miqdor")
    dosage_unit = fields.Selection(
        related="medicine_id.dosage_unit",
        string="Birlik",
        readonly=True
    )
    frequency_per_day = fields.Integer(string="Kuniga necha marta", help="Kun davomida qabul qilish soni")
    duration = fields.Char(string="Davomiylik", help="Masalan: '7 kun', '2 hafta'")
    note = fields.Text(string="Izoh")
    user_age = fields.Integer(compute="_compute_user_age")

    @api.depends('appointment_id')
    def _compute_user_age(self):
        today = datetime.today()
        for rec in self:
            birth_date = rec.appointment_id.patient_id.birth_date
            rec.user_age = today.year - birth_date.year
    
    @api.onchange('medicine_id')
    def age_validation(self):
        for rec in self:
            if rec.user_age<rec.medicine_id.suitable_age:
                raise ValidationError(f"{rec.medicine_id.name} {rec.medicine_id.suitable_age} yoshdan kattlar uchun beriladi.")
