#! /usr/bin/env python2.6
#
# Connect to the NETCONF server passed on the command line and
# display their capabilities. This script and the following scripts
# all assume that the user calling the script is known by the server
# and that suitable SSH keys are in place. For brevity and clarity
# of the examples, we omit proper exception handling.
#
# $ ./nc01.py broccoli

import sys, os, warnings
warnings.simplefilter("ignore", DeprecationWarning)
from ncclient import manager

exec_conf_prefix = """
      <config xmlns:xc="urn:ietf:params:xml:ns:netconf:base:1.0">
        <configure xmlns="http://www.cisco.com/nxos:1.0:vlan_mgr_cli">
          <__XML__MODE__exec_configure>
"""

exec_conf_postfix = """
          </__XML__MODE__exec_configure>
        </configure>
      </config>
"""

cmd_vlan_conf_snippet= """
            <vlan>
              <vlan-id-create-delete>
                <__XML__PARAM_value>%s</__XML__PARAM_value>
                <__XML__MODE_vlan>
                  <name>
                    <vlan-name>%s</vlan-name>
                  </name>
                  <state>
                    <vstate>active</vstate>
                  </state>
                  <no>
                    <shutdown/>
                  </no>
                </__XML__MODE_vlan>
              </vlan-id-create-delete>
            </vlan>
"""

cmd_vlan_int_snippet = """
          <interface> 
            <ethernet>
              <interface>%s</interface>
              <__XML__MODE_if-ethernet-switch>
                <switchport></switchport>
                <switchport>
                  <trunk>
                    <allowed>
                      <vlan>
                        <__XML__BLK_Cmd_switchport_trunk_allowed_allow-vlans>
                          <allow-vlans>%s</allow-vlans>
                        </__XML__BLK_Cmd_switchport_trunk_allowed_allow-vlans>
                      </vlan>
                    </allowed>
                  </trunk>
                </switchport>
              </__XML__MODE_if-ethernet-switch>
            </ethernet>
          </interface>
""" 


cmd_no_vlan_int_snippet = """
 <config xmlns:xc="urn:ietf:params:xml:ns:netconf:base:1.0">
   <configure xmlns="http://www.cisco.com/nxos:1.0:vlan_mgr_cli">
     <__XML__MODE__exec_configure>

     <interface>
       <ethernet>
         <interface>%s</interface>
         <__XML__MODE_if-ethernet-switch>
           <switchport></switchport>
           <switchport>
             <trunk>
               <allowed>
                 <vlan>
                   <__XML__BLK_Cmd_switchport_trunk_allowed_allow-vlans>
                     <allow-vlans>%s</allow-vlans>
                   </__XML__BLK_Cmd_switchport_trunk_allowed_allow-vlans>
                 </vlan>
               </allowed>
             </trunk>
           </switchport>
         </__XML__MODE_if-ethernet-switch>
       </ethernet>
     </interface>

     </__XML__MODE__exec_configure>
   </configure>
 </config>
"""



filter_show_vlan_brief_snippet =  """
      <show xmlns="http://www.cisco.com/nxos:1.0:vlan_mgr_cli">
        <vlan>
          <brief/>
        </vlan>
      </show> """

def nxos_connect(host, port, user, password):
    return manager.connect(host=host, port=port, username=user, 
                         password=password,hostkey_verify=False,device_params={'name': 'nexus'})


def enable_vlan(mgr, vlanid, vlanname):
    confstr = cmd_vlan_conf_snippet % (vlanid, vlanname) 
    confstr = exec_conf_prefix + confstr + exec_conf_postfix
    mgr.edit_config(target='running', config=confstr)


def enable_vlan_on_trunk_int(mgr, interface, vlanid):
    confstr = cmd_vlan_int_snippet % (interface, vlanid)
    confstr = exec_conf_prefix + confstr + exec_conf_postfix
    print confstr
    mgr.edit_config(target='running', config=confstr)


def disable_vlan_on_trunk_int(mgr, interface, vlanid):
    confstr = cmd_no_vlan_int_snippet % (interface, vlanid)
    print confstr
    mgr.edit_config(target='running', config=confstr)


def test_nxos_api(host, user, password):
    with nxos_connect(host, port=22, user=user, password=password) as m:
        enable_vlan(m, '250', 'customer')
        enable_vlan_on_trunk_int(m, '2/1', '101')
        #disable_vlan_on_trunk_int(m, '2/1', '102')
        #result = m.get(("subtree", filter_show_vlan_brief_snippet))
        #print result


if __name__ == '__main__':
    test_nxos_api(sys.argv[1], sys.argv[2], sys.argv[3])
