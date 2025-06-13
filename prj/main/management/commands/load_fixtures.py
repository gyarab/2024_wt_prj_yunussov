# prj/main/management/commands/load_fixtures.py
from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.db import transaction
import os

class Command(BaseCommand):
    help = 'Load all YAML fixture data in the correct order'

    @transaction.atomic
    def handle(self, *args, **kwargs):
        self.stdout.write('Running migrations first...')
        call_command('migrate')
        
        self.stdout.write('Loading YAML fixtures...')
        
        # Get the project root directory
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
        self.stdout.write(f'Project root: {project_root}')
        
        # Full paths to fixture files
        fixtures = [
            os.path.join(project_root, 'fixtures', 'teams.yaml'),
            os.path.join(project_root, 'fixtures', 'players.yaml'),
            os.path.join(project_root, 'fixtures', 'matches.yaml'),
            os.path.join(project_root, 'fixtures', 'matchstats.yaml')
        ]
        
        for fixture in fixtures:
            fixture_name = os.path.basename(fixture)
            self.stdout.write(f'Loading {fixture_name} from {fixture}...')
            try:
                if not os.path.exists(fixture):
                    raise FileNotFoundError(f'Fixture file not found: {fixture}')
                call_command('loaddata', fixture, verbosity=2)
                self.stdout.write(self.style.SUCCESS(f'Successfully loaded {fixture_name}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Failed to load {fixture_name}: {str(e)}'))
                raise  # Re-raise to abort the whole transaction

        self.stdout.write(self.style.SUCCESS('All YAML fixtures loaded successfully!'))
