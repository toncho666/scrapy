# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem
import json


class SjruSpider(scrapy.Spider):
    name = 'superjob'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://www.superjob.ru/vacancy/search/?keywords=python&geo%5Bc%5D%5B0%5D=1']
    resource = 'SuperJob'

    def parse(self, response: HtmlResponse):
        # если ставим точку останова здесь, то постоянно наблюдал как отсутствует спарсенный материал (подобно ситуации на первом уроке с ссылкой hh.ru
        #pass

        next_page = response.css(
            'div.L1p51 > a.f-test-link-dalshe::attr(href)').extract_first()  # формируем запрос по тегу

        yield response.follow(next_page, callback=self.parse)  # производим вызов функцией самой себя для след.страниц

        vacancy = response.css('div.f-test-vacancy-item a[class*=f-test-link][href^="/vakansii"]::attr(href)').extract()

        for link in vacancy:
            yield response.follow(link, self.vacancy_parse)

    def vacancy_parse(self, response: HtmlResponse):
        name = response.css('h1 ::text').extract()
        salary_min = \
        json.loads(response.css('div._1Tjoc._3C60a.Ghoh2.UGN79._1XYex > script::text').extract_first())['baseSalary'][
            'value']['minValue']
        salary_max = \
        json.loads(response.css('div._1Tjoc._3C60a.Ghoh2.UGN79._1XYex > script::text').extract_first())['baseSalary'][
            'value']['maxValue']
        currency = \
        json.loads(response.css('div._1Tjoc._3C60a.Ghoh2.UGN79._1XYex > script::text').extract_first())['baseSalary'][
            'currency']
        link = response.url
        resource = SjruSpider.resource

        yield JobparserItem(name=name, salary_min=salary_min, salary_max=salary_max, currency=currency, link=link,
                            resource=resource)
