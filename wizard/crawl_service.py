from odoo import models, fields

PROJECT = [("crawl.tamilkamaveri", "Tamilkamaveri")]
CRAWL_TYPE = [("url", "URL"),
              ("content", "Content"),
              ("series", "Series")]


class CrawlService(models.TransientModel):
    _name = "crawl.service"
    _description = "Crawl Service"

    project = fields.Selection(selection=PROJECT, string="Project", required=True)
    crawl_type = fields.Selection(selection=CRAWL_TYPE, string="Crawl Type", required=True)
    page_no = fields.Char(string="Page No")

    def trigger_crawl(self):
        obj = self.env[self.project].create({
            "page_no": self.page_no
        })

        if self.crawl_type == "url":
            obj.url_crawl()
        elif self.crawl_type == "content":
            obj.content_crawl()
        elif self.crawl_type == "series":
            obj.series_crawl()
