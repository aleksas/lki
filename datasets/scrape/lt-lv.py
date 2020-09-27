
import scrapy
import xmltodict
from scrapy import FormRequest

class LtLvSpider(scrapy.Spider):
    name = 'tl_lv_dict'
    start_urls = ['http://lkiis.lki.lt/paieska']
    scrape_using_keys = True

    def parse(self, response):
        for i in range(9312626, 9560222 + 1):
            formdata = {
                'remoteRecordId': str(i),
                'resourceId':str(105)
            }

            url = 'http://lkiis.lki.lt/paieska?p_p_id=LKISearch_WAR_LKISearchportlet&p_p_lifecycle=2&p_p_state=normal&p_p_mode=view&p_p_cacheability=cacheLevelPage&p_p_col_id=column-1&p_p_col_count=1&_LKISearch_WAR_LKISearchportlet_javax.faces.resource=export&_LKISearch_WAR_LKISearchportlet_ln=xmlResources'
            yield FormRequest(url, formdata=formdata, callback=self.parse_details)

    def parse_details(self, response):
        yield xmltodict.parse(response.text)
