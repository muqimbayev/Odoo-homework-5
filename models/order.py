from odoo import fields, models, api
from datetime import date
from odoo.exceptions import ValidationError

class Order(models.Model):
    _name="ecommerce2.order"
    _description="Buyurtma"

    customer_id = fields.Many2one(comodel_name="ecommerce2.customer", string="Mijoz")
    delivery_deadline =  fields.Date(string="Qachon yetkazib berish kerak", required=True)
    delivery_days_left =  fields.Integer(string="Yetkazib berishga necha kun qoldi?", compute="_compute_delivery_days_left")
    product_count = fields.Integer(string="Buyurtmada nechta mahsulot bor?", compute="_compute_product_count")
    product_ids = fields.One2many(comodel_name="ecommerce2.order_line", inverse_name="order_id")  
    amount = fields.Float(reversed="product_ids", compute="_compute_total_price", string="Umumiy summa")  
    order_status = fields.Selection([
        ("new", "Yangi"),
        ("confirm", "Tasdiqlandi"),
        ("deliver", "Yetkazildi"),
        ("cancel", "Bekor qilindi"),
    ], string="Buyurtma status", default="new")

    @api.depends('product_ids.count')
    def _compute_total_price(self):
        for record in self:
            record.amount = sum(record.product_ids.mapped('total_price'))

    @api.depends('delivery_deadline')
    def _compute_delivery_days_left(self):
        today = date.today()
        for record in self:
                if record.delivery_deadline:
                    record.delivery_days_left = (record.delivery_deadline - today).days
                else:
                    record.delivery_days_left = 0   
                         
    @api.depends('product_ids')
    def _compute_product_count(self):
        for record in self:
            record.product_count = sum(record.product_ids.mapped('count'))

    def action_confirm(self):
        for record in self:
            record.order_status = "confirm"
            for i in record.product_ids:
                if i.count<=i.product_id.quantity:
                    i.product_id.quantity-=i.count
                else:
                    raise ValidationError("Siz mahsulot miqdoridan ko'p buyurtma berdingiz!")

    def action_deliver(self):
        for record in self:
            record.order_status = "deliver"
    
    def action_cancel(self):
        for record in self:
            record.order_status = "cancel"
            for i in record.product_ids:
                    i.product_id.quantity+=i.count
    