# Set up

How to set up your machine for this project


## Versions

Install [`conda`](https://docs.conda.io/projects/conda/en/latest/user-guide/install/linux.html) 

you will need both node and python:
- install python version 3.9.15
- install node version 18.12.1

you can use [`nvm`](https://github.com/nvm-sh/nvm) to maintain multiple versions of node

The UI packs used are:
- daisy UI with tailwind

framwork used with django is [`Django rest framework`](https://www.django-rest-framework.org/)


## Set up


### Front end

Once all packages are installed we will test run the frontend
```bash
# cd into the frontend file
cd frontend

# install packages using package.json
npm install

# test if it all works
npm run dev
```
By connecting to `http://localhost:5173/` (the default port) you should see the front page of the website

### Back end

#### Install Django and other dependencies

First connect yourself to the created virtual env
```bash
conda activate #your env name

# You should see in the terminal the env name

# Let's make sure that you've installed the right python version

python --version
# This should return
# python 3.9.15

```

Once you are in your env let's install all the required packages

```bash
# while being in the base repository run this commande to isntall the python packages
pip install -r requirements.txt

```

#### Set up database

This project uses a [`postgresql`](https://www.postgresql.org/) database

Install psotgresql and check if it is running correctly

```bash
systemctl status postgresql
```

Once postgresql is running we need to create a user and database with the user having permissions other that db

Connect to postgresql  
```bash
psql -h localhost -U postgres

```

Create a new role or use current one
```sql
CREATE ROLE newuser WITH LOGIN PASSWORD 'password';
```

Next, you can create a new database using the CREATE DATABASE SQL command:
```sql
CREATE DATABASE mydatabase;
```

After creating the database, you can grant all privileges on this database to your role using the GRANT SQL command:
```sql
GRANT ALL PRIVILEGES ON DATABASE mydatabase TO myrole;
```

After running these commands, the role "myrole" will have full admin access to the "mydatabase" database.


Once the data is created you need to connect it to the django project.
Inside the crypto_ledger folder there is a settings.py file taht holds our connection to the postgres database

```python

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',  
        'NAME': 'crypto_ledger', 
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

```

Change the name,user and password based on what you set these values in your postgresql local server.

##### Now all that's left is to migrate and test.

cd to the django project directory
```bash
cd crypto_ledger
```


Apply Migrations: Django uses migrations to apply changes to your database schema. You'll need to run the following command to apply existing migrations:
```bash
python manage.py migrate
```

Start the Development Server: Django comes with a built-in development server. You can start this with the following command:
```bash
python manage.py runserver
```

Finally create a super user to acces the django admin pannel
```bash
python manage.py createsuperuser
```

Once all this is done run the server and test it
```bash
python manage.py runserver 9000
```

Connect yourself to the django admin panel
`http://localhost:9000/admin/`

Run the svelte frontend in a seperate terminal and you w=should be able to login via the svelte front end
