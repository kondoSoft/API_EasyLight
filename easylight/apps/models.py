from django.db import models
from jsonfield import JSONField
from django.core.validators import MinValueValidator

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
    # rate = models.CharField(max_length=20, choices=CHOICES_RATE)
    # rate = models.ForeignKey(Rate__name_rate, null=True, blank=False)
    key_mun = models.IntegerField(null=False, blank=False)
    name_mun = models.CharField(max_length=120, blank=False, null=False)

    class Meta:
        # unique_together = ('state',)
        verbose_name = "Municipio"
        ordering = ('state',)

    def __str__(self):
        return str(self.name_mun)

class Receipt(models.Model):
    payday_limit = models.DateField(auto_now=False)
    amount_payable = models.IntegerField(null=False)
    current_reading = models.IntegerField(null=False)
    previous_reading = models.IntegerField(null=False)
    current_data = models.IntegerField(null=True, blank=True)

    class Meta:
        verbose_name = "Recibo"

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
    number_contract = models.IntegerField(blank=False)
    state = models.ForeignKey(State, null=False, blank=False)
    municipality = models.ForeignKey(Municipality, null=False)
    rate = models.CharField(max_length=30, choices=CHOICES_RATE, null=True )
    # rate = models.ForeignKey(Rate, null=False)
    period_summer = models.CharField(max_length=20, choices=CHOICES_PERIOD)
    type_payment = models.CharField(max_length=20, choices=CHOICES_PAYMENT)
    receipt = models.ForeignKey(Receipt, null=False, blank=True)

    class Meta:
        verbose_name = "Contrato"

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
    description = models.TextField(blank=False)
    image = models.ImageField()

    class Meta:
        verbose_name = "Tip"

    def _str_(self):
        return '%s %s %s' %(self.name_tip_advertising, self.type_data, self.description)
