**Installation via requirements.txt**

**Windows**
```shell
 cd <project directory>
 py -3 -m venv venv
 venv\Scripts\activate
 pip install -r requirements.txt
```

**MacOS**
```shell
 cd <project directory>
 python3 -m venv venv
 source venv/bin/activate
 pip install -r requirements.txt
```

After That


````shell
$ flask run
````


Server Side:

sudo yum install python3-pip -y
sudo yum install git -y
sudo pip3 install gunicorn
git clone -b Test-Final https://github.com/liziang0415/DATA-MARKETPLACE.git
sudo pip install -r requirements.txt

sudo gunicorn --workers 3 --bind 0.0.0.0:80 wsgi:app



