from time import sleep
from pages import ProskaterMainPage
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
    sleep(2)

@pytest.mark.run
def test_add_to_chart(web_browser):
    page = ProskaterMainPage(web_browser)
    search_page = page.search('кеды')
    search_page.add_to_cart()
    sleep(5)

def delete_from_chart(web_browser):
    pass


def sort_by_price(web_browser):
    pass