from odoo import fields, models, api
from odoo.exceptions import ValidationError

class Customer(models.Model):
    _name = "rental_managment.customer"
    _description = "Customer"

    name = fields.Char(string="full name", required=True)
    phone = fields.Char(string="phone_number", required=True)
    email = fields.Char(string="Email")
    rental_order_ids = fields.One2many(comodel_name='rental_managment.rental_order', inverse_name="customer_id", required=True)
    
    @api.constrains('email')
    def check_email(self):
            for record in self:
                mail = record.email.split('@')
                if not ( "@" in record.email and mail[-1] in ['gmail.com', 'mail.ru']):
                    raise ValidationError("Email manzili to'g'ri emas!")
                

