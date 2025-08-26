from odoo import fields, models, api

class ServiceDistrict(models.Model):
    _name = "service.district"
    _description = "Tumanlar"

    name = fields.Char(string="Nomi")
    code = fields.Char(string="Kodi")
    is_active = fields.Boolean(string="Faolligi", default=True)
    country_id = fields.Many2one(comodel_name="service.country", string="Davlati")
    state_id = fields.Many2one(comodel_name="service.state", string="Viloyati")
    center_ids = fields.One2many(comodel_name="service.center", inverse_name="district_id")
    population = fields.Integer(string="Aholi soni")
    area_km2 = fields.Float(string="Hududi")
    latitude = fields.Float(string="Kengligi")
    longtitude = fields.Float(string="Uzunligi")
    technician_ids = fields.One2many(comodel_name="service.technician",  compute="_compute_technician_ids") #1
    #compute
    center_count = fields.Integer(string="Mrkazlar soni", compute="_compute_center_count") #1
    technician_count = fields.Integer(string="Ustalar soni", compute="_compute_technician_count") #1
    active_order_ids = fields.One2many(comodel_name="service.order",  compute="_compute_active_order_ids") #1
    active_order_count = fields.Integer(string="Faol buyurtmalar soni", compute="_compute_active_order_count") #1
    done_order_ids = fields.One2many(comodel_name="service.order",  compute="_compute_done_order_ids") #1
    done_order_count = fields.Integer(string="Tugallangan buyurtmalar soni", compute="_compute_done_order_count") #1
    total_revenue = fields.Float(string="Jami tushum", compute="_compute_total_revenue") #1
    last_order_date = fields.Date(string="Oxirigi buyurtma sanasi", compute="_compute_last_order_date") #1
    today_order_ids = fields.One2many(comodel_name="service.order", compute="_today_order_ids")  # 1
    today_order_count = fields.Integer(string="Bugungi buyurtmalar soni", compute="_compute_today_order_count")  # 1
    #Method
    #Vazifa: tumanni nofaol qilish (is_active=False).
    def action_deactivate(self):
        self.write({'is_active': False})

    #Vazifa: tumanni faol qilish (is_active=True).
    def action_activate(self):
        self.write({'is_active': True})

    #Vazifa: shu tumandagi faol buyurtmasi yo‘q servis markazlarini topib, ularni nofaol qilish (write).
    def action_deactivate_idle_centers(self):
        centers = self.env['service.center'].search([('active_order_count', '=', 0), ('center_id.district_id', '=', self.id)])
        centers.write({'is_active': False})

    #Vazifa: shu tumandagi markazlar bo‘yicha summasi 0 bo‘lgan service.payment yozuvlarini topib unlink qilish.
    def action_cleanup_zero_payments(self):
        payments = self.env['service.payment'].search([('center_id.district_id', '=', self.id), ('amount', '=', 0)])
        payments.unlink()

    #Vazifa: shu tumandagi markazlarda state='in_progress' buyurtmalarni topib, state='done' ga o‘tkazish (write).
    def action_finish_all_in_progress(self):
        orders = self.env['service.order'].search([('state', '=', 'in_progress'), ('center_id.district_id', '=', self.id)])
        orders.write({"state": 'done'})

    @api.depends()
    def _compute_technician_ids(self):
        for record in self:
            record.technician_ids = self.env['service.technician'].search([('center_id.district_id', '=', record.id)])

    @api.depends()
    def _compute_center_count(self):
        for record in self:
            record.center_count = len(record.center_ids)

    @api.depends('technician_ids')
    def _compute_technician_count(self):
        for record in self:
            record.technician_count = len(record.technician_ids)

    @api.depends()
    def _compute_active_order_ids(self):
        for record in self:
            record.active_order_ids = self.env["service.order"].search([('center_id.district_id', '=', record.id), ('state', 'not in', ['done', 'cancelled'])])

    @api.depends('active_order_ids')
    def _compute_active_order_count(self):
        for record in self:
            record.active_order_count = len(record.active_order_ids)

    @api.depends()
    def _compute_done_order_ids(self):
        for record in self:
            record.done_order_ids = self.env["service.order"].search([('center_id.district_id', '=', record.id), ('state', '=', 'done')])

    @api.depends('done_order_ids')
    def _compute_done_order_count(self):
        for record in self:
            record.done_order_count = len(record.done_order_ids)

    @api.depends('center_ids')
    def _compute_total_revenue(self):
        for record in self:
            center_ids = record.center_ids.ids or []
            if center_ids:
                payments = self.env['service.payment'].search(
                    [('center_id', 'in', center_ids), ('state', '=', 'confirmed')])
                record.total_revenue = sum(payments.mapped('amount'))
            else:
                record.total_revenue = 0.0

    @api.depends()
    def _compute_last_order_date(self):
        for record in self:
            orders = self.env['service.order'].search([('district_id', '=', record.id)])
            if orders:
                record.last_order_date = max(orders.mapped('order_date'))
            else:
                record.last_order_date = False

    @api.depends()
    def _today_order_ids(self):
        for record in self:
            record.today_order_ids = self.env['service.order'].search([('order_date', '>=', fields.Date.today())])

    @api.depends('today_order_ids')
    def _today_order_count(self):
        for record in self:
            record.today_order_count = len(record.today_order_ids)
