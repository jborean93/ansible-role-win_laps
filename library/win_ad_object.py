#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2018, Jordan Borean
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = r'''
---
module: win_ad_object
short_description: Manages AD object and their attributes
description:
- This module can be used to create and manage the attributes of various AD
  objects.
- You cannot use this module to delete existing objects.
options:
  attributes:
    description:
    - A dictionary that specifies the attributes to set on the AD object.
    - The key should be the LDAP name of the AD attribute and the value to set
      for that attribute.
    - Set a null value to clear/remove the attribute on the AD object.
    - Some attributes cannot be changed once set initially.
    type: dict
  context:
    description:
    - Configures the default context to search in for the AD object.
    - Run C(Get-ADRootDSE)` to find out what each value corresponds to.
    default: default
    choices:
    - configuration
    - default
    - root_domain
    - schema
    type: str
  domain_server:
    description:
    - Override the domain server to connect to, the default is the current
      domain logon server.
    type: str
  domain_username:
    description:
    - Specify a user to connect and modify the DACL with.
    - When omitted the current user will be used.
    - This will be required if not using Become, CredSSP, or Kerberos
      delegation and the remote Windows host is not the domain controller.
    type: str
  domain_password:
    description:
    - The password for I(domain_username).
    type: str
  may_contain:
    description:
    - A list of attributes to add to the C(mayContain) LDAP attribute for the
      object.
    type: list
  name:
    description:
    - The AD object to manage.
    - It is recommended to use the full distinguished name of the object.
    type: str
    required: True
  type:
    description:
    - The schema type of the AD object to manage.
    choices:
    - attribute
    - class
    default: attribute
    type: str
  update_schema:
    description:
    - Whether to update the root schema cache when changing a schema attribute.
    default: False
    type: bool
author:
- Jordan Borean (@jborean93)
'''

EXAMPLES = r'''
- name: set the admin description for an attribute
  win_ad_object:
    name: Computer
    attributes:
      adminDescription: AD Computer object
    context: schema
'''

RETURN = r'''
#
'''
