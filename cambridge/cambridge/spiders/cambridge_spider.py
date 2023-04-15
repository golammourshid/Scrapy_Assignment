import re

import scrapy
import requests
import lxml.html
from lxml.cssselect import CSSSelector
from ..items import CambridgeItem


class CambridgeSpider(scrapy.Spider):
    name = 'cambridge'
    start_urls = [
        'https://www.postgraduate.study.cam.ac.uk/courses/directory/poafmpafs'
    ]
    items = CambridgeItem()

    def parse(self, response, **kwargs):
        self.items["link"] = 'https://www.postgraduate.study.cam.ac.uk/courses/directory/poafmpafs'
        title = response.css('.easy-breadcrumb_segment-title::text')[0].extract()
        self.items['title'] = title
        self.items["study_level"] = 'Postgraduate'
        qualification = response.xpath(
            '//*[@id="block-fieldblock-node-gao-course-default-field-gao-sidebar"]/div/div/div/div/h4[2]/a/text()').get()
        self.items['qualification'] = qualification
        self.items["university_title"] = 'University of Cambridge'

        locations = response.xpath('/html/body/div[9]/div/div[1]/div/ul/li[1]//a/@href').get()

        description = response.css('.field-name-field-gao-course-overview p:nth-child(1)::text')[0].extract()
        description = repr(description)
        yield scrapy.Request(locations, callback=self.get_locations)
        self.items['description'] = description
        aboutTitle = response.css('p:nth-child(5)::text')[0].extract()

        about = response.css('ol li::text').extract()
        about = ' '.join(about)
        about = aboutTitle + ' ' + about
        self.items['about'] = about

        application_open_dates = response.css('dd:nth-child(2)::text').extract()
        self.items['application_open_dates'] = application_open_dates[0]

        application_close_dates = response.css('dd:nth-child(4)::text').extract()
        self.items['application_close_dates'] = application_close_dates[0]

        start_dates = response.css('dd:nth-child(6)::text').extract()
        self.items['start_dates'] = start_dates[0]

        requirements_page = response.css('#page-content li:nth-child(3) a::attr(href)').get()
        yield response.follow(requirements_page, callback=self.requirements_info)

        finance_page = response.css('#page-content li:nth-child(4) a::attr(href)').get()
        yield response.follow(finance_page, callback=self.finance_info)

        study_page = response.css('#page-content li:nth-child(2) a::attr(href)').get()
        yield response.follow(study_page, callback=self.study_info)

        apply_page = response.css('#page-content li:nth-child(5) a::attr(href)').get()
        print("Pages= ")
        print(apply_page)
        yield response.follow(apply_page, callback=self.apply_info)

    def get_locations(self, response):
        # locations = response.xpath('// *[ @ id = "content"] / div[2] / div[1] / div / div / p[2]/text()').get()
        locations = response.css('p~ h2+ p::text').extract()
        locations = ','.join(locations).replace('\n', ' ')
        self.items['locations'] = locations

        yield self.items

    def requirements_info(self, response):
        entry_requirements = response.css('#page-content p+ p:nth-child(4)::text').extract()
        entry_requirements = ','.join(entry_requirements)
        self.items['entry_requirements'] = entry_requirements

        language_requirements = []

        # For IELTS Academic:
        english_language_dict = {}
        academic = ''.join(response.css('h1+ .campl-column6 h3::text').extract())
        english_language_dict['language'] = 'English'
        english_language_dict['test'] = academic

        final_score = ''

        listening = ''.join(response.css('h1+ .campl-column6 tbody tr:nth-child(1) th::text').extract())
        final_score += listening
        final_score += ': '
        listening_score = ''.join(response.css('h1+ .campl-column6 tr:nth-child(1) td::text').extract())
        final_score += listening_score
        final_score += ', '

        writing = ''.join(response.css('h1+ .campl-column6 tr:nth-child(2) th::text').extract())
        final_score += writing
        final_score += ': '
        writing_score = ''.join(response.css('h1+ .campl-column6 tr:nth-child(2) td::text').extract())
        final_score += writing_score
        final_score += ', '

        reading = ''.join(response.css('h1+ .campl-column6 tr:nth-child(3) th::text').extract())
        final_score += reading
        final_score += ': '
        reading_score = ''.join(response.css('h1+ .campl-column6 tr:nth-child(3) td::text').extract())
        final_score += reading_score
        final_score += ', '

        speaking = ''.join(response.css('h1+ .campl-column6 tr:nth-child(4) th::text').extract())
        final_score += speaking
        final_score += ': '
        speaking_score = ''.join(response.css('h1+ .campl-column6 tr:nth-child(4) td::text').extract())
        final_score += speaking_score
        final_score += ', '

        total = ''.join(response.css('h1+ .campl-column6 tr:nth-child(5) th::text').extract())
        final_score += total
        final_score += ': '
        total_score = ''.join(response.css('h1+ .campl-column6 tr:nth-child(5) td::text').extract())
        final_score += total_score

        english_language_dict['score'] = final_score

        language_requirements.append(english_language_dict)

        # For TOEFL Internet Score
        english_language_dict = {}
        academic = ''.join(response.css('.campl-column6:nth-child(10) h3::text').extract())
        english_language_dict['language'] = 'English'
        english_language_dict['test'] = academic

        final_score = ''

        listening = ''.join(response.css('.campl-column6+ .campl-column6 tbody tr:nth-child(1) th::text').extract())
        final_score += listening
        final_score += ': '
        listening_score = ''.join(response.css('.campl-column6+ .campl-column6 tr:nth-child(1) td::text').extract())
        final_score += listening_score
        final_score += ', '

        writing = ''.join(response.css('.campl-column6+ .campl-column6 tr:nth-child(2) th::text').extract())
        final_score += writing
        final_score += ': '
        writing_score = ''.join(response.css('.campl-column6+ .campl-column6 tr:nth-child(2) td::text').extract())
        final_score += writing_score
        final_score += ', '

        reading = ''.join(response.css('.campl-column6+ .campl-column6 tr:nth-child(3) th::text').extract())
        final_score += reading
        final_score += ': '
        reading_score = ''.join(response.css('.campl-column6+ .campl-column6 tr:nth-child(3) td::text').extract())
        final_score += reading_score
        final_score += ', '

        speaking = ''.join(response.css('.campl-column6+ .campl-column6 tr:nth-child(4) th::text').extract())
        final_score += speaking
        final_score += ': '
        speaking_score = ''.join(response.css('.campl-column6+ .campl-column6 tr:nth-child(4) td::text').extract())
        final_score += speaking_score
        final_score += ', '

        total = ''.join(response.css('.campl-column6+ .campl-column6 tr:nth-child(5) th::text').extract())
        final_score += total
        final_score += ': '
        total_score = ''.join(response.css('.campl-column6+ .campl-column6 tr:nth-child(5) td::text').extract())
        final_score += total_score

        english_language_dict['score'] = final_score

        language_requirements.append(english_language_dict)

        # For CAE
        english_language_dict = {}
        academic = ''.join(response.css('.campl-column6~ .campl-column6+ .campl-column6 h3:nth-child(1)::text').extract())
        english_language_dict['language'] = 'English'
        english_language_dict['test'] = academic

        final_score = ''.join(response.css('.campl-side-padding p:nth-child(2)::text').extract()).strip()
        english_language_dict['score'] = final_score
        language_requirements.append(english_language_dict)

        # For CPE
        english_language_dict = {}
        academic = ''.join(response.css('p+ h3::text').extract())
        english_language_dict['language'] = 'English'
        english_language_dict['test'] = academic

        final_score = ''.join(response.css('.campl-side-padding p~ p::text').extract()).strip()
        english_language_dict['score'] = final_score
        language_requirements.append(english_language_dict)
        self.items['language_requirements'] = language_requirements


    def finance_info(self, response):
        tuition = []
        # For Home
        fee_dict = {}
        fee_status = ''.join(response.css('h3+ .campl-control-group .btn-primary::text').extract()).strip()
        fee_dict['fee_status'] = fee_status
        total_annual_commitment = ''.join(response.css('tfoot th+ th::text').extract())
        fee_dict['total_annual_commitment'] = total_annual_commitment
        tuition.append(fee_dict)
        self.items['tuition'] = tuition

    def study_info(self, response):
        assessments = []

        # For Thesis
        assessment_dict = {}
        thesis_assessment_field = ''.join(response.css('h1+ h2::text').extract()).strip()
        assessment_dict['field'] = thesis_assessment_field
        thesis_assessment = ''.join(response.css('p:nth-child(10)::text').extract())
        assessment_dict['details'] = thesis_assessment
        assessments.append(assessment_dict)

        # For Essays
        assessment_dict = {}
        essays_assessment_field = ''.join(response.css('h2:nth-child(11)::text').extract()).strip()
        assessment_dict['field'] = essays_assessment_field
        essays_assessment = ''.join(response.css('p:nth-child(12)::text').extract())
        assessment_dict['details'] = essays_assessment
        assessments.append(assessment_dict)

        # For Written
        assessment_dict = {}
        written_assessment_field = ''.join(response.css('h2:nth-child(14)::text').extract()).strip()
        assessment_dict['field'] = written_assessment_field
        written_assessment = ''.join(response.css('p:nth-child(16)::text').extract())
        assessment_dict['details'] = written_assessment
        assessments.append(assessment_dict)

        # For Other
        assessment_dict = {}
        other_assessment_field = ''.join(response.css('h2:nth-child(17)::text').extract()).strip()
        assessment_dict['field'] = other_assessment_field
        other_assessment = ''.join(response.css('p:nth-child(18)::text').extract())
        assessment_dict['details'] = other_assessment
        assessments.append(assessment_dict)
        self.items['assessments'] = assessments

    def apply_info(self, response):
        things_needed_to_apply = response.css('li strong::text').extract()
        things_needed_to_apply = [things.strip() for things in things_needed_to_apply if bool(re.search(r"[A-Z]", things))]
        things_needed_to_apply = ', '.join(things_needed_to_apply).replace('\n', '')
        self.items['things_needed_to_apply'] = things_needed_to_apply

