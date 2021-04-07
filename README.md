urlShortener
-------

A Django URL Shortener based on python [urlCutter](https://github.com/kostyaMosin/urlCutter).

It uses a bit-shuffling approach is used to avoid generating consecutive, predictable URLs. However, the algorithm is deterministic and will guarantee that no collisions will occur.


Setup
-----

````
git clone https://github.com/kostyaMosin/urlCutter.git
cd urlCutter
virtualenv -p python3 env
source env/bin/activate
pip install -r requirements.txt
````

First run
---

````
cd urlCutter
python manage.py migrate
python manage.py createsuperuser 
````


Run
---

It will listen on :8000
````
python manage.py runserver
````


Author
------

Kostya Mosin <kostyaMosin93@gmail.com>

References
----------

- First accreditation project at the school of programming [TeachMeSkills](https://teachmeskills.by/)
