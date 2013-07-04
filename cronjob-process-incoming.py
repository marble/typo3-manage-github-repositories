#! /usr/bin/python
# coding: ascii

# process-incoming-documentation-projects, mb, 2013-07-03, 2013-07-04

import os
import sys
import shutil
import subprocess
import codecs
import re
import time

try:
    from collections import OrderedDict as MyDict
except ImportError:
    MyDict = dict

HOME_DIR = '/home/mbless'
CRON_REBUILD_INCLUDED_FILE = '/home/mbless/HTDOCS/git.typo3.org/Documentation/cron_rebuild_included.sh'
KNOWN_GITHUB_MANUALS_FILE  = '/home/mbless/public_html/services/known-github-manuals.txt'
ROOT_OF_GITHUB_COM_PROJECTS = '/home/mbless/HTDOCS/github.com/'
FNAME_INFILE = 'incoming-NOT_VERSIONED.txt'
LOGFILE = 'logfile-NOT_VERSIONED.txt'
MAKEFOLDER_TEMPLATES = 'makefolder-templates'
LASTRUN = 'last-run-NOT_VERSIONED.txt'
MAIN_SEMAPHORE = '/home/mbless/HTDOCS/git.typo3.org/Documentation/REBUILD_REQUESTED'
KEYS = {
    '1': 'person',
    '2': 'githubuser',
    '3': 'repositoryurl',
    '4': 'masterdocurl',
    '5': 'publishurl',
    '6': 'status'
}

ospe = os.path.exists
ospj = os.path.join
NL = '\n'

def install_github_project(params):
    go = True
    if go and ospe(params['t3RepositoryDir']):
        print '%s/%s: t3RepositoryDir already exists' % (params['user'], params['repository'])
        go = False
    if go and ospe(params['t3MakeDir']):
        print '%s/%s: t3MakeDir already exists' % (params['user'], params['repository'])
        go = False
    if go:
        if not ospe(HOME_DIR):
            print '%s/%s: not on server' % (params['user'], params['repository'])
        else:
            shutil.copytree(MAKEFOLDER_TEMPLATES, params['t3MakeDir'])
            for fname in os.listdir(params['t3MakeDir']):
                fpath = ospj(params['t3MakeDir'], fname)
                if os.path.isfile(fpath):
                    f1 = file(fpath)
                    data = f1.read()
                    f1.close()
                    for k, v in params.items():
                        data = data.replace('###%s###' % k, v)
                    f2 = file(fpath, "w")
                    f2.write(data)
                    f2.close()
            if 1:
                # Add to cron processing
                f2 = file(CRON_REBUILD_INCLUDED_FILE, 'a')
                f2.write(params['file_cron_rebuild_sh'] + NL)
                f2.close()

            if 1:
                # Add to list of know github hooks
                f2 = file(KNOWN_GITHUB_MANUALS_FILE, 'a')
                f2.write('%s,%s\n' % (params['repositoryurl'].rstrip('/'), params['request_rebuild_url']))
                f2.close()

            if 1:
                # initiate build right away
                f2 = file(MAIN_SEMAPHORE, 'w')
                f2.close()

            msg = '%s/%s: installed' % (params['user'], params['repository'])

            if 1:
                # let that message appear on mail sent by cronjob
                print msg
                
            if 1:
                # Add line to logfile
                f2 = file(LOGFILE, 'a')
                f2.write('%s\n' % msg)
                f2.close()
                
       

def process_entry(dataset):
    params = {}
    D = {}

    for k, v in dataset.items():
        params[k] = v

    # check for Github entries
    pattern = (
        'https://github\.com/'
        '(?P<user>.+?)/'
        '(?P<repository>.+?)/'
        '(?P<githubrelpath>tree/master|blob/master)'
        '(?P<reporelpath>.*)/'
        '(?P<masterdoc>.+\.rst)'
        )
    m = re.match(pattern, dataset['masterdocurl'])
    if m:
        D = m.groupdict()
        D['reporelpath'] = D['reporelpath'].strip('/')
        params['user']          = D['user']
        params['repository']    = D['repository']
        params['githubrelpath'] = D['githubrelpath']
        params['reporelpath']   = D['reporelpath']
        params['masterdoc']     = D['masterdoc']

        s = dataset['publishurl']
        s.split('/drafts/github/', 1)
        
        # given:
        #   https://github.com/user/Project/tree/master/Documentation/Index.rst
        #   https://github.com/netresearch/t3x-contexts_geolocation/blob/master/README.rst
        # needed:
        #   t3DocTeam['relpath_to_master_doc'] = '../Project.git/Documentation/'

        relpath_to_master_doc = ospj('..', D['repository'] + '.git', D['reporelpath'])
        relpath_to_master_doc = relpath_to_master_doc.replace('\\', '/')
        params['relpath_to_master_doc'] = relpath_to_master_doc
        # print 'relpath_to_master_doc=%s' % params['relpath_to_master_doc']

        # 1: Martin Holtz
        # 2: maholtz
        # 3: https://github.com/maholtz/Typoscript/
        # 4: https://github.com/maholtz/Typoscript/tree/master/Documentation/Index.rst
        # 5: http://docs.typo3.org/typo3cms/drafts/github/maholtz/Typoscript/
        # 6: ACTIVE

        # t3BuildDir=/home/mbless/public_html/typo3cms/drafts/github/maholtz/Typoscript
        # t3RepositoryDir=/home/mbless/HTDOCS/github.com/maholtz/Typoscript.git
        # t3RepositoryUrl=https://github.com/maholtz/Typoscript
        # t3DocumentationDir=$t3RepositoryDir/Documentation
        # t3MakeDir=/home/mbless/HTDOCS/github.com/maholtz/Typoscript.git.make

        # t3BuildDir
        # t3BuildDir=/home/mbless/public_html/typo3cms/drafts/github/maholtz/Typoscript
        temp = dataset['publishurl'].split('http://docs.typo3.org/',1)
        if len(temp) == 2:
            t3BuildDir = ('/home/mbless/public_html/' + temp[1]).rstrip('/')
        else:
            t3BuildDir = ''
        params['t3BuildDir'] = t3BuildDir
        # print 't3BuildDir=%s' % params['t3BuildDir']
            

        # t3RepositoryDir
        # t3RepositoryDir=/home/mbless/HTDOCS/github.com/maholtz/Typoscript.git
        temp = dataset['repositoryurl'].split('https://github.com/',1)
        if len(temp) == 2:
            t3RepositoryDir = (ROOT_OF_GITHUB_COM_PROJECTS + temp[1]).rstrip('/') + '.git'
        else:
            t3RepositoryDir = ''
        params['t3RepositoryDir'] = t3RepositoryDir
        # print 't3RepositoryDir=%s' % params['t3RepositoryDir']

        # t3RepositoryUrl
        # t3RepositoryUrl=https://github.com/maholtz/Typoscript
        t3RepositoryUrl = dataset['repositoryurl'].rstrip('/')
        params['t3RepositoryUrl'] = t3RepositoryUrl
        # print 't3RepositoryUrl=%s' % params['t3RepositoryUrl']

        # t3DocumentationDir
        # t3DocumentationDir=/home/mbless/HTDOCS/github.com/maholtz/Typoscript.git/Documentation
        if D['reporelpath']:
            t3DocumentationDir = t3RepositoryDir + '/' + D['reporelpath']
        else:
            t3DocumentationDir = t3RepositoryDir
        params['t3DocumentationDir'] = t3DocumentationDir
        # print 't3DocumentationDir=%s' % params['t3DocumentationDir']

        # t3MakeDir
        # t3MakeDir=/home/mbless/HTDOCS/github.com/maholtz/Typoscript.git.make
        t3MakeDir = t3RepositoryDir + '.make'
        params['t3MakeDir'] = t3MakeDir
        # print 't3MakeDir=%s' % params['t3MakeDir']

        # T3DOCDIR
        # T3DOCDIR = /home/mbless/HTDOCS/github.com/maholtz/Typoscript.git/Documentation
        params['T3DOCDIR'] = params['t3DocumentationDir']
        # print 'T3DOCDIR=%s' % params['T3DOCDIR']

        # BUILDDIR
        # BUILDDIR = /home/mbless/public_html/typo3cms/drafts/github/maholtz/Typoscript
        params['BUILDDIR'] = params['t3BuildDir']
        # print 'BUILDDIR=%s' % params['BUILDDIR']

        params['file_cron_rebuild_sh'] = params['t3MakeDir'] + '/cron_rebuild.sh'
        params['request_rebuild_url']  = params['t3MakeDir'].replace('/home/mbless/HTDOCS/', 'http://docs.typo3.org/~mbless/') + '/request_rebuild.php'
            
        # print

        complete = True
        for k,v in params.items():
            if not v:
                complete = False
                break
            
        if complete:
            install_github_project(params)
            
       

    # handle Non-Github-entry ...
    pattern = (
        'https://SOME_OTHER_DOMAIN\.com/'
        '(?P<user>.+?)/'
        '(?P<repository>.+?)/'
        '(?P<githubrelpath>tree/master|blob/master)'
        '(?P<reporelpath>.*)/'
        '(?P<masterdoc>.+\.rst)'
        )
    m = re.match(pattern, dataset['masterdocurl'])
    if m:
        pass

    return
        

def handle_skipped_lines(L):
    pass

def process_infile(f1name):
    if not ospe(f1name):
        f2 = file(f1name, 'w')
        f2.close()
    f1 = codecs.open(f1name, 'r', 'utf-8', 'xmlcharrefreplace')
    dataset = {}
    linebuf = []
    skipping = False
    for line in f1:
        linebuf.append(line)
        line = line.strip()
        if line:
            i, v = line.split(':', 1)
            if not i in ['1','2','3','4','5','6']:
                skipping = True
                continue
            if i == '1':
                if skipping or (dataset and len(dataset) != len(KEYS)):
                    # throw away these line
                    dataset = {}
                    handle_skipped_lines(linebuf[:-1])
                    del linebuf[:-1]
                    skipping = False
                elif dataset:
                    process_entry(dataset)
                    dataset = {}
            k = KEYS[i]
            if dataset.has_key(k):
                skipping = True
            else:
                dataset[k] = v.strip()
    else:
        if skipping or (dataset and len(dataset) != len(KEYS)):
            dataset = {}
            handle_skipped_lines(linebuf[:-1])
            del linebuf[:-1]
            skipping = False
        elif dataset:
            process_entry(dataset)
            dataset = {}
    
 

if 1 and __name__=="__main__":
    if 1:
        # touch file LASTRUN
        f2 = file(LASTRUN, 'w')
        f2.write(str(time.time()))
        f2.close()
    process_infile(FNAME_INFILE)
