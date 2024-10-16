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

To Start Gunicorn:
Activate your virtual environment (if not already activated):

bash
复制代码
source /home/ec2-user/DATA-MARKETPLACE/venv/bin/activate
Start the Gunicorn service:

bash
复制代码
sudo systemctl start gunicorn
Check the status of Gunicorn to make sure it’s running:

bash
复制代码
sudo systemctl status gunicorn
To Stop Gunicorn:
Stop the Gunicorn service:

bash
复制代码
sudo systemctl stop gunicorn
Deactivate the virtual environment (if still active):

bash
复制代码
deactivate
Log out of your EC2 instance (optional, if you're finished working):

bash
复制代码
exit

