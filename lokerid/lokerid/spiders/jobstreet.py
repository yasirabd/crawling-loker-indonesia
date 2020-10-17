import scrapy
from scrapy.selector import Selector
from selenium import webdriver
import time, math
from lokerid.items import JobstreetItem
from bs4 import BeautifulSoup



class JobstreetSpider(scrapy.Spider):
    name = 'jobstreet'
    allowed_domains = ['jobstreet.co.id']
    start_urls = ['https://www.jobstreet.co.id/id/job-search/job-vacancy.php?']
    custom_settings = {
        # specifies exported fields and order
        'FEED_EXPORT_FIELDS': ["platform", "job_position", "company_name", "years_of_experience",
                               "company_location", "company_address", "posting_date", "closing_date",
                               "job_description", "average_processing_time", "company_industry", "company_site",
                               "company_size", "work_environment_waktu_bekerja", "work_environment_gaya_berpakaian", "work_environment_tunjangan",
                               "work_environment_bahasa", "company_overview"],
        'FEED_EXPORT_ENCODING': 'utf-8',
        }

    # def __init__(self):
    #     self.driver = webdriver.Chrome('E:/Belajar/scrapping/jobstreet/chromedriver.exe')

    def parse(self, response):
        # ambil list url pada halaman
        # self.driver.get(response.url)
        time.sleep(3)

        print(">> START LOOKING FOR URL <<")
        # responses = Selector(text=self.driver.page_source)
        for href in response.xpath('//div[@class="position-title header-text"]/a/@href'):
            time.sleep(2)
            url = response.urljoin(href.extract())
            # cek link url sudah benar
            if "sectionRank" in str(url):
                # print('-------', url)
                yield scrapy.Request(url, callback=self.parse_loker)

        # check next page
        next_page = response.xpath('//div[@class="panel-body text-center"]/ul/li/a[@id="page_next"]/@href')

        if next_page:
            url = response.urljoin(next_page.extract_first())
            yield scrapy.Request(url, self.parse)


    def preprocess_data(self, data):
        # join data jika beripa list
        output = " ".join(data)
        # hilangkan newline, space, tab
        output = output.strip()
        output = " ".join(output.split())
        # replace ;
        output = output.replace(";", ",")

        return output


    def parse_loker(self, response):

        item = JobstreetItem()
        item['platform'] = 'jobstreet'
        item['job_position'] = self.preprocess_data(response.xpath('//h1[@id="position_title"]/text()').extract())

        # cek jika company_name terdapat url perusahaan
        item['company_name'] = self.preprocess_data(response.xpath('//div[@id="company_name"]/text()').extract()) or \
                               self.preprocess_data(response.xpath('//div[@id="company_name"]/a/text()').extract())

        item['years_of_experience'] = self.preprocess_data(response.xpath('//div[@id="experience"]/p/span[@id="years_of_experience"]/text()').extract())
        item['company_location'] = self.preprocess_data(response.xpath('//p[@class="main_desc_detail"]/span[@id="single_work_location"]/text()').extract())
        item['company_address'] = self.preprocess_data(response.xpath('//p[@id="address"]/text()').extract())
        item['posting_date'] = self.preprocess_data(response.xpath('//p[@id="posting_date"]/span/text()').extract())
        item['closing_date'] = self.preprocess_data(response.xpath('//p[@id="closing_date"]/text()').extract())

        # # deskripsi pekerjaan
        job_desc = BeautifulSoup(" ".join(response.xpath('//div[@id="job_description"]').extract()), features="lxml")
        item['job_description'] = " ".join(job_desc.get_text().replace("\n", "[SEP]").split()).replace(";",",")

        # gambaran perusahaan
        item['average_processing_time'] = self.preprocess_data(response.xpath('//p[@id="fast_average_processing_time"]/text()').extract())
        item['company_industry'] = self.preprocess_data(response.xpath('//p[@id="company_industry"]/text()').extract())
        item['company_site'] = self.preprocess_data(response.xpath('//a[@id="company_website"]/text()').extract())
        item['company_size'] = self.preprocess_data(response.xpath('//p[@id="company_size"]/text()').extract())

        item['work_environment_waktu_bekerja'] = self.preprocess_data(response.xpath('//p[@id="work_environment_waktu_bekerja"]/text()').extract())

        item['work_environment_gaya_berpakaian'] = self.preprocess_data(response.xpath('//p[@id="work_environment_gaya_berpakaian"]/text()').extract())
        item['work_environment_tunjangan'] = self.preprocess_data(response.xpath('//p[@id="work_environment_tunjangan"]/text()').extract())
        item['work_environment_bahasa'] = self.preprocess_data(response.xpath('//p[@id="work_environment_bahasa_yang_digunakan"]/text()').extract())

        # informasi perusahaan
        company_overview = BeautifulSoup(" ".join(response.xpath('//div[@id="company_overview_all"]').extract()), features="lxml")
        item['company_overview'] = " ".join(company_overview.get_text().replace("\n", "[SEP]").split()).replace(";",",")

        return item
