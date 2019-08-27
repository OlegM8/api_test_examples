from time import sleep
from .pages import ProskaterMainPage
import pytest
# python3 -m pytest -v -s --driver Chrome --driver-path ../driver/chromedriver -m run test_selenium.p

def test_search(web_browser):
    page = ProskaterMainPage(web_browser)

    search_page = page.search('кеды')
    sleep(5)
    assert len(search_page.search_results) == 40
    assert int(search_page.displayed_results_number.text) == 40
    assert int(search_page.all_results_number.text) >= 40


def test_search_no_results(web_browser):
    page = ProskaterMainPage(web_browser)
    search_page = page.search('несуществующий товар')
    assert search_page.no_results_found.text == 'НИЧЕГО НЕ НАШЛОСЬ\nПОПРОБУЙТЕ ИЗМЕНИТЬ ЗАПРОС:'
    assert search_page.no_results_found.is_displayed() == True



def test_open_men_section(web_browser):
    page = ProskaterMainPage(web_browser)
    filter_page = page.open_section('мужское')
    assert filter_page.section_title.text == 'МУЖСКАЯ КОЛЛЕКЦИЯ'



def test_add_to_chart(web_browser):
    page = ProskaterMainPage(web_browser)
    search_page = page.search('кеды')
    search_page.add_to_cart()
    assert search_page.cart_counter.text == '1'


def test_delete_from_chart(web_browser):
    page = ProskaterMainPage(web_browser)
    search_page = page.search('кеды')
    search_page.add_to_cart()
    cart_page = search_page.open_cart()
    cart_page.delete_from_chart()
    assert int(cart_page.total_price.text) == 0


@pytest.mark.run
def test_sort_by_price(web_browser):
    page = ProskaterMainPage(web_browser)
    search_page = page.search('кеды')
    search_page.sort_by_price_asc()
    price_list = search_page.find_all_prices()
    sorted_price_list = sorted(price_list)
    assert price_list[0] == sorted_price_list[0]
