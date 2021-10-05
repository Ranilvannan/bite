from odoo import models, fields


class BlogDomain(models.Model):
    _name = "blog.domain"
    _description = "Blog Domain"
    _rec_name = "name"

    name = fields.Char(string="Name", required=True)
    code = fields.Char(string="Code", required=True)
    url = fields.Char(string="URL", required=True)
