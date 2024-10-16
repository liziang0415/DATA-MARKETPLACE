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


**Server Side**
Start the Gunicorn service:

```aws
sudo systemctl start gunicorn
sudo systemctl status gunicorn
sudo systemctl restart gunicorn
````
End the Gunicorn service:

```aws
sudo systemctl stop gunicorn
````


bash
复制代码
exit

