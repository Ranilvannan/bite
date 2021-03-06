from odoo import models, fields, exceptions

TRANSFER_TYPE = [("single_story", "Single Story"),
                 ("series_story", "Series Story")]


class TransferService(models.TransientModel):
    _name = "transfer.service"
    _description = "Transfer Service"

    story_ids = fields.Many2many(comodel_name="crawl.book", string="Stories",
                                 domain="[('is_content_crawled', '=', True),('article_id', '=', False),('series_id', '=', False)]")
    series_id = fields.Many2one(comodel_name="blog.series", string="Series",
                                domain="[('is_crawled', '=', True)]")
    transfer_type = fields.Selection(selection=TRANSFER_TYPE, string="Transfer Type", default="single_story",
                                     required=True)

    def trigger_move(self):
        recs = list()
        self.check_editor()
        if self.transfer_type == "single_story":
            recs = self.story_ids
        elif self.transfer_type == "series_story":
            self.check_series()
            recs = self.env["crawl.book"].search([('is_content_crawled', '=', True),
                                                  ('article_id', '=', False),
                                                  ("series_id", "=", self.series_id.id)])

        for rec in recs:
            editor_id = self.env["blog.editor"].search([("book_id", "=", rec.id)])
            data = {
                "name": rec.name,
                "book_id": rec.id,
                "title": rec.title,
                "content": rec.content
            }

            if rec.series_id:
                data["series_id"] = rec.series_id.id

            if not editor_id:
                self.env["blog.editor"].create(data)

    def check_editor(self):
        editor_obj = self.env["blog.editor"].search([])
        if editor_obj:
            raise exceptions.ValidationError("Error! Some records found in editor")

    def check_series(self):
        recs = self.env["crawl.book"].search([("series_id", "=", self.series_id.id),
                                              ("is_content_crawled", "!=", True)])

        if recs:
            raise exceptions.ValidationError("Error! Some records not crawled")
