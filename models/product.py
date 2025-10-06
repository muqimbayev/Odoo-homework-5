from odoo import fields, models, api
from datetime import timedelta

class Product(models.Model):
    _name = "rental_managment.product"
    _description = "Product"

    name = fields.Char(string="Name", required=True)
    availability = fields.Selection([('rented', "Rented"), ('available', "Available")], required=True, default="available", compute="_compute_availability")
    broken = fields.Boolean(string="Broken", readonly=True)
    future_availability_date = fields.Date(string="future_availability_date", compute="_compute_future_availability_date")
    category_id = fields.Many2one(comodel_name="rental_managment.category", string="Category")
    rental_price_ids = fields.One2many('rental_managment.rental_price', inverse_name="product_id")
    rental_order_ids = fields.One2many('rental_managment.rental_order', inverse_name="product_id")

    @api.depends()
    def _compute_future_availability_date(self):
            for record in self:
                order = self.env['rental_managment.rental_order'].search(
                    [('product_id', '=', record.id), ('status', '=', 'confirmed')],
                    order='end_date desc',
                    limit=1
                )

                if order:
                    if not order.returned_date:
                        record.future_availability_date = order.end_date + timedelta(days=1)
                    else:
                        record.future_availability_date = order.returned_date
                else:
                    record.future_availability_date = fields.Date.today()

    def button_broken_true(self):
        self.broken=True

    def button_broken_false(self):
        self.broken=False

    @api.depends()
    def _compute_availability(self):
        for record in self:
            orders = self.env['rental_managment.rental_order'].search([
                ('product_id', '=', record.id),
                ('status', '=', 'confirmed')
            ])

            record.availability = 'available'

            for order in orders:
                if order.start_date and order.start_date <= fields.Datetime.now():
                    record.availability = 'rented'
                    break  
