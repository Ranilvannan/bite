from odoo import models, fields, api
from datetime import datetime


class CrawlBook(models.Model):
    _name = "crawl.book"
    _description = "Crawl Book"
    _rec_name = "name"

    date = fields.Date(string="Date", default=datetime.now())
    name = fields.Char(string="Name", readonly=True)

    url = fields.Char(string="URL")
    domain_id = fields.Many2one(comodel_name="blog.domain", string="Domain")
    title = fields.Text(string="Title")
    cat_pin_id = fields.Many2one(comodel_name="category.pins", string="Category Pin")
    series_id = fields.Many2one(comodel_name="blog.series", string="Series")
    content = fields.Text(string="Content")
    published_on = fields.Datetime(string="Published On")

    article_id = fields.Many2one(comodel_name="blog.article", string="Article")

    is_url_crawled = fields.Boolean(string="Is URL", default=False)
    is_content_crawled = fields.Boolean(string="Is Content", default=False)
    is_tag_analysed = fields.Boolean(string="Is Analysed", default=False)

    @api.model
    def create(self, vals):
        vals["name"] = self.env['ir.sequence'].next_by_code("crawl.book")
        return super(CrawlBook, self).create(vals)
