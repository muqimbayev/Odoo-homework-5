from odoo import models, fields, api
from datetime import date
from dateutil.relativedelta import relativedelta  

class Customer(models.Model):
    _name = "ecommerce2.customer"
    _description = "Mijozlar"
    _rec_name = "full_name"

    
    first_name = fields.Char(string="Ismi", required=True)
    last_name = fields.Char(string="Familya", required=True)
    middle_name = fields.Char(string="Sharfi")
    full_name = fields.Char(string="To'liq ism familyasi", compute="_compute_full_name")
    abbr = fields.Char(string="Ism familya qisqartmasi", compute="_compute_abbr")
    birth_date = fields.Date(string="Tug'ilgan sanasi", required=True)
    age = fields.Char(string="Yoshi yil/oy/kun", compute="_compute_age")
    phone_number = fields.Char(string="Telefon raqami")
    email = fields.Char(string="Email")
    email_domain = fields.Char(string="Email domain", compute="_compute_email_domain")
    country = fields.Char(string="Yashayotgan davlat", required=True)
    region = fields.Char(string="Yashayotgan viloyat", required=True)
    district = fields.Char(string="Yashayotgan tuman", required=True)
    street = fields.Char(string="Yashayotgan ko'chasi", required=True)
    address = fields.Char(string="To'liq manzil", compute="_compute_full_adress")
    order_id = fields.One2many(comodel_name="ecommerce2.order", inverse_name="customer_id")
    order_count = fields.Integer(string="Buyurtmalar soni", compute="_compute_customer_order_count") 
    order_ids = fields.One2many("ecommerce2.order", "customer_id", string="Buyurtmalar")

 
    @api.depends("birth_date")
    def _compute_age(self):
        today = date.today()
        for rec in self:
            if rec.birth_date:
                delta = relativedelta(today, rec.birth_date)
                yil = f"{delta.years} yil" if delta.years else ""
                oy = f"{delta.months} oy" if delta.months else ""
                kun = f"{delta.days} kun" if delta.days else ""
                rec.age = f"{yil}/{oy}/{kun}".strip()
            else:
                rec.age = ""

    @api.depends('email')
    def _compute_email_domain(self):
        for record in self:
            if record.email:
                record.email_domain = record.email.split("@")[-1]
                continue
            record.email_domain = ""
            
    @api.depends('first_name', 'last_name', 'middle_name')
    def _compute_full_name(self):
        for record in self:
            if record.middle_name:
                record.full_name = f"{record.first_name} {record.last_name} {record.middle_name}"
                continue
            record.full_name = f"{record.first_name} {record.last_name}"

    @api.depends('first_name', 'last_name', 'middle_name')
    def _compute_abbr(self):
        for record in self:
            if record.middle_name:
                record.abbr = f"{record.first_name[0]}.{record.last_name[0]}.{record.middle_name[0]}."
                
            elif record.first_name:
                record.abbr = f"{record.first_name[0]}.{record.last_name[0]}."
    
    @api.depends('country', 'region', 'district', 'street')
    def _compute_full_adress(self):
        for record in self:
            record.address = f"{record.street}, {record.district}, {record.region}, {record.country}"

    @api.depends('order_id')
    def _compute_customer_order_count(self):
        count = 0
        for record in self:
            record.order_count = len(record.order_ids)


    def action_count_order_customer(self):
        return {
            "name": "Buyurtmalar",
            "type": "ir.actions.act_window",
            "res_model": "ecommerce2.order",
            "view_mode": "list,form",
            "domain": [('id', "in", self.order_ids.ids)],
        }
