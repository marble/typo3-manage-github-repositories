.. ==================================================
.. FOR YOUR INFORMATION
.. --------------------------------------------------
.. -*- coding: utf-8 -*- with BOM.  ÄÖÜäöüß

.. include:: ../Includes.txt


=================================
Step 3
=================================


Constructing paths
==================

.. code-block:: python

   def construct(github_manual):
       """Construct all kinds of needed string values"""
       
       github_user = github_manual[0].strip()
       github_repository_name = github_manual[1].strip()
       manual_name_for_url= github_manual[2].strip()
       url_start = github_manual[3].strip()
   
       # use an OrderedDict if possible
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
       d['cron_rebuild_included_file'] = '/home/mbless/HTDOCS/git.typo3.org/Documentation/cron_rebuild_included.sh'
       d['known-github-manuals-file']  = '/home/mbless/public_html/services/known-github-manuals.txt'
     
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
           d['request_rebuild_url'] = d['baseurl_of_cloned_github_repositories'] + d['github_user'] + '/' + d['github_repository_name'] + '.git.make/request_rebuild.php'
   
       return d
   