from odoo import models, fields, api
from datetime import timedelta

class Appointment(models.Model):
    _name = "clinic.appointment"
    _description = "Qabul"
    _rec_name = "title_field"

    doctor_id = fields.Many2one(comodel_name="clinic.doctor", required=True, string="Doktor")
    patient_id = fields.Many2one(comodel_name="clinic.patient", required=True, string="Bemor")
    start_time = fields.Datetime(string="Boshlanish vaqti", required=True)
    reception_duration = fields.Selection([("hall_hour", "30 daqiqa"), ("an_hour", "1 soat"), ("an_hour_half", "1,5 soat")], string="Qabul davomiyligi", required=True, default="hall_hour")
    end_time = fields.Datetime(string="Tugash vaqti", required=True, readonly=True, compute="_compute_end_time")
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
    total_price = fields.Float(string="Umumiy to'lov narxi", compute="_total_price", readonly=True)

    @api.depends('reception_duration')
    def _total_price(self):
        for rec in self:
            price = rec.doctor_id.reception_price
            duration_list = {'hall_hour':1, 'an_hour':2, 'an_hour_half':3}
            rec.total_price = price * duration_list[rec.reception_duration]

    @api.depends('prescription_line_ids')
    def _compute_medicine_name(self):
        for record in self:
            record.medicine_name = ", ".join((record.prescription_line_ids.mapped('medicine_id.name')))

    @api.depends('start_time')
    def _compute_end_time(self):
        duration_list = {'hall_hour':30, 'an_hour':60, 'an_hour_half':90}
        for rec in self:
            minutes = duration_list[rec.reception_duration]
            rec.end_time = rec.start_time+timedelta(minutes=minutes)


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

    
    