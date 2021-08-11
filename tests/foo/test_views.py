
def test_health_check(client):
    response = client.get('/public/hc')
    assert response.status_code == 200
    assert response.json() == "OK"


def test_keyval(client):
    response = client.post(
        '/keyval/set',
        headers={'x-forwarded-user': 'test'},
        json={
            "ns": "x",
            "key": "x",
            "val": "x",
        }
    )
    assert response.status_code == 200

    response = client.post(
        '/keyval/get',
        headers={'x-forwarded-user': 'test'},
        json={
            "ns": "x",
            "key": "x",
        }
    )
    assert response.status_code == 200
    assert response.json() == {'val': 'x'}

