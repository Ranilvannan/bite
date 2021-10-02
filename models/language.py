from odoo import models, fields


class BlogLanguage(models.Model):
    _name = "blog.language"
    _description = "Blog Language"
    _rec_name = "name"

    name = fields.Char(string="Name", required=True)
    code = fields.Char(string="Code", required=True)
