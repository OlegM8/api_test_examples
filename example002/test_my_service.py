import pytest
import requests
from requests.auth import HTTPBasicAuth

user = 'test_user'
password = 'test_password'


@pytest.fixture
def auth_cookie():
    url = 'http://0.0.0.0:7000/login'
    result = requests.get(url, auth=HTTPBasicAuth(user, password))
    data = result.json()

    yield data['auth_cookie']

def test_check_login():
    url = 'http://0.0.0.0:7000/login'
    result = requests.get(url, auth=HTTPBasicAuth(user, password))
    data = result.json()

    print('Status code:', result.status_code)
    assert result.status_code == 200
    assert data['auth_cookie'] > ''


def test_check_list_of_books(auth_cookie):
    url = 'http://0.0.0.0:7000/books'
    result = requests.get(url, cookies={'my_cookie': auth_cookie})

    print(result.text)
    assert result.status_code == 200

@pytest.mark.parametrize('title', ['test', 'War and piece', '123', '!?.\'\"'])
@pytest.mark.parametrize('author', ['Oleg', 'Tols Toy', '1230', '!?.\'\"'])
def test_add_book(auth_cookie, title, author):
    url = 'http://0.0.0.0:7000/add_book'
    result = requests.post(url, cookies={'my_cookie': auth_cookie},
                           data={'title': title, 'author': author})

    result2 = requests.get('http://0.0.0.0:7000/books', cookies={'my_cookie': auth_cookie})
    data = result2.json()

    assert data != []


def test_delete_book(auth_cookie):
    url = 'http://0.0.0.0:7000/delete_books'
    result = requests.delete(url, cookies={'my_cookie': auth_cookie})

    result2 = requests.get('http://0.0.0.0:7000/books', cookies={'my_cookie': auth_cookie})
    assert result2.json() == []


def test_delete_book_by_id(auth_cookie):
    pass