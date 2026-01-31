## 🎓 What I Learned

This project covers the core mechanics of Django's request-response cycle. Key topics include:

#### First to Third Section of the Course - Basics
- **Django Project Structure:** Understanding the organization of a standard project.
- **URL Routing:** Mapping URL patterns to specific view functions.
- **Dynamic URLs:** Using placeholders and captured values to create flexible routes.
- **Path Converters:** Ensuring type safety in URL segments (e.g., `<int:id>`).
- **Dynamic Views:** Using parameters and dictionaries to customize response data.
- **Redirection:** Implementing `HttpResponseRedirect` for flow control.
- **Maintainability:** Using `reverse()` and **Named URLs** to prevent hard-coding paths in `views.py`.
- **HTML Responses:** Generating and returning dynamic HTML content.

#### Fourth Section of the Course - Template and Django Template Language(DTL)
- **Template:** Registering templates, using `render()` function to render the template
- **Filters and Tags:**  
In the Django template language, a **filter** is used to perform simple transformations or processing on variables (usually formatting the output of strings or numbers), while a **tag** is more powerful, capable of executing logic control, loops, conditional statements, or inserting entire blocks of HTML.  
Simply put: **filters modify data, tags control flow or insert content.**  
    1. title filter : Captalize the word
    2. for tag : dynamical create repeated html code
    3. url tag : dynamical generate the url by utilzing the "name" of the view function and the dynamic fragment in the urls.py.
    4. if tag 

- **Template Inheritance:**  
    1. block tag
    2. include tag : To include a snippet of html code. Using addtional "with ...", we can pass value back to included parent template to do smth.
    3. the 404.html and the django.http.Http404()

- **Functions of DTL:**  {{ myDictionary.some_key }}
- **Dictionary of DTL:**  {{ result_from_a_function }} rather than {{ result_from_a_function() }}

- **Adding Static Files and CSS styling:**
    1. Static Files : CSS, Javascript and images are static files, which are not change by server from time to time. (Unlike the template do change according to the dynamic logic inside of them.)
    2. Use `{% load static %}` and `<link rel="stylesheet" href="{% static "path relative to the 'static' folder"%}">` in the template file to load the static file. Django would automatically find the file in the static folders of the Apps installed.
    3. Global level static folder : Django would not search the folders in the root folder (ig. BASE_DIR/static) by default. Just like we register the global template folder's path (ig. BASE_DIR/templates) in the settings.py in the `TEMPLATE`'s `DIR` list, we also need to register the path of the global by setting a new list `STATICFILES_DIRS` on our own.
    
    4. Inside the `settings.py`
    ```python
    # URL prefix for static files (used in both development and production)
    STATIC_URL = "/static/"

    # Additional locations Django will look for static files (besides app/static/),
    # used in both development and deployment (runserver and collectstatic)
    STATICFILES_DIRS = [
        BASE_DIR / "static"
    ]

    # Directory where collectstatic will collect static files for deployment
    STATIC_ROOT = BASE_DIR / "staticfiles"
    ```