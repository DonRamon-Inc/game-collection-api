#! /bin/sh

GIT_DIR=$(git rev-parse --show-toplevel)
$GIT_DIR/scripts/pytest.sh && $GIT_DIR/scripts/pylint.sh
