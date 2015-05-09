#!/usr/bin/env bash

DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
CSS_DIR="$DIR/../assets/css"
JS_DIR="$DIR/../assets/js"

cd $CSS_DIR
for i in main.css pure.css
do
  echo "Creating minified CSS for $i"
  java -jar ~/yuicompressor/yuicompressor-2.4.8.jar --type css -o "min.$i" "$i"
done

cd $JS_DIR
for i in main.js plugins.js
do
  echo "Creating minified JS for $i"
  java -jar ~/yuicompressor/yuicompressor-2.4.8.jar --type js -o "min.$i" "$i"
done

echo "Done!"
