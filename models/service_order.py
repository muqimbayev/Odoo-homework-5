from odoo import fields, models, api

class ServiceOrder(models.Model):
    _name = "service.order"
    _description = "Buyurtmalar"

    name = fields.Char(string="Buyurtma raqami")
    center_id = fields.Many2one(comodel_name="service.center", string="Servis markazi")
    customer_id = fields.Many2one(comodel_name="service.customer", string="Mijoz")
    technician_id = fields.Many2one(comodel_name="service.technician", string="Usta")
    order_date = fields.Datetime(default=fields.Datetime.today(), string="Buyurtma sanasi")
    state = fields.Selection([
        ('draft', 'Yangi'),
        ('received', "Qabul qilingan"),
        ('diagnosed', "Tashxis qo'yilgan"),
        ('in_progress', 'Jarayonda'),
        ('done', 'Bajarilgan'),
        ('cancelled', 'Bekor qilingan')
    ], string="Buyurtma holati")
    description = fields.Text(string="Izoh")
    line_ids = fields.One2many(comodel_name="service.order.line", inverse_name="order_id")
    labor_fee = fields.Float(string="Xizmat xaqi")
    discount_amount = fields.Float(string="Chegirma")
    payment_ids = fields.One2many(comodel_name="service.payment", inverse_name="order_id")
    rating_ids = fields.One2many(string="Baholashlar", comodel_name="service.order.rating", inverse_name="order_id")
    is_warranty = fields.Boolean(string="Kafolat mavjudligi", default=True)
    warranty_days = fields.Integer(string="Kafolat kuni")
    #compute
    payment_total = fields.Float(string="Jami to'lovlar", compute="_compute_payment_total") #0
    balance_due = fields.Float(string="Qarz", compute="_balance_due") #0
    last_payment_date = fields.Date(string="Oxirigi to'lov sanasi", compute="_compute_last_payment_date") #0
    total_amount = fields.Float(string="Jami summa", compute="_compute_total_amount") #0

    #Method
    #Vazifa: holatni received ga o‘tkazish (write).
    def action_receive(self):
        pass
    
    # Vazifa: holatni diagnosed ga o‘tkazish (write).
    def action_diagnose(self):
        pass

    # Vazifa: holatni in_progress ga o‘tkazish (write).
    def action_start_progress(self):
        pass

    # Vazifa: holatni done ga o‘tkazish; kerak bo‘lsa qarzni tekshirish (qoldiq 0 yoki manfiy bo‘lsa).
    def action_finish(self):
        pass

    # Vazifa: holatni cancelled ga o‘tkazish (write).
    def action_cancel(self):
        pass

    # Vazifa: shu buyurtmaga tegishli amount=0 to‘lovlarni topib unlink qilish.
    def action_cleanup_zero_payments(self):
        pass

    # Vazifa: balance_due <= 0 bo‘lsa state='done' qilish; aks holda xabar berish (status o‘zgarmaydi).
    def action_close_if_paid(self):
        pass

    

