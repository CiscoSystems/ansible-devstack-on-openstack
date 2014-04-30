ansible-devstack-on-openstack
=============================

    Ansible playbooks and scripts to bring up DevStack on top of OpenStack and
    run tempest tests.

    In order to run on-demand tempest tests with fresh multi-node DevStack
    installations, we wrote this Ansible playbook here. It allows us to deploy
    a complete multi-node DevStack cluster, run the tempest tests, publish the
    result files, all with a single command.

Overview
--------
    The playbook for running tempest tests on a multi-node DevStack cluster,
    which has been configured on top of our base OpenStack:

               +------------------+
               | DevStack cluster |
               +------------------+
                  |     |     |
                +----------------+
                | base OpenStack |
                +----------------+

    We are using the base OpenStack system to spin up DevStack clusters on
    demand, for the purpose of running tempest tests.

    IMPORTANT! This Ansible playbook needs to be run on the controller host of
               the base OpenStack installation!

    Example:

       $ ansible-playbook -v site.yml -i hosts

    The script returns an error (exit code 1) if anything went wrong throughout
    the setup of the running of the tempest tests.

    These steps are taken:

      1. Create a unique cluster ID (datetime plus random).
      2. Use Ansible's OpenStack modules to start three guests on the
         base OpenStack system.
      3. Connect these guests to the pre-existing networks and configure
         floating IP addresses for each guest.
      4. Perform basic system setup on each guest (install a couple of
         system packages, configure use of APT and PIP caches).
      5. Download and install DevStack, configure on guest as controller,
         the other two as compute hosts. The controller also acts as a
         third compute host.
      6. Run the tempest tests against the DevStack installation.
      7. Make the results available via a web server running on the controlle
         host of the base OpenStack controller.

Prerequisites
-------------
      1. You need an OpenStack base system.
      2. Two networks needs to be configured, one external one from which
         floating IP addresses will be assigned, one private one with DHCP
         enabled.
      3. This has been tested with Ubuntu guest images, specifically the
         Ubuntu 14.04 cloud server images. You should make those images
         available via Glance in your base OpenStack installation. The
         images can be found here:
            https://uec-images.ubuntu.com/trusty/current/trusty-server-cloudimg-amd64-disk1.img
            https://uec-images.ubuntu.com/trusty/current/trusty-server-cloudimg-i386-disk1.img
      4. You need to create a key. The name and the keyfile are needed
         for proper configuration:
            $ nova keypair-add my_key > my_key.pem
      5. Take the ansible/group_vars/_all.example file and copy it to
         ansible/group_vars/all. Then carefully examine this file and
         modify the various settings in order to configure it to your
         particular environment.
      6. The controller host of your base OpenStack system should have
         a web server running, so that it can server the result files
         of the tempest test runs. Since Apache is already configured
         in order to serve as front-end for the OpenStack Horizon
         application, you can modify the Apache config, so that this
         section is set in the 15-default.conf file:
              <Directory /var/www>
                Options Indexes FollowSymLinks MultiViews
                AllowOverride None
                Order allow,deny
                Allow from all
              </Directory>
         The local directory in which the files should be copied is
         then /var/www/... something of your choosing. This is also
         configured in ansible/group_vars/all.

