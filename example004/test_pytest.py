from unittest.mock import MagicMock
from unittest.mock import patch


from .product_example import MySuperProgram


def mock_get_request_ip(*args, **kwargs):
    result = MagicMock()
    result.json = MagicMock(return_value={'ip': '1.1.1.1', 'country': 'Russia'})

    return result


@patch('requests.get', side_effect=mock_get_request_ip)
def test_get_current_ip(mock_get):
    prog = MySuperProgram()
    ip = prog.get_current_ip()

    assert ip == '1.1.1.1'

    expected_url = 'https://api.ipify.org/?format=json'
    mock_get.assert_called_once_with(expected_url)


def test_real_ip():
    prog = MySuperProgram()
    ip = prog.get_current_ip()
    print(ip)