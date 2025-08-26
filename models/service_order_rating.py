from odoo import fields, models, api

class ServiceOrderRating(models.Model):
    _name = "service.order.rating"
    _description = "Servis uchun rating"

    customer_id = fields.Many2one(comodel_name="service.customer", string="Mijoz", required=True)
    center_id = fields.Many2one(comodel_name="service.center", compute="_compute_center_id") #0
    order_id = fields.Many2one(comodel_name="service.order", string="Buyurtmalar")
    technician_id = fields.Many2one(comodel_name="service.technician", string="Usta")
    score = fields.Float(string="Baho (1-5)")
    comment = fields.Text(string="Izoh")
    rating_date = fields.Datetime(default=fields.Datetime.today(), readonly=True, string="Sana")
    
