from odoo import models, api, fields

class Product(models.Model):
    _name = "log_module.product"
    _description = "Mahsulotlar"

    name = fields.Char(string="Nomi")
    price = fields.Float(string="Narxi")
    quantity = fields.Integer(string="Soni")

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)

        for record in records:
            self.env['log_module.log'].create([{"username": record.create_uid.id,
                                                "message": f"Mahsulot yaratildi: {record.name}---vaqti: {record.create_date}"}])
        return records
    
    def write(self, vals):
        for record in self:
            old_name = record.name
            old_price = record.price
            old_quantity = record.quantity

            super(Product, record).write(vals)

            new_name = record.name
            new_price = record.price
            new_quantity = record.quantity

            if old_price<new_price:
                self.env['log_module.log'].create({"username": record.write_uid.id,
                                               "message": f"{new_name} nomli mahsulot yangilandi: Narxi {old_price} dan {new_price} ga oshildi. Vaqti: {record.write_date}"})
            elif old_price > new_price:
                self.env['log_module.log'].create({"username": record.write_uid.id,
                                               "message": f"{new_name} nomli mahsulot yangilandi: Narxi {old_price} dan {new_price} ga pasaytirildi. Vaqti: {record.write_date}"})
            if old_quantity<new_quantity:
                self.env['log_module.log'].create({"username": record.write_uid.id,
                                               "message": f"{new_name} nomli mahsulot yangilandi: Miqdori {old_quantity} dan {new_quantity} ga oshirldi. Vaqti: {record.write_date}"})
            elif old_quantity>new_quantity:
                self.env['log_module.log'].create({"username": record.write_uid.id,
                                               "message": f"{new_name} nomli mahsulot yangilandi: Miqdori {old_quantity} dan {new_quantity} ga pasaytirildi. Vaqti: {record.write_date}"})
            
            
        return record
    
    def unlink(self):
        for record in self:
            self.env['log_module.log'].create([{"username": self.env.user.id,
                                                "message": f"Mahsulot o'chirldi: {record.name}--{record.price}--{record.quantity} Vaqti: {fields.Datetime.now()}"}])
        return super().unlink()

            