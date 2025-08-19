from odoo import models, fields, api

class Product(models.Model):
    _name="ecommerce2.product"
    _description="Mahsulotlar"

    name = fields.Char(string="Nomi", required=True)
    slug = fields.Char(string="Slug", compute="_compute_product_slug")
    category_id = fields.Many2one(string="Kategoriyasi", comodel_name="ecommerce2.category", required=True)
    quantity = fields.Integer(string="Miqdori", required=True)
    has_category = fields.Boolean(string="Biror toifaga tegishlimi?", compute="_compute_has_category", store=True)
    price = fields.Float(string="Sotuv narxi", required=True)
    real_price = fields.Float(string="Chegirmadagi narxi", compute="_compute_real_price", store=True)
    tex = fields.Float(string="Soliq (Foizda)", default=12)
    discount = fields.Float(string="Chegirma (Fozida)", default=0)
    cost = fields.Float(string="Tannarxi", required=True)
    tex_amount = fields.Float(string="Soliq summasi", compute="_compute_tex")
    markup_percent = fields.Float(string="Mahsulot ustiga necha foiz qo’yilgan", compute="_compute_markup_percent", store=True)
    total_price = fields.Float(string="Jami summa", compute="_compute_total_price")
    length = fields.Float(string="Bo'yi")
    width = fields.Float(string="Endi")
    height = fields.Float(string="Balandligi")
    volume = fields.Float(string="Hajmi", compute="_compute_volume", store=True)

    @api.depends('name')
    def _compute_product_slug(self):
        for record in self:
            if record.name:
                record.slug = "-".join(record.name.split())
            else:
                record.slug = ""

    
    @api.depends('category_id')
    def _compute_has_category(self):
        for record in self:
            if record.category_id:
                record.has_category = True
                continue
            record.has_category=False

    @api.depends('price', 'cost', 'discount')
    def _compute_markup_percent(self):
        for record in self:
            if not record.discount:
                record.markup_percent = ((record.price - record.cost) / record.cost) * 100 if record.cost > 0 else 0
                continue
            discount_price = record.price-((record.price/100)*record.discount) 
            record.markup_percent = ((discount_price - record.cost) / record.cost) * 100 if record.cost > 0 else 0

    @api.depends("length", "width", "height")
    def _compute_volume(self):
        for rec in self:
            if rec.length and rec.width and rec.height:
                rec.volume = rec.length * rec.width * rec.height
            else:
                rec.volume = 0

    @api.depends('price', 'discount')
    def _compute_real_price(self):
        for record in self:
            record.real_price = record.price-((record.price/100)*record.discount) 
    
    @api.depends('tex', 'price')
    def _compute_tex(self):
        for record in self:
            record.tex_amount = (record.real_price*((record.tex)/100))

    @api.depends('price', 'tex_amount', 'real_price')
    def _compute_total_price(self):
        for record in self:
            record.total_price = (record.real_price+record.tex_amount)




    



