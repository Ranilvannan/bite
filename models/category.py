from odoo import models, fields


class BlogCategory(models.Model):
    _name = "blog.category"
    _description = " Blog Category"
    _rec_name = "name"

    name = fields.Char(string="name", required=True)
    code = fields.Char(string="Code", required=True)
    description = fields.Text(string="Description")
    site_id = fields.Many2one(comodel_name="blog.site", string="Site")
    pin_ids = fields.One2many(comodel_name="category.pins", inverse_name="category_id", string="Pins")


class CategoryPins(models.Model):
    _name = "category.pins"
    _description = "Category Pins"
    _rec_name = "name"

    name = fields.Char(string="Name", required=True)
    category_id = fields.Many2one(comodel_name="blog.category", string="category")
