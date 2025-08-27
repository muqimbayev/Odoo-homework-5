from odoo import fields, models, api
from odoo.exceptions import ValidationError

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
    technician_ids = fields.One2many(comodel_name="service.technician", inverse_name="center_id")
    #compute fields
    technician_count = fields.Integer(string="Ustalar soni", compute="_compute_technician_count") #1
    active_order_count = fields.Integer(string="Faol buyurtmalar soni", compute="_compute_active_order_count") #1
    done_order_count = fields.Integer(string="Yakunlangan buyurtmalar soni", compute="_compute_done_order_count") #1
    done_order_ids = fields.One2many(comodel_name="service.order", inverse_name="center_id", compute="_compute_done_orders") #1
    today_order_ids = fields.One2many(comodel_name="service.order", inverse_name="center_id", compute="_compute_today_orders") #1
    today_order_count = fields.Integer(string="Bugungi buyurtmalar soni", compute="_compute_today_order_count") #1
    total_revenue = fields.Float(string="Jami tushum", compute="_compute_total_revenue") #1
    avg_rating = fields.Float(string="O'rtacha baho", compute="_compute_avg_rating") #1
    utilization_rate = fields.Float(string="Bandlik foizi", compute="_compute_utilization_rate") #1
    last_order_date = fields.Date(string="Oxirigi buyurtma sanasi", compute="_compute_last_order_date") #1
    payment_count = fields.Integer(string="To'lovlar soni", compute="_compute_payment_count") #1
    active_order_ids = fields.One2many(comodel_name="service.order",  compute="_compute_active_order_ids") #1

    #Mathod
    #Vazifa: agar faol buyurtma bo‘lmasa markazni nofaol qilish.
    def action_mark_inactive_if_idle(self):
        if self.active_order_count == 0:
            self.write({"is_active": False})
    
    #Vazifa: markazni qaytadan faol qilish (is_active=True).
    def action_activate(self):
        self.write({"is_active": True})

    #Vazifa: markaz bo‘yicha summasi 0 bo‘lgan to‘lovlarni o‘chirish.
    def action_cleanup_zero_payments(self):
        zero_payments = self.env["service.order.payment"].search([('amount', '=', 0)])
        zero_payments.unlink()


    #Vazifa: holati in_progress bo‘lgan barcha buyurtmalarni donega o‘tkazish.
    def action_finish_all_in_progress(self):
        in_progress_order = self.env['service.order'].search([('state', '=', 'in_progress')])
        in_progress_order.write({"state": 'done'})


    #Infobutton
    def payment_count_button(self):
        return {
            "name": "To'lovlar",
            "type": "ir.actions.act_window",
            "res_model": "service.payment",
            "view_mode": "list,form",
            "domain": [("order_id", "in", self.order_ids.ids)],
        }

    def order_count_button(self):
        return {
            "name": "Buyurtmalar",
            "type": "ir.actions.act_window",
            "res_model": "service.order",
            "view_mode": "list,form",
            "domain": [("center_id", "=", self.id)],
        }

    #Compute
    @api.depends('technician_ids')
    def _compute_technician_count(self):
        for record in self:
            record.technician_count = len(record.technician_ids)

    @api.depends('order_ids', 'order_ids.state')
    def _compute_active_order_count(self):
        for record in self:
            record.active_order_count = len(record.active_order_ids)

    @api.depends('order_ids', 'order_ids.state')
    def _compute_done_order_count(self):
        for record in self:
            record.done_order_count = len(record.order_ids.filtered(lambda x: x.state == 'done'))

    @api.depends('order_ids', 'order_ids.state')
    def _compute_done_orders(self):
        for record in self:
            record.done_order_ids = self.env['service.order'].search([('center_id', '=', record.id), ('state', '=', 'done')])

    @api.depends('order_ids')
    def _compute_today_orders(self):
        for record in self:
            record.today_order_ids = record.order_ids.filtered(lambda x: x.order_date and x.order_date.date()==fields.Date.today() and x.center_id == record.id)

    @api.depends('today_order_ids')
    def _compute_today_order_count(self):
        for record in self:
            record.today_order_count = len(record.today_order_ids)

    @api.depends('payment_ids', 'payment_ids.state')
    def _compute_total_revenue(self):
        for record in self:
            record.total_revenue = sum(record.payment_ids.filtered(lambda x: x.state == 'confirmed').mapped('amount'))

    @api.depends('rating_ids', 'rating_ids.score')
    def _compute_avg_rating(self):
        for record in self:
            ratings = record.rating_ids.mapped('score')
            if sum(ratings)>0:
                record.avg_rating = sum(ratings)/len(ratings)
            else:
                record.avg_rating = 0

    @api.depends('active_order_count', 'capacity_per_day')
    def _compute_utilization_rate(self):
        for record in self:
            if record.capacity_per_day != 0:
                record.utilization_rate = record.active_order_count/record.capacity_per_day*100
            else:
                record.utilization_rate = 0

    @api.depends('order_ids')
    def _compute_last_order_date(self):
        for record in self:

            last_order = self.env['service.order'].search([('center_id', '=', record.id)], order="order_date desc", limit=1)
            if last_order:
                record.last_order_date = last_order.order_date
            else:
                record.last_order_date=False

    @api.depends('payment_ids')
    def _compute_payment_count(self):
        for record in self:
            record.payment_count = len(record.payment_ids)

    #Cheklovlar
    @api.constrains('name')
    def check_center_name(self):
        for record in self:
            count = self.env['service.center'].search_count([('name', '=', record.name)])
            if count>1:
                raise ValidationError("Markaz nomi takrorlanmas bo'lishi kerak")

    @api.constrains('code')
    def check_center_code(self):
        for record in self:
            count = self.env['service.center'].search_count([('code', '=', record.code)])
            if count>1:
                raise ValidationError("Markaz kodi takrorlanmas bo'lishi kerak")

    @api.depends()
    def _compute_active_order_ids(self):
            for record in self:
                record.active_order_ids = self.env['service.order'].search([('center_id', '=', record.id), ('state', 'not in', ['cancelled', 'done'])])

