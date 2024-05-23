from django.db import models
from django.core.validators import MinValueValidator

class User(models.Model):
    user_id = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=15)

    def __str__(self):
        return self.name

class Split(models.Model):
    SPLIT_TYPE_CHOICES = [
        ('EQUALLY', 'Equally'),
        ('EXACT', 'Exact'),
        ('PERCENTAGE', 'Percentage'),
    ]

    paid_by = models.ForeignKey(User, related_name='splits_paid', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    split_type = models.CharField(max_length=10, choices=SPLIT_TYPE_CHOICES)
    participants = models.ManyToManyField(User, related_name='splits', through='SplitParticipant')
    split_values = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f'{self.paid_by.name} paid {self.amount}'

class SplitParticipant(models.Model):
    split = models.ForeignKey(Split, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    share = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])

    def __str__(self):
        return f'{self.user.name} owes {self.share} for split {self.split.id}'
    
class Balance(models.Model):
    user = models.ForeignKey(User, related_name='balances', on_delete=models.CASCADE)
    owes_to = models.ForeignKey(User, related_name='owed_balances', on_delete=models.CASCADE)
    amount = models.FloatField(validators=[MinValueValidator(0)])

    def __str__(self):
        return f'{self.user.name} owes {self.amount} to {self.owes_to.name}'
