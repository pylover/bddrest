import pytest

from bddrest.specification import HTTPStatus


def test_status_comparison():
    s = HTTPStatus('200 OK')
    assert s == '200 ok'
    assert s == 200
    assert s != 201
    assert s != '200 OKOK'
    assert s >= 100
    assert s > 100
    assert s <= 300
    assert s < 300
    assert s >= 200
    assert s <= 200

    with pytest.raises(ValueError):
        s >= '100 Continue'

    with pytest.raises(ValueError):
        s < '300 Multiple Choice'

    with pytest.raises(ValueError):
        s <= '300 Multiple Choice'

    with pytest.raises(ValueError):
        s > '100 Continue'
