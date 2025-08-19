from odoo import fields, models, api
from odoo.exceptions import ValidationError

class Order_line(models.Model):
    _name = "ecommerce2.order_line"
    _description = "Buyurtmadagi mahsulotlar"

    product_id = fields.Many2one(comodel_name="ecommerce2.product", string="Mahsulot")
    order_id = fields.Many2one(comodel_name="ecommerce2.order", string="Buyurtma")
    count = fields.Integer(string="Mahsulot soni", default=1)
    price = fields.Float(related="product_id.price", string="1 donasi narxi")
    tex = fields.Float(related="product_id.tex", string="Soliq (%)")
    tex_amount = fields.Float(string="Soliq summasi", related="product_id.tex_amount")
    discount = fields.Float(related="product_id.discount", string="Chegirma (%)")
    total_price = fields.Float(string="Jami summa", compute="_compute_total_price")
    profit_percent = fields.Float(string="Jami foyda (fozida)", compute="_compute_profit_percent")
    profit = fields.Float(string="Jami foyda (summada)", compute="_compute_profit")
    real_price = fields.Float(string="Chegirma narxi", related="product_id.real_price")

    
    @api.depends('product_id', 'tex_amount')
    def _compute_total_price(self):
        for record in self:
            record.total_price = ((record.real_price*record.count)+record.tex_amount)

    @api.onchange('count')
    def _check_limit(self):
        for record in self:
            if record.count>record.product_id.quantity:
                return {
                    "warning":{
                        "title": "Mahsulot miqdoridan ko'p buyurtma",
                        "message": f"Siz maksimal {record.product_id.quantity} ta mahsulot xarid qilishingiz mumkin."
                    }
                }
    
    @api.depends('real_price', 'count')
    def _compute_profit(self):
        for record in self:
            record.profit = (record.real_price - record.product_id.cost)*record.count

    @api.depends()
    def _compute_profit_percent(self):
        for record in self:
            record.profit_percent = (record.profit/(record.real_price*record.count))*100
    
