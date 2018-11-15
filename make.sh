#!/usr/bin/env bash

# print a trace of simple commands
set -x

# prepare for PyPI distribution
rm -rf build 2> /dev/null
mkdir eggs \
      sdist \
      wheels 2> /dev/null
mv -f dist/*.egg eggs/ 2> /dev/null
mv -f dist/*.whl wheels/ 2> /dev/null
mv -f dist/*.tar.gz sdist/ 2> /dev/null

python3 setup.py sdist bdist_wheel
file=$( ls dist/*.tar.gz )
name=${file%*.tar.gz*}
mv dist/*.whl "${name}-py3-none-macosx_10_14_x86_64.whl"
twine upload dist/* -r pypi --skip-existing
twine upload dist/* -r pypitest --skip-existing

git pull
ret="$?"
if [[ $ret -ne "0" ]] ; then
    exit $ret
fi
git add .
if [[ -z "$1" ]] ; then
    git commit -a -S
else
    git commit -a -S -m "$1"
fi
git push
