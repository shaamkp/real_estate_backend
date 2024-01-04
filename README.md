env

SECRET_KEY=django-insecure-r_=b@3x^&cvm&)832zk_63=xhoi(nn%l1op72w%ovpemk@^tu8
ENCRYPT_KEY=15rbdMArWP7qqryE4OkeuuHzoP2C_6a5NF0cABxBKtQ=

ACCESS_TOKEN_LIFETIME=365
REFRESH_TOKEN_LIFETIME=730

DATABASE_URL=psql://postgres:root@localhost:5432/real_estate




------------------------------------------------------------------------------------

After the initial project configuration and requirement implementation, you want to construct a ChiefUser. You must complete various procedures in order to create ChiefUser.

    1. python manage.py shell
    2. from general.functions import CreateChiefUser
    3. CreateChiefUser('email','password')
