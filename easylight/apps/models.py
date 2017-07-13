from django.db import models


class TableRate(models.Model):
    name = models.CharField(max_length=20, blank=False)
    precio = models.IntegerField(blank=False)

    def __str__(self):
        return str(self.name)

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
    rate = models.ForeignKey(TableRate, null=True, blank=False)
    key_mun = models.IntegerField(null=False, blank=False)
    name_mun = models.CharField(max_length=120, blank=False, null=False)

    class Meta:
        ordering = ('key_state__key_state',)

    def __str__(self):
        return str(self.name_mun)

class Receipt(models.Model):
    payday_limit = models.DateField(auto_now=False)
    amount_payable = models.IntegerField(null=False)
    current_reading = models.IntegerField(null=False)
    previous_reading = models.IntegerField(null=False)
    current_data = models.IntegerField(null=True)

    def __str__(self):
        return str(self.payday_limit)

class Contract(models.Model):

    TARIFA1 = 'tarifa1'
    TARIFA1A = 'tarifa1a'
    TARIFA1B = 'tarifa1b'
    TARIFA1C = 'tarifa1c'
    TARIFA1D = 'tarifa1d'
    TARIFA1E = 'tarifa1e'
    TARIFA1F = 'tarifa1f'
    PERIODO1 = 'ene_jun'
    PERIODO2 = 'jun_dic'
    MENSUAL = 'mensual'
    BIMESTRAL = 'bimestral'

    CHOICES_RATE = (
        (TARIFA1, 'TARIFA 1'),
        (TARIFA1A, 'TARIFA 1A'),
        (TARIFA1B, 'TARIFA 1B'),
        (TARIFA1C, 'TARIFA 1C'),
        (TARIFA1D, 'TARIFA 1D'),
        (TARIFA1E, 'TARIFA 1E'),
        (TARIFA1F, 'TARIFA 1F'),
    )
    CHOICES_PAYMENT = (
        (MENSUAL, 'Mensual'),
        (BIMESTRAL, 'Bimestral'),
    )
    CHOICES_PERIOD = (
        (PERIODO1, 'Enero - Junio'),
        (PERIODO2, 'Junio - Diciembre'),
    )

    name_contract = models.CharField(max_length=20, blank=False)
    number_contract = models.IntegerField(blank=False)
    state = models.ForeignKey(State, null=True)
    municipality = models.ForeignKey(Municipality, null=False)
    rate = models.CharField(max_length=10, choices=CHOICES_RATE )
    period_summer = models.CharField(max_length=20, choices=CHOICES_PERIOD)
    type_payment = models.CharField(max_length=20, choices=CHOICES_PAYMENT)
    receipt = models.ForeignKey(Receipt, null=False, blank=True)

    def __str__(self):
        return str(self.number_contract)

class TipsAndAdvertising(models.Model):

    TIP = 'tip'
    ADV = 'adv'

    CHOICES_TIPS = (
        (TIP, 'Tip'),
        (ADV, 'Advertising'),
    )

    name_tip_advertising = models.CharField(max_length=20, blank=False)
    type_data = models.CharField(max_length=20, choices=CHOICES_TIPS)

    def _str_(self):
        return str(self.name_tip_advertising)
