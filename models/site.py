from odoo import models, fields


class BlogSite(models.Model):
    _name = "blog.site"
    _description = "Blog Site"
    _rec_name = "name"

    name = fields.Char(string="Name", required=True)
    code = fields.Char(string="Code", required=True)

    host = fields.Char(string="Host")
    port = fields.Char(string="Port")
    username = fields.Char(string="Username")
    passkey = fields.Char(string="Passkey")
    destination = fields.Char(string="Destination")

    category_ids = fields.One2many(comodel_name="blog.category", inverse_name="site_id", string="Category")
