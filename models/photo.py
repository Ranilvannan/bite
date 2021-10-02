from odoo import models, fields, api


STATUS = [("no_action", "No Action"),
          ("accepted", "Accepted"),
          ("declined", "Declined")]


class BlogPhoto(models.Model):
    _name = "blog.photo"
    _description = "Blog Photo"
    _rec_name = "name"

    name = fields.Char(string="Name", readonly=True)
    photo_url = fields.Char(string="Photo URL")
    status = fields.Selection(selection=STATUS, string="Status", default="no_action")
    category_id = fields.Many2one(comodel_name="blog.category", string="Category")
    article_id = fields.Many2one(comodel_name="blog.article", string="Article")
    is_exported = fields.Boolean(string="Is Exported", default=False)

    @api.model
    def create(self, vals):
        vals["name"] = self.env['ir.sequence'].next_by_code("blog.photo")
        return super(BlogPhoto, self).create(vals)
