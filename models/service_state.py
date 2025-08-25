from odoo import fields, models, api

class ServiceState(models.Model):
    _name = "service.state"
    _description = "Viloyatlar"

    name = fields.Char(string="Nomi")
    code = fields.Char(string="Kodi")
    is_active = fields.Boolean(string="Faolligi")
    country_id = fields.Many2one(comodel_name="service.country", string="Davlati")
    district_ids = fields.One2many(comodel_name="service.district", inverse_name="state_id")
    center_ids = fields.One2many(comodel_name="service.center", inverse_name="state_id")
    technician_ids = fields.One2many(comodel_name="service.technician", inverse_name="center_id", compute="_compute_technician_id") #0
    population = fields.Integer(string="Aholisi")
    area_km2 = fields.Float(string="Maydoni (km2)")
    latitude = fields.Float(string="Kengligi")
    longtitude = fields.Float(string="Uzunligi")
    #compute
    district_count = fields.Integer(string="Tumanlar soni", compute="_compute_district_count") #0
    center_count = fields.Integer(string="Servis markazlar soni", compute="_compute_center_count") #0
    technician_count = fields.Integer(string="Ustalar soni", compute="_compute_technician_count") #0
    active_order_ids = fields.One2many(comodel_name="service.order", inverse_name="center_id", compute="_compute_active_order_ids") #0
    active_order_count = fields.Integer(string="Faol buyurtmalar soni", compute="_compute_active_order_count") #0
    done_order_ids = fields.One2many(comodel_name="service.order", inverse_name="center_id", compute="_compute_done_order_ids") #0
    done_order_count = fields.Integer(string="Tugallangan buyurtmalar soni", compute="_compute_done_order_count") #0
    total_revenue = fields.Float(string="Jami tushum", compute="_compute_total_revenue") #0
    avg_rating = fields.Float(string="O'rtacha baho", compute="_compute_avg_rating")
    last_order_date = fields.Date(string="Oxirigi buyurtma sanasi", compute="_compute_last_order_date")

    #Method
    #Vazifa: viloyatni nofaol qilish (is_active=False).
    def action_deactivate(self):
        pass

    #Vazifa: viloyatni faol qilish (is_active=True).
    def action_activate(self):
        pass

    #Vazifa: shu viloyatdagi faol buyurtmasi yo‘q markazlarni topib, ularni nofaol qilish (write).
    def action_deactivate_idle_centers(self):
        pass

    #Vazifa: viloyat markazlari bo‘yicha summasi 0 bo‘lgan service.payment yozuvlarini topib unlink qilish.
    def action_cleanup_zero_payments(self):
        pass

    #Vazifa: viloyat markazlaridagi state='in_progress' buyurtmalarni state='done' ga o‘tkazish (write).
    def action_finish_all_in_progress(self):
        pass





