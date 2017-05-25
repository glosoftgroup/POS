Installation Process
--------------------
1. install below packages using npm:
                    - npm i webpack -g
                    - npm i yarn -g
      Note: Requires latest version of Node installed.
2. setup Postgres database with name, user & password = saleor or change to your liking.
3. create your django environment.
4. git clone https://github.com/mirumee/saleor.git
5. cd saleor/
6. pip install -r requirements.txt
         - some of the requirements raising issues include lxml==3.7.2 and uwsgi==2.0.14.
         - install process runs smoothely when the above packages are commented, but one can opt to install
           manually if need be.
7. set environment key: (a) linux - export SECRET_KEY = <mysecretkey>
            		(b) windows - set SECRET_KEY = <mysecretkey>
	 Note: Django will not run without the secret key in your environment.
8. prepare the database by running - python manage.py migrate (not python manage.py makemigrations at first installation).
9. build the front-end dependecies using yarn by: (a) linux - $ yarn
                                                  (b) windows - yarn
          Note: Yarn works like npm. It's a package manager. In this case install packages specified in the package.json file.
10. prepare front-end assets in yarn by : (a) linux - $ yarn run build-assets
                                          (b) windows - yarn run build-assets
11. run django project as : - python manage.py runserver
12. During first installation, the database products, sales, customers and orders table are empty. To simulate data in the app run
    the following command : - python manage.py populatedb
13. To access the dashboard, create a user through the registration form of the site and grant him/her priviledges in the database like is staff and is super user.