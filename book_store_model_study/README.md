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
    `instance.delete()`