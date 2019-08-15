import pytest
import uuid

@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
    return rep


@pytest.fixture
def web_browser(request, selenium):

    browser = selenium

    yield browser

    if request.node.rep_call.failed:
        # Make screen-shot if test failed:
        try:
            browser.execute_script("document.body.bgColor = 'white' ; ")

            # Make screen-shot for local debug:
            browser.save_screenshot('../screenshots/' + str(uuid.uuid4()) + '.png')

            # For happy debugging:
            print('URL: ', browser.current_url)
            print('Browser logs:')
            for log in browser.get_log('browser'):
                print(log)

        except:
            pass # just ignore any errors here

