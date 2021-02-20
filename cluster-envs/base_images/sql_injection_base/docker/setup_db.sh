#!/bin/bash

echo "logging in"
# Login
curl --location --cookie cookie.txt --cookie-jar cookie.txt --request POST 'http://172.18.7.42/login.php' --header 'Content-Type: application/x-www-form-urlencoded' --data-urlencode 'username=admin' --data-urlencode 'password=password' --data-urlencode 'Login=Login'

sleep 5

echo "setting up database"
# Setup database
curl --location --cookie cookie.txt --cookie-jar cookie.txt --request POST 'http://172.18.7.42/setup.php' --header 'Content-Type: application/x-www-form-urlencoded' --data-urlencode 'create_db=Create / Reset Database'