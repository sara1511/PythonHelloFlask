#!/usr/bin/env bash

apt-get update
apt-get install -y gcc

pip install bertopic

cp /etc/ssl/openssl.cnf /home
sed -i -e 's/DEFAULT@SECLEVEL=2/DEFAULT@SECLEVEL=0/g' /home/openssl.cnf
cp /home/openssl.cnf /etc/ssl

gunicorn --bind=0.0.0.0 --timeout 600 run:app