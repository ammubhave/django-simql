from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission


class SimqlAuthBackend(object):

    def authenticate(self, username=None):
        # Just returns the user with the given username.
        if not username:
            return

        user = None

        UserModel = get_user_model()

        try:
            user = UserModel.objects.get_by_natural_key(username)
        except UserModel.DoesNotExist:
            pass
        return user

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel._default_manager.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
