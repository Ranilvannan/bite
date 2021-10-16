from odoo import models, fields


class BlogCategory(models.Model):
    _name = "blog.category"
    _description = " Blog Category"
    _rec_name = "name"

    name = fields.Char(string="name", required=True)
    code = fields.Char(string="Code", required=True)
    description = fields.Text(string="Description")
    site_id = fields.Many2one(comodel_name="blog.site", string="Site")
    pin_ids = fields.Many2many(comodel_name="category.pins", string="Pins")


class CategoryPins(models.Model):
    _name = "category.pins"
    _description = "Category Pins"
    _rec_name = "name"

    name = fields.Char(string="Name", required=True)
    category_ids = fields.Many2many(comodel_name="blog.category", string="Category")

    def create_if_not_exist(self, name):
        rec = self.env["category.pins"].search([("name", "=", name)])

        if not rec:
            obj_id = self.env["category.pins"].create({"name": name})
            return obj_id

        return rec
