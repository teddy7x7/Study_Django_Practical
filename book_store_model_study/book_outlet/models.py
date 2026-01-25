from typing import Iterable
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse
from django.utils.text import slugify

# Create your models here.
class Address(models.Model):
    street = models.CharField(max_length=80)
    postal_code = models.CharField(max_length=5)
    city = models.CharField(max_length=50)
    class Meta:
        verbose_name_plural = "Address Entries"
class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    address = models.OneToOneField(Address, on_delete=models.CASCADE, null=True)

    def generate_full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def __str__(self) -> str:
        return self.generate_full_name()


class Book(models.Model):
    title = models.CharField(max_length=50)
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)])

    # # old ver.
    # author = models.CharField(null=True,  max_length=100)
    # new ver., set a foreign key field to the Author table
    author = models.ForeignKey(
        Author, on_delete=models.CASCADE, null=True, related_name="books_set")

    is_bestselling = models.BooleanField(default=False)
    # slug = models.SlugField(default="", blank=True, editable=False, null=False, db_index=True)
    slug = models.SlugField(default="", blank=True, null=False, db_index=True)

    # we want automatically get the slug whenever we call .save() (eg.Harry Potter 1 => Harry-Potter-1)
    # The we can override the .save()
    # we use "prepopulated_fields = {"slug": ("title",)}" in the admin.py, so we can comment out this save function
    # def save(self, *args, **kwargs) -> None:
    #     # build the slug wiht django.utils.slugify
    #     self.slug = slugify(self.title)
    #     # forward the parameters to the bult-in save method
    #     super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.title} ({self.rating})"

    def get_absolute_url(self):
        # must match the name and the slug we set in the urls.py
        # url using id
        # return reverse("book_outlet:book_detail", args=[self.pk])
        # url using slug
        return reverse("book_outlet:book_detail", args=[self.slug])
