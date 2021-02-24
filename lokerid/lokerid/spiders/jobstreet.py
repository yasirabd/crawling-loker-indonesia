import scrapy
from scrapy.selector import Selector
from selenium import webdriver
import time, math, re, json
from lokerid.items import JobstreetItem
from bs4 import BeautifulSoup


current_page = 1  # current page
n_page = 730  # total crawling page

class JobstreetSpider(scrapy.Spider):
    name = 'jobstreet'
    allowed_domains = ['jobstreet.co.id']
    start_urls = ['https://www.jobstreet.co.id/id/job-search/job-vacancy/1/?sort=createdAt']
    custom_settings = {
        # specifies exported fields and order
        'FEED_EXPORT_FIELDS': ["platform", "job_id", "posted_date", "closing_date", "job_position",
                               "company_name", "salary", "company_location", "avg_process_time", "telephone_number",
                               "working_hours", "company_website", "company_size", "dress_code", "nearby_locations",
                               "company_overview", "job_description", "career_level", "years_of_experience", "qualification",
                               "field_of_study", "industry", "skills", "employment_type", "languages",
                               "job_function", "benefits"],
        'FEED_EXPORT_ENCODING': 'utf-8',
        }


    def parse(self, response):
        global current_page, n_page
        time.sleep(3)

        print(">> START LOOKING FOR URL <<")
        for href in response.xpath('//h1/a/@href'):
            time.sleep(2.2)
            url = response.urljoin(href.extract())
            # validasi link url
            if "sectionRank" in str(url):
                yield scrapy.Request(url, callback=self.parse_loker)

        if current_page < n_page:
            current_page += 1
            url = "https://www.jobstreet.co.id/id/job-search/job-vacancy/"+str(current_page)+"/?sort=createdAt"
            yield scrapy.Request(url, self.parse)

    def preprocess_data(self, data):
        output = data.strip()
        output = " ".join(output.split())
        output = output.replace(";", ",")
        return output


    def parse_loker(self, response):

        pattern = re.compile(r"window.REDUX_STATE = (.*);", re.MULTILINE)
        data = response.xpath('//script[contains(., "window.REDUX_STATE")]/text()').re(pattern)[0]
        data = json.loads(data)
        details = data['details']

        item = JobstreetItem()
        item['platform'] = 'jobstreet'
        item['job_id'] = details['id']

        # header
        header = details['header']
        item['posted_date'] = header['postedAt']
        item['closing_date'] = details['jobDetail']['jobRequirement']['closingDate']
        item['job_position'] = header['jobTitle']
        item['company_name'] = header['company']['name']
        min_salary, max_salary = header['salary']['min'], header['salary']['max']
        currency, type = header['salary']['currency'], header['salary']['type']
        item['salary'] = currency+' '+min_salary+' - '+max_salary+' / '+type

        # company detail
        company_detail = details['companyDetail']
        item['company_location'] = [d['location'] for d in details['location']]
        item['avg_process_time'] = company_detail['companySnapshot']['avgProcessTime']
        item['telephone_number'] = company_detail['companySnapshot']['telephoneNumber']
        item['working_hours'] = company_detail['companySnapshot']['workingHours']
        item['company_website'] = company_detail['companySnapshot']['website']
        item['company_size'] = company_detail['companySnapshot']['size']
        item['dress_code'] = company_detail['companySnapshot']['dressCode']
        item['nearby_locations'] = company_detail['companySnapshot']['nearbyLocations']
        item['company_overview'] = self.preprocess_data(company_detail['companyOverview']['html'])

        # job detail
        job_detail = details['jobDetail']
        item['job_description'] = self.preprocess_data(job_detail['jobDescription']['html'])
        item['career_level'] = job_detail['jobRequirement']['careerLevel']
        item['years_of_experience'] = job_detail['jobRequirement']['yearsOfExperience']
        item['qualification'] = job_detail['jobRequirement']['qualification']
        item['field_of_study'] = job_detail['jobRequirement']['fieldOfStudy']
        industry_val = job_detail['jobRequirement']['industryValue']
        item['industry'] = industry_val['label'] if industry_val else None
        item['skills'] = job_detail['jobRequirement']['skills']
        item['employment_type'] = job_detail['jobRequirement']['employmentType']
        item['languages'] = job_detail['jobRequirement']['languages']
        item['job_function'] = [j['name'] for j in job_detail['jobRequirement']['jobFunctionValue']]
        item['benefits'] = [b for b in job_detail['jobRequirement']['benefits']]

        return item
