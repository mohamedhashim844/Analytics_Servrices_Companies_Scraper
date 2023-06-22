import scrapy
from scrapy_playwright.page import PageMethod
import scraper_helper as sh
from urllib.parse import urljoin
from demo.items import DemoItem
def shold_abort_requests(request):
    if request.resource_type == 'image':
        return True
    if request.method == 'POST':
        return True
    
    return False


class DemowSpider(scrapy.Spider):
    name = "demow"
    allowed_domains = ["clutch.co"]

    custom_settings = {
        'PLAYWRIGHT_ABORT_REQUEST':shold_abort_requests
    }    
    #start_urls = ["https://www.f6s.com/companies/data-analytics/saudi-arabia/co"]
    #user_agent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"
    # timeout = 100000 , check_visibility=True
    def start_requests(self):
        
        #url = 'https://clutch.co/sa/it-services/analytics'
        for i in range(0,21):
            yield scrapy.Request(f'https://clutch.co/it-services/analytics?page={i}&related_services=field_pp_sl_artificial_intellige',
                                meta= {
                                    'playwright': True,
                                    'playwright_include_page' : True,
                                    'playwright_page_methods' : [
                                        PageMethod('wait_for_selector', '[data-type="Directory"]'),
                                    ]
                                    },callback=self.second_requests,errback=self.errback)

    async def second_requests(self, response):
        page = response.meta["playwright_page"]
        #page.goto(response, timeout = 0)
        await page.close()
        base_url = 'https://clutch.co'
        for links in response.css('[data-type="Directory"]'):
            link =  urljoin(base_url, links.css('a.company_title.directory_profile::attr(href)').get())
            yield scrapy.Request(link,meta=dict(
                playwright = True,
            
                playwright_include_page = True,
                playwright_page_methods = [
                    PageMethod('wait_for_selector','section#highlights')
                ]
            ),callback=self.parse,errback=self.errback)

    async def parse(self, response):
        item = DemoItem()
        page = response.meta['playwright_page']
        await page.close()
        item['company_name'] = response.css('[title="Provider Title"]::text').get().strip()
        item['company_website'] = response.css('[title="Visit website"]::attr(href)').get().strip()
        for info in response.css('section#highlights'):
            try:
                item['Descripiton'] = info.css('div#profile-summary-text p::text').get().strip(),
                item['Project_Size'] = info.css('[id="summary_section"] [data-tooltip-content="<i>Min. project size</i>"] span.sg-text__title::text').get().strip()
                item['Horly_Rate'] = info.css('[id="summary_section"] [data-tooltip-content="<i>Avg. hourly rate</i>"] span.sg-text__title::text').get().strip()
                item['Number_of_Employees'] = info.css('[id="summary_section"] [data-tooltip-content="<i>Employees</i>"] span.sg-text__title::text').get().strip()
                item['Founded_Year'] = info.css('[id="summary_section"] [data-tooltip-content="<i>Founded</i>"] span.sg-text__title::text').get().strip()
                item['Street_Adress'] = info.css('[id="location_0"] [itemprop="streetAddress"]::text').get().strip()
                item['Conutry_Adress'] = info.css('[id="location_0"] [itemprop="addressCountry"]::text').get().strip()
                item['Phone_Number'] = info.css('[id="location_0"] [title="Location Phone"]::text').get().strip()
            except AttributeError:
                print('none')    
            yield item

    async def errback(self, failure):
        page = failure.request.meta["playwright_page"]
        await page.close()
            