from typing import Iterable
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse
from django.utils.text import slugify

# Create your models here.

class Book(models.Model):
    title = models.CharField(max_length=50)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    author = models.CharField(null=True,  max_length=100)
    is_bestselling = models.BooleanField(default=False)
    slug = models.SlugField(default="", null=False, db_index=True) 

    # we want automatically get the slug whenever we call .save() (eg.Harry Potter 1 => Harry-Potter-1)
    # The we can override the .save()
    def save(self, *args, **kwargs) -> None:
        # build the slug wiht django.utils.slugify
        self.slug = slugify(self.title)
        # forward the parameters to the bult-in save method
        super().save(*args, **kwargs)


    def __str__(self) -> str:
        return f"{self.title} ({self.rating})"

    def get_absolute_url(self):
        # must match the name and the slug we set in the urls.py
        # url using id
        # return reverse("book_outlet:book_detail", args=[self.pk])
        # url using slug 
        return reverse("book_outlet:book_detail", args=[self.slug])