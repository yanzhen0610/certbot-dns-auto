# certbot auto wildcard

```sh
# I suggest to start a new virtual environment before running pip
pip install -r requirements.txt # install certbot
cp dns-down.example.sh dns-down.sh # dns-up script, modified for your own
cp dns-up.example.sh dns-up.sh # dnw-down script, modified for your own
env DOMAIN=example.com EMAIL=admin@example.com python3 main.py \
    --config-dir "${PWD}/config" \
    --work-dir "${PWD}/work" \
    --logs-dir "${PWD}/logs"
```

`--config-dir`, `--work-dir` and `--logs-dir` will be passed to certbot as arguments.

`main.py` will execute `dns-up.sh` for setup dns records and `dns-down.sh` for reset.

e.g. `dns-up.sh _acme-challenge.example.com the-text-record-data-will-be-here` or `dns-down.sh _acme-challenge.example.com`
