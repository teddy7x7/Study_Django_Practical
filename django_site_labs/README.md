## 🎓 What I Learned

This project study more details of the mechanics of Django. Key topics include:

#### Preparations for the Apps
- **Register Apps :** Register Apps in the `INSTALLED_APPS` list in the project's `config/settings`.

#### Preparations for URLs and Views
1. Planing the URLs and Views
- **/ :** Load starting page which list latest blog posts and some welcome text.
- **/posts :** Load page which lists all blog posts.
- **/posts/identifier-of-the-post :** By using the url `/posts/<slug>` , we can load individual blog post page which shows full blog post.

2. Register Apps' `urls.py` in the urlpatterns list in the project's `config/urls.py` .
3. Registering Apps' URLs in `App/urls.py` ,setting corresponding view functions and the name.
4. Be aware of the order of URLs in `App/urls.py`, since **named groups** might resolve the url wrong due to they only check the type of the dynamic segement.
```python
# We should put "reviews/<int:pk>" after "reviews/favorite/", or it will intercept the request to the "reviews/favorite/"
urlpatterns = [
    path("", views.ReviewView.as_view()),
    path("thank-you", views.ThankYouView.as_view()),
    path("reviews", views.ReviewsListView.as_view()),
    path("reviews/favorite/", views.AddFavoriteView.as_view()),
    path("reviews/<int:pk>", views.SingleReviewView.as_view()),
]
```

5. Comparison of Media and Static settings
    * Static
    ```python
    # settings.py

    # 1. The URL prefix used to reference static files in HTML templates.
    # Example: If set to '/static/', {% static 'css/style.css' %} becomes '/static/css/style.css'.
    STATIC_URL = '/static/' 

    # 2. Additional source directories where Django looks for static files.
    # Use this for "global" assets (e.g., a site-wide logo or layout CSS) that aren't tied to a specific app.
    # Django searches these folders in addition to the 'static/' folder inside each installed app.
    STATICFILES_DIRS = [
        BASE_DIR / "static",
    ]

    # 3. The absolute filesystem path where 'collectstatic' will gather all files for production.
    # This folder is intended for your web server (like Nginx or Apache) to serve files from.
    # WARNING: Do not put your source files here manually; they will be overwritten.
    STATIC_ROOT = BASE_DIR / 'staticfiles'
    ```

    * Media
    ```python
    # settings.py

    # Absolute filesystem path to the directory that will hold user-uploaded files.
    # This is where Django saves files uploaded through FileField or ImageField.
    # This setting value is used in the development stage, we should set it to other value in the production phase.
    MEDIA_ROOT = BASE_DIR / "media"

    # URL that handles the media served from MEDIA_ROOT.
    # It is the public URL prefix used in templates to access these files.
    # Example: If a file is at 'uploads/profile.jpg', its URL will be '/media/profile.jpg'.
    MEDIA_URL = "/media/"
    ```

    * Comparison: Static Files vs. Media Files

        | Feature | Static Files | Media Files |
        | --- | --- | --- |
        | **Definition** | Files that compose the application (CSS, JS, Images). | Files uploaded by users during runtime. |
        | **Origin** | Created by Developers. | Created by Users. |
        | **Version Control** | Tracked by Git (source files). | **Ignored** by Git (user content). |
        | **Deployment** | Collected via `collectstatic` to `STATIC_ROOT`. | Uploaded directly to `MEDIA_ROOT`. |
        | **Serving (Prod)** | Typically served via Web Server (Nginx). | Often stored in Cloud Storage (AWS S3). |
   

#### Basic Preparations for Templates and Static Files
1. Create folder `Templates` for global templates and `Static` for global static files in the root folder. 
2. Register global templates folder's path in the TEMPLATES list in the project's `config/settings`.
3. Register global static files folder's path in the STATICFILES_DIRS list in the project's `config/settings`.
4. Create folder `Templates` for specific App's templates and `Static` for specific App's static files in the App folder.
5. Within `App/templates` and `App/templates`, create namespaced template folder and namespaced static folder. Thus, prevent file name collisions.

####  Building prototype
1. Divide each page into several main section, then further divide them into more concrete detail sections.
2. Use lorem in the views.py before implement the database. DTL also provide lorem tag for the templates.
3. Using the `include` tag in template A to include code snippet from template B. Template A get some value pass from views.py can also be accessible in the template B due to the function of `include`.
4. The `add` filter can append things behind the hard coded part, ig. `{% static "blog/images/"|add:post.image %}`.
5. For the dictionary in the DTL, we use dot notation rather than the square bracket, ig `post.image` rather than `post["image"]`.

#### Adding Data and Models
1. Defining data and model requirements > adding Models and relationships > adjustings Views and Templates
2. `latest_posts = Post.objects.all().order_by("-date")[:3]`, django would convert this into a sql commend rather than fetch all the data from the database.

#### Forms
* Creating and Handling Forms, Simplifying Form Management
    1. Forms and different Http methods
        * The html button tag has the default property `type=submit`, this would summit the data of the form which embrace the button tag by construct a new http request and send to the server that serves this form. Without futher configuration, this would be send to the main server page of that domain.

        * By defualt, the request type is *GET*. For the defualt button being pressed, it would form a GET request and the entered data in the form is added to a so-called **query parameter** to the url which leads by a question mark in the url and coming with pairs of key-value pair bond by "=".

        * But usually, we would alter the form to send a *POST* request to send the data to the server by the setting the form's method attribue
            `<form method="POST">`
        
    2. The **CSRF** token/cookie for safety:
        * **CSRF** stands for cross site request forgery
        * For POST forms, you need to ensure:  
            1. Your browser is accepting cookies.  
            2. The view function passes a request to the template’s render method.  
            3. In the template, there is a `{% csrf_token %}` template tag inside each POST form that targets an internal URL.  
            4. If you are not using CsrfViewMiddleware, then you must use csrf_protect on any views that use the csrf_token template tag, as well as those that accept the POST data.  
            5. The form has a valid CSRF token. After logging in in another browser tab or hitting the back button after a login, you may need to reload the page with the form, because the token is rotated after a login.
        
        * `{% csrf_token %}` template tag would add a dynamic generated token to the form (the token is generated on the server side's Django), it would send with the form datas within the POST request. For the server side can check whether the send back POST request is with the valid token or not.

        In the django template :
                ```html
                <form method="POST">
                    {% csrf_token %}
                    <label for="username">username</label>
                    <input id="username" name="username" type="text">
                    <button>Send</button>
                </form>
                ```
        In the browser, look at the Element, we can find that token `csrfmiddlewaretoken` :   
        ```html  
        <form method="POST">
            <input type="hidden" name="csrfmiddlewaretoken" value="ZXLkBU9wve2Nrkfu2JgQHPQx31Lm3PZoLezYNdByroHgLp5It2Kt3wGxCZQbqGdH">
            <label for="username">username</label>
            <input id="username" name="username" type="text">
            <button>Send</button>
        </form>                    
        ```
            
    3. Where does the POST request sent the data to:
        * The `action` property of the form html tag can set the path after the domain to which the request should be sent.
        
        * We can sent GET and POST request to the same url, and in the `views.py`, within the view function corresponding to the url, we can first check the request type and then perform distinct operation afterward.

        * In a view function within the `views.py`, we can access the POSTed data from the request sent into the function by `request.POST`. This holds a dictionary. The key is the `name` property of a input tag in the form. By using the key, we can get the corresponding entered value, ig `request.POST["username"]`.
    
    4. Validation with the dango form  
        To validate the content of the form sent from the the browser, django has built-in **django form class**
        * Creat a `forms.py` file in the app folder and create the **django form class** in it.
        * In the `forms.py` file, we define a class defines the shape of our form, the different inputs we want, and the corresponding validation rules for those inputs. This would allow us let Django automatically validate the input and render the template for us.

        * Define the django form class just like the model classes.
            ```python
            # In the forms.py
            from django import forms

            class ReviewForm(forms.Form):
                user_name = forms.CharField()
            ```
            ```html
            <!--In the xxx.html-->
            <form action="/" method="POST">
                {% csrf_token %}
                {{ form }}
                <button type="submit">Send</button>
            </form>
            ```
        * Validate in the `views.py`:
            ```python
            def review(request):
                if request.method == 'POST':
                    form = ReviewForm(request.POST)

                    # return true if every thing is valid in the form
                    if form.is_valid():
                        print(form.cleaned_data)
            ```

        * Rerender the form with the not valid form (ie. `form.valid == false`) and its data which sent by the browser. We can do this by the following
        ```python
        if request.method == 'POST':
            form = ReviewForm(request.POST)

            if form.is_valid():
                print(form.cleaned_data)
                return HttpResponseRedirect("/thank-you")
            # if is invalid, send this form generate which has been validate(invalid) to the render function, and let the template generate hints of invalid inputs and preserve other valid inputs.
            
        else:
            # only create a new form when request.method == 'GET'
            form = ReviewForm()
        return render(request, "reviews/review.html", {
            "form": form
        })
        ```

        * If the input is invalid, django would return an unordered list which has property `class="errorlist"`.

        * Customizing the form controls
            * We can get different field of the form by the `form.<field>. ...` within the template
                ```html
                <div class="form-control {% if form.user_name.errors %}errors{% endif %}">
                    {{ form.user_name.label_tag}}
                    {{ form.user_name}}
                    {{ form.user_name.errors}}
                </div>
                <button type="submit">Send</button>
                ``` 
        
        * Use the **for tag** in the template and loop through all the field in the form to create repeated structure of the form, thus we can increase the fields of a form with minor changes (no need to change the views.py, just styling in the template, and mainly changes are what fields are added to a form class in the forms.py):
            ```html
            {% for field in form %}
                <div class="form-control {% if field.errors %}errors{% endif %}">
                    {{ field.label_tag}}
                    {{ field}}
                    {{ field.errors}}
                </div>
            {% endfor %}
            ```

        * Storing form data to database
            ```python
                if request.method == 'POST':
                    form = ReviewForm(request.POST)

                    if form.is_valid():
                        # print(form.cleaned_data)
                        review = Review(
                            user_name = form.cleaned_data['user_name'],
                            review = form.cleaned_data['review_text'],
                            rating = form.cleaned_data['rating']  
                        )
                        review.save()
                        return HttpResponseRedirect("/thank-you")
            ```


* Modelforms
    1. The `django.forms.ModelForm`:
        * Connect a form(ModelForm) class to a model class and django would automatically take all the model fields and infer html inputs for those fields. This is realized by using a nested Meta class within the form class:

        ```python
        class ReviewForm(forms.ModelForm):
            class Meta:
                model = Review
                # fields = '__all__'
                fields = ['user_name', 'review_text', 'rating']
                # exclude=['owner_comment']
        ```
    
    2. Configuring the ModelForm:
        * How to change defualt labels, error messages...etc. ? 
          We can set different kinds of dictionary to modify the form, field name as the key and what we want as the value.
          ```python
          class ReviewForm(forms.ModelForm):
            class Meta:
                model = Review
                fields = "__all__"
                # fields = ['user_name', 'review_text', 'rating']
                # exclude=['owner_comment']

                labels = {
                    "user_name": "Your Name",
                    "review_text": "Your Feedback",
                    "rating": "Your Rating"
                }
                error_messages = {
                    "user_name": {
                    "required": "Your name must not be empty!",
                    "max_length": "Please enter a shorter name!"
                    }
                }
          ```
        
    3. Saving data with a ModelForm
        * For saving a Form class data to in the `views.py`, we construct a `Form` object with the submitting data, validating the object, and construct a `Model` object to save the validated data.
            ```python
            form = ReviewForm(request.POST)

            if form.is_valid():
                # print(form.cleaned_data)
                review = Review(
                    user_name = form.cleaned_data['user_name'],
                    review_text = form.cleaned_data['review_text'],
                    rating = form.cleaned_data['rating']  
                )
                review.save()
            ```
        * For saving a ModelForm (rather than a Form class), we can skip the `Model` object contruction and directly saves it to the database.
            ```python
            form = ReviewForm(request.POST)
            
            if form.is_valid():
            form.save()
            return HttpResponseRedirect("/thank-you")

            ```
        
        * The `form.save()` can not only save a new entry of data, but also able to update an existing entry by using extra parameter `instance` which recieves a model object get from the database:
            ```python
            from .forms import ReviewForm
            from .models import Review

            def review(request):
                if request.method == 'POST':
                    existing_data = Review.objects.get(pk=1)
                    form = ReviewForm(request.POST, instance=existing_data)
            ```


* Exploring Class-based Views
    1. For the class-based views, it has functions corresponding to all the http methods named in lower-case, thus there's no need to go for a if branch to determine which kind of the http method does the request possess.

    2. In the urls.py, use `.as_view()` to wire the url to that view class.
        ```python
            urlpatterns = [
                # path("", views.review),
                path("", views.ReviewView.as_view()),
                path("thank-you", views.thank_you)
            ]
        ```
    
    3. There are many class-based View classes that we can inherit from, rather than just the View class.  
        Such as :
        * Template Views
        * List and Detail Views
        * Form View and Creat/Update/Delete Views
        
        1. Template Views
            * A specific view class for return a template for a get request (render a template for the get request)
            * Import by `from django.views.generic.base import TemplateView`
            * Just set the specific attribute `template_name` in the inherit class, django would render the template implicitly.
            ```python
            # def thank_you(request):
            #     return render(request, "reviews/thank_you.html")

            # class ThankYouView(View):
            #     def get(self, request):
            #         return render(request, "reviews/thank_you.html")


            # from django.views.generic.base import TemplateView
            class ThankYouView(View):
                template_name = "reviews/thank_you.html"
            ```

            * If there is some dynamic content which needed to pass to the template, we can override the function `get_context_data`. 
            ```python
            class ThankYouView(TemplateView):
                template_name = "reviews/thank_you.html"

                def get_context_data(self, **kwargs):
                    context = super().get_context_data(**kwargs)
                    # corresponding to the tag in thank_you.html template
                    context["message"] = "This Works"
                    return context
            ```

            We **must** call the `super().get_context_data(**kwargs)` inorder to get the **Named Groups**(in a dictionary form) defined in the path function in the `urls.py` first, and add extra key value pairs into the dictionary. Finally, return the dictionary to render the template stored in the `template_name` variable.


        2. ListView
            * The process of responsing a GET request with rendering a list of entries fetched from the database is alway similar, so django provide `ListView` which can import by `from django.views.generic import ListView`. It would return the list of data implicitly, so there is no need for us to return anything. If we want to alter what is returned, there are still a bunch of functions we can override.
            
            ```python
            class ReviewsListView(TemplateView):
                template_name = "reviews/review_list.html"
                # a specific variable point to the model class where to fetch the list of data
                model = Review
                # reset the name of returned list from default name object_list to what we want, ig. "reviews"
                context_object_name = "reviews"

                # def get_queryset(self):
                #    base_query = super().get_queryset()
                #    data = base_query.filter(rating__gt=4)
                #    return data
            ```

        3. DetailView
            * Whenever we want to return a template for a GET request with a single piece of data using the `DetailView` with other logics we want to add, might be a better option than the TemplateView.
            It can be also imported from `django.views.generic`
            * Django find the single piece of data by the url bind to the view function. The url needs to possess primary key `pk` in its named groups, such as `"reviews/<int:pk>"`
            * The name of the item in the template would be the all lowercase of the model class name, or we can use `object` which is the default name of django used in the template.

        4. Form View and Creat/Update/Delete Views
            * Support GET request to return a form and POST request to handle the form submission from the browser, such as validation, possibly display the form again with errors hints, or save some data.

            ```python
            from django.views.generic.edit import FormView
            class ReviewView(FormView):
                # which form class should be used to render the form in the template
                form_class = ReviewForm
                template_name = "reviews/review.html"
                # must provide
                success_url = "/thank-you"
            ```

            * The FormView doesn't know what to do with a successful or validated submission. Maybe we just want to print it in the console, send as an email, write into a file, or save it into a database. Thus, we have override a function `` to designate what to do:
            ```python
            class ReviewView(FormView):
                # which form class should be used to render the form in the template
                form_class = ReviewForm
                template_name = "reviews/review.html"
                # must provide
                success_url = "/thank-you"

                def form_valid(self, form):
                    # since we have designate which form class to deal with
                    form.save()
                    # must return parent's function to let django do it's work
                    return super().form_valid(form)
            ```
        
        5. CreatView
            * A more specilized forView would save the form automatically. It would render, validate, show errors if needed, and save the data through the designated model if the submission is successful.
            ```python
            class ReviewView(CreateView):
                # May no need a form class
                # form_class = ReviewForm 
                # just directly set the corresponding model to let django know how to create data, just like in the ListView
                model = Review

                # Or can set the form class here inorder to do more detail settings
                form_class = ReviewForm
                template_name = "reviews/review.html"
                success_url = "/thank-you"
            ```

            * Corresponding to the CRUD, there are also **UpdateView**, **DeleteView** which work in the same way, ie. fetching data, show a form pre-populated with the data and update the data in the database.  

            * CreateView also can be utilized to save file (validation and save the data)
    
    4. When to use which view
        * The class views let us can write less code, but it just an option.
        * Writing functionality explicitly also a valid personal preference.


#### File Upload and File Storage
* Main topics:
    How does files uploads and file storage work?  
    Adding file uploads
    serving stored files
    
1. Html form tag's attribute `enctype` needs to set to specific value corresponding to upload file types. Usually we set `enctype="multipart/form-data"`whenever upload the data, such as pictures and files.

2. In the view function, instead of using `request.POST`, we `request.Files` to get file types uploads. Inorder to access to that file, we need to set a name property inside the input html tag, such as `<input type="file" name="image"/>`, and thus we can use it as the key to access the file in the view function, such as `request.FILES['image']`. 

3. Using Models for File Storage
    * `models.FileField()` will not store the data in the database, since it's a bad practice to store files in the database. Because this bloats the database and make the database slower. Insteadly, files should be stored in hard drives. Thus, `models.FileField(upload_to="<path-of-the-file>")` stores data somewhere in the hard drive and only store the storage path of the file in the model into the database.

    * How to set the `<path-of-the-file>` in `models.FileField()`  
    In the `config/settings.py`, we can add a variable named **MEDIA_ROOT**, which tells django where our files should be stored in general and any folder we might point at in our Models.py would be a subfolder of this **MEDIA_ROOT**.

    ```python
    # Inside config/settings.py

    # Absolute filesystem path to the directory that will hold user-uploaded files
    # The actual physical location on the disk where files are stored.
    MEDIA_ROOT = BASE_DIR / "uploads"

    # URL that handles the media served from MEDIA_ROOT
    # The public URL used to access those files via a browser.
    MEDIA_URL = "/media/"
    ```

    * Using a model class to save the uploaded file just like the usual way we save an entry of data by `<modelinstance>.save()`, such as:
    ```python
    def post(self, request):
        submitted_form = ProfileForm(request.POST, request.FILES)

        if submitted_form.is_valid():
            # store_file(request.FILES['image'])

            profile = UserProfile(image=request.FILES['user_image'])
            profile.save()
            return HttpResponseRedirect("/profiles/")

        return render(request, "profiles/create_profile.html", {
            "form": submitted_form
        })
    ```

    * CreateView also can be utilized to save file (validation and save the data)
    ```python
    class CreatProfileView(CreateView):
    template_name = "profiles/creat_profile.html"
    model = UserProfile
    fields = "__all__"
    success_url = "/profiles/"
    ```

4. Serving the uploaded files
    * Inside the template, we can use `<list-item>.image.url` as the src of the img tag, inorder to get the image. This comes from the model's file or image field, which possess this built-in property `<field>.url`.  
    (`<field>.path` can be used when we want a file system path, which is nice to have if we run some python code on the server.)
    ```html
    {% for profile in profiles %}
      <li>
        <img src="{{ profile.image.url }}">
      </li>
    {% endfor %}
    ```

    * Django by default lock down all folders and does not expose them to the browser for security reason. Which means they're not accessible from outside the server. To expose the uploaded files, there are two things to be done:
        1. Set `MEDIA_URL` in the `config/settings.py`
        ```python
        # Inside config/settings.py

        # Absolute filesystem path to the directory that will hold user-uploaded files
        # The actual physical location on the disk where files are stored.
        MEDIA_ROOT = BASE_DIR / "uploads"

        # URL that handles the media served from MEDIA_ROOT
        # The public URL used to access those files via a browser.
        MEDIA_URL = "/user-media/"
        ```

        2. Register this url in the `config/urls.py` by appending a `static()` to the urlpatterns list. This is a helper function which serves static files. It needs two arguments, first is the url used for exposing the files (the one registered with the variable `MEDIA_URL` in the `settings.py`), and the second one is the corresponding path on the file system that holds the actual file, ie `MEDIA_ROOT`.  

        The example of using `+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)`:
        ```python
        from django.conf.urls.static import static
        from django.conf import settings

        urlpatterns = [
            path("admin/", admin.site.urls),
            path("", include("reviews.urls")),
            path("profiles/", include("profiles.urls")),
        ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
        ```

#### Sessions
* Enabling & configuring sessions
    * To enable the session functionality
        1. In the `config/settings.py`, make sure in the `MIDDLEWARE` list the `middleware.SessionMiddleWare` is added. 
        
        2. Also make sure that `django.contrib.sessions` is registered in the `INSTALLED_APPS` list.
    
    * Configuring the session
        * In the `config/settings.py`, we can set variable `SESSION_COOKIE_AGE`, ie. define how long a session cookie and therefore the session itself should survive. The unit of it is second. (The defualt is two weeks.)

    * Save and Read the session data
        * Within the view function, the `request` object has the `.session` property. We can utilize it to add new data or access to origin data in the session data in the way of using a dicitonary.

        * Sessions and Serializability  
        Under the hood, django takes whatever we store in a session and serializes it to JSON format. An object can't be directly serialized, since it not only contains data but also methods which can't be serialized, thus unable to be translated to JSON.

        ```python
        # wrong! we shall not to save a whole object to a session. We only save simple value in a session.
        # request.session["favorite_review"] = fav_review
        request.session["favorite_review"] = review_id
        ```

        * Read the saved session data  
        In a template, data of the input tag of a form is returned in type of **string**, so when we are fetching it in the view function must be careful of it's type, such as we shall convert it back to integer before comparing it with another integer in the view function.

        * Safely access session data  
        Trying to access any session data can fail if it wasn't set before. Thus, if we load the site without any sessions set, a key hasn't been set in the session, it would fail with KeyError.  
        So, the safer way is to use the **session's get method** to access data, if we are not sure that it has been set before or not.
        ```python
        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            
            # Get the current object being displayed
            loaded_review = self.object
            
            # Use .get() to avoid a KeyError if "favorite_review" hasn't been set in the session
            favorite_id = self.request.session.get("favorite_review")
            
            # Perform a type-safe comparison to check if this review is the favorite.
            # We cast to int because session data is often stored as strings.
            try:
                if favorite_id:
                    is_favorite = int(favorite_id) == loaded_review.id
                else:
                    is_favorite = False
            except (ValueError, TypeError):
                # Handle cases where favorite_id exists but isn't a valid integer
                is_favorite = False

            context["is_favorite"] = is_favorite
            return context
        ```

#### Complete the Blog project
* Session
    * Use `request.session.get` try to get the field saved in the session, and use `if` statement to check whether the `get` method return with a not none value.

    * Store or reset value in a session, just like using a dictionary, such as `request.session["stored_posts"] = stored_posts`.


    ```python
    class ReadLaterView(View):
        def get(self, request):
            stored_posts = request.session.get("stored_posts")

            context = {}

            if stored_posts is None or len(stored_posts) == 0:
                context["posts"] = []
                context["has_posts"] = False
            else:
            posts = Post.objects.filter(id__in=stored_posts)
            context["posts"] = posts
            context["has_posts"] = True

            return render(request, "blog/stored_posts.html", context)


        def post(self, request):
            stored_posts = request.session.get("stored_posts")

            if stored_posts is None:
            stored_posts = []

            post_id = int(request.POST["post_id"])

            if post_id not in stored_posts:
            stored_posts.append(post_id)
            else:
            stored_posts.remove(post_id)  
            
            request.session["stored_posts"] = stored_posts
            
            return HttpResponseRedirect("/")
    ```

* Deployment
    * The overall structure:
        * User (Browser) <--- HTTP ---> Nginx <--- uwsgi protocol ---> uWSGI <--- WSGI protocol ---> Python App (Django/Flask)

        * Request Flow and Technical Stack:
            1. External Layer: The Nginx server acts as the primary entry point, managing HTTP/HTTPS connections and serving static assets.
            2. Communication Bridge: For dynamic requests, Nginx communicates with the uWSGI server using the high-performance binary uwsgi protocol.
            3. Application Layer: uWSGI serves as the application container that implements the WSGI specification, ensuring seamless interaction with Python-based frameworks like Django or Flask.
            4. Internal Logic: The Python App processes the data and returns the response back through the same pipeline.

    * Deployment considerations and pitfalls
        1. Choose Database: SQLite work but might be too slow or be erased(depends on hosting provider).
        2. Adjust `settings.py`: Adjust config for chosen hosting provider, disable development-only settings.
        3. Collect Static Files: Static files are **NOT** served automatically (just like user uploads, .css files) by Django.
        4. Handle static & uploaded files serving
        5. Choose a Host & deploy: Also dive into host-specific docs & examples
    
    1. Static files 
        * Collect static files Before deployment by `uv run python manage.py collectstatic` 
        * **Options of serving the static files**
            1. Configure django to serve these files (by `config/urls.py`)
                Okay for smaller sites, not performance-optimized though.  
                Set the routing in the `config/urls.py` as following code using `static()` to do this:
                ```python
                urlpatterns = [
                    path("admin/", admin.site.urls),
                    path("", include("blog.urls")),  # Here, we set the blog app to be the root of the site, ie. link https://localhost:8000/ to it
                ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
                + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
                ```
            2. Configure web server to serve these files and the django app  
                Same server and device but seperate process, better for performance.

            3. Use dedicated service/server for static and uploaded files  
                Initial setup is more complex but offers best performance.
        
        * Before deployment, make sure the following:
            1. The migration is done
            2. superuser is created
            3. all the static files are already collected
            4. Within the `config/settings.py`
                * Set `DEBUG` from `TRUE` to `FALSE`
                
            
            5. The **Evnvironment Variables** settings
                *  We want to set/pulgin these variables with concrete values into the `settings.py` file only after deployment. The **Evnvironment Variables**, allow us to use a placeholder in the file, and assign the value afterwards.  

                This can be realized by using the python's package `dotenv` and python's built-in `os.getenv`.  

                1. Install the the `dotenv` first with `uv` and re-generate the `requirements.txt` by `uv export --format requirements-txt --output-file requirements.txt`.  

                2. In the `config/settings.py`, load the `.env` file with `load_dotenv()`, then get the value inside it with `os.getenv()`.
                
                ```python
                import os
                from pathlib import Path
                from dotenv import load_dotenv
                
                BASE_DIR = Path(__file__).resolve().parent.parent

                load_dotenv(os.path.join(BASE_DIR, '.env'))
                
                DEBUG = os.getenv('DEBUG') == 'True'
                SECRET_KEY = os.getenv("SECRET_KEY")
                ALLOWED_HOSTS = ALLOWED_HOSTS = [host.strip() for host in os.getenv("ALLOWED_HOSTS", "").split(",")]
                ```
                
                * `SECRET_KEY`  
                    Generate the `SECRET_KEY` going to used in the deployment phase, save it into the `.env` file and add this file into the `.gitignore` before any `git add` and `git commit`. Never expose this key to the public, instead we create another file `.env.example` to let coworkers know what fields need to be configured.
                
                * The `ALLOW_HOST` list  
                    We need to add all the hosts/domains, which basically should be able to send requests to this django application, ie. the hosting address of the server, which will host this application in the end.

            6. Security settings
                * Change the admin urls in `urls.py` for safety.
                * Add three more settings:
                    ```python
                    # SECURITY
                    SECURE_SSL_REDIRECT = os.getenv("SECURE_SSL_REDIRECT", "false") == "true"
                    SESSION_COOKIE_SECURE = SECURE_SSL_REDIRECT
                    CSRF_COOKIE_SECURE = SECURE_SSL_REDIRECT
                    ```

            7. Locking in Dependencies
                * Lock in the core dependencies(python packages), which this project use. In this project, the two core packages are django and pillow. We also need to make sure that these dependencies are installed on the host we're going to deploy our application to. Check the docs. of the hosting provider. 
                
                * Most python hosting providers support `requirements.txt`, which we add to our project listing the dependencies needed. Using `pip` with the command `python -m pip freeze > requirements.txt`, we can generate this file. However, we are using `uv` rather than `pip` in this project. 

                * While traditional `pip` uses `freeze` to capture currently installed packages, `uv export` is the modern standard. It generates a requirements file directly from our `uv.lock` file, ensuring that the exported dependencies are exactly what our project expects.  
                To generate a basic requirements.txt for the project, run:
                `uv export --format requirements-txt --output-file requirements.txt`

                * With the `requirements.txt` created, it will be picked up by many hosting providers to install all the required dependencies, and the AWS service which we are going to use is no exception. It will also automatically look at this file when we deploy our application and install all these packages on the server, where we deploy the application to.
        
        1. **Option1** : Configure django to serve static files, media files
            * The first step is to do this, test the basic setting works fine, then we can alter this setting to become other two settings (Configure web server to serve these files and the django app on distinct process, or Use dedicated service/server for static and uploaded files)

            * For the case of using **AWS Elastic Beanstalk**
                * We need to create a `.ebexteionsions` folder for the Elastic Beanstalk service to find the configuration files and create a YAML file `django.config` inside it. The basic content of `django.config` we used:

                ```YAML
                option_settings:
                    aws:elasticbeanstalk:container:python:
                        WSGIPath: config.wsgi:application
                ```
            
            * After all the files has been created and checked, we shall compress most of the files in the root folder in to a zip file 
                * **Don't include the .env file**, static folder(include staticfiles folder instead).
                * For the package related files, include `requirements.txt`, `uv.lock`, `pyproject.toml`
                * For the **AWS Elastic Beanstalk** settings, include `.ebexteionsions` folder.
                * For the Django application, include all the apps folder, `config` folder, `manage.py`. If we use the SQLite, then include the `db.sqlite3`
                * And include the `staticfiles` and `media` folder.

            * We can find some CI/CD method to automates this process.

            * Finally, we up load the zip file to the **AWS Elastic Beanstalk**. We can execute `git rev-parse --short HEAD` in the commandline in the root folder and  output the abbreviated commit hash (SHA-1 or SHA-256) of the current HEAD (the commit we are currently on). Then record this value in the version label field with the uploaded zip file on the AWS Elastic Beanstalk pannel.
        
        2. **Option2** : Configure a web server to serve both static files, media files and django app
            * Same server, but serve seperately. The request for static files and media files don't go to the django app any more.

            * To do this rather than let django handle these files, we need to change the web server configuration by, for example in the web server hosting provider control pannel, such as **AWS Elastic Beanstalk**.

            * In side the configuration pannel, we can find the **Proxy server**, such as Nginx.
            * For the Nginx to serve the django app, We shall create another file named **static-files.config** inside `.ebexteionsions` folder. Elastic Beanstalk would pickup this file and change its interal Nginx configuration to serve these static and media files differently. Inside the file, we set `<url>:<ROOT_forlder_path_of_that_kind_of_files>` as the following :

            ```YAML
            option_settings:
                aws:elasticbeanstalk:environment:proxy:staticfiles:
                    /static: staticfiles
                    /media: media
            ```

            * Since we set Nginx to serve these files, thus there is no need for django to deal with the request to these urls. So we can get rid of these in the `config/urls.py`, where we resolve the urls with `static()`, ie. remove or comment out the last two line of the following code:

            ```python
            urlpatterns = [
                path("top-secret-admin666/", admin.site.urls),
                path("", include("blog.urls")),
            ] # + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
              # + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
            ```

        * Use dedicated service/server for static and media files seperate from django app

        2. **Option3** : Use dedicated service/server for static and uploaded files
            * We use a totally different service/server than the Elastic Beanstalk. We use **AWS S3** (simple storage service) to serve our staticfiles and media files.

            * In this changing, we no longer store the static files, the uploads(media files) in the django project folders. Thus, when we collect the project static files into the `staticfiles` folder, **this folder shall not store in the project root folder anymore.** Instead, the collected static files and the media files shall be forwarded to the S3 server.

            * Create a S3 bucket

            * The IAM (Identity Access Management) service
                * A service that allow us to grant other users or applications access to our aws account or to the services in this aws account.
                    * create a new group -> attach policy (set up as little permissions as possible to restrict the kind of access django app has to this bucket in the end to only what is needed, for the security reason, or hackers might harm our aws account through the django app)
                    -> Here we set AmazonS3FullAccess policy
                    -> Add Django app as a programmtic user
                    -> Generate **access key id** and  **secret access key** at the end, and set these value to the django app. Let django app can connect S3 through this **user**.

                    * To let the django app can utilize the newly created aws user and access files on the S3, we shall:
                        * Install packages:  
                            `django-storages`: allow us to change the way that django handles local files
                            `boto3`: the offical aws sdk for python which allows us to communicate with aws services programmatically from inside python applications.
                        
                        * Update packages in the `requirements.txt`.
                        
                        * Modify the `settings.py` to control how django stores and manages files
                            * Register the `'storages'`(`django-storages`) into the `INSTALLED_APPS`, inorder to overwrite the default mechanism.

                            * Add AWS specific settings, which would be picked up by the `boto3`, to inform django and python how to communicate with our aws account:
                                ```python
                                AWS_STORAGE_BUCKET_NAME = "<your-s3-bucketname>"
                                AWS_S3_REGION_NAME = "<your-s3-bucket-region>"
                                AWS_ACCESS_KEY_ID = "<your-aws-access-key-id>"
                                AWS_SECRET_ACCESS_KEY = "<your-aws-secret-access-key>"

                                AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"

                                STATICFILES_FOLDER = "static"
                                MEDIAFILES_FOLDER = "media"

                                STATICFILES_STORAGE = "custom_storages.StaticFileStorage" # the file storage engine to use when collecting static files with the collectstatic management command. We swap the default setting with the S3boto storage, which move the collected static files to aws s3. 
                                
                                DEFAULT_FILE_STORAGE = "custom_storages.MediaFileStorage" # This field is for the media files in django settings
                                ```
                            **We shall save these value, aspecially the AWS_ACCESS_KEY_ID and the AWS_SECRET_ACCESS_KEY, as environment variables in the .env file, DON'T expose to others!!!**

                            * **We shall not set DEFAULT_FILE_STORAGE as the same value to the STATICFILES_STORAGE, which means saving uploaded media file to the same position/folder to the static files. This would introduce the security problems, which the hackers might be able to alter or override the contents of our static files**

                            * To seperate the static files and media files storage, we shall:
                                * Create file `custom_storages.py` in the root folder of the django project. Create the class inherit from `S3Boto3Storage` to set the folders customly.
                                    ```python
                                    from django.conf import settings
                                    from storages.backends.s3boto3 import S3Boto3Storage

                                    class StaticFileStorage(S3Boto3Storage):
                                        location = settings.STATICFILES_FOLDER

                                    class MediaFileStorage(S3Boto3Storage):
                                        location = settings.MEDIAFILES_FOLDER
                                    ```
                                
                                * Add two keys `STATICFILES_FOLDER` and `MEDIAFILES_FOLDER` in the `settings.py`. These folders would be created in the S3 automatically.

                                    ```python
                                    STATICFILES_FOLDER = "static"   # collect and store static files in the subfolder "static" of the s3 bucket
                                    MEDIAFILES_FOLDER = "media"     # save the uploaded files in the subfolder "media" of the s3 bucket
                                    ```

                            * We can test it with the collectstatic command and check if the files are uploaded in the s3 control pannel. Then locally run `python manage.py runserver --nostatic` to tell django not to serve the static files. Check the request responses header. In the html files, find the link tag and check does it match the `AWS_S3_CUSTOM_DOMAIN`.

                        * upload the new zip file and redeploy the django app on the Elastic Beanstalk.
    
    2. Database
        * SQLite
        * Postgresql
            * Need to install additional package inorder to work with django.
            * For example, AWS RDS provides this data base. We need to change the database settings inside the `config/settings.py`. We shall create the superuser first and then set the following with the other values provide by AWS RDS.

            ```python
            DATABASES = {
                "default": {
                    "ENGINE": os.getenv("DB_ENGINE", "django.db.backends.postgresql"),
                    "NAME": os.getenv("DB_NAME"),
                    "USER": os.getenv("DB_USER"),
                    "PASSWORD": os.getenv("DB_PASSWORD"),
                    "HOST": os.getenv("DB_HOST"),
                    "PORT": os.getenv("DB_PORT", "5432"),
                }
            }
            ```

            * We also need to set the inbound rules to let the django apps run on the web server can legal access this database based on the firewall settings. For the AWS RDS, we can add the security group of the web server run the django app to the inbound rules to fulfill the requirements.
    
    3. Web server
        * asgi
        * Wsgi