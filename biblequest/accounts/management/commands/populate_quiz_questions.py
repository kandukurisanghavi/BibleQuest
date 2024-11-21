# accounts/management/commands/populate_quiz_questions.py

from django.core.management.base import BaseCommand
from accounts.models import QuizQuestion

class Command(BaseCommand):
    help = 'Populate the database with quiz questions from a file'

    def handle(self, *args, **kwargs):
        file_path = r'C:\Users\HP\OneDrive\Desktop\quiz.txt'  
        
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        
        question_data = []
        question = None
        options = {}
        answer = None

        for line in lines:
            line = line.strip()
            if line.startswith('Answer:'):
                answer = line.split(': ')[1][0].lower()  # Get the first letter of the answer
                if question and options and answer:
                    question_data.append((question, options, answer))
                question = None
                options = {}
                answer = None
            elif line.startswith('A)') or line.startswith('B)') or line.startswith('C)') or line.startswith('D)'):
                option_key = line[0].lower()
                option_value = line[3:].strip()
                options[option_key] = option_value
            elif line and '. ' in line:  
                parts = line.split('. ', 1)
                if len(parts) > 1:
                    question = parts[1]  

        for q, opts, ans in question_data:
            QuizQuestion.objects.create(
                question=q,
                option_a=opts.get('a', ''),
                option_b=opts.get('b', ''),
                option_c=opts.get('c', ''),
                option_d=opts.get('d', ''),
                correct_answer=ans
            )

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with quiz questions'))