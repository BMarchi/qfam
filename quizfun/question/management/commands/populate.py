from django.core.management import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
        help = "My test command"
        from question.models import Difficulty
        Difficulty.objects.get_or_create(difficulty='Dificil', max_reward=100, min_reward=70,
                                         max_loss=30, min_loss=1)
        Difficulty.objects.get_or_create(difficulty='Medio', max_reward=70,
                                         min_reward=30, max_loss=70,
                                         min_loss=30) 
        Difficulty.objects.get_or_create(difficulty='Facil', max_reward=30,
                                         min_reward=1,
                                         max_loss=100, min_loss=70)
