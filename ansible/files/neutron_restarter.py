# Copyright 2014 Cisco Systems, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
#
# @author: Dane LeBlanc, Juergen Brendel, Cisco Systems, Inc.

# -----------------------------------------------------------------------------
# This quickly restarts all neutron related processes in a DevStack deployment.
#
# This is based on Dane's original script, which performed an entire DevStack
# deployment. This stripped-down version here, created by Juergen, merely
# removed everything, except the restarting of the Neutron processes. The
# remaining code and logic were taken as-is from Dane's excellent script.
# -----------------------------------------------------------------------------

import os
import re
import subprocess
import sys
import time
import datetime

logfile = open("/tmp/restart.log", "w")
runfile = open("/tmp/run.sh", "w")
runfile.write("#!/bin/bash\n\n")

NEUTRON_RESTART_PROCS = [
    'neutron-server', 'neutron-openvswitch-agent',
    'neutron-dhcp-agent', 'neutron-l3-agent',
    'neutron-metadata-agent', 'neutron-lbaas-agent']


def restart_neutron_processes(workspace):
    reg_exes = {}
    for proc in NEUTRON_RESTART_PROCS:
        reg_exes[proc] = re.compile(
            "^(?P<uid>\S+)\s+(?P<pid>\d+)\s+(?P<ppid>\d+).*python(?P<cmd>.*%s.*)"
            % proc)
    time.sleep(5)
    ps_output = run_cmd_line('ps -ef')
    logfile.write("\n\n@@@@@@@@@@@@@@@ first %s\n" % datetime.datetime.now())
    for line in ps_output.splitlines():
        for proc, reg_ex in reg_exes.items():
            result = reg_ex.search(line)
            if result:
                 logfile.write(line + "\n")
                 print 'Restarting ', proc
                 # Kill the process
                 run_cmd_line('kill -9 %d' % int(result.group('pid')))
                 # Re-run the  process
                 filename = os.path.join(workspace, proc + '.log')
                 cmd = result.group('cmd') + ' > %s 2>&1 &' % filename
                 print cmd
                 runfile.write(cmd + "\n")
                 os.system(cmd)

    print 'Neutron processes: '
    ps_output = run_cmd_line('ps -ef')
    for line in ps_output.splitlines():
        for proc, reg_ex in reg_exes.items():
            result = reg_ex.search(line)
            if result:
                 logfile.write(line + "\n")
                 print line

    time.sleep(5)

def run_cmd_line(cmd_str, stdout=None, stderr=None, check_result=True):
    print cmd_str
    output = None
    try:
        if stdout:
            subprocess.check_call(cmd_str.split(), stdout=stdout,
                                  stderr=stderr)
        else:
            output = subprocess.check_output(cmd_str.split(), stderr=stderr)
    except Exception as e:
        if check_result:
            print e
            sys.exit(1)
    return output


if __name__ == '__main__':
    try:
        workspace = sys.argv[1]
    except:
        print "Need WORKSPACE as first argument."
        sys.exit(1)

    restart_neutron_processes(workspace)
    runfile.close()


