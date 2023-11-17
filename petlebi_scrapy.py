import scrapy
from scrapy.crawler import CrawlerProcess


class ScrapeItem(scrapy.Item):
    UrL = scrapy.Field()
    Name = scrapy.Field()
    Barcode = scrapy.Field()
    Price = scrapy.Field()
    Stock = scrapy.Field()
    Images = scrapy.Field()
    Sku = scrapy.Field()
    Description = scrapy.Field()
    Category = scrapy.Field()
    P_id = scrapy.Field()
    Brand = scrapy.Field()
    pass


class ScrapeSpider(scrapy.Spider):
    name = "Spider"
    allowed_domains = ["petlebi.com"]
    start_urls = ["https://www.petlebi.com/"]

    custom_settings = {
        "FEED_URI": "petlebi_products.json",
        "FEED_FORMAT": "json",
        "FEED_EXPORTERS": {
            "json": "scrapy.exporters.JsonItemExporter",
        },
        "FEED_EXPORT_ENCODING": "utf-8",
    }

    def __init__(self):
        self.declare_xpath()

    def declare_xpath(self):
        self.getCatCategoriesPath = '//*[@id="header"]/div[2]/div/div/nav/ul/li[1]/div/div/ul/li[1]/div/div/div/div//@href'
        self.getDogCategoriesPath = '//*[@id="header"]/div[2]/div/div/nav/ul/li[2]/div/div/ul/li[1]/div/div/div/div//@href'
        self.getBirdCategoriesPath = '//*[@id="header"]/div[2]/div/div/nav/ul/li[3]/div/div/ul/li/div/div/div/div//@href'
        self.getAllItemsPath = '//*[@id="products"]//@href'
        self.UrlPath = ""
        self.NamePath = "/html/body/div[3]/div[2]/div/div/div[2]/h1/text()"
        self.BarcodePath = '//*[@id="hakkinda"]/div[3]/div[2]/text()'
        self.PricePath = (
            "/html/body/div[3]/div[2]/div/div/div[2]/div[2]/div[2]/span/p[2]/text()"
        )
        self.StockPath = ""
        self.ImagesPath = '//*[@id="photoGallery"]//@href'
        self.SkuPath = '//*[@id="hakkinda"]/div[4]/div[2]/text()'
        self.DescriptionPath = '//*[@id="productDescription"]/p/text()'
        self.CategoryPath = "/html/body/div[3]/div[1]/div/div/div[1]/ol/li//@title"
        self.P_idPath = ""
        self.BrandPath = '//*[@id="hakkinda"]/div[1]/div[2]/span/a/text()'

    def parse(self, response):
        all = (
            response.xpath(self.getDogCategoriesPath)
            + response.xpath(self.getCatCategoriesPath)
            + response.xpath(self.getBirdCategoriesPath)
        )
        for href in all:
            url = response.urljoin(href.extract())
            yield scrapy.Request(
                url=url, callback=self.parse_subcategory, dont_filter=True
            )

    def parse_subcategory(self, response):
        for href in response.xpath(self.getAllItemsPath):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_main_item, dont_filter=True)

    def parse_main_item(self, response):
        item = ScrapeItem()

        UrL = response.url
        Name = "".join(response.xpath(self.NamePath).extract())
        Category = "-".join(response.xpath(self.CategoryPath).extract()[1:4])
        Barcode = "".join(response.xpath(self.BarcodePath).extract())
        Price = "".join(response.xpath(self.PricePath).extract())
        # Stock = response.xpath(self.StockPath).extract()
        Images = "".join(response.xpath(self.ImagesPath).extract())
        Sku = "".join(response.xpath(self.SkuPath).extract())
        Description = " ".join(response.xpath(self.DescriptionPath).extract())
        # P_id = response.xpath(self.P_idPath).extract()
        Brand = "".join(response.xpath(self.BrandPath).extract())

        item["UrL"] = UrL
        item["Name"] = Name
        item["Category"] = Category
        item["Barcode"] = Barcode
        item["Price"] = Price
        # item["Stock"] = Stock
        item["Images"] = Images
        item["Sku"] = Sku
        item["Description"] = Description
        # item["ID"] = P_id
        item["Brand"] = Brand

        return item


craw = CrawlerProcess()
craw.crawl(ScrapeSpider)
craw.start()
