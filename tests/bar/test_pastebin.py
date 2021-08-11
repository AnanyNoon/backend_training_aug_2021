from datetime import datetime
import pytest

from libbar import Context, domain

def test_domain():
    with Context.service():
        pastebin_code = domain.pastebin.UploadPastebin(txt="pastebin text").execute()
        assert pastebin_code

    with Context.service():
        val = domain.pastebin.get_pastebin(pastebin_code)
        assert val == {'txt': 'pastebin text', 'id_pastebin': 1}

        val = domain.pastebin.get_pastebin('fake')
        assert val is None


def test_views(client):
    response = client.post(
        '/pastebin/create',
        json={
            "txt": "pastebin text 2",
        },
    )
    pastebin_code = response.json()['pastebin_code']

    response = client.post(
        '/pastebin/get_views',
        json={
            "pastebin_code": pastebin_code,
        }
    )
    assert response.json()['views'] == 0

    response = client.post(
        '/pastebin/get',
        json={
            "pastebin_code": pastebin_code,
        }
    )
    assert response.json()['txt'] == "pastebin text 2"

    response = client.post(
        '/pastebin/get_views',
        json={
            "pastebin_code": pastebin_code,
        }
    )
    assert response.json()['views'] == 1


def test_illegal_content(client):
    response = client.post(
        '/pastebin/create',
        json={
            "txt": "illegal content",
        },
        assert_status=400
    )

    with pytest.raises(AssertionError, match='.*cant store illegal content.*'):
        response = client.post(
            '/pastebin/create',
            json={
                "txt": "illegal content",
            },
        )

