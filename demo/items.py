# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DemoItem(scrapy.Item):
    # define the fields for your item here like:
    company_name = scrapy.Field()
    Descripiton = scrapy.Field()
    Project_Size = scrapy.Field()
    Horly_Rate = scrapy.Field()
    Number_of_Employees = scrapy.Field()
    Founded_Year = scrapy.Field()
    Street_Adress = scrapy.Field()
    Conutry_Adress = scrapy.Field()
    Phone_Number = scrapy.Field()
    company_website = scrapy.Field()    

    pass
