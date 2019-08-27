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
    first_available_size = PageElement(xpath='((//div[@class="photo"])[1]//li[@class="size-type-cm active"]//ul[@class="size-list"]//li/label[not(contains(@class,"disabled"))])[1]')
    cart_counter = PageElement(xpath='//span[@class="count-contents"]')
    open_cart_button = PageElement(xpath='(//span[@class="bg"])[1]')
    all_sums = MultiPageElement(xpath='//div[@class="sum"]')
    sorting_dropdown = PageElement(xpath='//div[@class="sort-box"]//span[text()="Популярное"]')
    sort_by_price_asc_b = PageElement(xpath='//span[text()="По возрастанию цены"]')


    def __init__(self, web_driver, uri=''):
        super().__init__(web_driver, uri)
        self.popup_close.click()
        sleep(2)

    def add_to_cart(self):
        action = ActionChains(self.w)
        action.move_to_element(self.first_result).click(self.add_to_cart_button).perform()
        sleep(1)
        self.first_available_size.click()
        sleep(1)

    def open_cart(self):
        self.open_cart_button.click()
        return ChartPage(self.w)


    def find_all_prices(self):
        prices = self.w.find_elements_by_xpath('//div[@class="sum"]')
        price_list = []
        for i in range(len(prices)):
            price_list.append(prices[i].text)
        return price_list

    def sort_by_price_asc(self):
        action = ActionChains(self.w)
        action.move_to_element(self.sorting_dropdown).click(self.sort_by_price_asc_b).perform()
        sleep(2)


class FilterPage(PageObject):

    section_title = PageElement(xpath='//*[@class="inlineBlock"]')
    popup_close = PageElement(xpath='(//a[@class="btn-close1"])[10]')

    def __init__(self, web_driver, uri=''):
        super().__init__(web_driver, uri)
        self.popup_close.click()
        sleep(2)


class ChartPage(PageObject):

    del_from_cart_button = PageElement(xpath='//a[@class="del"]')
    total_price = PageElement(xpath='(//div[@class="total"]//span[@class="value"])[1]')

    def __init__(self, web_driver, uri=''):
        super().__init__(web_driver, uri)

    def delete_from_chart(self):
        self.del_from_cart_button.click()
        sleep(1)