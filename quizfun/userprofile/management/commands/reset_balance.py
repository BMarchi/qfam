from django.core.management import BaseCommand


class Command(BaseCommand):
    help = "Reset the monthly balance"

    def handle(self, *args, **options):
        from userprofile.models import UserProfile

        profile_list = UserProfile.objects.all()
        for p in profile_list:
            self.stdout.write("Balance Reseted!")
            p.balance = 0
            p.save()