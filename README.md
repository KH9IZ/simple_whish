Build:
```shell
docker build --tag=simple_whish .
```

> anonymous volumes removes with container if `--rm` passed, so let it be named

Secrets required:
- FLASK_SECRET_KEY
- OAUTH_CLIENT_ID
- OAUTH_CLIENT_SECRET

Run:
```shell
docker run \
    --interactive \
    --tty \
    --rm \
    --name=simple_whish \
    --publish=80:80 \
    --volume=simple_whish_db:/var/db/simple_whish \
    --mount=/var/secrets/:/var/secrets/ \
    simple_whish
```
