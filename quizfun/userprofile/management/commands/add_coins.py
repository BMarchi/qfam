from django.core.management import BaseCommand


class Command(BaseCommand):
    help = "Gives the user a fixed amount of coins if they have"
    "less than that amount"

    def handle(self, *args, **options):
        from userprofile.models import UserProfile
        from notification.models import Notification
        profile_list = UserProfile.objects.filter(coins__lte=9)
        for p in profile_list:
            self.stdout.write("Daily Reward!")
            p.coins = 10
            p.save()
            n = Notification(description='Daily Reward: '
                             'You have 10 coins now!', profile=p)
            n.save()
