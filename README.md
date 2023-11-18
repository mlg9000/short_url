# short_url_app.py

**URL shortener application in Python**

*Author: Matt Goebel*

## Running

This application is intended to be run as a container. You will need a platform that can run containers, such as Docker or Podman. The following commands should also work for Docker by replacing `podman` with `docker`:

### Build the container

```bash
podman build --tag short_url_app .
```

### Run the container in the foreground on port 5000 with the default bridge network

```bash
podman run --name short_url_app -p 5000:5000 localhost/short_url_app
```

## Automated Testing

An automated test script is provided in `./tests`. The only requirements to run it are that Python 3 and `requests` are installed on the system.

Run with the default `base_url` (http://127.0.0.1:5000). This can be overridden by supplying the `--base_url` argument.

Default example:

```bash
python test_short_url_app.py
```

With an alternative host and/or port:

```bash
python test_short_url_app.py --base_url=http://some_other_host:8080
```

## Manual Testing

A simple way to manually test the app is with `curl`.

Valid test example for the `/encode` endpoint:

```bash
curl -X POST -H 'Content-type: application/json' --data '{"long_url": "http://example.com"}' http://localhost:5000/encode
```

Valid test example for the `/decode` endpoint (will return something if there's at least one URL that's been encoded):

```bash
curl -X POST -H 'Content-type: application/json' --data '{"short_url": "http://smallurl/0"}' http://localhost:5000/decode
```
```
