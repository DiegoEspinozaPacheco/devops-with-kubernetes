# Todo app (GKE, Kustomize)

Frontend for "the project". Serves a page that shows a random image,
lets you add a todo (max 140 characters) and lists the existing ones.

## Endpoints

- `GET /` - the HTML page. Also doubles as GKE's Gateway health check
  target.
- `GET /image` - a cached random image from Picsum, refreshed every
  `CACHE_SECONDS`.

The page's own JavaScript calls `GET /todos` and `POST /todos` on the
same origin - those are served by `todo-backend`, reached through the
shared Gateway route. See the exercise-level README for build, push
and deploy commands.

## Environment variables

- `PORT` - port the server listens on (default `3000`)
- `IMAGE_PATH` - where the cached image is stored on the mounted
  volume
- `CACHE_SECONDS` - how long the cached image is reused before
  fetching a new one
- `PICSUM_URL` - source of the random image