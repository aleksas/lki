from scrapy import FormRequest, Spider
from zipfile import ZipFile, ZIP_DEFLATED

class LkiSpider(Spider):
    name = 'dlkz'
    start_urls = ['http://lkiis.lki.lt']
    resource_id = 0
    resource_range = 0, 0
    url = 'http://lkiis.lki.lt/paieska?p_p_id=LKISearch_WAR_LKISearchportlet&p_p_lifecycle=2&p_p_state=normal&p_p_mode=view&p_p_cacheability=cacheLevelPage&p_p_col_id=column-1&p_p_col_count=1&_LKISearch_WAR_LKISearchportlet_javax.faces.resource=export&_LKISearch_WAR_LKISearchportlet_ln=xmlResources'

    def closed(self, reason):
        pass

    def parse(self, response):
        for i in range(self.resource_range[0], self.resource_range[1] + 1):
            formdata = {
                'remoteRecordId': str(i),
                'resourceId': str(self.resource_id)
            }

            yield FormRequest(self.url, formdata=formdata, callback=self.parse_details, meta={'record_id': str(i)})

    def parse_details(self, response):
        pass

class LkiSpiderZip(LkiSpider):
    def __init__(self):
        filename = "%d-%s.zip" % (self.resource_id, self.name)
        self.zip = ZipFile(filename, "w", ZIP_DEFLATED)

    def closed(self, reason):
        self.zip.close()

    def parse_details(self, response):
        filename = response.meta['record_id'] + '.xml'
        self.zip.writestr(filename, response.text)
    