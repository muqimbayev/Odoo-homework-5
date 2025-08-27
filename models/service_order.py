from odoo import fields, models, api
from odoo.exceptions import ValidationError

class ServiceOrder(models.Model):
    _name = "service.order"
    _description = "Buyurtmalar"

    name = fields.Char(string="Buyurtma raqami", compute='_compute_name') #1
    center_id = fields.Many2one(comodel_name="service.center", string="Servis markazi", required=True)
    customer_id = fields.Many2one(comodel_name="service.customer", string="Mijoz", required=True)
    technician_id = fields.Many2one(comodel_name="service.technician", string="Usta",     domain=[('is_active', '=', True)])
    order_date = fields.Datetime(default=fields.Datetime.now(), string="Buyurtma sanasi")
    state = fields.Selection([
        ('draft', 'Yangi'),
        ('received', "Qabul qilingan"),
        ('diagnosed', "Tashxis qo'yilgan"),
        ('in_progress', 'Jarayonda'),
        ('done', 'Bajarilgan'),
        ('cancelled', 'Bekor qilingan')
    ], string="Buyurtma holati", default="draft", required=True)
    description = fields.Text(string="Izoh")
    line_ids = fields.One2many(comodel_name="service.order.line", inverse_name="order_id")
    labor_fee = fields.Float(string="Xizmat xaqi")
    discount_amount = fields.Float(string="Chegirma (%)")
    payment_ids = fields.One2many(comodel_name="service.payment", inverse_name="order_id")
    rating_ids = fields.One2many(string="Baholashlar", comodel_name="service.order.rating", inverse_name="order_id")
    is_warranty = fields.Boolean(string="Kafolat mavjudligi")
    warranty_days = fields.Integer(string="Kafolat kuni")
    # #compute
    payment_total = fields.Float(string="Jami to'lov", compute="_compute_payment_total") #1
    balance_due = fields.Float(string="Qarz", compute="_compute_balance_due") #1
    last_payment_date = fields.Date(string="Oxirigi to'lov sanasi", compute="_compute_last_payment_date") #1
    total_amount = fields.Float(string="Jami to'langan summa", compute="_compute_total_amount") #1

    #To'lov qilish tugmasi
    def action_create_payment(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'To‘lov yaratish',
            'res_model': 'service.payment',
            'view_mode': 'form',
            'target': 'current',
            'context': {
                'default_order_id': self.id,
            }
        }

    #Method
    #Vazifa: holatni received ga o‘tkazish (write).
    def action_receive(self):
        self.write({'state': 'received'})

    # Vazifa: holatni diagnosed ga o‘tkazish (write).
    def action_diagnose(self):
        self.write({'state': 'diagnosed'})

    # Vazifa: holatni in_progress ga o‘tkazish (write).
    def action_start_progress(self):
        self.write({'state': 'in_progress'})

    # Vazifa: holatni done ga o‘tkazish; kerak bo‘lsa qarzni tekshirish (qoldiq 0 yoki manfiy bo‘lsa).
    def action_finish(self):
        self.write({'state': 'done'})

    # Vazifa: holatni cancelled ga o‘tkazish (write).
    def action_cancel(self):
        self.write({'state': 'cancelled'})

    # Vazifa: shu buyurtmaga tegishli amount=0 to‘lovlarni topib unlink qilish.
    def action_cleanup_zero_payments(self):
        self.env['service.payment'].search([('amount', '=', 0), ('order_id', '=', self.id)]).unlink()

    # Vazifa: balance_due <= 0 bo‘lsa state='done' qilish; aks holda xabar berish (status o‘zgarmaydi).
    def action_close_if_paid(self):
        orders = self.env['service.payment'].search_count([('balance_due', '<=', 0)])
        if orders:
            self.write({'state': 'done'})
        else:
            raise ValidationError("Qarzdorlik mavjud!")

    @api.depends()
    def _compute_name(self):
        for record in self:
            record.name = f"Servis #{record.id}"

    @api.depends('discount_amount', 'labor_fee')
    def _compute_payment_total(self):
        for record in self:
            if record.discount_amount > 0:
                record.payment_total = record.labor_fee - (record.labor_fee*(record.discount_amount/100))
            else:
                record.payment_total = record.labor_fee

    @api.depends()
    def _compute_total_amount(self):
        for record in self:
            payments = self.env['service.payment'].search([('order_id', '=', record.id), ('state', '=', 'confirmed')])
            record.total_amount = sum(payments.mapped('amount'))

    @api.depends()
    def _compute_balance_due(self):
        for record in self:
            record.balance_due = record.payment_total - record.total_amount

    @api.depends()
    def _compute_last_payment_date(self):
        for record in self:
            record.last_payment_date = self.env['service.payment'].search([], order="payment_date desc", limit=1).payment_date

    @api.constrains('is_warranty', 'warranty_days')
    def _check_is_warranty(self):
        if self.is_warranty and self.warranty_days <= 0:
            raise ValidationError("Kafolat mavjud! Kuni kiritishingiz kerak.")

