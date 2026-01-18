## 🎓 What I Learned

This project covers the core mechanics of Django's request-response cycle. Key topics include:

#### First to Third Section of the Course
- **Django Project Structure:** Understanding the organization of a standard project.
- **URL Routing:** Mapping URL patterns to specific view functions.
- **Dynamic URLs:** Using placeholders and captured values to create flexible routes.
- **Path Converters:** Ensuring type safety in URL segments (e.g., `<int:id>`).
- **Dynamic Views:** Using parameters and dictionaries to customize response data.
- **Redirection:** Implementing `HttpResponseRedirect` for flow control.
- **Maintainability:** Using `reverse()` and **Named URLs** to prevent hard-coding paths in `views.py`.
- **HTML Responses:** Generating and returning dynamic HTML content.

#### Fourth Section of the Course
- **Template:**
- **Filters and Tags:**  
In the Django template language, a **filter** is used to perform simple transformations or processing on variables (usually formatting the output of strings or numbers), while a **tag** is more powerful, capable of executing logic control, loops, conditional statements, or inserting entire blocks of HTML.  
Simply put: **filters modify data, tags control flow or insert content.**  
    1. title filter
    2. for tag
    3. url tag
    4. if tag 
