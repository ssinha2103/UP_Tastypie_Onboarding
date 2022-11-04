from django.apps import AppConfig


class PointOfSaleConfig(AppConfig):
    """This is the app configuration here."""
    name = 'point_of_sale'

    def ready(self):
        """This method generated API keys after each user is generated."""
        from django.db.models import signals
        from django.contrib.auth.models import User
        from tastypie.models import create_api_key
        # This line dispatches signal to Tastypie to create APIKey
        signals.post_save.connect(create_api_key, sender=User)
