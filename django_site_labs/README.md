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


        2. List and Detail Views
        3. Form View and Creat/Update/Delete Views
