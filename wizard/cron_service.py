from odoo import models, fields
from datetime import datetime


class CronService(models.TransientModel):
    _name = "cron.service"
    _description = "Cron Service"

    def trigger_update_category(self):
        recs = self.env["crawl.book"].search([("is_content_crawled", "=", True),
                                              ("is_category_checked", "=", False)])[:10]

        for rec in recs:
            category_id = self.env["category.pins"].search([("name", "=", rec.category)])

            if not category_id:
                self.env["category.pins"].create({"name": rec.category})

            rec.write({"is_category_checked": True})

    def trigger_update_series(self):
        recs = self.env["crawl.book"].search([("is_content_crawled", "=", True),
                                              ("is_series_checked", "=", False),
                                              ("series_url", "!=", False)])[:10]

        for rec in recs:
            series_id = self.env["blog.series"].search([("series_url", "=", rec.series_url)])

            if not series_id:
                self.env["blog.series"].create({"series_url": rec.series_url})

            rec.write({"is_series_checked": True})

    def trigger_tag_analysis(self):
        recs = self.env["crawl.book"].search([("is_content_crawled", "=", True),
                                              ("is_tag_analysed", "=", False)])[:1]

        for rec in recs:
            contents = rec.content.split(" ")
            for content in contents:
                analysis_id = self.env["tag.analysis"].search([("name", "=", content)])
                analysis_id.write({"count": analysis_id.count + 1})

                if not analysis_id:
                    self.env["tag.analysis"].create({"name": content})

            rec.write({"is_tag_analysed": True})

    def trigger_check_series(self):
        recs = self.env["blog.series"].search([("is_story_available", "=", False),
                                               ("last_updated", "!=", datetime.now())])[:50]

        for rec in recs:
            book_id = self.env["crawl.book"].search([("series_url", "=", rec.series_url),
                                                     ("article_id", "=", False)])

            if book_id:
                rec.write({"is_story_available": True})

            rec.write({"last_updated": datetime.now()})

