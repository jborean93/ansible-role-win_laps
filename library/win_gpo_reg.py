#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2018, Jordan Borean
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = r'''
---
module: win_gpo_reg
short_description: Manages Group Policy Objects registry settings.
description:
- Used to configure a Group Policy Object's registry settings.
options:
  gpo:
    description:
    - The name of the GPO to set the registry settings in.
    required: True
    type: str
  name:
    description:
    - The registry property name to manage.
    required: True
    type: str
  path:
    description:
    - The registry path of the key to manage.
    - This should be in the form of C(HIVE\Key\Path), e.g.
      C(HKLM\Software\Microsoft).
    required: True
    type: str
  state:
    description:
    - When C(absent), will remove the property value and set's the policy to
      the C(Not Configured) option.
    - When C(disabled), will set the property value to be disabled.
    - When C(present), will enable the property and set the value specified
      by I(value).
    choices:
    - absent
    - disabled
    - present
    default: present
    type: str
  type:
    description:
    - Set the type of the registry value to set.
    - If the value of an existing key is the same but the type is different,
      the module will remove the existing key and create a new one based on the
      type specified.
    choices:
    - string
    - expandstring
    - binary
    - dword
    - multistring
    - qword
    default: string
    type: str
  value:
    description:
    - The value to set for the registry key.
    - The type of this option depends on what is set for the I(type) option.
author:
- Jordan Borean (@jborean93)
'''

EXAMPLES = r'''
- name: enable the LAPS policy
  win_gpo_reg:
    gpo: test-gpo
    name: AdmPwdEnabled
    path: HKLM\Software\Policies\Microsoft Services\AdmPwd
    state: present
    type: dword
    value: 1

- name: disable the LAP policy
  win_gpo_reg:
    gpo: test-gpo
    name: AdmPwdEnabled
    path: HKLM\Software\Policies\Microsoft Services\AdmPwd
    state: disabled
'''

RETURN = r'''
'''
