from django.db import models

class State(models.Model):
    key_state = models.CharField(max_length=100, primary_key=True)
    state = models.CharField(max_length=35, null=False, blank=False)
    abbreviation = models.CharField(max_length=10, blank=False)

    class Meta:
        ordering = ('key_state',)

    def __str__(self):
        return str(self.state)

class Municipality(models.Model):
    key_state = models.ForeignKey(State, null=True, blank=True)
    key_mun = models.IntegerField(null=False, blank=False)
    name_mun = models.CharField(max_length=120, blank=False, null=False)

    class Meta:
        ordering = ('key_state__key_state',)

    def __str__(self):
        return str(self.name_mun)
