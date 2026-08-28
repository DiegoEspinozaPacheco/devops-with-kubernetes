# Todo app

Serves the HTML page, its JavaScript, and a random cached
picture. All configuration (image path, cache duration, and the
Lorem Picsum URL) is read from a ConfigMap, nothing is hard
coded in the source. The page lets the user add a new todo (max
140 characters) and lists the existing ones, both handled by
fetching directly from the "todo-backend" service in the
browser.

## How to consume
Load the page:
```
GET /
```

Get the cached picture:
```
GET /image
```