# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class GlintsItem(scrapy.Item):
    platform = scrapy.Field()
    job_position = scrapy.Field()
    company_name = scrapy.Field()
    job_category = scrapy.Field()
    company_location = scrapy.Field()
    job_salary = scrapy.Field()
    job_type = scrapy.Field()
    job_desc = scrapy.Field()
    skills_to_have = scrapy.Field()


class JobstreetItem(scrapy.Item):
    platform = scrapy.Field()
    job_position = scrapy.Field()
    company_name = scrapy.Field()
    years_of_experience = scrapy.Field()
    company_location = scrapy.Field()
    company_address = scrapy.Field()
    posting_date = scrapy.Field()
    closing_date = scrapy.Field()

    # deskripsi pekerjaan
    job_description = scrapy.Field()

    # gambaran perusahaan
    average_processing_time = scrapy.Field()
    company_industry = scrapy.Field()
    company_site = scrapy.Field()
    company_size = scrapy.Field()
    work_environment_waktu_bekerja = scrapy.Field()
    work_environment_gaya_berpakaian = scrapy.Field()
    work_environment_tunjangan = scrapy.Field()
    work_environment_bahasa = scrapy.Field()

    # informasi perusahaan
    company_overview = scrapy.Field()
