from odoo import models, fields

class Doctor(models.Model):
    _name = "clinic.doctor"
    _description = "Doktor"
    _rec_name = "full_name"

    full_name = fields.Char(string="To'liq ism familyasi", required=True)
    specialty = fields.Char(string="Mutaxasisligi", required=True)
    experience = fields.Float(string="Tajribasi")
    phone_number = fields.Char(string="Telefon raqami")
    work_schedule_ids = fields.One2many(comodel_name="clinic.work_schedule", inverse_name="doctor_id")
    is_active = fields.Boolean(string="Ish statusi", default=True)
    appointment_ids = fields.One2many(comodel_name="clinic.appointment", inverse_name="doctor_id")
    reception_price = fields.Float(string="30 daqiqalik qabul narxi")
    