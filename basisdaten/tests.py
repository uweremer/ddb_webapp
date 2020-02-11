from django.test import TestCase
from django.urls import reverse

class BasisdatenViewTests(TestCase):
    """
    Tests that every view is mapped to an URL
    """
    def test_basisdaten(self):
        response = self.client.get(reverse('basisdaten'))
        self.assertEqual(response.status_code, 200)