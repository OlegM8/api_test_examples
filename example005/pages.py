from page_objects import PageObject, PageElement, MultiPageElement


class ProskaterMainPage(PageObject):

    search_text = PageElement(xpath='//*[@name="keywordss"]')

    def __init__(self, web_driver, uri=''):
        super().__init__(web_driver, uri)
        self.get('https://www.proskater.ru/')
