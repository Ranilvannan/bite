from odoo import models, fields
from datetime import datetime


class BlogSeries(models.Model):
    _name = "blog.series"
    _description = "Blog Series"
    _rec_name = "title"

    url = fields.Char(string="URL")
    title = fields.Text(string="Title")
    preview = fields.Text(string="Preview")
    series_url = fields.Char(string="Series URL")
    last_updated = fields.Date(string="Last Updated", default=datetime.now())
    is_crawled = fields.Boolean(string="Is Crawled", default=False)
    article_ids = fields.One2many(comodel_name="blog.article", inverse_name="series_id", string="Articles")

    def create_if_not_exist(self, series_url):
        rec = self.env["blog.series"].search([("series_url", "=", series_url)])

        if not rec:
            obj_id = self.env["blog.series"].create({"series_url": series_url})
            return obj_id

        return rec
