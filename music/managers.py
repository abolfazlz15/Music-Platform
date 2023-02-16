from django.db import models


class MusicManager(models.Manager):
    def published(self):
        return self.filter(status=True)