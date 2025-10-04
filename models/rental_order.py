from odoo import fields, models, api
from odoo.exceptions import ValidationError

class RentalOrder(models.Model):
    _name = "rental_managment.rental_order"
    _description = "Rental Order"

    name = fields.Char(string="Name")
    customer_id = fields.Many2one("rental_managment.customer", string="Customer")
    product_id = fields.Many2one('rental_managment.product', string="Product", required=True)
    start_date = fields.Datetime(string="Start date", required=True, default=fields.Datetime.now())
    end_date = fields.Datetime(string="End date", required=True)
    returned_date = fields.Datetime(string="Returned date")
    duration = fields.Float(string="Hours", compute="_compute_duration", store=True)
    human_readable_duration = fields.Char(string="Duration", compute="_compute_human_readable_duration", store=True)
    total_price = fields.Float(string="Total price", compute="_compute_total_price", store=True)
    compute_price = fields.Float(string="Total amount", compute="_compute_compute_price", store=True)
    status = fields.Selection([
        ('draft', "Draft"),
        ('confirmed', "Confirmed"),
        ('returned', "Returned"),
        ('cancelled', "Cancelled")
    ], default="draft", readonly=True)

    @api.depends('start_date', 'end_date')
    def _compute_duration(self):
        for record in self:
            if record.start_date and record.end_date:
                delta = record.end_date - record.start_date
                record.duration = delta.total_seconds() / 3600
            else:
                record.duration = 0

    @api.constrains('start_date', 'end_date')
    def check_end_date(self):
        for record in self:
            if record.start_date and record.end_date and record.start_date >= record.end_date:
                raise ValidationError("Tugash sanasi boshlanish sanasidan keyin bo'lishi kerak!")

    @api.depends('duration')
    def _compute_human_readable_duration(self):
        for record in self:
            hours = int(record.duration or 0)
            days, hours = divmod(hours, 24)
            years, rem_days = divmod(days, 365)
            months, days = divmod(rem_days, 30)
            weeks, days = divmod(days, 7)

            parts = []
            if years:
                parts.append(f"{years} yil")
            if months:
                parts.append(f"{months} oy")
            if weeks:
                parts.append(f"{weeks} hafta")
            if days:
                parts.append(f"{days} kun")
            if hours:
                parts.append(f"{hours} soat")

            record.human_readable_duration = " ".join(parts) if parts else "0 soat"

    @api.depends('duration', 'product_id')
    def _compute_total_price(self):
        for record in self:
            if not record.product_id or record.duration <= 0:
                record.total_price = 0
                continue

            hours = int(record.duration)
            days, hours = divmod(hours, 24)
            years, rem_days = divmod(days, 365)
            months, days = divmod(rem_days, 30)
            weeks, days = divmod(days, 7)

            price = 0
            env_price = self.env['rental_managment.rental_price']

            def get_price(interval_type):
                price_rec = env_price.search([
                    ('product_id', '=', record.product_id.id),
                    ('interval_type', '=', interval_type)
                ], limit=1)
                return price_rec.price if price_rec else 0

            price += years * get_price('year')
            price += months * get_price('month')
            price += weeks * get_price('week')
            price += days * get_price('day')
            price += hours * get_price('hour')

            record.total_price = price

    @api.depends('product_id', 'duration')
    def _compute_compute_price(self):
        for record in self:
            record.compute_price = 0
            if record.product_id and record.duration > 0:
                price = record.get_result_price(record.product_id.id, record.duration)
                record.compute_price = price or 0

    def confirm_button(self):
        for record in self:
            product = record.product_id
            if product.availability == "available" and not product.broken:
                record.status = "confirmed"
            else:
                raise ValidationError("Mahsulotni ijaraga berish mumkin emas!")

    def returned_button(self):
        for record in self:
            record.status = 'returned'
            record.returned_date = fields.Datetime.now()

    def canceled_button(self):
        for record in self:
            record.status = 'cancelled'

    def get_min_rental_price(self, product_id, hours):
        recs = self.env["rental_managment.rental_price"].search([
            ("product_id", "=", product_id),
            ("hour", "<=", hours)
        ], order="hour asc")
        return recs[-1] if recs else None

    def get_max_rental_price(self, product_id, hours):
        recs = self.env["rental_managment.rental_price"].search([
            ("product_id", "=", product_id),
            ("hour", ">=", hours)
        ], order="hour asc")
        return recs[0] if recs else None

    def get_result_price(self, product_id, hours):
        min_price = self.get_min_rental_price(product_id, hours)
        max_price = self.get_max_rental_price(product_id, hours)

        if not min_price and not max_price:
            return 0
        if min_price and not max_price:
            return min_price.price
        if not min_price and max_price:
            return max_price.price

        price_by_min = min_price.price * (hours / min_price.hour)
        price_by_max = max_price.price
        return min(price_by_min, price_by_max)
