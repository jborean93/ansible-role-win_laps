#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2018, Jordan Borean
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = r'''
---
module: win_gpo_link
short_description: Manages Group Policy Object links.
description:
- Used to link or unlink a Group Policy OBject to an Organizational Unit.
options:
  name:
    description:
    - The name of the GPO to link to.
    required: True
    type: str
  state:
    description:
    - When C(state=absent), will remove the link if it exists.
    - When C(state=present), will create a link.
    choices:
    - absent
    - present
    default: present
    type: str
  enforced:
    description:
    - Will set the GPO link to be enforced in the OU.
    type: bool
  enabled:
    description:
    - Will set the GPO link to be enabled in the OU.
    type: bool
  target:
    description:
    - The Organizational Unit to create the link in.
    - When ommitted, this will default to the C(defaultNamingContext) of the
      domain.
    type: str
author:
- Jordan Borean (@jborean93)
'''

EXAMPLES = r'''
- name: create a GPO link to the default domain context
  win_gpo_link:
    name: test-gpo
    state: present
    enabled: True

- name: remove a GPO link
  win_gpo_link:
    name: test-gpo
    state: absent

- name: create a GPO link to a specific OU
  win_gpo_link:
    name: test-gpo
    state: present
    enabled: True
    enforced: True
    target: OU=Workstations,DC=domain,DC=local
'''

RETURN = r'''
#
'''
