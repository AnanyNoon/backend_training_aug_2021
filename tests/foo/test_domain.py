from datetime import datetime

from libfoo import Context, domain, messages

def test_keyval():
    with Context.service():
        # set by fixture
        val = domain.keyval.get_kv(messages.GetKeyRequest(ns='namespace', key='key'))
        assert val == 'val'

        val = domain.keyval.get_kv(messages.GetKeyRequest(ns='namespace', key='key2'))
        assert val is None

    with Context.service():
        domain.keyval.set_kv(messages.SetKeyValRequest(ns='a', key='x', val='x'))

    with Context.service():
        val = domain.keyval.get_kv(messages.GetKeyRequest(ns='a', key='x'))
        assert val == 'x'

