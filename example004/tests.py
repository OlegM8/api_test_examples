import unittest
from unittest.mock import MagicMock
from unittest.mock import patch
from unittest.mock import mock_open

from product_example import MySuperProgram


def mock_get_request_ip(*args, **kwargs):
    data = {'ip': '1.1.1.1', 'country': 'Russia'}
    result = MagicMock()
    result.json.return_value = data
    result.status_code = 300
    return result


class MyTests(unittest.TestCase):

    @patch('product_example.open', mock_open(read_data='test1\ntest3\ntest2\n'))
    def test_read_one_line_with_mock(self):
        """ Check read_string_from_file() function. """

        prog = MySuperProgram()
        str = prog.read_string_from_file()

        msg = 'Expected: "{0}" Actual: "{1}"'.format('test1\n', str)
        assert str == 'test1\n', msg

    @patch('product_example.open', mock_open(read_data='test1\ntest3\ntest2\n'))
    def test_read_all_lines_with_mock(self):
        """ Check read_and_sort_all_strings() function. """

        prog = MySuperProgram()
        all_strings = prog.read_and_sort_all_strings()

        print(all_strings)
        assert all_strings == ['test1\n', 'test2\n', 'test3\n']

    @patch('product_example.open', mock_open(read_data='test1 Test2 tEST3'))
    def test_title_all_words_with_mock(self):
        """ Check title_all_words_in_line() function. """

        prog = MySuperProgram()
        all_strings = prog.title_all_words_in_line()

        print(all_strings)
        assert all_strings == 'Test1 Test2 Test3'

    @patch('requests.get', side_effect=mock_get_request_ip)
    def test_get_current_ip(self, mock_get):
        prog = MySuperProgram()
        ip = prog.get_current_ip()

        assert ip == '1.1.1.1'

        expected_url = 'https://api.ipify.org/?format=json'
        mock_get.assert_called_once_with(expected_url)

    @patch('requests.get', side_effect=mock_get_request_ip)
    def test_get_current_country(self, mock_get):
        prog = MySuperProgram()
        country = prog.get_current_country()

        print(dir(mock_get))
        assert country == 'Russia'

        expected_url = 'https://api.ipify.org/?format=json'
        mock_get.assert_called_once_with(expected_url)


    @patch('requests.get', side_effect=mock_get_request_ip)
    def test_get_status_code(self, mock_get):
        prog = MySuperProgram()
        status = prog.get_current_status_code()
        print('status code is '+ str(status.status_code))

        assert status.status_code == 300

    @patch('requests.get')
    def test_get_status_code_v2(self, mock_get):
        mock_get.return_value.status_code = 200
        prog = MySuperProgram()
        status = prog.get_current_status_code()
        print('status code is ' + str(status.status_code))

        self.assertEqual(status.status_code, 200)



if __name__ == '__main__':
    unittest.main()