from django.db import models
from django.db.models import OneToOneField, CASCADE
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from model_utils import Choices


SHOE_SIZE = Choices(
    (0, 36, 36),
    (1, 37, 37),
    (2, 38, 38),
    (3, 39, 39),
    (4, 40, 40),
    (5, 41, 41),
    (6, 42, 42),
    (7, 43, 43),
    (8, 44, 44),
    (9, 45, 45),
    (10, 46, 46),
    (11, 47, 47),
)

class Profile(models.Model):
    # shoe_size = models.IntegerField(
    #     null=False, validators=[MaxValueValidator(36), MinValueValidator(47)]
    # )
    shoe_size = models.IntegerField(choices=SHOE_SIZE, default=40)
    user = OneToOneField(User, on_delete=CASCADE)

    def __str__(self):
        return f"Shoe size: {self.shoe_size}"
