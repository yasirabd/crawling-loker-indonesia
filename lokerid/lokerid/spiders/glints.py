import scrapy
from selenium import webdriver
from scrapy.selector import Selector
import time
from bs4 import BeautifulSoup
from lokerid.items import GlintsItem
from webdriver_manager.chrome import ChromeDriverManager


class GlintsSpider(scrapy.Spider):
    name = 'glints'
    allowed_domains = ['glints.com']
    start_urls = ['https://glints.com/id/opportunities/jobs/explore?countries=ID&sortBy=latest']
    custom_settings = {
        # specifies exported fields and order
        'FEED_EXPORT_FIELDS': ["platform", "job_position", "company_name", "job_category",
                               "company_location", "job_salary", "job_type", "job_desc",
                               "skills_to_have"],
        }

    def __init__(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        # self.driver = webdriver.Chrome('E:/Fun/Solver Society/crawling-loker-indonesia/lokerid/chromedriver.exe')

    def parse(self, response):
        self.driver.get(response.url)

        last_height = self.driver.execute_script("return document.body.scrollHeight")
        urls = list()
        while True:
            if len(urls) <= 5000:
                for href in response.css('a::attr(href)'):
                    if "opportunities/jobs" in href.extract():
                        urls.append(href)
            else:
                break
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight-1200);")
            time.sleep(5)
            new_height =  self.driver.execute_script("return document.body.scrollHeight")

        response = Selector(text=self.driver.page_source)
        url_root = "https://glints.com"
        for href in response.css('a::attr(href)'):
            if "opportunities/jobs" in href.extract():
                url = url_root + href.get()
                yield scrapy.Request(url, callback=self.parse_loker)

        self.driver.close()

    def parse_loker(self, response):

        item = GlintsItem()
        item["platform"] = "glints"
        item["job_position"] = response.css('h1::text').extract()[0]
        item["company_name"] = response.css('a::text').extract()[1]
        item["job_category"] =  response.css('p::attr(data-gtm-job-category)').extract()[0] if True else ""
        item["company_location"] = response.css('span::text').getall()[14]

        salary = response.css('span::text').getall()[15:22]
        item["job_salary"] = salary[0] if salary[0] == "Perusahaan tidak menampilkan gaji" else "".join(salary)
        item["job_type"] =  response.css('p::attr(data-gtm-job-type)').extract()[0]

        jdesc = BeautifulSoup(" ".join(response.xpath('//div[@class="DraftEditor-editorContainer"]').extract()), features="lxml")
        item["job_desc"] = " ".join(jdesc.get_text(separator="\n").replace("\n", " [SEP] ").split()).replace(";",",")

        skills = BeautifulSoup(response.xpath('//div[@data-testid="collapsible-content"]').extract()[1], features="lxml")
        item["skills_to_have"] = " ".join(skills.get_text(separator="\n").replace("\n", " [SEP] ").split())

        return item
