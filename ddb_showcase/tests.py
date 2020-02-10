from django.test import TestCase
from django.urls import reverse

# Create your tests here.


class ShowcaseViewTests(TestCase):
    """
    Tests that every view is mapped to an URL
    """
    def test_zusammenfassung(self):
        response = self.client.get(reverse('zusammenfassung'))
        self.assertEqual(response.status_code, 200) 