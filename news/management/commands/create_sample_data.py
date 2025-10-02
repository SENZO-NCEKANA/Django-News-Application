"""
Management command to create sample data for testing.
"""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from news.models import Publisher, Category, Article, Newsletter

User = get_user_model()


class Command(BaseCommand):
    """
    Django management command to create sample data for testing and
    development.

    This command creates a comprehensive set of sample data including
    users, publishers, categories, articles, and newsletters for testing
    the news application functionality.

    :param help: Command description for Django CLI
    :type help: str, 'Create sample data for testing'
    """
    help = 'Create sample data for testing'

    def handle(self, *args, **options):
        """
        Execute the sample data creation process.

        Creates sample publishers, categories, users (journalists, editors,
        readers), articles, and newsletters with realistic data for testing
        purposes.

        :param args: Positional arguments (unused)
        :type args: tuple
        :param options: Command options (unused)
        :type options: dict
        :return: None
        :rtype: None
        """
        # Create publishers
        publisher1, created = Publisher.objects.get_or_create(
            name='Tech News Daily',
            defaults={
                'description': 'Latest technology news and updates',
                'website': 'https://technewsdaily.com'
            }
        )
        if created:
            self.stdout.write(
                self.style.SUCCESS('Created publisher: Tech News Daily')
            )

        publisher2, created = Publisher.objects.get_or_create(
            name='World Affairs',
            defaults={
                'description': 'Global news and current events',
                'website': 'https://worldaffairs.com'
            }
        )
        if created:
            self.stdout.write(
                self.style.SUCCESS('Created publisher: World Affairs')
            )

        # Create categories
        tech_category, created = Category.objects.get_or_create(
            name='Technology',
            defaults={'description': 'Technology news and updates'}
        )
        if created:
            self.stdout.write(
                self.style.SUCCESS('Created category: Technology')
            )

        world_category, created = Category.objects.get_or_create(
            name='World News',
            defaults={'description': 'Global news and events'}
        )
        if created:
            self.stdout.write(
                self.style.SUCCESS('Created category: World News')
            )

        # Create users
        journalist1, created = User.objects.get_or_create(
            username='Aphiwe_tech',
            defaults={
                'email': 'aphiwe@example.com',
                'first_name': 'Aphiwe',
                'last_name': 'Mthembu',
                'role': 'journalist'
            }
        )
        if created:
            journalist1.set_password('testpass123')
            journalist1.save()
            self.stdout.write(
                self.style.SUCCESS('Created journalist: Aphiwe_tech')
            )

        journalist2, created = User.objects.get_or_create(
            username='Kwanele_world',
            defaults={
                'email': 'kwanele@example.com',
                'first_name': 'Kwanele',
                'last_name': 'Ndlovu',
                'role': 'journalist'
            }
        )
        if created:
            journalist2.set_password('testpass123')
            journalist2.save()
            self.stdout.write(
                self.style.SUCCESS('Created journalist: Kwanele_world')
            )

        editor1, created = User.objects.get_or_create(
            username='editor_tech',
            defaults={
                'email': 'editor@technews.com',
                'first_name': 'Mike',
                'last_name': 'Editor',
                'role': 'editor'
            }
        )
        if created:
            editor1.set_password('testpass123')
            editor1.save()
            self.stdout.write(
                self.style.SUCCESS('Created editor: editor_tech')
            )

        reader1, created = User.objects.get_or_create(
            username='reader1',
            defaults={
                'email': 'reader1@example.com',
                'first_name': 'Alice',
                'last_name': 'Reader',
                'role': 'reader'
            }
        )
        if created:
            reader1.set_password('testpass123')
            reader1.save()
            self.stdout.write(
                self.style.SUCCESS('Created reader: reader1')
            )

        # Add journalists to publishers
        publisher1.journalists.add(journalist1)
        publisher2.journalists.add(journalist2)
        publisher1.editors.add(editor1)

        # Create sample articles
        article1, created = Article.objects.get_or_create(
            title='New Solar Panel Technology Increases Efficiency by 40%',
            defaults={
                'content': (
                    'Researchers at the University of Technology have '
                    'developed a revolutionary solar panel design that '
                    'increases energy conversion efficiency by 40% compared '
                    'to traditional panels. The new technology uses a '
                    'multi-layered approach with advanced materials that '
                    'capture sunlight across a broader spectrum. This '
                    'breakthrough could significantly reduce the cost of '
                    'solar energy and accelerate the transition to '
                    'renewable power sources. The panels are expected to '
                    'be commercially available within the next two years, '
                    'with pilot installations planned in several countries.'
                ),
                'summary': (
                    'Revolutionary solar panel technology increases '
                    'efficiency by 40%, potentially transforming renewable '
                    'energy economics.'
                ),
                'author': journalist1,
                'publisher': publisher1,
                'category': tech_category,
                'status': 'published',
                'is_approved': True
            }
        )
        if created:
            self.stdout.write(
                self.style.SUCCESS(
                    'Created article: New Solar Panel Technology...'
                )
            )

        article2, created = Article.objects.get_or_create(
            title='Global Climate Summit Reaches Historic Agreement',
            defaults={
                'content': 'World leaders have reached a historic agreement '
                           'on climate change at the latest global summit. '
                           'The agreement includes ambitious targets for '
                           'reducing carbon emissions and transitioning to '
                           'renewable energy sources.',
                'summary': 'Historic climate agreement reached with ambitious '
                           'emission reduction targets.',
                'author': journalist2,
                'publisher': publisher2,
                'category': world_category,
                'status': 'published',
                'is_approved': True
            }
        )
        if created:
            self.stdout.write(
                self.style.SUCCESS('Created article: Global Climate Summit...')
            )

        # Create sample newsletter
        newsletter1, created = Newsletter.objects.get_or_create(
            title='Weekly Tech Roundup',
            defaults={
                'content': (
                    'This week in technology: renewable energy breakthroughs, '
                    'new smartphone releases, and cybersecurity updates.'
                ),
                'author': journalist1,
                'publisher': publisher1
            }
        )
        if created:
            self.stdout.write(
                self.style.SUCCESS('Created newsletter: Weekly Tech Roundup')
            )

        self.stdout.write(
            self.style.SUCCESS('Sample data creation completed successfully!')
        )
