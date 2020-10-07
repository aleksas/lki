import lki

class LastNameSpider(lki.LkiSpiderZip):
    name = 'last_names'
    resource_id = 1101
    resource_range = 13496770, 13676574