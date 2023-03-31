from django.db import models


class Person(models.Model):
    name = models.CharField(max_length=10, blank=True, null=True)


class QuantitativeAttribute(models.Model):
    value = models.PositiveIntegerField()
    name = models.CharField(max_length=10)
    person = models.ForeignKey(Person,  on_delete=models.CASCADE)
