# -*- coding: utf-8 -*-
from odoo import models, fields

class EduProductSimple(models.Model):
    _name = "edu.product.simple"
    _description = "Educational Product (Only Char, Text, Integer, Float)"

    # --- Char fields ---
    name = fields.Char(required=True)                 # Mahsulot nomi
    sku = fields.Char(string="SKU")                   # Mahsulot kodi
    barcode = fields.Char(string="Barcode")           # Shtrix-kod
    brand = fields.Char(string="Brand")               # Brendi
    category = fields.Char(string="Category")         # Toifasi
    color = fields.Char(string="Color")               # Rangi

    # --- Text fields ---
    description = fields.Text(string="Description")   # Tavsif
    notes = fields.Text(string="Internal Notes")      # Ichki eslatmalar

    # --- Integer fields ---
    qty_on_hand = fields.Integer(string="Qty On Hand", default=0)      # Ombordagi miqdor
    min_qty = fields.Integer(string="Min Qty", default=0)              # Minimal miqdor
    max_qty = fields.Integer(string="Max Qty", default=0)              # Maksimal miqdor
    reorder_step = fields.Integer(string="Reorder Step", default=1)    # Qayta buyurtma qadam
    sold_month = fields.Integer(string="Sold This Month", default=0)   # Ushbu oyda sotilgan miqdor

    # --- Float fields ---
    list_price = fields.Float(string="List Price", default=0.0)        # Sotuv narxi
    cost = fields.Float(string="Cost", default=0.0)                    # Tannarx
    discount_percent = fields.Float(string="Discount %", default=0.0)  # Chegirma foizi (%)
    weight = fields.Float(string="Weight (kg)", default=0.0)           # Og'irligi (kg)
    volume = fields.Float(string="Volume (m3)", default=0.0)           # Hajmi (m3)
    rating = fields.Float(string="Rating", default=0.0)                # Reyting
    tax_rate = fields.Float(string="Tax Rate %", default=0.0)          # Soliq stavkasi (%)
    length_cm = fields.Float(string="Length (cm)", default=0.0)        # Uzunligi (sm)
    width_cm  = fields.Float(string="Width (cm)", default=0.0)         # Kengligi (sm)
    height_cm = fields.Float(string="Height (cm)", default=0.0)        # Balandligi (sm)


    def test_method_1(self):
        #1-vazifa Toifasi 'Electronics' bo‘lgan mahsulotlar ro‘yxatini ol.
        self.env['edu.product.simple'].search([('category', '=', 'Electronics')])

    def test_method_2(self):
        #2-vazifa Brendi 'Apple' va narxi 500 dan yuqori mahsulotlar ro‘yxatini ol.
        self.env['edu.product.simple'].search([('brand', '=', 'Apple'), ('list_price', '>', 500)])

    def test_method_3(self):
        #3-vazifa Brendi 'Samsung' yoki 'Xiaomi' bo‘lgan mahsulotlar ro‘yxatini ol.
        self.env['edu.product.simple'].search([('brand', 'in', ['Xiaomi', 'Samsung'])])

    def test_method_4(self):
        #4-vazifa Brendi 'Sony' yoki 'LG' bo‘lib, narxi 300 dan past mahsulotlar ro‘yxatini ol.
        self.env['edu.product.simple'].search([('brand', 'in', ['Sony', 'LG']), ('list_price', '<', 300)])
    
    def test_method_5(self):
        #5-vazifa Nomida 'pro' so‘zi bor mahsulotlar ro‘yxatini ol.
        self.env['edu.product.simple'].search([('name', 'ilike', '%pro%')])

    def test_method_6(self):
        #6-vazifa SKU 'ABC' bilan boshlanadigan mahsulotlar ro‘yxatini ol.
        self.env['edu.product.simple'].search([('sku', 'like', 'ABC%')])

    def test_method_7(self):
        #7-vazifa Shtrix-kodi '789' bilan tugaydigan mahsulotlar ro‘yxatini ol.
        self.env['edu.product.simple'].search([('barcode', 'like', '%789')])

    def test_method_8(self):
        #8-vazifa Tavsifida 'waterproof' so‘zi bor mahsulotlar ro‘yxatini ol.
        self.env['edu.product.simple'].search([('description', 'ilike', 'waterproof')])

    def test_method_9(self):
        #9-vazifa Ombordagi miqdori 10–100 oralig‘idagi mahsulotlar ro‘yxatini ol.
        self.env['edu.product.simple'].search([('qty_on_hand', '>=', 10), ('qty_on_hand', '<=', 100)])

    def test_method_10(self):
        #10-vazifa Og‘irligi 0.5–2.0 kg oralig‘idagi mahsulotlar ro‘yxatini ol.
        self.env['edu.product.simple'].search([('weight', '>=', 0.5), ('weight', '<=', 2)])

    def test_method_11(self):
        #11-vazifa Narxi eng yuqori 5 ta mahsulot ro‘yxatini ol.
        self.env['edu.product.simple'].search([], limit=5, order="list_price desc")

    def test_method_12(self):
        #12-vazifa Narxi bo‘yicha kamayish tartibida 6–10-o‘rinlardagi mahsulotlar ro‘yxatini ol.
        self.env['edu.product.simple'].search([], limit=5, offset=5, order="list_price desc")

    def test_method_13(self):
        #13-vazifa SKU kiritilgan mahsulotlar ro‘yxatini ol.
        self.env['edu.product.simple'].search([('sku', '!=', False)])

    def test_method_14(self):
        #14-vazifa Shtrix-kodi kiritilmagan mahsulotlar ro‘yxatini ol.
        self.env['edu.product.simple'].search([('barcode', '=', False)])

    def test_method_15(self):
        #15-vazifa Chegirmasi ≥ 10% va narxi > 0 bo‘lgan mahsulotlar ro‘yxatini ol.
        self.env['edu.product.simple'].search([('discount_percent', '>=', 10), ('list_price', '>', 0)])

    def test_method_16(self):
        #16-vazifa Ushbu oyda sotilishi 50 dan yuqori mahsulotlar ro‘yxatini ol.
        self.env['edu.product.simple'].search([('sold_month', '>=', 50)])

    def test_method_17(self):
        #17-vazifa Ombordagi miqdori minimal miqdordan past yoki teng (yoki qty_on_hand + reorder_step ≤ min_qty) bo‘lgan mahsulotlar ro‘yxatini ol.
        self.env['edu.product.simple'].search([('qty_on_hand', '<=', 'min_qty')])

    def test_method_18(self):
        #18-vazifa Hajmi > 0 bo‘lgan mahsulotlarni og‘irligi o‘sish, hajmi kamayish tartibida ro‘yxatini ol.
        self.env['edu.product.simple'].search([('volume', '>', 0)], order="weight, volume desc")

    def test_method_19(self):
        #19-vazifa Reytingi ≥ 4.5 va narxi ≤ 1000 bo‘lgan mahsulotlar ro‘yxatini ol.
        self.env['edu.product.simple'].search([('rating', '>=', 4.5), ('list_price', '<=', 1000)])

    def test_method_20(self):
        #20-vazifa Toifasida 'phone' yoki 'tablet' so‘zi bor mahsulotlar ro‘yxatini ol.
        self.env['edu.product.simple'].search(['|', ('category', 'ilike', 'phone'), ('category', 'ilike', 'tablet')])

    def test_method_21(self):
        #21-vazifa Uzunligi ≥ 10, kengligi ≥ 5, balandligi ≥ 2 bo‘lgan mahsulotlar ro‘yxatini ol.
        self.env['edu.product.simple'].search([('length_cm', '>=', 10), ('width_cm', '>=', 5), ('height_cm', '>=', 2)])

    def test_mathod_22(self):
        #22-vazifa Soliq stavkasi 12% yoki 15% bo‘lgan mahsulotlar ro‘yxatini ol.
        self.env['edu.product.simple'].search([('tax_rate', 'in', [12, 15])])

    def test_method_23(self):
        #23-vazifa Brendi 'S' bilan boshlanib, rangi 'red' bilan tugaydigan mahsulotlar ro‘yxatini ol.
        self.env['edu.product.simple'].search([('brand', 'like', 'S%'), ('color', 'like', '%red')])

    def test_method_24(self):
        #24-vazifa Narxi ≥ 1000 va chegirmasi ≥ 20% bo‘lgan mahsulotlar ro‘yxatini ol.
        self.env['edu.product.simple'].search([('list_price', '>=', 1000), ('discount_percent', '>=', 20)])

    def test_method_25(self):
        #25-vazifa Ichki eslatmalarida 'fragile' so‘zi bor mahsulotlar ro‘yxatini ol.
        self.env['edu.product.simple'].search([('notes', 'like', 'fragile')])

    def test_method_26(self):
        #26-vazifa Brendi Apple/Samsung/Xiaomi bo‘lib, toifasida 'phone' so‘zi bor mahsulotlar ro‘yxatini ol.
        self.env['edu.product.simple'].search([('brand', 'in', ['Apple', 'Samsung', 'Xiaomi']), ('category', '=', 'phone')])

    def test_method_27(self):
        #27-vazifa Omborda ≥ 100 bo‘lib, ushbu oyda sotilishi ≤ 5 bo‘lgan mahsulotlar ro‘yxatini ol.
        self.env['edu.product.simple'].search([('qty_on_hand', '>=', 100), ('sold_month', '<=', 5)])

    def test_method_28(self):
        #28-vazifa Narxi 0 yoki tannarxi 0 bo‘lgan mahsulotlar ro‘yxatini ol.
        self.env['edu.product.simple'].search('|', ('list_price', '=', 0), ('cost', '=', 0))

    def test_method_29(self):
        #29-vazifa Chegirma foizi < 0 yoki > 100 bo‘lgan mahsulotlar ro‘yxatini ol.
        self.env['edu.product.simple'].search(['|', ('discount_percent', '<', 0), ('discount_percent', '>', 100)])

    def test_method_30(self):
        #30-vazifa Mahsulotlarni avval brendi A→Z, so‘ng narxi Z→A tartibida ro‘yxatini ol.
        self.env['edu.product.simple'].search([], order="brand, list_price desc")