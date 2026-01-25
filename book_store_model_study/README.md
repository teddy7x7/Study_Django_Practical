1. Whenever we create a new table, update a table in the `models.py`. We need to `manage.py makemigrations` (or `uv run python manage.py makemigrations`) to create all the files and apps that migrations needed in the `migrations` folder. Then, run `manage.py migrate` (or `uv run python manage.py migrate`) to utilze the things created in the `migrations` folder.

2. Basic CRUD with Shell
* Create:  
    Run `python manage.py shell` would give us an interactive shell/python interpreter to work with this django project and also work with the database belongs to it. In this shell, we can try to insert some dummy data into the table defined in the `models.py` by creating instance of a model class and use the function `.save` or `object.create()` to save it into the database, such as:

    ```python
    ### first method
    from book_outlet.models import Book
    harry_potter = Book(title="Harry Potter 1", rating=5)
    harry_potter.save()

    ### second method
    Book.objects.create(title="Harry Potter 2", rating=5)
    ```
    Both creating(insert) a new entry and update the old entry, we use `.save()`

* Read:
    We use the class itself (the static field ~ `objects`) to fetch the table data, such as:

    ```python
    ### all()
    Book.objects.all() # return a list with all the table entries

    # Book.objects.all()[index].field

    ### Querying and filtering data
    # objects.get() only can get one entry at a call, if multiple entry matches, it would return an Erro
    # Usually use with unique value, such as id
    # Book.objects.get(field = some_val)
    Book.objects.get()


    # objects.filter() can return multiple result
    Book.objects.filter(rating=5)
    Book.objects.filter(rating__lt=3)   # < 3
    Book.objects.filter(rating__lte=3)  # <= 3
    Book.objects.filter(title__contains="My")  # normally with case sensitive check, but with SQLite here would not have case sensitive check

    Book.objects.filter(title__icontains="My") # ignore casing

    # and filtering
    Book.objects.filter(rating__lt=4, title__icontains="My") 
    
    # or filtering
    from django.db.models import Q # stands for query
    # '|' represents 'or'
    Book.objects.filter(Q(rating__gte=5) | Q(is_bestselling=True))
    # the',' represents 'and'
    Book.objects.filter(Q(rating__gte=5) | Q(is_bestselling=True), Q(author="J.K. Rowling"))

    # Dealing with fail to find the entry
    # #  implementation 1
    try:
        book = Book.objects.get(pk=id)
    except:
        raise django.http.Http404()

    #  implementation 2
    book = django.shortcuts.get_object_or_404(Book, id=id)

    ```

* Update:
    We can add field, add or override a funciton, such as the `__str__(self)`.  
    If we change the table's fields, we need to do the step 1 . For the old datas that don't have the new added fields, we can:
    ```python
    author = models.CharField(default="default val")
    # or 
    author = models.CharField(null=True)
    # or 
    author = models.CharField(blank=True)
    ```

* Delete:  
    First get the entry with `entry_instance = ClassName.objects.get()`, and then `entry_instance.delete()`

3. Retrive the url by `django.urls.reverse` in the overrided function `get_absolute_url` by ourselves in the `models.py` file, so we can use another way to get the url in the template without the url tag.  
**If we use the namespace technique and set the `app_name`, such as`app_name = "book_outlet"` in the `urls.py`, be aware of that no matter we are using the url tag or the reverse function, we have to use the `namespace:name` rather just `name`, such as the following**
```django
<!-- method 1 -->
<!-- Get the url by using django's url tag -->
<!-- <a href="{% url 'book_detail' id=book.id %}"> would get error that can't find the path-->
<a href="{% url 'book_outlet:book_detail' id=book.id %}">
```

```python
# method2
# by the django.urls.reverse
from django.urls import reverse

# a function that would be called implicitly by django, we can overwrite it
class Book(models.Model):
    def get_absolute_url(self):
        # must match the name and the slug we set in the urls.py
        # return reverse("book_detail", args=[self.pk]) # this would get an error that can't find the path
        return reverse("book_outlet:book_detail", args=[self.pk])
```

4. Convert `id` in the url into slug-like url by creating the slug field in the model class with `self.slug = models.slugField()` in the `models.py`. Override the `.save()`, and before calling and forwarding parameters to the overrided parent function, building the slug with `django.utils.text.slugify`.

5. Change the urls with id into slug by:
    * Modifing the get_absolute_url to reverse the url with slug, rather than id. Also, set the `db_index=True` to let the query more efficient.
        ```python
        class Book(models.Model):
            # setting db_index=True
            slug = models.SlugField(default="", null=False, db_index=True) 
            def get_absolute_url(self):
                return reverse("book_outlet:book_detail", args=[self.slug])
        ```
    * Modifing the dynamic fragement in the path function for the url in `urls.py`, from `<int:id>` to `<slug:slug>`
    * Modifing the view function's signature from receving id to slug in the `views.py`.

6. Aggregation and Ordering
    * In Django, the built-in aggregation functions can return summary statistics.
        ```python
        # aggregate functions
        from django.db.models import Avg, Max, Min

        def index(request):
            # add '-' to ger decending order
            books = Book.objects.all().order_by("-rating")    
            
            # aggregate functions
            num_books = books.count()
            avg_rating = books.aggregate(Avg("rating"))
        ```

7. `admin/`
    * username:123, email address: 123@123.com, password: 123
    * Register App to the `admin.py` in the same folder.
        ```python
        from django.contrib import admin
        from .models import Book
        
        admin.site.register(Book).
        ```
    
    * To make admin site field can left blank when creating a new entry, we can set the parameter `blank=True` in the ...Field() functions in the `models.py`, such as:
        ```python
        slug = models.SlugField(blank=True)
        ```
        Or set `editable=False`, leave all work for assigning value in the coding way. This will let the field cant't be seen in the admin control pannel.
    
    * A much better way to control the admin area, such as how the fields are being displayed in the admin form, we can set a class named `AppNameAdmin` in the `admin.py`, such as:
    ```python
    class BookAdmin(admin.ModelAdmin):
    # prepopulate the 'key' field base on the all the fields in the value tuple
    prepopulated_fields = {"slug": ("title",)}
    # seting filters can be seen in the admin form on the right hand side
    list_filter = ("rating", "author")
    # setting fields showed in the entries list
    list_display = ("title", "author",)

    admin.site.register(Book, BookAdmin)
    ```

8. Relationships
    * One to one, one to many, many to many
    * Foreign Key, a field point to another table's primary key, eg. in the class `Book`, we can set `author = models.ForeignKey(Author, on_delete=models.CASCADE)`, point to the table `Author` 's primary key.

    * Filtering with the foreign key by the field name following with double under score and then the field name in the table corresponding to the foreign key. (and also can add more condition or so called **modifier** with more double under score with the condition, such as `__contain`)  
    (eg.`Book.objects.filter(author__last_name__contains="ling")`)

    * When we set the foreign key field, we can set parameter `related_name` for we can conversely search from the foreign key's corresponding data back to this table's data with that name, such as: `author = models.ForeignKey(Author,on_delete=models.CASCADE, null=True,related_name="books_set")` in the `models.py` and `jkr = Author.objects.get(first_name="J.K.")`

    * For many-to-one relation, we use `models.ForeignKey()`, for the one-to-one relation, we use `models.OneToOneField()`, and for the many to many relation, we use `models.ManyToManyField()`

    * Whenever we are setting the relations between the two table, we must `.save()` the value to be connected first, then the setting thus become legal.

    * Setting the relation of one-to-one and one-to-many, we use the `=` operator, and for many-to-many, we use `.add()`.

    * Nested `Meta` class within the model class:
        1. What is class Meta?
        In Django, the fields within the Address class (such as street and city) define the database structure. In contrast, class Meta is used to define the behavior and presentation of the model. It does not become a column in the database; instead, it tells Django how to handle the class itself.

        2. The Role of verbose_name_plural
        This is one of the most commonly used settings within class Meta.

        Default Behavior: If you omit this line, the Django Admin interface will automatically convert your class name to lowercase and simply append an "s" to the end.

        For example: Address would become "addresss" (which is grammatically incorrect in English).

        Custom Effect: By setting verbose_name_plural, you can manually specify the plural form.

        In this case, you are telling Django: "Whenever you need to display the plural name, please use 'Address Entries' instead of just adding an 's'."

        ```python
        class Address(models.Model):
            street = models.CharField(max_length=80)
            postal_code = models.CharField(max_length=5)
            city = models.CharField(max_length=50)
            class Meta:
                verbose_name_plural = "Address Entries"
        ```
    
        3. Circular Relations & Lazy Relations