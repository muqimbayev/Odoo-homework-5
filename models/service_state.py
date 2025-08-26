from odoo import fields, models, api
from odoo.exceptions import ValidationError

class ServiceState(models.Model):
    _name = "service.state"
    _description = "Viloyatlar"

    name = fields.Char(string="Nomi", required=True)
    code = fields.Char(string="Kodi")
    is_active = fields.Boolean(string="Faolligi", default=True)
    country_id = fields.Many2one(comodel_name="service.country", string="Davlati")
    district_ids = fields.One2many(comodel_name="service.district", inverse_name="state_id")
    center_ids = fields.One2many(comodel_name="service.center", inverse_name="state_id")
    technician_ids = fields.One2many(comodel_name="service.technician", compute="_compute_technician_id") #1
    population = fields.Integer(string="Aholisi")
    area_km2 = fields.Float(string="Maydoni (km2)")
    latitude = fields.Float(string="Kengligi")
    longtitude = fields.Float(string="Uzunligi")
    #compute
    today_order_ids = fields.One2many(comodel_name="service.order", compute="_today_order_ids") #1
    today_order_count = fields.Integer(string="Bugungi buyurtmala soni", compute="_compute_today_order_count") #1
    district_count = fields.Integer(string="Tumanlar soni", compute="_compute_district_count") #1
    center_count = fields.Integer(string="Servis markazlar soni", compute="_compute_center_count") #1
    technician_count = fields.Integer(string="Ustalar soni", compute="_compute_technician_count") #1
    active_order_ids = fields.One2many(comodel_name="service.order", compute="_compute_active_order_ids") #1
    active_order_count = fields.Integer(string="Faol buyurtmalar soni", compute="_compute_active_order_count") #1
    done_order_ids = fields.One2many(comodel_name="service.order", compute="_compute_done_order_ids") #1
    done_order_count = fields.Integer(string="Tugallangan buyurtmalar soni", compute="_compute_done_order_count") #1
    total_revenue = fields.Float(string="Jami tushum", compute="_compute_total_revenue") #1
    avg_rating = fields.Float(string="O'rtacha baho", compute="_compute_avg_rating") #1
    last_order_date = fields.Date(string="Oxirigi buyurtma sanasi", compute="_compute_last_order_date") #0

    #Method
    #Vazifa: viloyatni nofaol qilish (is_active=False).
    def action_deactivate(self):
        self.write({"is_active": False})

    #Vazifa: viloyatni faol qilish (is_active=True).
    def action_activate(self):
        self.write({"is_active": True})

    #Vazifa: shu viloyatdagi faol buyurtmasi yo‘q markazlarni topib, ularni nofaol qilish (write).
    def action_deactivate_idle_centers(self):
        centers = self.env['service.center'].search([('active_order_count', '=', 0), ('state_id', '=', self.id)])
        centers.write({"is_active": False})

    #Vazifa: viloyat markazlari bo‘yicha summasi 0 bo‘lgan service.payment yozuvlarini topib unlink qilish.
    def action_cleanup_zero_payments(self):
        payments = self.env['service.payment'].search([('center_id.state_id', '=', self.id), ('amount', '=', 0)])
        payments.unlink()

    #Vazifa: viloyat markazlaridagi state='in_progress' buyurtmalarni state='done' ga o‘tkazish (write).
    def action_finish_all_in_progress(self):
        orders = self.env['service.order'].search([('state', '=', 'done'), ('center_id.state_id', '=', self.id)])
        orders.write({"state", "done"})

    #compute
    @api.depends()
    def _today_order_ids(self):
        for record in self:
            record.today_order_ids = self.env['service.order'].search([('order_date', '>=', fields.Date.today())])

    @api.depends('today_order_ids')
    def _today_order_count(self):
        for record in self:
            record.today_order_count = len(record.today_order_ids)

    @api.depends('district_ids')
    def _compute_district_count(self):
        for record in self:
            record.district_count = len(record.district_ids)

    @api.depends('center_ids')
    def _compute_center_count(self):
        for record in self:
            record.center_count = len(record.center_ids)

    @api.depends()
    def _compute_technician_id(self):
        for record in self:
            record.technician_ids = self.env['service.technician'].search([('center_id.state_id', '=', record.id)])

    @api.depends('technician_ids')
    def _compute_technician_count(self):
        for record in self:
            record.technician_count = len(record.technician_ids)

    @api.depends()
    def _compute_active_order_ids(self):
        for record in self:
            record.active_order_ids = self.env['service.order'].search([('center_id.state_id', '=', record.id), ('state', 'not in', ['done', 'cancelled'])])

    @api.depends('active_order_ids')
    def _compute_active_order_count(self):
        for record in self:
            record.active_order_count = len(record.active_order_ids)

    @api.depends()
    def _compute_done_order_ids(self):
        for record in self:
            record.done_order_ids = self.env['service.order'].search([('center_id.state_id', '=', record.id), ('state', '=', 'done')])

    @api.depends('done_order_ids')
    def _compute_done_order_count(self):
        for record in self:
            record.done_order_count = len(record.done_order_ids)

    @api.depends()
    def _compute_total_revenue(self):
        for record in self:
            payments = self.env['service.payment'].search([('center_id.state_id', '=', record.id), ('state', '=', 'confirmed')])
            record.total_revenue = sum(payments.mapped('amount'))

    @api.depends()
    def _compute_avg_rating(self):
        for record in self:
            ratings = self.env['service.order.rating'].search([('center_id.state_id', '=', record.id)])
            if ratings:
                record.avg_rating = sum(ratings.mapped('amount'))/len(ratings)
            else:
                record.avg_rating = 0

    @api.depends()
    def _compute_last_order_date(self):
        for record in self:
            orders = self.env['service.order'].search([('center_id.state_id', '=', record.id)])
            record.last_order_date = max(orders.mapped('order_date'))

    @api.constrains('area_km2')
    def check_area_condition(self):
        for record in self:
            if record.area_km2<0:
                raise ValidationsError("Maydon qiymati 0 dan katta bo'lishi kerak")

    @api.constrains('population')
    def _check_population_condition(self):
        for record in self:
            if record.population<0:
                raise ValidationsError("Aholi soni 0 dan katta bo'lishi kerak")



































