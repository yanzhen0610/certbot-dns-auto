# certbot auto wildcard

`main.py` wraps `certbot` command, deals with the interactions. These scripts allows the renewal to be ran programmatically(in cron job or something else.)

`main.py` will execute `dns-up.sh` for setup dns records and `dns-down.sh` for reset.

e.g. `dns-up.sh _acme-challenge.example.com the-text-record-data-will-be-here` or `dns-down.sh _acme-challenge.example.com`

## How to use?

```sh
# I suggest to start a new virtual environment before running pip
# activate virtual envrionment
python3 -m venv .venv
source .venv/bin/activate
# install dependices(certbot)
pip install -r requirements.txt # install certbot
# your DNS scripts
cp dns-down.example.sh dns-down.sh # dns-up script
vim dns-down.sh # change it for your own DNS
cp dns-up.example.sh dns-up.sh # dnw-down script
vim dns-up.sh # change it for your own DNS
# Run the wrapped certbot
env DOMAIN=example.com EMAIL=admin@example.com python3 main.py \
    --config-dir "${PWD}/config" \
    --work-dir "${PWD}/work" \
    --logs-dir "${PWD}/logs"
```

`--config-dir`, `--work-dir` and `--logs-dir` will be passed to certbot as arguments. (It's not required arguements.)
