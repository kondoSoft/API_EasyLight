from django.db import models

class State(models.Model):
    key_state = models.IntegerField(null=False, blank=False)
    state = models.CharField(max_length=35, null=False, blank=False)
    abbreviation = models.CharField(max_length=10, blank=False)

    class Meta:
        ordering = ('key_state',)

class Municipality(models.Model):
    key_state = models.ForeignKey(State)
    key_mun = models.IntegerField(null=False, blank=False)
    name_mun = models.CharField(max_length=70, blank=False, null=False)

    class Meta:
        ordering = ('key_state__key_state',)

    def __str__(self):
        state = []
        for item in self.key_state.all():
            state.append(item)
            print(state)

        return str(state)
