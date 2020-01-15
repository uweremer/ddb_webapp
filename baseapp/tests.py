from django.test import TestCase
from django.urls import reverse

# Create your tests here.


class ViewTests(TestCase):
    """
    Tests that every view is mapped to an URL
    """
    def test_home(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
    def test_contact(self):
        response = self.client.get(reverse('contact'))
        self.assertEqual(response.status_code, 200)
    def test_datenschutz(self):
        response = self.client.get(reverse('datenschutz'))
        self.assertEqual(response.status_code, 200)        