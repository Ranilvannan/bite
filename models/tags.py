from odoo import models, fields


class BlogTags(models.Model):
    _name = "blog.tags"
    _description = "Blog Tags"
    _rec_name = "name"

    name = fields.Char(string="Name", required=True)
    url = fields.Char(string="URL", required=True)
    article_ids = fields.Many2many(comodel_name="blog.article", string="Articles")
    pin_ids = fields.One2many(comodel_name="tag.pins", inverse_name="tag_id", string="Pins")


class TagPins(models.Model):
    _name = "tag.pins"
    _description = "tag Pins"
    _rec_name = "name"

    name = fields.Char(string="Name", required=True)
    tag_id = fields.Many2one(comodel_name="blog.tags", string="Tag")
