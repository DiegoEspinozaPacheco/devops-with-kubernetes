# Todo app

Serves the HTML page, its JavaScript, and a random cached
picture. The page lets the user add a new todo (max 140
characters) and lists the existing ones. Both the listing and
the creation of todos are handled by fetching directly from the
"todo-backend" service in the browser, not by todo-app itself.

## How to consume
Load the page:
```
GET /
```

Get the cached picture:
```
GET /image
```