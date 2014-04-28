from django.db import models
from django.conf import settings
from constants import COMMON_PERMISSIONS


class UserPermission(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    permissions_json = models.TextField(default='[]')  # a JSON encoded list of permissions

    def _get_permissions(self):
        return json.loads(self.permissions_json)

    def _set_permissions(self, permissions):
        assert type(permissions) == list
        self.permissions_json = json.dumps(permissions)

    permissions = property(_get_permissions, _set_permissions)

    class Meta:
        app_label = 'tgs'


class App(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL)
    name = models.TextField()
    description = models.TextField()
    app_key = models.CharField(max_length=32)
    app_secret = models.CharField(max_length=32)

    default_permissions_json = models.TextField(default='[]')

    def _get_default_permissions(self):
        return json.loads(self.default_permissions_json)

    def _set_default_permissions(self, permissions):
        assert type(permissions) == list
        self.default_permissions_json = json.dumps(permissions)
    default_permissions = property(_get_default_permissions, _set_default_permissions)

    extended_permissions_json = models.TextField(default='[]')

    def _get_extended_permissions(self):
        return json.loads(self.extended_permissions_json)

    def _set_extended_permissions(self, permissions):
        assert type(permissions) == list
        self.extended_permissions_json = json.dumps(permissions)
    extended_permissions = property(_get_extended_permissions, _set_extended_permissions)

    redirect_url = models.TextField()

    def __unicode__(self):
        return "{0} ({1})".format(self.app_key, self.owner)

    class Meta:
        app_label = 'tgs'


class AccessToken(models.Model):
    access_token = models.CharField(max_length=32, unique=True)
    expires = models.DateTimeField()
    permissions_json = models.TextField(default='[]')  # a JSON encoded list of permissions

    def _get_permissions(self):
        return json.loads(self.permissions_json)

    def _set_permissions(self, permissions):
        assert type(permissions) == list
        self.permissions_json = json.dumps(permissions)

    permissions = property(_get_permissions, _set_permissions)

    def __unicode__(self):
        return "{0}".format(self.access_token)

    @staticmethod
    def random(permissions):
        import string, random, datetime
        access_token = AccessToken(access_token=''.join(random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for _ in range(l)), expires=datetime.datetime.now() + datetime.timedelta(hours=1))
        access_token.permissions = permissions
        return access_token

    class Meta:
        app_label = 'tgs'
