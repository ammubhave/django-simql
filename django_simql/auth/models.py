from django.db import models
import django.contrib.auth.models as auth_models
from django.utils import timezone


class UserManager(auth_models.BaseUserManager):
    def _create_user(self, username, is_staff, is_superuser, is_active):
        """
        Creates and saves a User with the given username.
        """
        if not username:
            raise ValueError('The given username must be set')

        user = self.model(username=username,
                          is_staff=is_staff, is_active=True, last_login=timezone.now(),
                          is_superuser=is_superuser)
        user.save(using=self._db)
        return user

    def create_user(self, username):
        return self._create_user(username, False, False, True)

    def create_superuser(self, username):
        return self._create_user(username, True, True, True)


class User(auth_models.PermissionsMixin):
    username = models.CharField(max_length=255, unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    last_login = models.DateTimeField('last login', default=timezone.now)

    REQUIRED_FIELDS = []

    def get_username(self):
        "Return the identifying username for this User"
        return getattr(self, self.USERNAME_FIELD)

    def __str__(self):
        return self.get_username()

    def natural_key(self):
        return (self.get_username(),)

    def is_anonymous(self):
        """
        Always returns False. This is a way of comparing User objects to
        anonymous users.
        """
        return False

    def is_authenticated(self):
        """
        Always return True. This is a way to tell if the user has been
        authenticated in templates.
        """
        return True

    def set_password(self, raw_password):
        pass

    def check_password(self, raw_password):
        return False

    def set_unusable_password(self):
        pass

    def has_usable_password(self):
        return False

    def get_session_auth_hash(self):
        """
        Returns an HMAC of the username field.
        """
        key_salt = "django.contrib.auth.models.AbstractBaseUser.get_session_auth_hash"
        return salted_hmac(key_salt, self.username).hexdigest()

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def __unicode__(self):
        return self.username

    class Meta:
        db_table = 'user'
        app_label = 'simmons_db'

