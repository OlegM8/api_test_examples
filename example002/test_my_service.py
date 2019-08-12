import pytest
import requests
from requests.auth import HTTPBasicAuth

user = 'test_user'
password = 'test_password'
wrong_user = 'test_user1'
wrong_password = 'test_password1'

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


def test_check_wrong_login():
    url = 'http://0.0.0.0:7000/login'
    result = requests.get(url, auth=HTTPBasicAuth(wrong_user, wrong_password))

    print('Status code:', result.status_code)
    assert result.status_code == 401

def test_check_list_of_books(auth_cookie):
    url = 'http://0.0.0.0:7000/books'
    result = requests.get(url, cookies={'my_cookie': auth_cookie})

    print(result.text)
    assert result.status_code == 200


@pytest.mark.parametrize('title', ['', 'test', 'War and piece', '123', '!?.\'\"'])
@pytest.mark.parametrize('author', ['', 'Oleg', 'Tols Toy', '1230', '!?.\'\"'])
def test_add_book(auth_cookie, title, author):
    url = 'http://0.0.0.0:7000/add_book'
    result = requests.post(url, cookies={'my_cookie': auth_cookie},
                           data={'title': title, 'author': author})

    result2 = requests.get('http://0.0.0.0:7000/books', cookies={'my_cookie': auth_cookie})
    data = result2.json()

    assert data != []


def test_add_two_books(auth_cookie):
    url = 'http://0.0.0.0:7000/add_book'
    requests.post(url, cookies={'my_cookie': auth_cookie},
                           data={'title': 'first book', 'author': 'first author'})
    requests.post(url, cookies={'my_cookie': auth_cookie},
                  data={'title': 'second book', 'author': 'second author'})


    result2 = requests.get('http://0.0.0.0:7000/books', cookies={'my_cookie': auth_cookie})
    data = result2.json()

    assert len(data) >= 2


def test_delete_book(auth_cookie):
    url = 'http://0.0.0.0:7000/delete_books'
    result = requests.delete(url, cookies={'my_cookie': auth_cookie})

    result2 = requests.get('http://0.0.0.0:7000/books', cookies={'my_cookie': auth_cookie})
    assert result2.json() == []


def test_delete_book_by_id(auth_cookie):
    url = 'http://0.0.0.0:7000/add_book'
    result = requests.post(url, cookies={'my_cookie': auth_cookie},
                           data={'title': 'test title1', 'author': 'test author1'})
    data = result.json()
    book_id = data['id']

    url = 'http://0.0.0.0:7000/books/' + book_id
    requests.delete(url, cookies={'my_cookie': auth_cookie})

    url = 'http://0.0.0.0:7000/books'
    result = requests.get(url, cookies={'my_cookie': auth_cookie})
    data = result.json()
    book_ids = [i['id'] for i in data]
    assert book_id not in book_ids


def test_add_two_book_delete_one(auth_cookie):
    url = 'http://0.0.0.0:7000/add_book'
    result = requests.post(url, cookies={'my_cookie': auth_cookie},
                           data={'title': 'test title1', 'author': 'test author1'})
    data = result.json()
    book_id1 = data['id']

    result = requests.post(url, cookies={'my_cookie': auth_cookie},
                           data={'title': 'test title2', 'author': 'test author2'})
    data = result.json()
    book_id2 = data['id']

    url = 'http://0.0.0.0:7000/books/' + book_id1
    requests.delete(url, cookies={'my_cookie': auth_cookie})

    url = 'http://0.0.0.0:7000/books'
    result = requests.get(url, cookies={'my_cookie': auth_cookie})
    data = result.json()
    book_ids = [i['id'] for i in data]
    assert book_id1 not in book_ids
    assert book_id2 in book_ids