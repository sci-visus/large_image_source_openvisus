
# Digital Slide Archive

Links:
- https://github.com/DigitalSlideArchive/digital_slide_archive/tree/master/devops/minimal
- https://github.com/girder/large_image
- https://github.com/DigitalSlideArchive/HistomicsUI

Notes:
- the minimal version (vs dsa version) does NOT support tasks and workers


```bash
cd Docker

# change the large_image_source_openvisus version as needed

docker-compose build
```

Clean all the stuff

```bash
docker-compose down --volumes
docker container prune

docker stop $(docker ps -a -q)
docker volume rm $(docker volume ls -q)
```

If you want to debug inside the container

```bash

# start mongodb in background
docker-compose up -d mongodb

# so I can attach using VS COde
docker compose run -d --entrypoint="sleep 999999999999" girder 

# **Attach in VS Code `Attach to running container`**

# this may be slow the first time
python /provision.py --sample-data --slicer-cli-image= 

# serve
girder serve --database mongodb://mongodb:27017/girder

# in a split window check logs
tail -f ./.girder/logs/*.log 
```

Use the browser:

- http://localhost:8080  DO NOT USE 0.0.0.0  since it does NOT work in WSL2
- USERNAME `admin` 
- PASSWORD `password`

To Add a local datasets:
- remember to mount the datasets in `docker-compose.yml`
- go to `Admin Console/AssetsStore` 
- click `Import Data`:
- `Destination ID` select `Samples/Images`
- `Import Path` specify an existing file inside the filesystem

To add S3 datasets:
- go to `Admin Console/AssetsStore` 
- Create an S3 assetstore
  - Assetstore Name=`my_s3_assetstore`
  - S3 bucket name `test-girder` (the bucket must pre-exists; or do `aws --profile wasabi s3 mb s3://<bucket-name-here>`)
  - Prefix `empty` (or check SealStorage prefix)
  - Access Key `XXXXX`
  - Secret Access Key `YYYYY`
  - Service `s3.us-west-1.wasabisys.com`
  - Region `us-west-1`
- *You may import a specific directory of keys within the bucket, or a specific key by path* 
  - *If you wish to import the entire bucket into the selected destination, simply leave the import path field blank*
  - *If you specify a directory, it will be imported recursively.*


In production:

```bash
# NOTE: it could take several runs (and CTRL+C) to make it working on WSL2
docker-compose up
```

# MongoDB

# Attach to mongodb


```bash


mongosh
show dbs
use girder
show collections
db.assetstore.find()
db.file.find()
```