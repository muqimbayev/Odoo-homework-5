from odoo import fields, models, api
from odoo.exceptions import ValidationError

class ServiceCountry(models.Model):
    _name = "service.country"
    _description = "Davlatlar"

    name = fields.Char(string="Nomi")
    code = fields.Char(string="Kodi")
    phone_code = fields.Char(string="Telefon kodi")
    is_active = fields.Boolean(string="Faolligi", default=True)
    state_ids = fields.One2many(comodel_name="service.state", inverse_name="country_id", string="Viloyatlari")
    center_ids = fields.One2many(comodel_name="service.center", inverse_name="country_id", string="Servis markazlari")
    district_ids = fields.One2many(comodel_name="service.district", inverse_name="country_id", string="Tumanlar")
    #compute
    technician_count = fields.Integer(string="Ustalar soni", compute="_compute_technician_count") #1
    state_count = fields.Integer(string="Viloyatlar soni", compute="_compute_state_count") #1
    center_count = fields.Integer(string="Markazlar soni", compute="_compute_center_count") #1
    active_order_count = fields.Integer(string="Faol buyurtmalar soni", compute="_compute_active_order_count") #1
    active_order_ids = fields.One2many(comodel_name="service.order",  compute="_compute_active_order_ids") #1
    done_order_ids = fields.One2many(comodel_name="service.order",  compute="_compute_done_order_ids") #1
    done_order_count = fields.Integer(string="Yakunlangan buyurtmalar soni", compute="_compute_done_order_count") #1
    today_order_ids = fields.One2many(comodel_name="service.order",  compute="_compute_today_order_ids") #1
    today_order_count = fields.One2many(comodel_name="service.order",  compute="_compute_today_order_count") #1
    total_revenue = fields.Float(string="Jami tushum", compute="_compute_total_revenue") #1
    avg_rating = fields.Float(string="O'rtacha rating", compute="_compute_avg_rating") #0
    last_date_order = fields.Date(string="Oxirigi buyurtma sanasi", compute="_compute_last_date_order") #0

    #Method
    #Vazifa: ushbu davlatni nofaol qilish (is_active=False).
    def action_deactivate(self):
        self.write({"is_active": False})

    #Vazifa: ushbu davlatni faol qilish (is_active=True).
    def action_activate(self):
        self.write({"is_active": True})

    #Vazifa: shu davlatdagi faol buyurtmasi yo‘q servis markazlarini topib, ularni nofaol qilish (write).
    def action_deactivate_idle_centers(self):
        centers = self.env['service.center'].search([('active_order_count', '=', 0)])
        centers.write({"is_active": False})

    #Vazifa: shu davlatdagi markazlar bo‘yicha summasi 0 bo‘lgan service.payment yozuvlarini topib unlink qilish.
    def action_cleanup_zero_payments(self):
        centers = self.env['service.payment'].search([('center_id', '=', self.id), ('amount', '=', 0)])
        centers.unlink()

    #Vazifa: shu davlatdagi markazlarda state='in_progress' buyurtmalarni topib, state='done' ga o‘tkazish (write).
    def action_finish_all_in_progress(self):
        in_progress_orders = self.env['service.order'].search([('state', '=', 'in_progress'), ('center_id', '=', self.id)])
        in_progress_orders.write({"state": 'done'})

    #Infobutton
    def center_count_button(self):
        return {
            "name": "Markazlar",
            "type": "ir.actions.act_window",
            "res_model": "service.center",
            "view_mode": "list,form",
            "domain": [("country_id", "in", self.center_ids.mapped("country_id").ids)],
        }

    def done_order_button(self):
        return {
            "name": "Bajarilgan buyurtmalar",
            "type": "ir.actions.act_window",
            "res_model": "service.order",
            "view_mode": "list,form",
            "domain": [("center_id.country_id", "in", self.done_order_ids.mapped("center_id.country_id").ids)],
        }

    #compute
    @api.depends('center_ids.technician_count')
    def _compute_technician_count(self):
        for record in self:
            record.technician_count = self.env['service.technician'].search_count([('center_id.country_id', '=', record.id)])

    @api.depends('state_ids', 'state_ids.country_id')
    def _compute_state_count(self):
        for record in self:
            record.state_count = len(record.state_ids)

    @api.depends('center_ids', 'center_ids.country_id')
    def _compute_center_count(self):
        for record in self:
            record.center_count = len(record.center_ids)

    @api.depends('center_ids.order_ids')
    def _compute_active_order_ids(self):
        for record in self:
            record.active_order_ids = self.env['service.order'].search([('center_id.country_id', '=', record.id), ('state', 'not in', ['cancelled', 'done'])])

    @api.depends('center_ids.order_ids')
    def _compute_active_order_count(self):
        for record in self:
            record.active_order_count = len(record.active_order_ids)

    @api.depends('center_ids.order_ids.state')
    def _compute_done_order_ids(self):
        for record in self:
            record.done_order_ids = self.env['service.order'].search([('center_id.country_id', '=', record.id), ('state', '=', 'done')])

    @api.depends('done_order_ids')
    def _compute_done_order_count(self):
        for record in self:
            record.done_order_count = len(record.done_order_ids)

    @api.depends('center_ids.order_ids')
    def _compute_today_order_ids(self):
        for record in self:
            record.today_order_ids = self.env['service.order'].search([('center_id.country_id', '=', record.id), ('order_date', '<=', fields.Date.today())])

    @api.depends('today_order_ids')
    def _compute_today_order_count(self):
        for record in self:
            record.today_order_count = len(record.today_order_ids)

    @api.depends()
    def _compute_total_revenue(self):
        for record in self:
            payments = self.env['service.payment'].search([('center_id.country_id', '=', record.id), ('state', '=', 'confirmed')])
            record.total_revenue = sum(payments.mapped('amount'))

    @api.depends()
    def _compute_avg_rating(self):
        for record in self:
            rating = self.env['service.order.rating'].search([('center_id.country_id', '=', record.id)])
            if rating:
                record.avg_rating = sum(rating.mapped('score'))/len(rating)
            else:
                record.avg_rating = 0

    @api.depends('center_ids.order_ids')
    def _compute_last_date_order(self):
        for record in self:
            orders = self.env['service.order'].search([('center_id.country_id', '=', record.id)])
            order_date = orders.mapped('order_date')
            if orders:
                record.last_date_order = max(order_date)
            else:
                record.last_date_order = False

    # Cheklovlar
    @api.constrains('name')
    def check_country_name(self):
        for record in self:
            country = self.env['service.country'].search_count([('name', '=', record.name)])
            if country > 1:
                raise ValidationError("Davlat nomi takrorlanmasligi kerak!")

    @api.constrains('code')
    def check_country_code(self):
        for record in self:
            country = self.env['service.country'].search_count([('code', '=', record.code)])
            if country > 1:
                raise ValidationError("Davlat kodi takrorlanmasligi kerak!")

    @api.constrains('phone_code')
    def check_phone_code(self):
        for record in self:
            phone = self.env['service.country'].search_count([('phone_code', '=', record.phone_code)])
            if phone>1:
                raise ValidationError("Davlat telefon kodi takrorlanmasligi kerak!")



