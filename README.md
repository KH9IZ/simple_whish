Build:
```shell
docker build --tag=simple_whish .
```

> anonymous volumes removes with container if `--rm` passed, so let it be named

Run:
```shell
docker run \
    --interactive \
    --tty \
    --rm \
    --name=simple_whish \
    --publish=80:80 \
    --volume=simple_whish_db:/var/db/simple_whish \
    simple_whish
```
