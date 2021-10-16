from odoo import models, fields, exceptions


class BlogEditor(models.Model):
    _name = "blog.editor"
    _description = "Blog Editor"
    _rec_name = "name"

    name = fields.Char(string="Name", readonly=True)
    book_id = fields.Many2one(comodel_name="crawl.book", string="Book")
    url = fields.Char(string="URL")
    site_id = fields.Many2one(comodel_name="blog.site", string="Site")
    title = fields.Text(string="Title")
    category_id = fields.Many2one(comodel_name="blog.category", string="Category")
    content = fields.Text(string="Content")
    series_id = fields.Many2one(comodel_name="blog.series", string="Series")
    published_on = fields.Datetime(string="Published On")
    tag_ids = fields.Many2many(comodel_name="blog.tags", string="Tags")
    gallery_ids = fields.Many2many(comodel_name="blog.photo", string="Photos")
    duplicate_ids = fields.One2many(comodel_name="article.duplicate", inverse_name="editor_id", string="Duplicates")
    in_progress = fields.Boolean(string="In Progress", default=False)

    def check_site(self):
        if not self.site_id:
            raise exceptions.ValidationError("Error! Site not found")

    def trigger_get_category(self):
        self.check_site()
        pin_id = self.env["category.pins"].search([("category_id.site_id", "=", self.site_id.id),
                                                   ("name", "=", self.book_id.category)])
        if not pin_id:
            raise exceptions.ValidationError("Error! Category pins not found")

        if not pin_id.category_id:
            raise exceptions.ValidationError("Error! Category not found")

        self.write({"category_id": pin_id.category_id.id})

    def trigger_get_series(self):
        if self.book_id.series_url:
            series_id = self.env["blog.series"].search([("series_url", "=", self.book_id.series_url)])
            if not series_id:
                raise exceptions.ValidationError("Error! Series not found")

            if not series_id.url:
                raise exceptions.ValidationError("Error! Series URL not found")

            self.write({"series_id": series_id.id})

    def trigger_get_tags(self):
        pass

    def trigger_get_galleries(self):
        pass

    def trigger_check_duplicate(self):
        recs = self.env["blog.editor"].search([("in_progress", "=", True), ("id", "!=", self.id)])

        if recs:
            raise exceptions.ValidationError("Error! Another record In-Progress")

        self.write({"in_progress": True})

    def trigger_generate_article(self):
        pass


class ArticleDuplicate(models.Model):
    _name = "article.duplicate"
    _description = "Article Duplicate"
    _rec_name = "article_id"

    article_id = fields.Many2one(comodel_name="blog.article", string="Article")
    percentage = fields.Float(string="Percentage", default=0.0)
    editor_id = fields.Many2one(comodel_name="blog.editor", string="Editor")
