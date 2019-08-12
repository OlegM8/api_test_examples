import pytest

from .utils import *






def test_check_login():
    data = auth()
    assert data['my_cookie'] > '', 'empty auth cookie'


def test_check_wrong_login():
    data = auth('wrong user', 'wrong password')

    # Wrong credentials status code is 401
    assert data == 401, 'status code is not 401'


def test_check_list_of_books(auth_cookie):
    url = 'http://0.0.0.0:7000/books'
    result = requests.get(url, cookies={'my_cookie': auth_cookie})

    print(result.text)
    assert result.status_code == 200


@pytest.mark.parametrize('title', ['', 'test', 'War and piece', '123', '!?.\'\"'])
@pytest.mark.parametrize('author', ['', 'Oleg', 'Tols Toy', '1230', '!?.\'\"'])
def test_add_book(auth_cookie, title, author):
    """Add several books with different titles and authors"""
    url = 'http://0.0.0.0:7000/add_book'
    requests.post(url, cookies={'my_cookie': auth_cookie},
                           data={'title': title, 'author': author})

    # Get the list of all books
    result2 = requests.get('http://0.0.0.0:7000/books', cookies={'my_cookie': auth_cookie})
    data = result2.json()

    # Check that book list is not empty
    assert data != []


def test_add_two_books(auth_cookie):
    """Add two books"""
    url = 'http://0.0.0.0:7000/add_book'
    requests.post(url, cookies={'my_cookie': auth_cookie},
                           data={'title': 'first book', 'author': 'first author'})
    requests.post(url, cookies={'my_cookie': auth_cookie},
                  data={'title': 'second book', 'author': 'second author'})

    # Get the list of all books
    result2 = requests.get('http://0.0.0.0:7000/books', cookies={'my_cookie': auth_cookie})
    data = result2.json()

    # Check that at least two books in book list
    assert len(data) >= 2


def test_delete_book(auth_cookie):
    """Delete all books"""
    url = 'http://0.0.0.0:7000/delete_books'
    result = requests.delete(url, cookies={'my_cookie': auth_cookie})

    result2 = requests.get('http://0.0.0.0:7000/books', cookies={'my_cookie': auth_cookie})
    assert result2.json() == []


def test_delete_book_by_id(auth_cookie):
    # Add a book
    url = 'http://0.0.0.0:7000/add_book'
    result = requests.post(url, cookies={'my_cookie': auth_cookie},
                           data={'title': 'test title1', 'author': 'test author1'})
    data = result.json()
    # Save added book's id
    book_id = data['id']

    # Delete added book
    url = 'http://0.0.0.0:7000/books/' + book_id
    requests.delete(url, cookies={'my_cookie': auth_cookie})

    # Get book list and check that book was deleted
    url = 'http://0.0.0.0:7000/books'
    result = requests.get(url, cookies={'my_cookie': auth_cookie})
    data = result.json()
    book_ids = [i['id'] for i in data]
    assert book_id not in book_ids


def test_add_two_book_delete_one(auth_cookie):
    # Add two books and save their ids
    url = 'http://0.0.0.0:7000/add_book'
    result = requests.post(url, cookies={'my_cookie': auth_cookie},
                           data={'title': 'test title1', 'author': 'test author1'})
    data = result.json()
    book_id1 = data['id']

    result = requests.post(url, cookies={'my_cookie': auth_cookie},
                           data={'title': 'test title2', 'author': 'test author2'})
    data = result.json()
    book_id2 = data['id']

    # Delete the first book
    url = 'http://0.0.0.0:7000/books/' + book_id1
    requests.delete(url, cookies={'my_cookie': auth_cookie})

    # Get books list and check that only one book was deleted
    url = 'http://0.0.0.0:7000/books'
    result = requests.get(url, cookies={'my_cookie': auth_cookie})
    data = result.json()
    book_ids = [i['id'] for i in data]
    assert book_id1 not in book_ids
    assert book_id2 in book_ids