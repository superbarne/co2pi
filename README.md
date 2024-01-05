# co2pi

``` bash
python -m venv venv
source ./venv/bin/activate
# python -m pip <pkg>
python -m pip install -r requirements.txt
```


https://peps.python.org/pep-0008/


```/etc/rc.local```

``` bash
sudo bash -c '/home/barne/src/co2pi/venv/bin/python /home/barne/src/co2pi/main.py > /home/barne/src/co2pi/co2pi.log 2>&1' &
```