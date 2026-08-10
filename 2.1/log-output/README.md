# Log output (multi-container)

## log-randomizer
Generates a random string on startup and appends a line with the string and a timestamp to a shared file every 5 seconds

## http-endpoint
Reads that shared file and serves its content on GET /.