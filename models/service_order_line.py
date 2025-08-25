from odoo import fields, models, api


class ServiceOrderLine(models.Model):
    _name = "service.order.line"
    _description = "Buyurtma qatorlari"

    order_id = fields.Many2one(comodel_name="service.order", string="Buyurtma")
    part_id = fields.Many2one(comodel_name="service.part")
    description = fields.Char(string="Izoh")
    note = fields.Text(string="Eslatma")
    
