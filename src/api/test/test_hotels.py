from fastapi.testclient import TestClient
from http import HTTPStatus
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent.parent.parent))

from src.main import app # noqa
from api.routers.hotels import hotels # noqa
from src.api.test.fixtures import hotel_data_to_post # noqa

client = TestClient(app)


def hotel_url(hotel_id: int | None = None):
    if hotel_id is not None:
        return f'/hotels/?id={hotel_id}'
    return '/hotels'


def test_list_of_hotels():
    assert client.get(hotel_url()).status_code == HTTPStatus.OK
    assert client.get(hotel_url()).json() == hotels[0: 3]


def test_hotels_pagination():
    test_data = ((2, 3), (3, 3), (1, 4), (2, 4), (1, 5), (2, 5), (3, 5))
    for cur_test_data in test_data:
        end_point = cur_test_data[0] * cur_test_data[1]
        start_point = end_point - cur_test_data[1]
        response = client.get(
            f'{hotel_url()}/?page='
            f'{cur_test_data[0]}&per_page={cur_test_data[1]}')
        assert response.status_code == HTTPStatus.OK
        assert response.json() == hotels[start_point: end_point]


def test_get_hotel_by_id():
    assert client.get(hotel_url(1)).status_code == HTTPStatus.OK
    assert client.get(hotel_url(1)).json() == [hotels[0],]
    assert client.get(hotel_url(len(hotels) + 1)).status_code == (
        HTTPStatus.OK
    )
    assert client.get(hotel_url(len(hotels) + 1)).json() == list()


def test_delete_hotel_by_id():
    innitial_len = len(hotels)
    response = client.delete('hotels/1')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == 'Отель с id 1 успешно удален.'
    assert innitial_len - 1 == len(hotels)


def test_post_new_hotel():
    response = client.post(
        hotel_url(), json=hotel_data_to_post)
    assert response.status_code == HTTPStatus.OK
    assert len(hotels) == 8


def test_update_hotel():
    response = client.put(
        '/hotels/2/', json={'name': 'new_name_1', 'title': 'new_title_1'}
    )
    assert response.json()['name'] == 'new_name_1'
    assert response.json()['title'] == 'new_title_1'


def test_partial_update_hotel():
    response = client.patch(
        '/hotels/2/', json={'name': 'new_name_2'}
    )
    assert response.json()['name'] == 'new_name_2'
