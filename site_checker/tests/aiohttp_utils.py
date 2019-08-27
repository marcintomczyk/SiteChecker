from aiohttp import ClientWebSocketResponse
from asynctest import mock
from yarl import URL
from aiohttp.client_reqrep import ClientResponse
from aiohttp.helpers import TimerNoop


def create_base_response(url):
    loop = mock.Mock()
    request_info = mock.Mock()
    writer = mock.Mock()
    session = mock.Mock()
    return ClientResponse(
        'head', URL(url), request_info=request_info,
        writer=writer,
        continue100=None,
        timer=TimerNoop(),
        traces=[],
        loop=loop,
        session=session)


def create_base_ws_response():
    loop = mock.Mock()
    reader = mock.Mock()
    writer = mock.Mock()
    protocol = mock.Mock()
    response = mock.Mock()
    timeout = mock.Mock()
    autoclose = mock.Mock()
    autoping = mock.Mock()
    return ClientWebSocketResponse(
        reader=reader,
        writer=writer,
        protocol=protocol,
        response=response,
        timeout=timeout,
        autoclose=autoclose,
        autoping=autoping,
        loop=loop)
