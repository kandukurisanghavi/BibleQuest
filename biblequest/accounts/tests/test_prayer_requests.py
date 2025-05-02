from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from accounts.models import PrayerRequest

class PrayerRequestTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.prayer_url = reverse('prayer_request')

    def test_login_required_for_prayer_request_view(self):
        response = self.client.get(self.prayer_url)
        self.assertRedirects(response, f'/accounts/login/?next={self.prayer_url}')

    def test_prayer_request_submission(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(self.prayer_url, {
            'prayer_request': 'Please pray for my job interview.',
            'category': 'career'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Your prayer request has been submitted.')
        self.assertTrue(PrayerRequest.objects.filter(user=self.user, text__icontains='job interview').exists())

    def test_prayer_request_invalid_submission(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(self.prayer_url, {
            'prayer_request': '',  # Empty request
            'category': 'health'
        })
        self.assertNotContains(response, 'Your prayer request has been submitted.')
        self.assertEqual(PrayerRequest.objects.count(), 0)

    def test_prayer_request_page_content(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(self.prayer_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Submit Your Prayer Request')
        self.assertContains(response, 'Category:')
        self.assertContains(response, 'Your Prayer Request:')
