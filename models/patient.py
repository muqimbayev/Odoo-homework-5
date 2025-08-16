from odoo import models, fields

class Patient(models.Model):
    _name = "clinic.patient"
    _description = "Bemor"
    _rec_name = "full_name"


    full_name = fields.Char(string="To'liq ism familyasi", required=True)
    birth_date = fields.Date(string="Tug'ilgan yili", required=True)
    gender = fields.Selection([('male', 'Erkak'), ('female', 'Ayol')], required=True, string="Jinsi")
    phone_number = fields.Char(string="Telefon raqami")
    blood_type = fields.Selection([("first", "Birinchi"), ("second", "Ikkinchi"), ("third", "Uchinchi")], required=True, string="Qon guruhi")
    insured_number = fields.Char(string="Sug'irta raqami")
    relative_ids = fields.One2many(comodel_name="clinic.relatives", inverse_name="patient_id")
    appointment_ids = fields.One2many(comodel_name="clinic.appointment", inverse_name="patient_id")

class Relatives(models.Model):
    _name = "clinic.relatives"
    _description = "Bemor yaqinlari haqida malumot"

    patient_id = fields.Many2one(comodel_name="clinic.patient", string="Bemor")
    full_name = fields.Char(string="To'liq ism failyasi")
    phone_number = fields.Char(string="Telefon raqami")

        

