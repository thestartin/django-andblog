#!/usr/bin/env bash

DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
MINI_DIR="$DIR/../../django_andblog/scripts/"

cd $MINI_DIR
sh compress_css_js.sh

