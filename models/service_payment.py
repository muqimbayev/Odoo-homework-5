from odoo import fields, models, api
from odoo.exceptions import ValidationError

class ServicePayment(models.Model):
    _name = "service.payment"
    _description = "To'lovlar"

    name = fields.Char(string="To'lov raqami", compute="_compute_name")#1
    center_id = fields.Many2one(comodel_name="service.center", string="Markaz", compute="_compute_center_id", store=True) #1
    order_id = fields.Many2one(comodel_name="service.order", string="Buyurtma", required=True)
    customer_id = fields.Many2one(comodel_name="service.customer", string="Mijoz", compute="_compute_customer_id",  store=True,) #1
    payment_date = fields.Datetime(default=fields.Datetime.now(), string="To'ov sanasi")
    amount = fields.Float(string="To'lov summasi")
    note = fields.Text(string="Izoh")
    state = fields.Selection([
        ('draft', 'yangi'),
        ('confirmed', "To'langan"),
        ('canceled', 'Bekor qilingan')
    ], string="To'lov holati", default="draft")
    method = fields.Selection([
        ('cash', 'Naqd'),
        ('card', 'Karta'),
        ('bank', 'Bank')
    ])

    #compute
    order_total = fields.Float(string="Buyurtma summasi", compute="_compute_order_total") #1
    order_balance_due = fields.Float(string="Buyurtma bo'yicha qoldiq", compute="_compute_order_balance_due") #1
    customer_total_payment = fields.Float(string="Mijozni jami to'lavlari", compute="_compute_customer_total_payment") #1

    #Method 
    #Vazifa: to‘lovni state='confirmed' ga o‘tkazish.
    def action_confirm(self):
        self.write({'state': 'confirmed'})

    #Vazifa: to‘lovni state='cancelled' ga o‘tkazish.
    def action_cancel(self):
        self.write({'state': 'canceled'})

    #Vazifa: to‘lovni state='draft' holatiga qaytarish.
    def action_reset_draft(self):
        self.write({'state': 'draft'})

    @api.depends('order_id')
    def _compute_center_id(self):
        for record in self:
            record.center_id = record.order_id.center_id

    @api.depends('order_id')
    def _compute_customer_id(self):
        for record in self:
            record.customer_id = record.order_id.customer_id

    @api.depends('order_id')
    def _compute_order_total(self):
        for record in self:
            record.order_total = record.order_id.payment_total

    @api.depends('amount', 'order_id')
    def _compute_customer_total_payment(self):
        for record in self:
            payments = self.env['service.payment'].search([('order_id', '=', record.order_id.id), ('state', '=', 'confirmed')])
            record.customer_total_payment = sum(payments.mapped('amount'))

    @api.depends('order_id')
    def _compute_order_balance_due(self):
        for record in self:
            record.order_balance_due = record.order_id.balance_due

    @api.depends()
    def _compute_name(self):
        for record in self:
            record.name = f"Payment #{record.id}"

    @api.constrains('amount', 'state')
    def _check_payment(self):
        for record in self:
            if record.customer_total_payment > record.order_total:
                raise ValidationError(f"Siz buyurtma summasidan ko'p to'lov qabul qilmoqdasiz!")



