import lki

class HistLocNameSpider(lki.LkiSpiderZip):
    name = 'location_names'
    resource_id = 1001
    resource_range = 9975550, 9984942