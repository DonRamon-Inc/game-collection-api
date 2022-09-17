#! /bin/sh

DISABLED_RULES=C0114,C0115,C0116,E1101,R0902
DISABLED_TEST_RULES=W0621,W0212

pytest --ignore=lib --ignore=lib64 && pylint $(git ls-files '*.py') --disable=$DISABLED_RULES,$DISABLED_TEST_RULES
