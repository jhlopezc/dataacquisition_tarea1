# -*- coding: utf-8 -*-
import scrapy
from wikipedia_daily.items import articles, article
import w3lib.html

class ArticleSpider(scrapy.Spider):
    name = 'article'
    allowed_domains = ['en.wikipedia.org']
    start_urls = ['https://en.wikipedia.org/wiki/Wikipedia:Featured_articles']

    custom_settings = {
        'FEED_FORMAT' : 'json',
        'FEED_URI' : 'file:c://Users//jhlopez//wikipedia_scraping//wikipedia_daily//wikipedia_daily//featured_article-%(time)s.json'
    }

    def parse(self, response):
        contador = 0
        host = self.allowed_domains[0]
        for link in response.css(".featured_article_metadata > a"):
            title = link.attrib.get("title")   #link
            link = f"https://{host}{link.attrib.get('href')}"
            contador = contador + 1
            yield response.follow(link, callback=self.parse_detail, meta={'link' : link, 'title':title})
            #yield articles(
            #    title = link.attrib.get("title"),
            #    link = f"https://{host}{link.attrib.get('href')}"
            #)
            if contador == 25:
                exit()

    def parse_detail(self, response):
        items = articles()
        item = article()

        items["link"] = response.meta["link"]
        item["title"] = response.meta["title"]
        item["paragraph"] = list()

        #for text in response.css(".mw-body-content p::text").extract():
        for link in response.css(".mw-body-content p").extract():
            link2 = w3lib.html.remove_tags(link).strip()
            hay_punto = link2.find(".",0)
            if len(link2) > 0:
                item["paragraph"].append(link2[:hay_punto]+".")
            if hay_punto >= 0: # and len(link2) > 30:
                break

        items["body"] = item
        return items
