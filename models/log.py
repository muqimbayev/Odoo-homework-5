from odoo import models, fields, api
from odoo.exceptions import UserError

class Log(models.Model):
    _name = "log_module.log"
    _description = "Log"
    _rec_name = "message"

    username = fields.Many2one("res.users", string="Foydalanuvchi", readonly=True)
    message = fields.Char("Bajargan amali", readonly=True)

    def unlink(self):
        raise UserError("Loglarni o'chirish mumkin emas!")
