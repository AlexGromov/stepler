===================
Launcher parameters
===================

---------------------
Environment variables
---------------------

* ``OS_AUTH_URL`` - openstack keystone auth URL. Is required explicitly:
  **v3** - ``http://keystone/url/v3``, **v2** - ``http://keystone/url/v2.0``.
  Tests assume **admin** access for cloud management. In practice it requires
  **admin** auth URL usage. Keystone **v2** is supported partially.
* ``OS_USERNAME`` - openstack user name. By default is ``admin``.
* ``OS_PASSWORD`` - openstack user password. By default is ``password``.
* ``OS_PROJECT_NAME`` - openstack project name. By default is ``admin``.
* ``OS_PROJECT_DOMAIN_NAME`` - openstack project domain name. By default is
  ``default``.
* ``OS_USER_DOMAIN_NAME`` - openstack user domain name. By default is
  ``default``.
* ``OS_DASHBOARD_URL`` - URL of horizon dashboard. Is required for UI testing.
* ``VIRTUAL_DISPLAY`` - Flag to notify that virtual framebuffer should be used.
  It requires of installed ``xvfb``. Is disabled by default.
* ``TEST_REPORTS_DIR`` - directory where ``test_reports`` folder will be
  created. By default it will be in directory where tests are launched.
* ``OS_FLOATING_NETWORK`` - name of external (floating) network. By default is
  ``admin_floating_net``.
* ``OPENRC_ACTIVATE_CMD`` - command to source the admin credentials. By default
  is ``source /root/openrc``.


Os-faults specific environment variables:

* ``OS_FAULTS_CLOUD_DRIVER`` - Cloud driver. Can be one of ``devstack``,
  ``fuel`` or ``tcpcloud``.
* ``OS_FAULTS_CLOUD_DRIVER_ADDRESS`` - Ip address of fuel master (or mk cfg)
  node.
* ``OS_FAULTS_CLOUD_DRIVER_USERNAME`` - Username to connect to nodes. By
  default is ``root``.
* ``OS_FAULTS_CLOUD_DRIVER_KEYFILE`` - Path to private keyfile to connect via SSH
  to any node in cloud with ``OS_FAULTS_CLOUD_DRIVER_USERNAME``.
* ``OS_FAULTS_POWER_DRIVER`` - Name of os-faults power driver to cloud. By
  default it ``libvirt``.
* ``OS_FAULTS_POWER_DRIVER_URI`` - URI to connect to power driver.


---------------------------
Launch tests for components
---------------------------

.. code::

    py.test stepler/<component name>

For example::

    py.test stepler/cinder

Available component names:

* ``baremetal``
* ``cinder``
* ``cli_clients``
* ``glance``
* ``heat``
* ``horizon``
* ``keystone``
* ``neutron``
* ``nova``
* ``swift``

.. note::

    Be sure that you specify all required
    `environment variables <#environment-variables>`_
    before launching. Please keep in mind, that some components require
    additional environment variables. For example, horizon requires
    ``OS_DASHBOARD_URL`` and ``VIRTUAL_DISPLAY``.

--------------
Pytest options
--------------

* ``--disable-steps-checker`` - Suppress steps consitency checking before
  tests. Only for debugging. Isn't recommended on production.
* ``--snapshot-name <snapshot name>`` - Specify environment snapshot name for
  cloud reverting. Is required for destructive tests.
* ``--bugs-file <file path>`` - Define a path to file, which contains opened
  bugs for tests. These tests will be skipped according to file info. More
  details are in :doc:`third_party`.
