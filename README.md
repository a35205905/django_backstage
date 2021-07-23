# django_backstage 1.0

## 環境
- MySQL：8.0
- Python：3.7

## 安裝方式
### 虛擬環境
```shell
安裝虛擬環境
$ pip3 install pipenv
設定虛擬環境路徑
$ export PIPENV_VENV_IN_PROJECT=1
建立虛擬環境
$ pipenv --three
進入虛擬環境
$ pipenv shell
安裝django package
$ pipenv install
```

### 資料庫遷移
編輯`env/lib/python3.7/site-packages/django/db/backends/mysql/base.py`註解下列程式碼
```python
version = Database.version_info
#if version < (1, 3, 13):
#    raise ImproperlyConfigured('mysqlclient 1.3.13 or newer is required; you have %s.' % Database.__version__)
```
> Python版本依據該環境為主


### .env
複製 `.env`
```shell
$ cp .env.example .env
```
> 編輯`.env`並修改`DB_HOST`, `DB_DATABASE`, `DB_USERNAME`, `DB_PASSWORD`, `DEBUG`

### 建立資料庫
由資料庫遷移檔建立資料表
```shell
$ python3 manage.py migrate
```
> 要記得先到MySQL建立該資料庫

### 建立超級使用者帳號
```shell
python3 manage.py createsuperuser
```

### 啟動開發伺服器
```shell
$ python3 manage.py runserver
```
### 開始開發吧:)
http://localhost:8000/

## 正式部署

### 環境
OS
- Ubuntu：18.04 LTS
- 專案路徑：`/var/app/`

更新APT
```shell
$ sudo apt update
```

安裝pip
```shell
$ sudo apt install python3-pip
```

安裝虛擬環境
```shell
$ pip3 install pipenv
```

在使用`pip`安裝`mysqlclient`時要**根據**版本來下載相關的Ubuntu套件，預設版本為[mysqlclient 2.0.1](https://pypi.org/project/mysqlclient/2.0.1/)
```shell
$ apt-get install python3-dev default-libmysqlclient-dev build-essential
```

### MySQL 8.0
安裝教學：[網址](https://leadingtides.com/article/%E6%95%99%E5%AD%B8-%E5%A6%82%E4%BD%95%E5%9C%A8-Ubuntu-18.04-%E5%AE%89%E8%A3%9D-MySQL-8.0)

登入MySQL
```shell
$ mysql -u <USER> -p
```

建立資料庫
```sql
CREATE DATABASE <DATABASE NAME> CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 靜態資源
```shell
$ python3 manage.py collectstatic
```

### Apache2
架站教學：[網址](https://chenuin.blogspot.com/2019/01/django-ubuntuapache2modwsgi-django.html)

安裝Apache套件
```shell
$ sudo apt install apache2 libapache2-mod-wsgi-py3
```

開機自動啟動Apache
```shell
$ sudo systemctl enable apache2
```

切換至Apache設定檔目錄
```shell
$ cd /etc/apache2/sites-available
```

新增`django.conf`並加入以下設定
```shell
$ vim django.conf
```

```
<VirtualHost *:80>
    DocumentRoot /var/app/<PROJECT>

    Alias /media /var/app/<PROJECT>/media
    <Directory /var/app/<PROJECT>/media>
        Require all granted
    </Directory>

    Alias /static /var/app/<PROJECT>/static
    <Directory /var/app/<PROJECT>/static>
        Require all granted
    </Directory>

    <Directory /var/app/<PROJECT>/core>
        <Files wsgi.py>
            Require all granted
        </Files>
    </Directory>

    WSGIDaemonProcess core python-path=/var/app/<PROJECT> python-home=/var/app/<PROJECT>/env
    WSGIProcessGroup core
    WSGIScriptAlias / /var/app/<PROJECT>/core/wsgi.py

</VirtualHost>
```
> 使用vi/Vim取代：`:%s/<SEARCH_FROM>/<REPLACE_TO>/g`

設定權限(才能上傳檔案/圖片)
```shell
chown -R www-data /var/app/<PROJECT>
```

啟用自訂設定 & 關閉預設設定
```shell
$ sudo a2ensite django.conf
$ sudo a2dissite 000-default.conf
$ sudo service apache2 reload
```

#### Django Rest Framework JWT
至`/etc/apache2/sites-available/django.conf`新增下列設定
```shell
<VirtualHost *:80>
    ...
    WSGIPassAuthorization On
</VirtualHost>
```

### 部署完成:)
http://localhost:80/