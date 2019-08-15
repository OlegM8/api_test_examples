from time import sleep
from pages import ProskaterMainPage

def test_google(web_browser):
    page = ProskaterMainPage(web_browser)

    page.search_text = 'super kicks'
    sleep(10)