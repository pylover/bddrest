from bddrest.helpers import Status


def test_status_comparison():
    s = Status('200 OK')
    assert s == '200 ok'
    assert s == 200
    assert s != 201
    assert s != '200 OKOK'
    assert s >= 100
    assert not s >= '100 Continue'
    assert s > 100
    assert not s > '100 Continue'
    assert s <= 300
    assert not s <= '300 Multiple Choice'
    assert s < 300
    assert not s < '300 Multiple Choice'
    assert s >= 200
    assert s <= 200
