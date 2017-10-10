from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.core.validators import MinValueValidator
from django.conf import settings
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

class Profile(models.Model):
    user = models.OneToOneField(User, primary_key = True, on_delete=models.CASCADE)
    phone = models.CharField(max_length=13, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    zip_code = models.IntegerField(null=True, blank=True)
    avatar = models.ImageField(upload_to='media/', null=True, blank=True)
    premium = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user.username)

    class Meta:
        # unique_together = ('state',)
        verbose_name = "Perfile"


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

class Rate(models.Model):
    VERANO = 'Verano'
    NOVERANO = 'NoVerano'
    CONSUMOBASICO = 'Consumo Basico'
    CONSUMOINTERMEDIO = 'Consumo Intermedio'
    CONSUMOINTERMEDIOALTO = 'Consumo Intermedio Alto'
    CONSUMOEXCEDENTE = 'Consumo Excedente'
    TARIFA1 = 'TARIFA 1'
    TARIFA1A = 'TARIFA 1A'
    TARIFA1B = 'TARIFA 1B'
    TARIFA1C = 'TARIFA 1C'
    TARIFA1D = 'TARIFA 1D'
    TARIFA1E = 'TARIFA 1E'
    TARIFA1F = 'TARIFA 1F'

    CHOICES_RATE = (
        (TARIFA1, 'TARIFA 1'),
        (TARIFA1A, 'TARIFA 1A'),
        (TARIFA1B, 'TARIFA 1B'),
        (TARIFA1C, 'TARIFA 1C'),
        (TARIFA1D, 'TARIFA 1D'),
        (TARIFA1E, 'TARIFA 1E'),
        (TARIFA1F, 'TARIFA 1F'),
    )

    CHOICES_SUMMER = (
        (VERANO, 'Verano'),
        (NOVERANO, 'Fuera de Verano'),
    )
    CHOICES_CONSUMPTION = (
        (CONSUMOBASICO, 'Consumo Básico'),
        (CONSUMOINTERMEDIO, 'Consumo Intermedio'),
        (CONSUMOINTERMEDIOALTO, 'Consumo Intermedio Alto'),
        (CONSUMOEXCEDENTE, 'Consumo Excedente'),
    )

    name_rate = models.CharField(max_length=15, choices=CHOICES_RATE)
    period_name = models.CharField(max_length=20, choices=CHOICES_SUMMER)
    consumption_name = models.CharField(max_length=30, choices=CHOICES_CONSUMPTION)
    kilowatt = models.PositiveSmallIntegerField(null=True, blank=False)
    cost = models.DecimalField(null=True, blank=False, validators=[MinValueValidator(0.001)], max_digits=5, decimal_places=3)

    class Meta:
        verbose_name = "Tarifa"
        ordering = ('id',)

    def __str__(self):
        return "%s %s %s %s %s" %(self.name_rate, self.period_name, self.consumption_name, self.kilowatt, self.cost)

class State(models.Model):
    state = models.CharField(max_length=35, null=False, blank=False)
    abbreviation = models.CharField(max_length=10, blank=False)

    class Meta:
        verbose_name = "Estado"
        ordering = ('id',)

    def __str__(self):
        return str(self.state)

class Municipality(models.Model):
    TARIFA1 = 'TARIFA 1'
    TARIFA1A = 'TARIFA 1A'
    TARIFA1B = 'TARIFA 1B'
    TARIFA1C = 'TARIFA 1C'
    TARIFA1D = 'TARIFA 1D'
    TARIFA1E = 'TARIFA 1E'
    TARIFA1F = 'TARIFA 1F'

    CHOICES_RATE = (
        (TARIFA1, 'TARIFA 1'),
        (TARIFA1A, 'TARIFA 1A'),
        (TARIFA1B, 'TARIFA 1B'),
        (TARIFA1C, 'TARIFA 1C'),
        (TARIFA1D, 'TARIFA 1D'),
        (TARIFA1E, 'TARIFA 1E'),
        (TARIFA1F, 'TARIFA 1F'),
    )

    state = models.ForeignKey(State, related_name='states', null=False, blank=False)
    key_mun = models.IntegerField(null=False, blank=False)
    name_mun = models.CharField(max_length=120, blank=False, null=False)
    rate = models.CharField(max_length=30, choices=CHOICES_RATE, null=True )

    class Meta:
        # unique_together = ('state',)
        verbose_name = "Municipio"
        ordering = ('name_mun',)

    def __str__(self):
        return '%s %s' % (self.id, self.name_mun)

class Receipt(models.Model):
    payday_limit = models.DateField(auto_now=False)
    amount_payable = models.IntegerField(null=False, default=0)
    current_reading = models.IntegerField(null=False, default=0)
    current_reading_updated = models.IntegerField(null=False, default=0)
    previous_reading = models.IntegerField(null=False)
    update_date = models.DateField(blank=True, null=True, auto_now=True)
    contract = models.ForeignKey('Contract', related_name='contract', on_delete=models.CASCADE)
    period = models.CharField(blank=True, null=True, max_length=10)
    status = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Recibo"
        ordering = ('id',)

    def __str__(self):
        return str(self.payday_limit)

class Contract(models.Model):

    PERIODO1 = 'Verano'
    PERIODO2 = 'Verano'
    PERIODO3 = 'Verano'
    PERIODO4 = 'Verano'
    MENSUAL = 'Mensual'
    BIMESTRAL = 'Bimestral'
    TARIFA1 = 'TARIFA 1'
    TARIFA1A = 'TARIFA 1A'
    TARIFA1B = 'TARIFA 1B'
    TARIFA1C = 'TARIFA 1C'
    TARIFA1D = 'TARIFA 1D'
    TARIFA1E = 'TARIFA 1E'
    TARIFA1F = 'TARIFA 1F'

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
        (PERIODO1, 'Febrero - Julio'),
        (PERIODO2, 'Marzo - Agosto'),
        (PERIODO3, 'Abril - Septiembre'),
        (PERIODO4, 'Mayo - Octubre'),
    )

    name_contract = models.CharField(max_length=20, blank=False)
    number_contract = models.CharField(max_length=15, blank=False)
    state = models.ForeignKey(State, null=False, blank=False)
    municipality = models.ForeignKey(Municipality, null=False)
    rate = models.CharField(max_length=30, choices=CHOICES_RATE, null=True )
    initialDateRange = models.DateField(null=True, blank=True)
    finalDateRange = models.DateField(null=True, blank=True)
    # period_summer = models.CharField(max_length=20, choices=CHOICES_PERIOD, null=True, blank=True)
    type_payment = models.CharField(max_length=20, choices=CHOICES_PAYMENT)
    image = models.ImageField(upload_to='media/', blank=True, null=True)
    owner = models.ForeignKey('auth.User', related_name='contracts', on_delete=models.CASCADE)
    

    class Meta:
        verbose_name = "Contrato"
        ordering = ('id',)

    def __str__(self):
        return str(self.number_contract)

class Records(models.Model):

    date = models.DateField()
    day = models.CharField(max_length=10)
    daily_reading = models.IntegerField(null=False, default=0)
    hours_elapsed = models.CharField(max_length=10)
    hours_totals = models.CharField(max_length=10)
    days_elapsed = models.CharField(max_length=10)
    days_totals = models.CharField(max_length=10)
    daily_consumption = models.IntegerField(null=False, default=0)
    cumulative_consumption = models.CharField(max_length=10)
    actual_consumption = models.CharField(max_length=10)
    average_global = models.CharField(max_length=10)
    rest_day = models.CharField(max_length=10, blank=True, null=True)
    projection = models.CharField(max_length=25)
    contracts = models.ManyToManyField(Contract, blank=True)

    class Meta:
        verbose_name = "Record"

    def __str__(self):
        return '%s %s %s' %(self.date, self.day, self.projection)

class TipsAndAdvertising(models.Model):

    TIP = 'tip'
    ADV = 'adv'

    CHOICES_TIPS = (
        (TIP, 'Tip'),
        (ADV, 'Advertising'),
    )

    name_tip_advertising = models.CharField(max_length=20, blank=False)
    type_data = models.CharField(max_length=20, choices=CHOICES_TIPS)
    description = models.TextField(blank=False)
    image = models.ImageField(upload_to='media/', blank=True)

    class Meta:
        verbose_name = "Tip"

    def __str__(self):
        return '%s %s %s' %(self.name_tip_advertising, self.type_data, self.description)






