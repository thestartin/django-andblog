#!/usr/bin/env bash

DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
CSS_DIR="$DIR/../assets/css"
JS_DIR="$DIR/../assets/js"

cd $CSS_DIR
filename="min.all.css.gz"
[ -e $filename ] && rm "$filename"
filename="min.all.css"
[ -f $filename ] && rm "$filename"

for i in pure.css main.css
do
  echo "Creating minified CSS for $i"
  java -jar ~/yuicompressor/yuicompressor-2.4.8.jar --type css -o "min.$i" "$i"
  cat "min.$i" >> min.all.css
done

#echo "Gzipping min.all.css"
#gzip min.all.css

cd $JS_DIR
filename="min.all.js.gz"
[[ -e $filename ]] && rm "$filename"
filename="min.all.js"
[[ -f $filename ]] && rm "$filename"

for i in main.js plugins.js
do
  echo "Creating minified JS for $i"
  java -jar ~/yuicompressor/yuicompressor-2.4.8.jar --type js -o "min.$i" "$i"
  cat "min.$i" >> min.all.js
done

#echo "Gzipping min.all.js"
#gzip min.all.js

echo "Done!"
