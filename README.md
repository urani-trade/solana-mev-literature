# Crypto Search Portal



----

# Project Structure

This project has the following structure:

* The point of entry is in the main app named `main`. That's where `settings.py` and (root) `urls.py` files are.

* There are three other apps: `accounts`(handling login), `core` (containing extra commands for `manage.py`), and `implementations` (contain all the search structures, and 
data models for the app).

* HTML pages are inside `templates` (including CSS `style`). Static files are served by
AWS S3 ([this bucket](https://image-arxiv.s3.amazonaws.com)). See [this document to see how we deploy](https://www.notion.so/How-to-upload-static-files-to-AWS-5d0720d7d21f4cc4a313016e3c61262e).



----

# Local Development

## Setting it up

Create a virtual environment (in the root of the project):

```bash
virtualenv venv
source venv/bin/activate
```

Install with:

```bash
make install
```

## Setting Environment Variables

Create an enviroment files and add the database information (e.g. host URL, username, password):

```bash
cp .env_example .env
vim .env
```

## Running 

Run server locally by setting `DEBUG=True`  in  `settings.py` and running:

```bash
make run
```

You should be able to open on `localhost:8000`.


## Testing

Tests for each Django sub-app can be found in the app's directory. Run all the tests with:

```bash
make test
```

To lint the code according to Pythons PEP8:

```bash
make lint
```

## Troubleshooting 

#### Bad Request (400)
If you get a "Bad Request (400)" in the browser, you need to set `DEBUG = True` in `settings.py.

#### 500 HTTP Errors
If you get a 500-error and need to debug it locally, run:

```bash
now dev
```



----

# Deployment to Staging

We use [now](https://zeit.co/) to deploy our NISQ Alg Zoo app. It can install it with `npm`, as described [here](https://zeit.co/download).

A staging deployment can be triggered with:

```bash
make staging
```

Make sure that `settings.py` has set `DEBUG=False`. Our staging URL at [https://nisqalgzoo-steinkirch.wearequantum.now.sh](https://nisqalgzoo-steinkirch.wearequantum.now.sh/).

You can deploy in staging as often as you want, this will not affect the main website. 

More information on how we deploy to staging is available [here](https://www.notion.so/Deploying-to-Dev-and-Staging-68d503cf16884d7885c23c7fc17cea45).

---


# Deployment to Production

Any new code that is merged to master should be deployed to production with:

```bash
make prod
```

More information on how we deploy to staging is available [here](https://www.notion.so/Deploying-to-Production-9890f03cc42141cbb9c74ad2e3857e96). 


### Static Files

Our static files are served by an S3 bucket named [image-arxiv](https://image-arxiv.s3.amazonaws.com).
Information on how we serve static files is available [here](https://www.notion.so/How-to-upload-static-files-to-AWS-5d0720d7d21f4cc4a313016e3c61262e). 

---

# Handling the Database

NISQ Algorithm Zoo data is held in an [AWS PostgresSQL](https://aws.amazon.com/rds/postgresql/) database cluster.


## Installing Postgres Locally

If you are a macOS user, you can run:

```bash
brew install postgresql
```

Make sure you are running a version 12+:

```bash
postgres -V
```

Start the connection with:

```bash
pg_ctl -D /usr/local/var/postgres start && brew services start postgresql
```

## Monitoring the Database

The database monitoring dashboard can be found [here](https://console.aws.amazon.com/cloudwatch/home?ad=c&cp=bn&p=clw&region=us-east-1#cw:dashboard=RDS). 

All the logs for database operation can be found [here](https://console.aws.amazon.com/cloudwatch/home?region=us-east-1#logEventViewer:group=/aws/rds/instance/nisq-alg-zoo-prod/postgresql;stream=nisq-alg-zoo-prod.0;start=2020-03-11T04:06:42Z).

Database monitorning alerts are set with SNS to be sent to our emails. This can be set or edited in [this](https://console.aws.amazon.com/sns/v3/home?region=us-east-1#/topic/arn:aws:sns:us-east-1:544586890207:Default_CloudWatch_Alarms_Topic).



## Our AWS Postgres Database Cluster

Our production database instance is named [nisq-alg-zoo-prod](https://console.aws.amazon.com/rds/home?ad=c&cp=bn&p=rds&region=us-east-1#database:id=nisq-alg-zoo-prod;is-cluster=false).

To access the AWS database instance from the CLI, run:

```
psql --host=<HOST URL> --port=5115 --username=postgres --password --dbname=postgres

```

You can also use a GUI. If you are in MacOS, the best option is [postico](https://eggerapps.at/postico/).
If you are in Linux, [here are some options](https://wiki.postgresql.org/wiki/PostgreSQL_Clients#Cross-platform_GUI_Clients). Instructions to connect to the database via GUI can be found at [this document](https://www.notion.so/Database-8d939e1bafa949ad82fb7965dc0483e7).




## Troubleshooting

#### Operation Timeout on Trying to Connect

If you get a `timeout error` when trying to connect to the database instance from your machine (either through the terminal or through the GUI), you need to add your IP CIDR to the 
database instance inbound rule in AWS. You will need RDS admin permission for this.

On the other hand, to check whether this is a problem, you can try to netcat to the instance with:

```bash
nc -zv  nisq-alg-zoo-<db url name>.us-east-1.rds.amazonaws.com 5115
```

See more details [here](https://aws.amazon.com/premiumsupport/knowledge-center/rds-cannot-connect/).

Note, in the future, we should have a custom VPN set to avoid this problem.


## Migration notes

Below are some notes on how we migrated from SQLite to Postgres. This can be useful anytime we change `models.py`, or we perform any local backup (not recomme ded), or we do another migration.

#### Populating the Database Schema Locally

If you are re-creating the database or changing its model, you might need to migrate the data and then populate with our `implementations` tables. This can be achieved with:


```bash
make populate

[*] Starting populate script...
[*] Populated algorithms: {'Scrambling', 'QKD', 'Verification', 'DJ', 'HS', 'QEC', 'Simon', 'QAQC', 'QPE', 'Qubit', 'SVM', 'Benchmark', 'Gates', 'Order finding', 'QITE', 'VQA', 'Mermin inequalties', 'Shor', 'VQSD', 'Sim', 'VQE', 'QML', 'Grover', 'QFT', 'Multiple', 'Q. Walk', 'S.O.', 'Sim.', 'QSE', 'Entanglement', 'VQLS', 'BV', 'QLanczos'}
[*] Populated computers: {'Rigetti Aspen', 'IBMQX4', 'Rigetti 19Q-Acorn', 'IBMQX5', 'IBMQ20', 'IBMQ20 (Tokyo)', 'IBMQX2', 'Rigetti 8Q-Agave', 'IBMQX3', 'IBMQ 16', 'IBMQ16', 'IBM Q Tenerife', 'IBMQX1', 'Rigetti Aspen QPU', 'IonQ', 'IBM Q Experience', 'IBMQX14', 'IBMQ Tokyo', 'IBM Q 16 Melbourne', 'IBM Q Poughkeepsie', 'IBMQ', 'Trimon', 'IBMQ Poughkeepsie'}
[*] Populated Qubit Type: {'Photon', 'NMR', 'Linear optics', 'Trapped ion', 'Photonic', 'NV Center', 'Ion trap', 'Superconducting', 'atom', 'Neutral atom'}
[*] Populated Qubit subtypes: {'171Yb+', '40Ca+', '9Be+', '111Cd+'}
[*] Data imported successfully
```

and

```bash
make populate_imp:
```

And then:

```bash
make migrate
```

and

```bash
make migrations
```

#### Populating the Data Locally

A backup can be imported using the following command:

```bash
python manage.py loaddata db_backup[timestamp].json
```

Help for loaddata/dumpdata can be found at [this link](https://coderwall.com/p/mvsoyg/django-dumpdata-and-loaddata). The official Django documentation is also helpful.




