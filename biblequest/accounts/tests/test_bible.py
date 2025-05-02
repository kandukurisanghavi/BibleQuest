from django.test import TestCase
from django.urls import reverse

class BibleTests(TestCase):
    def test_bible_view_status_code(self):
        response = self.client.get(reverse('bible_view'))
        self.assertEqual(response.status_code, 200)

    def test_bible_template_used(self):
        response = self.client.get(reverse('bible_view'))
        self.assertTemplateUsed(response, 'accounts/bible_view.html')

    def test_testament_selection_renders_books(self):
        response = self.client.get(reverse('bible_view'), {'testament': 'Old Testament'})
        self.assertContains(response, 'Select Book')

    def test_valid_book_and_chapter(self):
        response = self.client.get(reverse('bible_view'), {
            'testament': 'Old Testament',
            'book': 'Genesis',
            'chapter': '1'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Genesis Chapter 1')

    def test_invalid_chapter(self):
        response = self.client.get(reverse('bible_view'), {
            'testament': 'Old Testament',
            'book': 'Genesis',
            'chapter': '999'
        })
        self.assertContains(response, 'Invalid chapter number')

    def test_search_query_parsing(self):
        response = self.client.get(reverse('bible_view'), {
            'search': 'Genesis 1:1'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Genesis Chapter 1')
