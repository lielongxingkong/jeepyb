#! /usr/bin/env python
# Copyright (c) 2013 Hewlett-Packard Development Company, L.P.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
#
# create_cgitrepos.py reads the project config file called projects.yaml
# and generates a cgitrepos configuration file which is then copied to
# the cgit server.
#
# It also creates the necessary top-level directories for each project
# organization (openstack, stackforge, etc)

import os
import yaml


PROJECTS_YAML = os.environ.get('PROJECTS_YAML',
                               '/home/cgit/projects.yaml')
CGIT_REPOS = os.environ.get('CGIT_REPOS',
                            '/etc/cgitrepos')
REPO_PATH = os.environ.get('REPO_PATH',
                           '/var/lib/git')


def main():
    (defaults, config) = tuple(yaml.safe_load_all(open(PROJECTS_YAML)))
    gitorgs = {}
    names = set()
    for entry in config:
        (org, name) = entry['project'].split('/')
        description = entry.get('description', name)
        assert name not in names
        names.add(name)
        gitorgs.setdefault(org, []).append((name, description))
    for org in gitorgs:
        if not os.path.isdir('%s/%s' % (REPO_PATH, org)):
            os.makedirs('%s/%s' % (REPO_PATH, org))
    with open(CGIT_REPOS, 'w') as cgit_file:
        cgit_file.write('# Autogenerated by create_cgitrepos.py\n')
        for org in sorted(gitorgs):
            cgit_file.write('\n')
            cgit_file.write('section=%s\n' % (org))
            projects = gitorgs[org]
            projects.sort()
            for (name, description) in projects:
                cgit_file.write('\n')
                cgit_file.write('repo.url=%s/%s\n' % (org, name))
                cgit_file.write('repo.path=%s/%s/%s.git/\n' % (REPO_PATH,
                                                               org, name))
                cgit_file.write('repo.desc=%s\n' % (description))


if __name__ == "__main__":
    main()