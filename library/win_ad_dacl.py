#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2018, Jordan Borean
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = r'''
---
module: win_ad_dacl
short_description: Manages the ACEs for a DACL on an Active Directory object.
description:
- This module can add or remove individual ACEs on a DACL on an Active
  Directory object.
- While the order of the ACEs when adding will be preserved, there is no
  guarantee that the order will be the same if an ACE already exists on the
  object.
options:
  aces:
    description:
    - A list of ACEs to apply to the DACL.
    type: list
    required: True
    suboptions:
      access:
        description:
        - Controls whether to create an Allow or Deny ACEs.
        - Deny ACEs have a higher precedence over Allow ACEs.
        required: True
        choices:
        - allow
        - deny
        type: str
      account:
        description:
        - The account or SID that the ACE applies to.
        required: True
        type: str
      inheritance_type:
        description:
        - Controls how the ACE is applied to an object and its descendents.
        - See U(https://docs.microsoft.com/en-us/dotnet/api/system.directoryservices.activedirectorysecurityinheritance?view=netframework-4.7.2)
          for more details.
        choices:
        - All
        - Children
        - Descendents
        - None
        - SelfAndChildren
        required: True
        type: str
      inherited_object_type:
        description:
        - The schema GUID or name of the AD object type that inheritance will
          apply to.
        - When ommitted, this will apply to all descendent objects.
        - This is ignored when I(inheritance_type) is set to C(None).
        type: str
      object_type:
        description:
        - The schema GUID or name of the AD object that the ACE applies to.
        - When ommitted, this this will apply to the whole AD object and not
          one attribute.
        - This can be used to control access to individual attributes in an AD
          object rather than the whole object itself.
        type: str
      rights:
        description:
        - A list of access rights specified by the ACE.
        - See U(https://docs.microsoft.com/en-us/dotnet/api/system.directoryservices.activedirectoryrights?view=netframework-4.7.2)
          for a list of valid rights.
        - This can be specified as a comma separated string or a literal list.
        required: True
        type: list
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
  path:
    description:
    - The path to the AD object to apply the DACL to.
    - This is recommended to tbe the full distinguished name.
    required: True
  state:
    description:
    - When C(state=present), will ensure the ACEs are present on the DACL.
    - When C(state=absent), will ensure the ACEs are missing on the DACL.
    default: present
    choices:
    - absent
    - present
author:
- Jordan Borean (@jborean93)
'''

EXAMPLES = r'''
- name: allow access to the LAPS attributes
  win_ad_dacl:
    path: OU=Workstations,DC=domain,DC=local
    state: present
    aces:
    - rights: ReadProperty
      inheritance_type: Descendents
      inherited_object_type: Computer
      object_type: ms-Mcs-AdmPwd
      access: allow
      account: DOMAIN\PasswordReaders
    - rights:
      - ReadProperty
      - WriteProperty
      inheritance_type: Descendents
      inherited_object_type: Computer
      object_type: ms-Mcs-AdmPwdExpirationTime
      access: allow
      account: DOMAIN\PasswordExpirers
'''

RETURN = r'''
#
'''
