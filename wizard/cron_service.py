from odoo import models, fields, exceptions
from odoo.addons.bite.tools.common import get_content


class CronService(models.TransientModel):
    _name = "cron.service"
    _description = "Cron Service"

    def trigger_tag_analysis(self):
        recs = self.env["crawl.book"].search([("is_content_crawled", "=", True),
                                              ("is_tag_analysed", "=", False)])[:5]

        if not recs:
            raise exceptions.ValidationError("Error! No records found")

        rec = recs[0]
        vals = get_content(rec.content)
        contents = vals.split(" ")
        for content in contents:
            analysis_id = self.env["tag.analysis"].search([("name", "=", content)])
            analysis_id.write({"count": analysis_id.count + 1})

            if not analysis_id:
                self.env["tag.analysis"].create({"name": content})

        rec.write({"is_tag_analysed": True})


