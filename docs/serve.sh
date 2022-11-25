#!/bin/bash

docker run --rm \
  --volume="$PWD:/srv/jekyll" \
  -it -p 4000:4000 jekyll/jekyll \
  jekyll serve -I -V \
  --config "_config.yml,_config_dev.yml"