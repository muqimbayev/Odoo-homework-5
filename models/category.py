from odoo import models, fields, api

class Category(models.Model):
    _name = "ecommerce2.category"
    _description = "Kategoriya"

    name = fields.Char(string="Nomi", required=True)
    product_count = fields.Integer(string="Mahsulotlar soni", compute="_compute_product_count")
    product_ids = fields.One2many(string="Mahsulotlar", inverse_name="category_id", comodel_name="ecommerce2.product")

    @api.depends('product_ids')
    def _compute_product_count(self):
        for rec in self:
            rec.product_count = len(rec.product_ids)
    
    