# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CambridgeItem(scrapy.Item):
    # define the fields for your item here like:
    link = scrapy.Field()
    title = scrapy.Field()
    study_level = scrapy.Field()
    qualification = scrapy.Field()
    university_title = scrapy.Field()
    locations = scrapy.Field()
    description = scrapy.Field()
    about = scrapy.Field()
    start_dates = scrapy.Field()
    application_open_dates = scrapy.Field()
    application_close_dates = scrapy.Field()
    entry_requirements = scrapy.Field()
    language_requirements = scrapy.Field()
    modules = scrapy.Field()
    tuitions = scrapy.Field()



