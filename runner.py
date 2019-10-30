from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from jobparser import settings
from jobparser.spiders.hhru import HhruSpider
from jobparser.spiders.sjru import SjruSpider

if __name__ == '__main__':
    crawler_settings = Settings()  # создаем экземпляр класса Settings
    crawler_settings.setmodule(settings)  # и присваиваем экземпляру параменты из Settings
    process = CrawlerProcess(settings=crawler_settings)  # создаем процесс и устанавливаем Settings
    process.crawl(HhruSpider)  # указываем процессу какой паук использовать
    process.crawl(SjruSpider)
    process.start()  # запуск процесса
