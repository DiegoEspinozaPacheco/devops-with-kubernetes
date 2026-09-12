# Wikipedia reminder

A CronJob, not a long-running service. Runs once every hour,
fetches a random Wikipedia article URL from
https://en.wikipedia.org/wiki/Special:Random (reading the
Location header of its redirect, with an identifying User-Agent
as required by Wikipedia), and creates a todo "Read <URL>" by
calling todo-backend's POST /todos.

## How to consume
Not an HTTP service, has no endpoints of its own. Its only
effect is a new todo appearing in the "Todo app" list once per
hour.