#!/bin/bash

t3BuildDir=###t3BuildDir###
t3RepositoryDir=###t3RepositoryDir###
t3RepositoryUrl=###t3RepositoryUrl###
t3DocumentationDir=###t3DocumentationDir###
t3MakeDir=###t3MakeDir###

pushd $t3MakeDir

# touch REBUILD_REQUESTED

if [ -r "REBUILD_REQUESTED" ]; then
    if [ ! -r $t3RepositoryDir ]; then
        git clone $t3RepositoryUrl $t3RepositoryDir
    fi
    cd $t3RepositoryDir
    git fetch
    git checkout master
    git pull
    git status
    if [ ! -r "$t3RepositoryDir/Documentation/Index.rst" ] && [ -r "$t3RepositoryDir/README.rst" ]; then
        t3DocumentationDir=$t3RepositoryDir
    fi
    cd $t3MakeDir
    make clean
    # make gettext
    # make json
    make singlehtml
    # make dirhtml
    make html
    ln -s $t3MakeDir $t3BuildDir/_make
    pushd $t3BuildDir >/dev/null
    if [ ! -r Index.html ] && [ -r README.html ]; then
        ln -s README.html Index.html
    fi
    popd >/dev/null
    rm -I REBUILD_REQUESTED
fi

echo "t3BuildDir        : $t3BuildDir"          > dirs-of-last-build.txt
echo "t3RepositoryDir   : $t3RepositoryDir"     >>dirs-of-last-build.txt
echo "t3RepositoryUrl   : $t3RepositoryUrl"     >>dirs-of-last-build.txt
echo "t3DocumentationDir: $t3DocumentationDir"  >>dirs-of-last-build.txt
echo "t3MakeDir         : $t3MakeDir"           >>dirs-of-last-build.txt

popd
