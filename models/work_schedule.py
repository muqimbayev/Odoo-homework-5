from odoo import models, fields

class Work_schedule(models.Model):
    _name = "clinic.work_schedule"
    _description = "Ish jadvali"
    _rec_name = "week_days"
    
    week_days = fields.Selection([("moday", "Dushanba"), ("tuesday", "Seshanba"), ("wednesday", "Chorshanba"), ("thursday", "Payshanba"), ("friday", "Juma"), ("saturday", "Shanba"), ("sunday", "Yakshanba")], string="Hafta kuni", required=True)
    working_hours = fields.Float(string="Ish soati", widget="float_time")
    lunch_time = fields.Float(string="Tushlik vaqti", widget="float_time")
    doctor_id = fields.Many2one(comodel_name="clinic.doctor")