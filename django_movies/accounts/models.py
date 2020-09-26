from django.db import models
from model_utils import Choices


shoe_size = Choices(
    (0, 38, 38),
    (0, 39, 39),
    (0, 40, 40),
    (0, 41, 41),
    (0, 42, 42),
    (0, 43, 43),
    (0, 44, 44),
    (0, 45, 45),
)

class ShoeSize(models.Model):
    name = models.IntegerField(null=True, blank=True)
    shoe_size = models.IntegerField(choices=shoe_size, default=0)

    def __str__(self):
        return f"Shoe size: {self.name}"
