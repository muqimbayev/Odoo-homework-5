from odoo import fields, models, api
from odoo.exceptions import ValidationError

class ServiceOrderRating(models.Model):
    _name = "service.order.rating"
    _description = "Servis uchun rating"

    customer_id = fields.Many2one(comodel_name="service.customer", string="Mijoz", required=True)
    center_id = fields.Many2one(comodel_name="service.center", compute="_compute_center_id") #1
    order_id = fields.Many2one(comodel_name="service.order", string="Buyurtmalar", required=True)
    technician_id = fields.Many2one(comodel_name="service.technician", string="Usta", compute="_compute_technician_id") #1
    score = fields.Float(string="Baho (1-5)", required=True)
    comment = fields.Text(string="Izoh")
    rating_date = fields.Datetime(default=fields.Datetime.now(), readonly=True, string="Sana")
    
    @api.depends('order_id')
    def _compute_center_id(self):
        for record in self:
            record.center_id = record.order_id.center_id

    @api.depends('order_id')
    def _compute_technician_id(self):
        for record in self:
            record.technician_id = record.order_id.technician_id

    @api.constrains('socre')
    def _check_socre(self):
        for record in self:
            if record.score<1 or record.score>5:
                raise ValidationError("Baho 1 va 5 orasida bo'lishi kerak")

    @api.constrains()
    def _check_customer_rating(self):
        for record in self:
            rating_count = self.env['service.order.rating'].search_count([('customer_id', '=', record.customer_id), ('order_id', '=', record.order_id)])
            if rating_count>1:
                raise ValidationError("1 ta buyurtmaga faqat 1 marta baholay olasiz!")
