import scrapy 

# titulo response.xpath('//h1[@class="documentFirstHeading"]/text()').get()
# parrafo = response.xpath('//div[@class="field-item even"]//p[not(@class)]/text()').get()


class SpiderCIA(scrapy.Spider):
    name = 'cia'
    start_urls = {
        'https://www.cia.gov/readingroom/historical-collections'
    }
    custom_settings = {
        'FEEDS': {
            'cia.json': {
                'format': 'json',
                'encoding': 'utf8',
                'store_empty': False,
                'fields': None,
                'indent': 4,
                'item_export_kwargs': {
                    'export_empty_fields': True,
                },
            },
        },
    }

    def parse(self, response):
        links_desclassified = response.xpath('//a[starts-with(@href, "collection") and (parent::h3|parent::h2)]/@href').getall() ## getall
        for link in links_desclassified:
            yield response.follow(link, callback=self.parse_link, cb_kwargs={'url': response.urljoin(link)})

    def parse_link(self, response, **kwargs):
        link = kwargs['url']
        title = response.xpath('//h1[@class="documentFirstHeading"]/text()').get() ##get
        paragraph = response.xpath('//div[@class="field-item even"]//p[not(@class)]/text()').get() ##get

        yield {
            'url': link,
            'title': title,
            'body': paragraph
        }
