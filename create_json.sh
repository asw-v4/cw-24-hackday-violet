#!/bin/bash -x

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
  [ ! -f $DATA_DIR/${REPO_FILENAME}.json ] && scorecard --repo=$REPO --checks=Maintained,Packaging --format=json >$DATA_DIR/${REPO_FILENAME}.json
  REPO_ARGS="$REPO_ARGS $DATA_DIR/${REPO_FILENAME}.json"
done

python src/data/gh_retrieve.py $REPO_ARGS >$DATA_DIR/github.json

python src/data/combine_metrics.py $DATA_DIR/github.json $REPO_ARGS >$DATA_DIR/ui.json
