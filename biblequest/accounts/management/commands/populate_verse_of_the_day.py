# accounts/management/commands/populate_verses.py

from django.core.management.base import BaseCommand
from accounts.models import VerseOfTheDay

class Command(BaseCommand):
    help = 'Populate the database with verses of the day from a file'

    def handle(self, *args, **kwargs):
        file_path = r'C:\Users\HP\OneDrive\Desktop\Verses.txt' 
        
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        
        for i in range(0, len(lines), 2):
            reference = lines[i].strip()
            text = lines[i + 1].strip()
            VerseOfTheDay.objects.create(reference=reference, text=text)

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with verses of the day'))