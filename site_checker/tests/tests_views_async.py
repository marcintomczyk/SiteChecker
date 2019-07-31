from asynctest import MagicMock, patch
from aiohttp import web, ClientConnectorError
from aiohttp.test_utils import AioHTTPTestCase, unittest_run_loop
from yarl import URL

from site_checker.tests.aiohttp_utils import create_base_response
from site_checker.views import check_site_status


FB_ORIGINAL_URL = URL('https://facebook.pl/')

# in case of fb_original_url we should get another one which is our real final site - this is the url after redirect
FB_FINAL_URL = URL('https://pl-pl.facebook.com/')

#url where there is no redirect
ONET_ORIGINAL_URL = URL('https://www.onet.pl')


# monkey patch MagicMock as MagicMock itself can't be used in await expression
# the real code awaits on session.head method so we need response not a magicMock
async def async_magic(mocked_response):
    return mocked_response


def create_correct_response_for_fb_with_url_after_redirect():
    mocked_response = create_base_response(FB_FINAL_URL)
    mocked_response.status = 200
    return mocked_response


def create_correct_response_for_onet_no_redirect():
    mocked_response = create_base_response(ONET_ORIGINAL_URL)
    mocked_response.status = 200
    return mocked_response


class TestAsyncSiteCheckerFunction(AioHTTPTestCase):

    async def get_application(self):
        return web.Application()

    @unittest_run_loop
    @patch('aiohttp.ClientSession.head')
    async def test_is_correct_response_returned_after_site_checking_with_correct_url_and_redirect(self, mock_head):

        # doesn't work - workaround using 'MagicMock.__await' is needed
        # mock_head.return_value.__aenter__.return_value.head = create_correct_response_for_fb_with_url_after_redirect()
        MagicMock.__await__ = lambda x: async_magic(create_correct_response_for_fb_with_url_after_redirect()).__await__()
        site_response = await check_site_status(FB_ORIGINAL_URL)

        self.assertIsNotNone(site_response)
        self.assertEqual(site_response.status, 200)
        self.assertEqual(site_response.url, FB_FINAL_URL)



    @unittest_run_loop
    @patch('aiohttp.ClientSession.head')
    async def test_is_correct_response_produced_after_site_checking_with_correct_url_and_no_redirect(self, mock_head):
        MagicMock.__await__ = lambda x: async_magic(create_correct_response_for_onet_no_redirect()).__await__()
        site_response = await check_site_status(ONET_ORIGINAL_URL)

        self.assertIsNotNone(site_response)
        self.assertEqual(site_response.status, 200)
        self.assertEqual(site_response.url, ONET_ORIGINAL_URL)


    @unittest_run_loop
    async def test_is_exception_produced_after_site_checking_with_incorrect_url_or_no_internet(self):

        site_response = await check_site_status('https://aaa.bbb.ccc')

        self.assertIsNotNone(site_response)
        self.assertIsInstance(site_response, ClientConnectorError)






