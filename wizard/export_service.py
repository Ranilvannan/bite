from odoo import models, fields


class ExportService(models.TransientModel):
    _name = "export.service"
    _description = "Export Service"

    site_id = fields.Many2one(comodel_name="blog.site", string="Site")
    img = fields.Html(string="Image")

    def trigger_export(self):
        self.img = '<img src="https://pocket-syndicated-images.s3.amazonaws.com/613933ab9b8ca.png" width=60%/>'
        pass
