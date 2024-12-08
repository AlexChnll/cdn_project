from django.core.management.commands.runserver import Command as RunserverCommand

class Command(RunserverCommand):
    def add_arguments(self, parser):
        super().add_arguments(parser)
        # Définir ici votre IP et votre port
        self.default_addr = '10.0.0.11'
        self.default_port = '8080'