# the tests below do not work anymore after last changes ie: adding django channels and communication via websockets
# - take a look ie: at checker.html template and note that:
#  - form submission is now realised via ajax call <form action="" action is now 'empty'
#  - there is no full page reload as previously (and no redirect to site_checker/check/ url)

# I decided not to remove these tests for future reference/knowledge refresh etc.

'''
from django.test import TestCase
from django.urls import reverse

SITE_CHECKER_VIEW_NAME = 'site_checker:check'


class SimpleCheckMethodTest(TestCase):

    def test_is_user_properly_informed_get_request_not_supported(self):
        response = self.client.get(reverse(SITE_CHECKER_VIEW_NAME))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['message'], 'This kind of request ie: GET currently not supported')

    def test_is_user_properly_informed_head_request_not_supported(self):
        response = self.client.head(reverse(SITE_CHECKER_VIEW_NAME))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['message'], 'This kind of request ie: HEAD currently not supported')
'''