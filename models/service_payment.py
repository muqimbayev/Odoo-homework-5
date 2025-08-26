from odoo import fields, models, api

class ServicePayment(models.Model):
    _name = "service.payment"
    _description = "To'lovlar"

    name = fields.Char(string="To'lov raqami", required=True)
    center_id = fields.Many2one(comodel_name="service.center", string="Markaz", compute="_compute_center_id") #0
    order_id = fields.Many2one(comodel_name="service.order", string="Buyurtma")
    customer_id = fields.Integer(string="Mijoz", compute="_compute_customer_id") #0
    payment_date = fields.Datetime(default=fields.Datetime.today(), string="To'ov sanasi")
    amount = fields.Float(string="To'lov summasi")
    note = fields.Text(string="Izoh")
    state = fields.Selection([
        ('draft', 'yangi'),
        ('confirmed', "To'langan"),
        ('canceled', 'Bekor qilingan')
    ])
    method = fields.Selection([
        ('cash', 'Naqd'),
        ('card', 'Karta'),
        ('bank', 'Bank')
    ])
    #compute
    order_total = fields.Float(string="Buyurtma summasi", compute="_compute_order_total") #0
    order_balance_due = fields.Float(string="Buyurtma bo'yicha qoldiq", compute="_compute_order_balance_due") #0
    customer_total_payment = fields.Float(string="Mijozni jami to'lavlari", compute="_compute_customer_total_payment")

    #Method 
    #Vazifa: to‘lovni state='draft' holatiga qaytarish.
    def action_confirm(self):
        pass

    #Vazifa: to‘lovni state='cancelled' ga o‘tkazish.
    def action_cancel(self):
        pass

    #Vazifa: to‘lovni state='draft' holatiga qaytarish.
    def action_reset_draft(self):
        pass

