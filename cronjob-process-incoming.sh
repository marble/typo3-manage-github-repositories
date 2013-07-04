#!/bin/bash

pushd /home/mbless/HTDOCS/github.com/marble/typo3-manage-github-repositories.git >/dev/null
python cronjob-process-incoming.py
popd >/dev/null