import os
from django.core.management.base import BaseCommand
from accounts.models import QuizQuestion

class Command(BaseCommand):
    help = 'Populate the database with quiz questions from a file'

    def handle(self, *args, **kwargs):
        file_path = r'C:\Users\HP\OneDrive\Desktop\Bible Quiz from King James Version.txt'  # Update this path to your file location

        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f"File does not exist: {file_path}"))
            return

        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        question_data = []
        question = None
        options = {}
        answer = None
        difficulty = 'easy'  # Default difficulty

        for line in lines:
            line = line.strip()

            if line.startswith('Answer:'):
                answer = line.split(': ')[1][0].lower()  # Get the first letter of the answer
                self.stdout.write(self.style.SUCCESS(f"Parsed answer: {answer}"))  # Debugging statement
                # Ensure the question gets added only when all parts are present
                if question and options and answer:
                    question_data.append((question, options, answer, difficulty))
                    self.stdout.write(self.style.SUCCESS(f"Appended question: {question}"))  # Debugging statement
                question = None
                options = {}
                answer = None

            elif line.startswith('A)') or line.startswith('B)') or line.startswith('C)') or line.startswith('D)'):
                option_key = line[0].lower()
                option_value = line[3:].strip()
                options[option_key] = option_value
                self.stdout.write(self.style.SUCCESS(f"Parsed option {option_key}: {option_value}"))  # Debugging statement

            elif line.startswith('Difficulty:'):
                difficulty = line.split(': ')[1].strip().lower()  # Get the difficulty level
                self.stdout.write(self.style.SUCCESS(f"Parsed difficulty: {difficulty}"))  # Debugging statement
                # Ensure it's one of the valid difficulty levels
                if difficulty not in ['easy', 'medium', 'hard']:
                    self.stdout.write(self.style.WARNING(f"Invalid difficulty found: {difficulty}, defaulting to 'easy'"))
                    difficulty = 'easy'

            elif line and (line.endswith('?') or line.startswith('Who') or line.startswith('Which')):  # Adjusted check for question
                question = line.strip()
                self.stdout.write(self.style.SUCCESS(f"Parsed question: {question}"))  # Debugging statement

            # Catch the case where the question section ends without processing the final one
            elif not line and question and options and answer:
                question_data.append((question, options, answer, difficulty))
                self.stdout.write(self.style.SUCCESS(f"Appended final question: {question}"))  # Debugging statement
                question = None
                options = {}
                answer = None

        # Debugging: Output the extracted data
        self.stdout.write(self.style.SUCCESS(f"Extracted {len(question_data)} questions"))

        # Insert data into the database
        for q, opts, ans, diff in question_data:
            QuizQuestion.objects.create(
                question=q,
                option_a=opts.get('a', ''),
                option_b=opts.get('b', ''),
                option_c=opts.get('c', ''),
                option_d=opts.get('d', ''),
                correct_answer=ans,
                difficulty=diff
            )

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with quiz questions'))
