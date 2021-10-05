from odoo import models, fields, exceptions
from odoo.addons.bite.tools.common import clean_url


class CrawlTamilkamaveri(models.Model):
    _name = "crawl.tamilkamaveri"
    _description = "Crawl Tamilkamaveri"
    _code = "TKV"

    page_no = fields.Integer(string="Page Number")

    def url_crawl(self):
        domain_id = self.env["blog.domain"].search([("code", "=", self._code)])

        if not domain_id:
            raise exceptions.ValidationError("Error! Domain not found")

    def content_crawl(self):
        recs = self.env["crawl.book"].search([("is_url_crawled", "=", True),
                                              ("is_content_crawled", "=", False)])[:5]

        for rec in recs:
            pass

            rec.write({"is_content_crawled": True})

    def series_crawl(self):
        pass

