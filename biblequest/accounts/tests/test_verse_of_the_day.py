from django.test import TestCase
from django.urls import reverse
from accounts.models import VerseOfTheDay
from django.contrib.auth.models import User
import datetime

class VerseOfTheDayTests(TestCase):
    def setUp(self):
        # Create a test user to satisfy @login_required
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')

        # Create sample verses
        VerseOfTheDay.objects.create(
            text="For God so loved the world.",
            reference="John 3:16"
        )
        VerseOfTheDay.objects.create(
            text="The Lord is my shepherd.",
            reference="Psalm 23:1"
        )

    def test_verse_of_the_day_view_status_code(self):
        response = self.client.get(reverse('verse_of_the_day'))
        self.assertEqual(response.status_code, 200)

    def test_verse_of_the_day_content(self):
        today = datetime.date.today()
        formatted_date = today.strftime("%B %d, %Y").replace(" 0", " ")  # Windows-safe date formatting
        day_of_year = today.timetuple().tm_yday
        verses = list(VerseOfTheDay.objects.all())
        expected_verse = verses[day_of_year % len(verses)]

        response = self.client.get(reverse('verse_of_the_day'))
        self.assertContains(response, expected_verse.text)
        self.assertContains(response, expected_verse.reference)
        self.assertContains(response, f"Verse of the Day for {formatted_date}")
