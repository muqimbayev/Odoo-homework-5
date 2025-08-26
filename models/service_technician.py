from odoo import models, fields, api

class ServiceTechnican(models.Model):
    _name = "service.technician"
    _description = "Ustalar"

    full_name = fields.Char("To'liq ism familyasi", required=True)
    code = fields.Char(string="Kodi")
    is_active = fields.Boolean(string="Faolligi")
    center_id = fields.Many2one(comodel_name="service.center", string="Markazi")
    phone = fields.Char(string="Telefon raqami")
    email = fields.Char(string="Email")
    specialty = fields.Char(string="Mutaxasisligi")
    hire_date = fields.Date(string="Ushga yo'llangan sanasi")
    capacity_per_day = fields.Integer(string="Kunlik maksimal bajaradigan ishlar soni")
    order_ids = fields.One2many(comodel_name="service.order", inverse_name="technician_id")
    #compute
    active_order_ids = fields.One2many(comodel_name="service.order", inverse_name="technician_id", compute="_compute_active_order_ids") #0
    active_order_count = fields.Integer(string="Faol buyurtmalar soni", compute="_compute_order_count") #0
    done_order_ids = fields.One2many(comodel_name="service.order", inverse_name="technician_id", compute="_compute_done_order_ids") #0
    done_order_count = fields.Integer(string="Yakunlangan buyurtmalar soni", compute="_compute_done_order_count") #0
    today_order_ids = fields.One2many(comodel_name="service.order", inverse_name="technician_id", compute="_compute_today_order_ids") #0
    today_order_count = fields.Integer(string="Bugungi buyurtmalar soni", compute="_compute_today_order_count") #0
    utilization_rate = fields.Float(string="Bandlik foizi", compute="_compute_utilization_rate") #0
    avg_rating = fields.Float(string="O'rtacha baho", compute="_compute_avg_rating") #0
    total_revenue = fields.Float(string="Jami tushum", compute="_compute_total_revenue") #0
    last_order_date = fields.Date(string="Oxirigi buyurtma sanasi", compute="_compute_last_order_date") #0
    is_buzy = fields.Boolean(string="Hozirgi bandligi", compute="_comute_is_buzy")
    
    #mathod
    #Vazifa: usta yozuvini nofaol qilish (is_active=False).
    def action_deactivate(self):
        pass

    #Vazifa: usta yozuvini faol qilish (is_active=True).
    def action_activate(self):
        pass
    


