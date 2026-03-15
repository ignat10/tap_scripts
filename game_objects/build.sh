#!/bin/bash

set -e

cd game_objects

maturin develop


SITE_PACKAGES=$(python -c "
import site;
print(site.getsitepackages()[0])
")

cp game_objects.pyi "$SITE_PACKAGES/game_objects"
