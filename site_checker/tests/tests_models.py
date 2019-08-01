from django.test import TestCase
from datetime import datetime
from site_checker.models import Site


class SiteTest(TestCase):

    # TODO: when there are more tests move it to separate file (similar to what was done in tests_views)
    def create_site(self, original_address, final_address, status_code, check_date):
        return Site.objects.create(original_address=original_address,
                                   final_address=final_address,
                                   status_code=status_code,
                                   check_date=check_date)

    def test_site_creation(self):
        site = self.create_site('aaaa', 'bbbb', 200, datetime.timestamp(datetime.now()))
        self.assertTrue(isinstance(site, Site))
        self.assertEqual(site.original_address, 'aaaa')
