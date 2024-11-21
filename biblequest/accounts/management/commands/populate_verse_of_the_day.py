# accounts/management/commands/populate_verse_of_the_day.py

from django.core.management.base import BaseCommand
from accounts.models import VerseOfTheDay

class Command(BaseCommand):
    help = 'Populate the database with verses of the day from a file'

    def handle(self, *args, **kwargs):
        # Update the file path to the new location
        file_path = r'C:\Users\HP\OneDrive\Desktop\bibleverse.txt'
        
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        
        for i in range(0, len(lines), 2):  # Assuming each verse entry is 2 lines: reference and text
            if i + 1 < len(lines):  # Ensure there is a next line for the text
                reference = lines[i].strip()
                text = lines[i + 1].strip()
                VerseOfTheDay.objects.create(reference=reference, text=text)

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with verses of the day'))