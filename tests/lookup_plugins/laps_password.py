from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = """
lookup: laps_password
author: Jordan Borean (@jborean93)
short_description: Retrieve the LAPS configured password.
description:
- Retrieves the password of a host that has been set by LAPS.
options:
  _terms:
    description:
    - The server(s) to get the password for.
    required: True
  domain_server:
    description:
    - The domain server to query.
    required: True
  username:
    description:
    - The username to use for authentication with the domain server.
    - This user should have the C(ReadProperty) rights on the C(ms-Mcs-AdmPwd)
      attribute.
    required: True
  password:
    description:
    - The password for I(username).
    required: True
  search_base:
    description:
    - The distinguished name for the container that contains the server object
      in Active Directory.
    required: True
notes:
- This is a POC, all data, including the initial auth user/pass is sent in
  plaintext and is therefore not secure.
- You should look at trying to run over LDAPS or get Kerberos auth working so
  the data is encrypted.
- If the lookup fails to retrieve the password, or the attribute isn't set then
  it will fail.
"""

EXAMPLES = """
- name: get the LAPS managed password for a host
  debug:
    msg: "{{ lookup('laps_password', 'SERVER01', domain_server='dc01.domain.local', username='username@DOMAIN.LOCAL', password='Password01', search_base='OU=Workstations,DC=domain,DC=local') }}"
"""

RETURN = """
_string:
  description:
  - The LAPS password for the hostname specified
  type: str
"""

from ansible.errors import AnsibleError
from ansible.module_utils._text import to_text
from ansible.plugins.lookup import LookupBase

try:
    import ldap
    HAS_LDAP = True
except ImportError:
    HAS_LDAP = False


class LookupModule(LookupBase):

    def run(self, terms, variables=None, domain_server=None, username=None, password=None, search_base=None, **kwargs):
        if not HAS_LDAP:
            raise AnsibleError('The python-ldap package is required for the laps_password lookup plugin')

        connection = ldap.initialize(u"LDAP://%s" % to_text(domain_server), bytes_mode=False)
        connection.simple_bind_s(to_text(username), to_text(password))
        ldap_results = connection.search_s(to_text(search_base), ldap.SCOPE_SUBTREE,
                                           attrlist=[u"cn", u"ms-Mcs-AdmPwd"])

        ret = []
        for term in terms:
            ldap_result = [r for r in ldap_results if to_text(r[1].get(u'cn', [""])[0]) == to_text(term)]
            if len(ldap_result) != 1:
                raise AnsibleError("Expecting only 1 result for 'CN=%s,%s' but found %d"
                                   % (term, search_base, len(ldap_result)))
            attributes = ldap_result[0][1]
            laps_password = attributes.get('ms-Mcs-AdmPwd', None)
            if not laps_password:
                raise AnsibleError("Failed to retrieve the ms-Mcs-AdmPwd attribute for %s" % term)
            ret.append(to_text(laps_password[0]))

        return ret
