from page_objects import PageObject, PageElement, MultiPageElement
from time import sleep
from selenium.webdriver import ActionChains

class ProskaterMainPage(PageObject):

    search_text = PageElement(name='keywords')
    search_button = PageElement(xpath='(//button[@type="submit"])[1]')
    page_title = PageElement(xpath='(//a)[1]')

    def __init__(self, web_driver, uri=''):
        super().__init__(web_driver, uri)
        self.get('https://www.proskater.ru/')


    def search(self, text):
        self.search_text = text
        self.search_button.click()
        return SearchResultsPage(self.w)

    def open_section(self, text):
        search_button = self.w.find_element_by_xpath('//a[text()="' + text + '"]')
        search_button.click()
        return FilterPage(self.w)

class SearchResultsPage(PageObject):

    search_results = MultiPageElement(xpath='//div[@class="photo"]')
    popup_close = PageElement(xpath='(//a[@class="btn-close1"])[9]')
    displayed_results_number = PageElement(xpath='//*[@class="listing-progress-text__viewed-count"]')
    all_results_number = PageElement(xpath='//*[@class="listing-progress-text__all-count"]')
    no_results_found = PageElement(xpath='(//div[@class="no-products"])[2]')
    first_result = PageElement(xpath='(//div[@class="photo"])[1]')
    add_to_cart_button = PageElement(xpath='(//div[@class="add-cart"])[1]') # first result "Add to cart" button

    def __init__(self, web_driver, uri=''):
        super().__init__(web_driver, uri)
        self.popup_close.click()
        sleep(2)

    def add_to_cart(self):
        sleep(5)
        action = ActionChains(self.w)
        # action.move_to_element(self.first_result).pause(5).perform()
        #sleep(10)
        self.add_to_cart_button.click()

class FilterPage(PageObject):

    section_title = PageElement(xpath='//*[@class="inlineBlock"]')
    popup_close = PageElement(xpath='(//a[@class="btn-close1"])[10]')

    def __init__(self, web_driver, uri=''):
        super().__init__(web_driver, uri)
        self.popup_close.click()
        sleep(5)