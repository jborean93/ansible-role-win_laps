#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2018, Jordan Borean
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = r'''
---
module: win_gpo
short_description: Manages Group Policy Objects.
description:
- Used to create and remove Group Policy Objects (GPOs).
options:
  description:
    description:
    - A comment or description to set when creating the GPO.
    - This is only set when creating a new GPO, existing GPOs won't change the
      comment if it doesn't match.
    type: str
  name:
    description:
    - The name of the GPO to create.
    required: True
    type: str
  state:
    description:
    - Whether to create or remove a GPO.
    choices:
    - absent
    - present
    default present
    type: str
author:
- Jordan Borean (@jborean93)
'''

EXAMPLES = r'''
- name: create a new GPO
  win_gpo:
    name: test gpo
    state: present

- name: remove a GPO
  win_gpo:
    name: test gpo
    state: absent
'''

RETURN = r'''
id:
  description: The ID of the GPO
  returned: if a GPO exists or was created
  type: str
  sample: af99a5b2-e8b7-4172-bbaa-9bc95954e47f
path:
  description: The full distinguished name of the GPO in AD
  returned: if a GPO exists or was created
  type: str
  sample: cn=test-gpo,cn=policies,cn=system,dc=domain,dc=local
'''
