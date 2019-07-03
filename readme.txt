install postgresql-10

sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt/ xenial-pgdg main" >> /etc/apt/sources.list.d/pgdg.list'
wget -q https://www.postgresql.org/media/keys/ACCC4CF8.asc -O - | sudo apt-key add -
sudo apt-get update

проверка наличия 10 версии в репозитории
apt-cache search postgresql-10

sudo apt-get install postgresql-10 postgresql-contrib

проверка работы
systemctl status postgresql


sudo -u postgres psql
CREATE DATABASE db;
CREATE USER postuser WITH password 'passuser';
GRANT ALL ON DATABASE db TO postuser;
ALTER USER postuser CREATEDB;               # право на создание db, понадобилось для юнит тестов
\q

sudo service postgresql restart

sudo apt-get install rabbitmq-server
sudo rabbitmqctl add_user celeryuser celerypass
sudo rabbitmqctl add_vhost myvhost
sudo rabbitmqctl set_user_tags celeryuser mytag
sudo rabbitmqctl set_permissions -p myvhost celeryuser ".*" ".*" ".*"

sudo rabbitmq-plugins enable rabbitmq_management  -start web interface[default user guest:guest]

При работе с celery очень важен часовой пояс. Если задачи через брокера сыпятся постоянно,
проверьте настройки часового пояса

-A TelegramSi8 beat -l info --scheduler django_celery_beat.schedulers.DatabaseScheduler

git checkout master
git merge viber

Продление сертификатов Let’s Encrypt
https://blog.m4rr.ru/all/letsencrypt-renewal/
cd letsencrypt/             # перейти в директорию letsencrypt
git pull                    # скачать обновления репозитория
./letsencrypt-auto --help   # проверить, что все нормально
sudo service nginx stop     # остановить сервер
./letsencrypt-auto renew    # ← обновить сертификаты
sudo service nginx start    # запустить сервер
