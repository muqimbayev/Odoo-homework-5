from odoo import fields, models, api

class RenalPrice(models.Model):
    _name = "rental_managment.rental_price"
    _description = "Rental Price"

    product_id = fields.Many2one("rental_managment.product", string="Product", required=True)
    interval_number = fields.Integer(string="Interval number", required=True)
    interval_type = fields.Selection([('hour', 'Hour'), ('day', 'Day'), ('week','Week'), ('month', 'Month'), ('year', 'Year')], required=True, default='hour')
    price = fields.Integer(string="Price", required=True)
    hour = fields.Integer(string="Hour", compute="_compute_hour", store=True)

    @api.depends()
    def _compute_hour(self):
        for record in self:
            if record.interval_type=='hour':
                hours = 1
            elif record.interval_type=='day':
                hours = 24
            elif record.interval_type=='week':
                hours = 24*7
            elif record.interval_type=='month':
                hours = 24*30
            else:
                hours=365*24
        record.hour = record.interval_number * hours

   