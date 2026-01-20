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

####  
