# Wikipedia reminder (GKE, Kustomize)

A CronJob that runs once an hour (`0 * * * *`), fetches a random
Wikipedia article, and posts it as a new todo (`"Read <url>"`) to
`todo-backend`.

## Environment variables

- `TODO_BACKEND_URL` - full URL of `todo-backend`'s `/todos` endpoint

Each run creates a Job that exits after a single request; nothing is
retried (`restartPolicy: Never`). See the exercise-level README for
how to trigger it manually instead of waiting for the schedule.