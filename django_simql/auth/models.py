from django.db.models


class User(models.Model, models.PermissionsMixin):
    username = models.CharField(max_length=255)
    name = models.TextField()
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.username

    def get_username(self):
        return self.username

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

    def __unicode__(self):
        return '{0} ({1})'.format(self.username, self.name)
