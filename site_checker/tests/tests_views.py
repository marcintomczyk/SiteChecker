from django.test import RequestFactory, TestCase
from django.urls import reverse

SITE_CHECKER_VIEW_NAME = 'site_checker:check'


class SimpleCheckMethodTest(TestCase):

    # for more complex tests
    #def setUp(self):
    #    self.request_factory = RequestFactory()

    def test_is_user_properly_informed_get_request_not_supported(self):
        response = self.client.get(reverse(SITE_CHECKER_VIEW_NAME))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['message'], 'This kind of request ie: GET currently not supported')

    def test_is_user_properly_informed_head_request_not_supported(self):
        response = self.client.head(reverse(SITE_CHECKER_VIEW_NAME))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['message'], 'This kind of request ie: HEAD currently not supported')