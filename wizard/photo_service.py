from odoo import models, fields, exceptions


class PhotoService(models.TransientModel):
    _name = "photo.service"
    _description = "Photo Service"

    site_id = fields.Many2one(comodel_name="blog.site", string="Site")
    photo_id = fields.Many2one(comodel_name="blog.photo", string="Photo")
    category_id = fields.Many2one(comodel_name="blog.category", string="Category")
    preview = fields.Html(string="Preview")

    def trigger_accept(self):
        if self.photo_id:
            self.photo_id.write({"category_id": self.category_id.id,
                                 "status": "accepted"})

    def trigger_decline(self):
        if self.photo_id:
            self.photo_id.write({"status": "declined"})

    def trigger_load(self):
        recs = self.env["blog.photo"].search([("article_id", "=", False),
                                              ("status", "=", "no_action")])

        if not recs:
            raise exceptions.ValidationError("Error! No photo found")

        self.write({
            "photo_id": recs[0].id,
            "preview": '<img src="{0}" style="max-width:100%;"/>'.format(recs[0].photo_url)
        })
