#! /usr/bin/python

# coding: ascii
# process-the-list, mb, 2013-03-25, 2013-03-25

import os
import sys
import shutil
try:
    from collections import OrderedDict as MyDict
except ImportError:
    MyDict = dict
ospe = os.path.exists
ospj = os.path.join

def construct(github_manual):

    github_user = github_manual[0].strip()
    github_repository_name = github_manual[1].strip()
    manual_name_for_url= github_manual[2].strip()
    url_start = github_manual[3].strip()

    d = MyDict()
    d['github_user'] = github_user
    d['github_repository_name'] = github_repository_name
    d['manual_name_for_url'] = manual_name_for_url
    d['url_start'] = url_start

    d['known_hosters'] = ['git.typo3.org', 'github.ocm']
    d['repository_hoster'] = 'github.com'
    d['documentation_folder_in_repository'] = 'Documentation'

    d['webroot_of_cloned_repositories'] = '/home/mbless/HTDOCS'
    d['webroot_of_cloned_github_repositories'] = '/home/mbless/HTDOCS/github.com'
    d['webroot_of_cloned_typo3_repositories'] = '/home/mbless/HTDOCS/git.typo3.org'
    d['webroot_of_docs_typo3_org'] = '/home/mbless/public_html'

    d['baseurl_of_cloned_repositories'] = 'http://docs.typo3.org/~mbless/'
    d['baseurl_of_cloned_github_repositories'] = 'http://docs.typo3.org/~mbless/github.com/'
    d['baseurl_of_cloned_typo3_repositories'] = 'http://docs.typo3.org/~mbless/git.typo3.org/'
    d['baseurl_of_docs_typo3_org'] = 'http://docs.typo3.org/'

    d['github_url'] = 'https://github.com'
    d['github_make_folder_template'] = '/home/mbless/HTDOCS/github.com/make-folder-template'
  
    if d['repository_hoster'] == 'github.com':
        d['clone_source'] = d['github_url'] + '/' + d['github_user'] + '/' + d['github_repository_name']
        d['clone_destination'] = d['webroot_of_cloned_github_repositories'] + '/' + d['github_user'] + '/' + d['github_repository_name'] + '.git'
        d['make_folder_destination'] = d['clone_destination'] + '.make'
        d['clone_cmd'] = 'git clone ' + d['clone_source'] + ' ' + d['clone_destination']
        d['copy_make_cmd'] = 'cp -rp ' + d['github_make_folder_template'] + ' ' + d['make_folder_destination']
        d['file_conf_py'] = d['make_folder_destination'] + '/conf.py'
        d['file_makefile'] = d['make_folder_destination'] + '/Makefile'
        d['file_cron_rebuild_sh'] = d['make_folder_destination'] + '/cron_rebuild.sh'

        d['replacements'] = []
        d['replacements'].append(('GITHUB_USER', d['github_user']))
        d['replacements'].append(('REPOSITORY_NAME', d['github_repository_name']))
        d['replacements'].append(('URL_START', d['url_start']))
        d['replacements'].append(('MANUAL_NAME_FOR_URL', d['manual_name_for_url']))

    return d

def process_csv_list(csvfile):
    for lineno, line in enumerate(file(csvfile)):
        line = line.strip()
        if not line:
            continue
        github_manual = line.split(',')
        if not len(github_manual) == 4:
            print "Error: 4 values expected in line:", line
            print
            sys.exit(1)

            
        if lineno:
            d = construct(github_manual)
            if not 'dummy' in d['github_repository_name']:
                continue
            print d['clone_destination'] + ',',
            if ospe(d['clone_destination']):
                print 'exists',
            else:
                print 'to be created',
            print
            if 0:
                print d['clone_cmd']
            if 1:
                if ospe(d['github_make_folder_template']):
                    shutil.copytree(d['github_make_folder_template'], d['make_folder_destination'])




if 1 and __name__=="__main__":

    process_csv_list('list-of-github-manuals.csv')
