from django.contrib import admin
from .models import Book, Author, Address

# Register your models here.

class BookAdmin(admin.ModelAdmin):
    # readonly_fields = ("slug",)
    # prepopulate the 'key' field base on the all the fields in the value tuple
    prepopulated_fields = {"slug": ("title",)}
    # seting filters can be seen in the admin form on the right hand side
    list_filter = ("rating", "author")
    # setting fields showed in the entries list
    list_display = ("title", "author",)

admin.site.register(Book, BookAdmin)
admin.site.register(Author)
admin.site.register(Address)
