"""Create database models for implementation app"""

from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()

class Algorithm(models.Model):
    type = models.CharField(max_length=100,
                            verbose_name='Algorithm data field.')

    def __str__(self):
        return self.type


class QubitType(models.Model):
    type = models.CharField(max_length=100,
                            verbose_name='QubitType data field.')

    def __str__(self):
        return self.type


class QubitSubtype(models.Model):
    type = models.CharField(max_length=100,
                            verbose_name='QubitSubtype data field.')

    def __str__(self):
        return self.type


class QuantumComputer(models.Model):
    computer_type = models.CharField(max_length=200,
                                    verbose_name='Quantum Computing data field.')

    def __str__(self):
        return self.computer_type


class NISQImplementation(models.Model):
    """NISQ Data Model for indexed publication data."""

    timestamp = models.DateTimeField(auto_now_add=True)

    submitted_by = models.ForeignKey(User,
                                     on_delete=models.SET_DEFAULT,
                                     default="Anonymous",
                                     related_name='user')

    year = models.CharField(max_length=4,
                            editable=False,
                            blank=True,
                            null=True)

    year_int = models.PositiveIntegerField(verbose_name='Year',
                                           blank=True,
                                           null=True,
                                           default=None)

    month = models.CharField(max_length=10)

    algorithm = models.ManyToManyField(Algorithm,
                                       blank=True,
                                       related_name="algorithm")

    description = models.TextField()

    qubit_type = models.ManyToManyField(QubitType,
                                        blank=True,
                                        related_name='qubit_type')

    qubit_subtype = models.ManyToManyField(QubitSubtype,
                                           related_name='qubit_subtype',
                                           blank=True)

    computer = models.ManyToManyField(QuantumComputer,
                                      related_name='computer',
                                      blank=True)

    qubit_number = models.PositiveIntegerField(blank=True,
                                               null=True,
                                               default=None)

    reference_url = models.CharField(max_length=400,
                                     blank=True,
                                     null=True)

    approved = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.month} {self.year_int} | {self.description}'