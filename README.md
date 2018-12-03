# Ansible Role win_laps

[![Build Status](https://travis-ci.org/jborean93/ansible-role-win_laps.svg?branch=master)](https://travis-ci.org/jborean93/ansible-role-win_laps)
[![win_openssh Ansible Galaxy Role](https://img.shields.io/ansible/role/34482.svg)](https://galaxy.ansible.com/jborean93/win_laps)

Installs and configures the [Local Administrator Password Solution](https://technet.microsoft.com/en-us/mt227395.aspx)
application on a Windows host.

This can be used to do the following;

* Install the server side components and add the required active directory schema objects and permissions
* Create a GPO to automatically push the LAPS configuration to clients
* Install the client side components

This role is mostly as a proof of concept and to make it easy to set up a test
domain with LAPS integrated. There's no reason why you can't run this in a real
environment but due to the complex changes LAPS requires in AD, please test
this before touching a production environment.


## Requirements

* Windows Server 2012 R2+

_Note: This role has been tested on Windows Server 2016, other versions should work but this is not guaranteed_

### Server Side Component Requirements

When using this role to install the server side components you will need to;

* Connect as a user that is part of the `Schema Admin` domain group
* Or, specify a user that is part of the `Schema Admin` domain group through the `opt_laps_domain_username` or `opt_laps_domain_password` variable
* Ensure you are connected to a domain controller as an admin

### GPO Configuration Requirements

When using this role to configure the GPO policy you will need to ensure you
have connected as a user that has permissions to create new GPOs and link them
to the target organizational units.

### Client Side Component Requirements

The only requirement for installing the client side components is to be an
admin on the host.


## Variables

### Mandatory Variables

When `opt_laps_install_server` or `opt_laps_configure_gpo` is `True`, the
following variables are mandatory;

* `man_laps_ou_containers`: A list of organizational units to configure with the LAPS install. This will apply the proper permissions in AD as well as link the newly created LAPS GPO if necessary.

The values for `man_laps_ou_containers` should be the full distinguished name
of the OU, e.g. `OU=Workstations,DC=domain,DC=local`.

### Optional Variables

The following variables are optional;

* `opt_laps_admin_account`: Changes the name of the admin account to manage with LAPS, will default to the `BUILTIN\Administrator` account
* `opt_laps_configure_gpo`: When set to `True` and `opt_laps_install_server` is `True`, will create a GPO to enforce the LAPS configuration and link it to `man_laps_out_containers` (default: `False`)
* `opt_laps_install_client`: When set to `True`, will install the client side components (default: `False`)
* `opt_laps_install_powershell`: When set to `True`, will install the LAPS PowerShell module `AdmPwd.PS` (default: `False`)
* `opt_laps_install_server`: When set to `True`, will install and configure the server side components as well as the active directory configurations (default: `False`)
* `opt_laps_install_ui`: When set to `True`, will install the LAPS UI application (default: `False`)
* `opt_laps_install_source`: The path or URL of the LAPS msi to install, defaults to Microsoft's download URL
* `opt_laps_product_id`: Specify the LAPS installer unique product ID that is used for idempotency checks, by default the installer will be skipped if `%ProgramFiles%\LAPS` already exists
* `opt_laps_skip_reboot`: When set to `True`, will not reboot the host if the LAPS install says one was needed, will set `out_laps_reboot_required` if it was skipped (default: `False`)

The following optional variables can be set to control the server config;

* `opt_laps_domain_server`: Specify the target domain controller to add the LAPS configuration to, defaults to `localhost`
* `opt_laps_domain_username`: Override the connection user that used to configure AD, this account should be a member of the `Schema Admins` group
* `opt_laps_domain_password`: The password for `opt_laps_domain_username`

The following optional variables can be set to control the GPO config;

* `opt_laps_enforce_password_expiry`: Corresponds with the `Do not allow password expiration time longer than required by policy` policy
* `opt_laps_gpo_name`: The name of the group policy object that contains the LAPS configuration
* `opt_laps_password_policy_age`: The maximum age of the password in days (default: `30`)
* `opt_laps_password_policy_complexity`: The password complexity policy, can be one of the following;
    * `uppercase`
    * `uppercase,lowercase`
    * `uppercase,lowercase,digits`
    * `uppercase,lowercase,digits,symbols` *default*
* `opt_laps_password_policy_length`: The length of the password to generate (default: `14`)

### Output Variables

* `out_laps_reboot_required`: This is set to `True` when `opt_laps_skip_reboot` is `True` and a reboot is required to complete the install


## Role Dependencies

None


## Example Playbooks

```
- name: install the LAPS client with the UI
  hosts: windows
  gather_facts: no
  roles:
  - role: jborean93.win_laps
    opt_laps_install_client: True
    opt_laps_install_ui: True

- name: install the LAPS server and configure it against 1 OU
  hosts: windows
  gather_facts: no
  roles:
  - role: jborean93.win_laps
    man_laps_ou_containers:
    - OU=Workstations,DC=domain,DC=local
    - OU=Accounting,DC=domain,DC=local
    opt_laps_install_server: True

- name: install the LAPS server and create a GPO
  hosts: windows
  gather_facts: no
  roles:
  - role: jborean93.win_laps
    man_laps_ou_containers:
    - OU=Workstations,DC=domain,DC=local
    opt_laps_install_server; True
    opt_laps_configure_gpo: True
```

Once the role has been run the `win_ad_dacl` module, and others, will be
available in the Ansible path. This module can be used to apply read/write
access to the password and expiry attributes to other accounts. By default
only domain admins or the actual computer account can touch these value. To add
a new user or group to the DACL you can run a task like;

```
- name: add users read access to the password attribute
  win_ad_dacl:
    # best to use the full distinguished name for the OU
    path: OU=Workstations,DC=ansible,DC=laps
    state: present
    # ACEs contain a list of rights to apply
    aces:
    # Adds read access to the password attribute
    - rights: ReadProperty
      inheritance_type: Descendents
      inherited_object_type: Computer
      object_type: ms-Mcs-AdmPwd
      access: allow
      account: ANSIBLE\PasswordUsers
    # Adds read and write access to the password expiry attribute
    - rights: ReadProperty, WriteProperty
      inheritance_type: Descendents
      inherited_object_type: Computer
      object_type: ms-Mcs-AdmPwdExpirationTime
      access: allow
      account: ANSIBLE\ExpiryUsers
```

See `library/win_ad_dacl.py` for more details.

The modules in `library` are not guaranteed to stay the same in each role
release. Make sure you read the changelog for any changes to these modules
before upgrading the role version.


## Testing

This role relies on a domain being setup and it running on two different hosts.
This is hard to setup in a CI environment that is free so the only testing that
will occur is through Vagrant locally. To test out this role, do the following;

```
pip install pypsrp

cd tests
vagrant up
ansible-playbook -i inventory.ini main.yml -vvv
```

These steps may take some time depending on whether the Vagrant boxes are
already downloaded. The current test suite just installs the server components
on the domain controller and the client CSE on the other server and makes sure
we can retrieve the password.


## Backlog

* Add an optional parameter to control the SACL (auditing) of each AD attribute
None - feature requests are welcome
