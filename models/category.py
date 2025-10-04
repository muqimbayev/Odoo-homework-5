from odoo import fields, models, api

class Category(models.Model):
    _name="rental_managment.category"
    _description = "Category"

    name = fields.Char(string="Name", required=True)
    product_ids = fields.One2many("rental_managment.product", inverse_name="category_id")
