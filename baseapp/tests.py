from django.test import TestCase
from django.urls import reverse

# Create your tests here.


class QuestionIndexViewTests(TestCase):
    def test_landingpage(self):
        """
        If no landingpage exist, all fine.
        """
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)