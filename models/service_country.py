from odoo import fields, models, api

class ServiceCountry(models.Model):
    _name = "service.country"
    _description = "Davlatlar"

    name = fields.Char(string="Nomi")
    code = fields.Char(string="Kodi")
    phone_code = fields.Char(string="Telefon kodi")
    is_active = fields.Boolean(string="Faolligi")
    currency_id = fields.Many2one(comodel_name="service.currency", string="Valyuta")
    state_ids = fields.One2many(comodel_name="service.state", inverse_name="country_id", string="Viloyatlari")
    center_ids = fields.One2many(comodel_name="service.center", inverse_name="country_id", string="Servis markazlari")
    #compute
    technician_count = fields.Integer(string="Ustalar soni", compute="_compute_technician_count") #0
    state_count = fields.Integer(string="Viloyatlar soni", compute="_compute_state_count") #0
    center_count = fields.Integer(string="Markazlar soni", compute="_compute_center_count") #0
    active_order_count = fields.Integer(string="Faol buyurtmalar soni", compute="_compute_active_order_count") #0
    done_order_ids = fields.One2many(comodel_name="service.order", inverse_name="center_id", compute="_compute_active_order_count") #0
    done_order_count = fields.Integer(string="Yakunlangan buyurtmalar soni", compute="_compute_done_order_count") #0
    total_revenue = fields.Float(string="Jami tushum", compute="_compute_total_revenue") #0
    avg_rating = fields.Float(string="O'rtacha rating", compute="_compute_avg_rating") #0
    last_date_order = fields.Date(string="Oxirigi buyurtma sanasi", compute="_compute_last_date_order") #0

    #Method
    #Vazifa: ushbu davlatni nofaol qilish (is_active=False).
    def action_deactivate(self):
        pass

    #Vazifa: ushbu davlatni faol qilish (is_active=True).
    def action_activate(self):
        pass

    #Vazifa: shu davlatdagi faol buyurtmasi yo‘q servis markazlarini topib, ularni nofaol qilish (write).
    def action_deactivate_idle_centers(self):
        pass

    #Vazifa: shu davlatdagi markazlar bo‘yicha summasi 0 bo‘lgan service.payment yozuvlarini topib unlink qilish.
    def action_cleanup_zero_payments(self):
        pass

    #Vazifa: shu davlatdagi markazlarda state='in_progress' buyurtmalarni topib, state='done' ga o‘tkazish (write).
    def action_finish_all_in_progress(self):
        pass



