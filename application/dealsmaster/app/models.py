from django.db import models


class Person(models.Model):
    username = models.CharField(max_length=75)

    def __str__(self):
        return self.username


class Gems(models.Model):
    named = models.CharField(max_length=75)
    price = models.PositiveIntegerField()

    def __str__(self):
        return self.named


class Deals(models.Model):
    purchaser = models.ForeignKey(
        Person,
        on_delte=models.CASCADE,
        related_name='deals',
    )
    item = models.ForeignKey(
        Gems,
        on_delete=models.CASCADE,
        related_name='deals'
    )
    count = models.PositiveSmallIntegerField()
    date = models.DateTimeField()

    class Meta:
        unique_together = ('item', 'date', 'count')

    @property
    def total(self):
        return self.count * self.item.price

    def __str__(self):
        return self.purchaser
