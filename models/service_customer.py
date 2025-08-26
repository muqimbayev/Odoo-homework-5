from odoo import fields, models, api

class ServiceCustomer(models.Model):
    _name = "service.customer"
    _description = "Mijozlar"

    full_name = fields.Char(string="To'liq ism familyasi", required=True)
    code = fields.Char(string="Kodi")
    phone = fields.Char(string="Telefon raqami")
    mobile = fields.Char(string="Qo'shimcha telefon raqami")
    email = fields.Char(string="Email")
    address = fields.Text(string="Manzil")
    order_ids = fields.One2many(comodel_name="service.order", inverse_name="customer_id")
    rating_ids = fields.One2many(comodel_name="service.order.rating", inverse_name="customer_id")
    payment_ids = fields.One2many(comodel_name="service.payment", inverse_name="customer_id")

    #compute
    center_ids = fields.Many2many(comodel_name="service.order", compute="_compute_center_ids") #1
    order_count = fields.Integer(string="Buyurtmalar soni", compute="_compute_order_count") #1
    payment_count = fields.Integer(string="Buyurtmalar soni", compute="_compute_payment_count") #1
    active_order_ids = fields.One2many(comodel_name="service.order", inverse_name="customer_id", compute="_compute_active_order_ids") #1
    done_order_count = fields.Integer(string="Bajarilgan buyurtmalar soni", compute="_compute_done_order_count") #1
    total_payment = fields.Float(string="Jami to'lov summasi", compute="_compute_total_payment") #1
    balance_due = fields.Float(string="Jami qarz summasi", compute="_compute_balance_due") #1
    avg_rating = fields.Float(string="O'rtacha baho", compute="_compute_avg_rating") #1
    last_order_date = fields.Date(string="Oxirigi buyurtma sanasi", compute="_compute_last_order_date") #1
    last_payment_date = fields.Date(string="Oxirigi to'lov sanasi", compute="_compute_last_payment_date") #1


    #Mathod
    #Vazifa: qarzdorligi bo’yicha to’lov yaratib, tasdiqlab yuborish.
    def action_close_debt(self):
        pass

    #Vazifa: shu mijozga tegishli summasi 0 bo‘lgan service.payment yozuvlarini topib unlink qilish.
    def action_cleanup_zero_payments(self):
        zero_payments = self.env['service.payment'].search([('amount', '=', 0), ('customer_id', '=', self.id)])
        zero_payments.unlink()

    #Vazifa: shu mijozning state='cancelled' bo‘lgan buyurtmalarini topib o‘chirish (unlink).
    def action_cleanup_cancelled_orders(self):
        cancelled_orders = self.env['service.order'].search([('state', '=', 'cancelled'), ('customer_id', '=', self.id)])
        cancelled_orders.unlink()


    #info-button
    def order_count_button(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Buyurtmalar",
            "res_model": "service.order",
            "view_mode": "list,form",
            "domain": [("customer_id", "in", self.order_ids.mapped("customer_id"))],

        }
    def payment_count_button(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Buyurtmalar",
            "res_model": "service.order",
            "view_mode": "list,form",
            "domain": [("customer_id", "in", self.payment_ids.mapped("customer_id"))],
        }


    #compute
    @api.depends('order_ids')
    def _compute_active_order_ids(self):
        for record in self:
            record.active_order_ids = self.env['service.order'].search(domain=[('state', 'not in', ['cancelled', 'done']), ('customer_id', '=', record.id)])

    @api.depends('order_ids')
    def _compute_center_ids(self):
        for record in self:
            record.center_ids = self.order_ids.mapped('center_id')._origin

    @api.depends('order_ids')
    def _compute_order_count(self):
        for record in self:
            record.order_count = len(record.order_ids)


    @api.depends('order_ids')
    def _compute_payment_count(self):
        for record in self:
            record.payment_count = self.env['service.payment'].search_count([('customer_id', '=', record.id)])

    @api.depends('order_ids.state')
    def _compute_done_order_count(self):
        for record in self:
            record.done_order_count = self.env['service.order'].search_count([('customer_id', '=', record.id), ('state', '=', 'done')])

    @api.depends('payment_ids.amount')
    def _compute_total_payment(self):
        for record in self:
            record.total_payment = sum(record.payment_ids.filtered(lambda x: x.state == 'confirmed').mapped('amount'))

    @api.depends('order_ids.balance_due')
    def _compute_balance_due(self):
        for record in self:
            record.balance_due = sum(record.order_ids.mapped('balance_due'))

    @api.depends('rating_ids.score')
    def _compute_avg_rating(self):
        for record in self:
            if record.rating_ids:
                record.avg_rating = sum(record.rating_ids.mapped('score')) / len(record.rating_ids)
            else:
                record.avg_rating = 0

    @api.depends('order_ids.order_date')
    def _compute_last_order_date(self):
        for record in self:
            if record.order_ids:
                record.last_order_date = max(record.order_ids.mapped('order_date'))
            else:
                record.last_order_date = False

    @api.depends('payment_ids.payment_date')
    def _compute_last_payment_date(self):
        for record in self:
            if record.payment_ids:
                record.last_payment_date = max(record.payment_ids.mapped('payment_date'))
            else:
                record.last_payment_date = False
    


