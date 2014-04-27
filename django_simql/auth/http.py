from django.http import HttpResponseRedirectBase
from django.conf import settings


class SimqlLoginResponseRedirect(HttpResponseRedirectBase):
    status_code = 302

    def __init__(self):
        super(HttpResponseRedirect, self).__init__(settings.SIMQL_LOGIN_URL)
