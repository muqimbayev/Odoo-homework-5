from odoo import fields, models, api

class ServiceDistrict(models.Model):
    _name = "service.district"
    _description = "Tumanlar"

    name = fields.Char(string="Nomi")
    code = fields.Char(string="Kodi")
    is_active = fields.Boolean(string="Faolligi", default=True)
    state_id = fields.Many2one(comodel_name="service.region", string="Viloyati")
    country_id = fields.Many2one(comodel_name="service.country", string="Davlati")
    center_ids = fields.One2many(comodel_name="service.center", inverse_name="district_id")
    population = fields.Integer(string="Aholi soni")
    area_km2 = fields.Float(string="Hududi")
    latitude = fields.Float(string="Kengligi")
    longtitude = fields.Float(string="Uzunligi")
    technician_ids = fields.One2many(comodel_name="service.technician", inverse_name="center_id") #0
    #compute
    center_count = fields.Integer(string="Mrkazlar soni", compute="_compute_center_count") #0
    technician_count = fields.Integer(string="Ustalar soni", compute="_compute_technician_count") #0
    active_order_ids = fields.One2many(comodel_name="service.order", inverse_name="center_id", compute="_compute_active_order_ids") #0
    active_order_count = fields.Integer(string="Faol buyurtmalar soni", compute="_compute_active_order_count") #0
    done_order_ids = fields.One2many(comodel_name="service.order", inverse_name="center_id", compute="_compute_done_order_ids") #0
    done_order_count = fields.Integer(string="Tugallangan buyurtmalar soni", compute="_compute_done_order_count") #0
    total_revenue = fields.Float(string="Jami tushum", compute="_compute_tatal_revenue") #0
    last_order_date = fields.Date(string="Oxirigi buyurtma sanasi", compute="_compute_last_order_date") #0

    #Method
    #Vazifa: tumanni nofaol qilish (is_active=False).
    def action_deactivate(self):
        pass

    #Vazifa: tumanni faol qilish (is_active=True).
    def action_activate(self):
        pass

    #Vazifa: shu tumandagi faol buyurtmasi yo‘q servis markazlarini topib, ularni nofaol qilish (write).
    def action_deactivate_idle_centers(self):
        pass

    #Vazifa: shu tumandagi markazlar bo‘yicha summasi 0 bo‘lgan service.payment yozuvlarini topib unlink qilish.
    def action_cleanup_zero_payments(self):
        pass

    #Vazifa: shu tumandagi markazlarda state='in_progress' buyurtmalarni topib, state='done' ga o‘tkazish (write).
    def action_finish_all_in_progress(self):
        pass





    
