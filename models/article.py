from odoo import models, fields, api
from datetime import datetime


class BlogArticle(models.Model):
    _name = "blog.article"
    _description = "Blog Article"
    _rec_name = "name"

    date = fields.Date(string="Date", default=datetime.now())
    name = fields.Char(string="Name", readonly=True)
    url = fields.Char(string="URL")
    site_id = fields.Many2one(comodel_name="blog.site", string="Site")
    title = fields.Text(string="Title")
    category_id = fields.Many2one(comodel_name="blog.category", string="Category")
    content = fields.Text(string="Content")
    series_id = fields.Many2one(comodel_name="blog.series", string="Series")
    published_on = fields.Datetime(string="Published On")
    tag_ids = fields.Many2many(comodel_name="blog.tags", string="Tags")
    gallery_ids = fields.One2many(comodel_name="blog.photo", inverse_name="article_id", string="Photos")
    is_completed = fields.Boolean(string="Is Completed", default=False)
    is_exported = fields.Boolean(string="Is Exported", default=False)
    analysis_ref = fields.Boolean(string="Ref", default=False)

    @api.model
    def create(self, vals):
        vals["name"] = self.env['ir.sequence'].next_by_code("blog.article")
        return super(BlogArticle, self).create(vals)
