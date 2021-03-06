from odoo import models, fields, exceptions
from odoo.addons.bite.tools.common import clean_url, get_url_content
from datetime import datetime


class CrawlTamilkamaveri(models.Model):
    _name = "crawl.tamilkamaveri"
    _description = "Crawl Tamilkamaveri"
    _code = "TKV"

    page_no = fields.Integer(string="Page Number")

    def url_crawl(self):
        domain_id = self.env["blog.domain"].search([("code", "=", self._code)])

        if not domain_id:
            raise exceptions.ValidationError("Error! Domain not found")

        url = domain_id.url.format(page_no=self.page_no)
        article_html = get_url_content(url)
        self.generate_article(article_html)

    def content_crawl(self):
        recs = self.env["crawl.book"].search([("is_url_crawled", "=", True),
                                              ("is_content_crawled", "=", False)])[:5]

        for rec in recs:
            data = {"is_content_crawled": True}
            article_html = get_url_content(rec.url)
            content = article_html.find("div", class_="entry-content")
            series_url = self.article_series(article_html)

            if series_url:
                series_id = self.env["blog.series"].create_if_not_exist(series_url=series_url)
                data["series_id"] = series_id.id
                series_id.write({"is_crawled": False})

            if content:
                recs = content.find_all("p")
                content_list = ["<p>{data}</p>".format(data=rec.text.strip()) for rec in recs]
                data["content"] = "\n".join(content_list)

            rec.write(data)

    def series_crawl(self):
        recs = self.env["blog.series"].search([("is_crawled", "=", False)])[:5]

        # Not to raise exception if no records found
        if not recs:
            return True

        rec = recs[0]
        url = rec.series_url
        old_url = list()

        while (url not in old_url) and url:
            article_html = get_url_content(url)
            self.generate_article(article_html, rec.id)
            old_url.append(url)
            url = self.get_next_page(article_html)

        rec.write({"is_crawled": True})

    def article_title(self, article):
        result = None
        title_tag = article.find("h2")

        if title_tag:
            a_tag = title_tag.find("a")
            if a_tag:
                result = a_tag.text.strip()

        return result

    def article_url(self, article):
        result = None
        title_tag = article.find("h2")

        if title_tag:
            a_tag = title_tag.find("a")
            if a_tag:
                result = clean_url(a_tag["href"])

        return result

    def article_category(self, article):
        result = "Others"
        category = article.find("span", class_="cat-links")
        if category:
            category_link = category.find("a")
            if category_link:
                result = category_link.text.strip()

        return result

    def article_published_on(self, article):
        result = datetime.now()
        time_tag = article.find("time")
        if time_tag:
            data = time_tag["datetime"]
            result = datetime.strptime(data, "%Y-%m-%dT%H:%M:%S%z")
        return result

    def article_series(self, article):
        result = None
        story_parts = article.find("section", {"id": "story-parts"})
        if story_parts:
            h3 = story_parts.find("h3")
            if h3:
                a_tag = h3.find("a")
                if a_tag:
                    result = clean_url(a_tag["href"])

        return result

    def generate_article(self, soup, series_id=False):
        domain_id = self.env["blog.domain"].search([("code", "=", self._code)])
        article_list = soup.find_all("article")

        for article in article_list:
            data = {"is_url_crawled": True}
            url = self.article_url(article)
            rec = self.env["crawl.book"].search([("url", "=", url)])

            if series_id:
                data["series_id"] = series_id

            if not rec:
                title = self.article_title(article)
                category = self.article_category(article)
                published_on = self.article_published_on(article)
                cat_pin_id = self.env["category.pins"].create_if_not_exist(name=category)
                data.update({
                    "url": url,
                    "title": title,
                    "cat_pin_id": cat_pin_id.id,
                    "domain_id": domain_id.id,
                    "published_on": published_on.strftime("%Y-%m-%d %H:%M:%S"),
                })

                self.env["crawl.book"].create(data)

    def get_next_page(self, soup):
        url = None
        next_page_list = soup.find_all("a", class_="next page-numbers")

        if next_page_list:
            next_page = next_page_list[0]
            url = clean_url(next_page["href"])

        return url


