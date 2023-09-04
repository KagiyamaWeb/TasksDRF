from django.contrib.auth.management.commands.createsuperuser import Command as BaseCommand
from User.models import Role


class Command(BaseCommand):
    help = 'Create a superuser and assign the "admin" Role'

    def handle(self, *args, **options):
        super().handle(*args, **options)

        username = options.get('username')
        user = self.UserModel._default_manager.get_by_natural_key(username)

        admin_role = Role.objects.get(pk=2)
        user.roles.add(admin_role)
        user.save()


