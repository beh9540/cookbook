from django.db import models

# Create your models here.
class Review(models.Model):
    recipe = models.ForeignKey('Recipe')
    rating = models.PositiveSmallIntegerField()
    review = models.TextField(blank=True, default='')