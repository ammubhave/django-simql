from django.db import models


class People(models.Model):
    username = models.TextField()
    firstname = models.TextField()
    lastname = models.TextField()
    email = models.TextField()

    def __unicode__(self):
        return "{0} - {1} {2}".format(
            self.username, self.firstname, self.lastname
        )

    class Meta:
        db_table = 'people'
        app_label = 'simmons_db'
