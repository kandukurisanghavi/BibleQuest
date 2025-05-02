from django.test import TestCase
from django.urls import reverse
from accounts.models import QuizQuestion
import json


class QuizTests(TestCase):

    def setUp(self):
        # Setting up some dummy data for quiz questions
        self.easy_question = QuizQuestion.objects.create(
            question="What is the first book of the Bible?",
            option_a="Genesis",
            option_b="Exodus",
            option_c="Leviticus",
            option_d="Numbers",
            correct_answer="a",
            difficulty="easy"
        )
        self.medium_question = QuizQuestion.objects.create(
            question="Who led the Israelites into the Promised Land?",
            option_a="Moses",
            option_b="Joshua",
            option_c="David",
            option_d="Solomon",
            correct_answer="b",
            difficulty="medium"
        )

    def test_quiz_view_status_code(self):
        """Test that the quiz page for easy difficulty returns a 200 status code."""
        response = self.client.get(reverse('quiz', args=['easy']))
        self.assertEqual(response.status_code, 200)

    def test_quiz_template_used(self):
        """Test that the quiz view uses the correct template."""
        response = self.client.get(reverse('quiz', args=['easy']))
        self.assertTemplateUsed(response, 'accounts/quiz.html')

    def test_quiz_question_display(self):
        """Test that the quiz questions are displayed correctly."""
        response = self.client.get(reverse('quiz', args=['easy']))
        self.assertContains(response, self.easy_question.question)
        self.assertContains(response, self.easy_question.option_a)
        self.assertContains(response, self.easy_question.option_b)
        self.assertContains(response, self.easy_question.option_c)
        self.assertContains(response, self.easy_question.option_d)

    def test_quiz_email_send(self):
        """Test the quiz email sending functionality."""
        # Simulate a user taking the quiz and submitting their score
        response = self.client.post(
            reverse('send_quiz_email'),
            data=json.dumps({
                'email': 'test@example.com',
                'score': 8,
                'total_questions': 10
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), {'success': True})
