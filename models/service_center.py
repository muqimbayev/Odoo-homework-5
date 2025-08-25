from odoo import fields, models, api


class ServiceCenter(models.Model):
    _name = "service.center"
    _description = "Xzmat ko'rsatish markazlari"
    
    name = fields.Char(string="Servis markazi nomi", required=True)
    code = fields.Char(string="Markaz kodi")
    is_active = fields.Boolean(string="Faolligi", default=True)
    country_id = fields.Many2one(comodel_name="service.country", string="Davlati")
    state_id = fields.Many2one(comodel_name="service.state", string="Viloyati")
    district_id = fields.Many2one(comodel_name="service.district", string="Tumani")
    address = fields.Char(string="Manzili")
    latitude = fields.Char(string="Kengligi")
    longitude = fields.Char(string="Uzunligi")
    phone = fields.Char(string="Telefon raqami")
    email = fields.Char(string="Email")
    manager_name = fields.Char(string="Masul shaxs")
    capacity_per_day = fields.Integer(string="Kunlik quvvati (Buyurtmada)")
    order_ids = fields.One2many(comodel_name="service.order", inverse_name="center_id")
    payment_ids = fields.One2many(comodel_name="service.payment", inverse_name="center_id")
    rating_ids = fields.One2many(comodel_name="service.order.rating", inverse_name="center_id")
    #compute fields
    technician_count = fields.Integer(string="Ustalar soni", compute="_compute_technician_count") #0
    active_order_count = fields.Integer(string="Faol buyurtmalar soni", compute="_compute_active_order_count") #0
    done_order_count = fields.Integer(string="Yakunlangan buyurtmalar soni", compute="_compute_done_order_count") #0
    done_order_ids = fields.One2many(comodel_name="service.order", inverse_name="center_id", compute="_compute_done_orders") #0
    today_order_ids = fields.One2many(comodel_name="service.order", inverse_name="center_id", compute="_compute_today_orders") #0
    total_revenue = fields.Float(string="Jami tushum", compute="_compute_total_revenue") #0
    avg_rating = fields.Float(string="O'rtacha baho", compute="_compute_avg_rating") #0
    utilization_rate = fields.Float(string="Bandlik foizi", compute="_compute_utilization_rate") #0
    last_order_state = fields.Date(string="Oxirigi buyurtma sanasi", compute="_compute_last_order_date") #0

    #Mathod
    #Vazifa: agar faol buyurtma bo‘lmasa markazni nofaol qilish.
    def action_mark_inactive_if_idle(self):
        pass

    #Vazifa: markazni qaytadan faol qilish (is_active=True).
    def action_activate(self):
        pass

    #Vazifa: markaz bo‘yicha summasi 0 bo‘lgan to‘lovlarni o‘chirish.
    def action_cleanup_zero_payments(self):
        pass

    #Vazifa: holati in_progress bo‘lgan barcha buyurtmalarni donega o‘tkazish.
    def action_finish_all_in_progress(self):
        pass





