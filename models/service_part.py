from odoo import fields, models, api

class ServicePart(models.Model):
    _name = "service.part"
    _description = "Detallar"

    name = fields.Char(string="Nomi", required=True)
    code = fields.Char(string="Kodi")
    is_active = fields.Boolean(string="Faolligi", default=True)
    description = fields.Text(string="Izoh")

    #Method
    #Vazifa: detalni nofaol qilish (is_active=False).
    def action_deactivate(self):
        self.write({'is_active': False})

    #Vazifa: detalni faol qilish (is_active=True).
    def action_activate(self):
        self.write({'is_active': True})

