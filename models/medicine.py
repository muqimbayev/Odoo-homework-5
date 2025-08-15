from odoo import models, fields

class ClinicMedicine(models.Model):
    _name = "clinic.medicine"
    _description = "Dori ma'lumotlari"
    _rec_name = "name"

    name = fields.Char(string="Dori nomi", required=True)
    generic_name = fields.Char(string="Umumiy nomi (Generic)")
    dosage_unit = fields.Selection(
        [('mg', "Milligram (mg)"), ('ml', "Millilitr (ml)"), ('tablet', "Tablet"), ('capsule', "Capsule")], string="Dozalash birligi", required=True)
    description = fields.Text(string="Tavsif")
    manufacturer = fields.Char(string="Ishlab chiqaruvchi")
    contraindications = fields.Many2many(comodel_name="clinic.medicine", relation="clinic_medicine_contraindication_rel", column1="medicine_id", column2="contraindication_id")
    suitable_age = fields.Integer(string="Mos keladigan yosh", required=True, help="Kiritilgan yoshdan kattalar uchun")


