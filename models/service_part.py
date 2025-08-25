from odoo import fields, models, api

class ServicePart(models.Model):
    _name = "service.part"
    _description = "Detallar"

    name = fields.Char(string="Nomi")
    code = fields.Char(string="Kodi")
    is_active = fields.Boolean(string="Faolligi")
    description = fields.Text(string="Izoh")

    #Method
    #Vazifa: detalni nofaol qilish (is_active=False).
    def action_deactivate(self):
        pass

    #Vazifa: detalni faol qilish (is_active=True).
    def action_activate(self):
        pass

