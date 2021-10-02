from odoo import models, fields

STATUS = [("added", "Added"), ("excluded", "Excluded"), ("no_action", "No Action")]


class TagAnalysis(models.Model):
    _name = "tag.analysis"
    _description = "Tag Analysis"
    _rec_name = "name"

    name = fields.Char(string="Name", required=True)
    count = fields.Integer(string="Count", required=True, default=1)
    status = fields.Selection(selection=STATUS, string="Status", required=True, default="no_action")
