#!/bin/bash

REPO_FILE=${1}

if [ ! -f "$REPO_FILE" ]; then
  echo "No file, bad argument"
  exit 1
fi

DATA_DIR=temp_data
mkdir $DATA_DIR

REPO_ARGS=""
for REPO in $( cat $REPO_FILE ); do
  REPO_FILENAME="${REPO##*/}"
  echo "Grabbing scorecard for $REPO"
  [ ! -f $DATA_DIR/${REPO_FILENAME}.json ] && scorecard --repo=$REPO --checks=Maintained,Packaging,Contributors,CI-Tests,Code-Review --format=json >$DATA_DIR/${REPO_FILENAME}.json
  echo "Grabbing fair assessment for $REPO"
  [ ! -f $DATA_DIR/${REPO_FILENAME}.fair.json ] && python src/data/fair_api.py $REPO >$DATA_DIR/${REPO_FILENAME}.fair.json
  REPO_ARGS="$REPO_ARGS $REPO"
  FILE_ARGS="$FILE_ARGS $DATA_DIR/${REPO_FILENAME}.json"
done

echo $REPO_ARGS
echo $FILE_ARGS
echo "Getting github data"
python src/data/gh_retrieve.py $REPO_ARGS >$DATA_DIR/github.json

echo "Combining data"
python src/data/combine_metrics.py $DATA_DIR/github.json $FILE_ARGS >$DATA_DIR/ui.json
