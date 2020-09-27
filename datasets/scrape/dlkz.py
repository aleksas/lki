
import scrapy
import xmltodict
from scrapy import FormRequest

class AikosSpider(scrapy.Spider):
    name = 'aikos_mokymo_programos'
    start_urls = ['https://www.aikos.smm.lt/Registrai/SitePages/Studij%C5%B3%20ir%20mokymo%20programos.aspx?ss=9a12994c-547d-442c-a52d-dd2cdb9268f7']
    scrape_using_keys = True

    def parse(self, response):
        for i in range(12479806, 12671814 + 1):
            formdata = {
                'remoteRecordId': str(i),
                'resourceId':str(207)
            }

            url = 'http://lkiis.lki.lt/paieska?p_p_id=LKISearch_WAR_LKISearchportlet&p_p_lifecycle=2&p_p_state=normal&p_p_mode=view&p_p_cacheability=cacheLevelPage&p_p_col_id=column-1&p_p_col_count=1&_LKISearch_WAR_LKISearchportlet_javax.faces.resource=export&_LKISearch_WAR_LKISearchportlet_ln=xmlResources'
            yield FormRequest(url, formdata=formdata, callback=self.parse_details)

    def parse_details(self, response):
        yield xmltodict.parse(response.text)
