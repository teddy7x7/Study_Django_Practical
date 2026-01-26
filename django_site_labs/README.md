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
* Exploring Class-based Views