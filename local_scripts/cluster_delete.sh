#!/bin/bash

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
# @author: Juergen Brendel, Cisco Systems, Inc.

# -----------------------------------------------------------------------------
# Delete the nodes belonging to a cluster with a given name. It is sufficient
# to just specify a subset of the cluster name: All guests who contain that
# subset in their name will be deleted.
#
# The script also deletes all unused floating IP addresses: Useful, since we
# are assigning floating IP addresses to the guests.
#
# Usage:
#
# $ ./cluster_delete.sh <cluster-ID-prefix>
# -----------------------------------------------------------------------------

cd /root
source openrc

cluster_name="$1"

# Shutting down the nodes
for node_name in `nova list | grep "$cluster_name" | awk '{print $4}'`;
do
    echo "@@@ Shutting down node: " $node_name
    nova delete $node_name
done

sleep 10

# Cleaning up any unused floating IP addresses
for floating_ip in `nova floating-ip-list | grep None | awk '{print $2}'`;
do
    echo "@@@ Deleting floating IP: " $floating_ip
    nova floating-ip-delete $floating_ip 
done

echo "@@@ Done!"


