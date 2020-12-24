from django.db import models


class Person(models.Model):
    username = models.CharField(max_length=75)

    def __str__(self):
        return self.username


class Gem(models.Model):
    named = models.CharField(max_length=75)

    def __str__(self):
        return self.named


class Deal(models.Model):
    purchaser = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        related_name='deals',
    )
    item = models.ForeignKey(
        Gem,
        on_delete=models.CASCADE,
        related_name='deals'
    )
    total = models.PositiveIntegerField()
    quantity = models.PositiveSmallIntegerField()
    date = models.DateTimeField()

    class Meta:
        unique_together = (
            'purchaser',
            'total',
            'item',
            'date',
            'quantity'
        )

    def __str__(self):
        return self.purchaser.username
