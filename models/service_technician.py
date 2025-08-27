from odoo import models, fields, api

class ServiceTechnican(models.Model):
    _name = "service.technician"
    _description = "Ustalar"
    _rec_name = "full_name"

    full_name = fields.Char("To'liq ism familyasi", required=True)
    code = fields.Char(string="Kodi")
    is_active = fields.Boolean(string="Faolligi", default=True)
    center_id = fields.Many2one(comodel_name="service.center", string="Markazi")
    phone = fields.Char(string="Telefon raqami")
    email = fields.Char(string="Email")
    specialty = fields.Char(string="Mutaxasisligi", required=True)
    hire_date = fields.Date(string="Ishga yo'llangan sanasi")
    capacity_per_day = fields.Integer(string="Kunlik maksimal bajaradigan ishlar soni")
    order_ids = fields.One2many(comodel_name="service.order", inverse_name="technician_id")
    #compute
    active_order_ids = fields.One2many(comodel_name="service.order", inverse_name="technician_id", compute="_compute_active_order_ids") #1
    active_order_count = fields.Integer(string="Faol buyurtmalar soni", compute="_compute_order_count") #1
    done_order_ids = fields.One2many(comodel_name="service.order", inverse_name="technician_id", compute="_compute_done_order_ids") #1
    done_order_count = fields.Integer(string="Yakunlangan buyurtmalar soni", compute="_compute_done_order_count") #1
    today_order_ids = fields.One2many(comodel_name="service.order", inverse_name="technician_id", compute="_compute_today_order_ids") #1
    today_order_count = fields.Integer(string="Bugungi buyurtmalar soni", compute="_compute_today_order_count") #1
    utilization_rate = fields.Float(string="Bandlik foizi", compute="_compute_utilization_rate") #1
    avg_rating = fields.Float(string="O'rtacha baho", compute="_compute_avg_rating") #1
    total_revenue = fields.Float(string="Jami tushum", compute="_compute_total_revenue") #1
    last_order_date = fields.Date(string="Oxirigi buyurtma sanasi", compute="_compute_last_order_date") #1
    is_buzy = fields.Boolean(string="Hozirgi bandligi", compute="_comute_is_buzy") #1
    
    #mathod
    #Vazifa: usta yozuvini nofaol qilish (is_active=False).
    def action_deactivate(self):
        self.write({"is_active": False})

    #Vazifa: usta yozuvini faol qilish (is_active=True).
    def action_activate(self):
        self.write({"is_active": True})

    @api.depends()
    def _compute_active_order_ids(self):
        for record in self:
            record.active_order_ids = record.order_ids.filtered(lambda r: r.state == 'in_progress' or r.state == 'received' or r.state=='diagnosed')

    @api.depends('active_order_ids')
    def _compute_order_count(self):
        for record in self:
            record.active_order_count = len(record.active_order_ids)

    @api.depends()
    def _compute_done_order_ids(self):
        for record in self:
            record.done_order_ids = record.order_ids.filtered(lambda x: x.state == 'done')

    @api.depends('done_order_ids')
    def _compute_done_order_count(self):
        for record in self:
            record.done_order_count = len(record.done_order_ids)

    @api.depends()
    def _compute_today_order_ids(self):
        for record in self:
            record.today_order_ids = self.env['service.order'].search([('order_date', '>=', fields.Date.today())])

    @api.depends('today_order_ids')
    def _compute_today_order_count(self):
        for record in self:
            record.today_order_count = len(record.today_order_ids)

    @api.depends()
    def _compute_utilization_rate(self):
        for record in self:
            if record.active_order_count > 0 and record.capacity_per_day>0:
                record.utilization_rate = (record.active_order_count / record.capacity_per_day)*100
            else:
                record.utilization_rate = 0

    @api.depends()
    def _compute_avg_rating(self):
        for record in self:
            ratings = self.env['service.order.rating'].search([('technician_id', '=', record.id)])
            if sum(ratings) > 0:
                record.avg_rating = sum(ratings) / len(ratings)
            else:
                record.avg_rating = 0

    @api.depends()
    def _compute_total_revenue(self):
        for record in self:
            payments = self.env['service.payment'].search([('order_id.technician_id', '=', record.id), ('state', '=', 'confirmed')])
            record.total_revenue = sum(payments.mapped('amount'))

    @api.depends()
    def _compute_last_order_date(self):
        for record in self:
            date = self.env['service.order'].search([('technician_id', '=', record.id)], order="order_date desc", limit=1)
            if date:
                record.last_order_date = date.order_date
            else:
                record.last_order_date = False

    @api.depends('active_order_ids')
    def _comute_is_buzy(self):
        for record in self:
            if record.today_order_count >= record.capacity_per_day:
                record.is_buzy = True
            else:
                record.is_buzy = False


