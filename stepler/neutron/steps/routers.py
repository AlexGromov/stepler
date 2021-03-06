"""
------------
Router steps
------------
"""

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from hamcrest import (assert_that, calling, empty, equal_to, has_entries,
                      has_length, is_in, is_not, raises)  # noqa H301
from neutronclient.common import exceptions

from stepler import base
from stepler.third_party import steps_checker
from stepler.third_party import utils
from stepler.third_party import waiter

__all__ = ["RouterSteps"]


class RouterSteps(base.BaseSteps):
    """Router steps."""

    @steps_checker.step
    def create(self, router_name, distributed=None, check=True, **kwargs):
        """Step to create router.

        Args:
            router_name (str): router name
            distributed (bool): should router be distributed
            check (bool): flag whether to check step or not
            **kwargs: other arguments to pass to API

        Returns:
            dict: router
        """
        router = self._client.create(name=router_name, distributed=distributed,
                                     **kwargs)

        if check:
            self.check_presence(router)

        return router

    @steps_checker.step
    def delete(self, router, check=True):
        """Step to delete router.

        Args:
            router (dict): router
            check (bool): flag whether to check step or not
        """
        self._client.delete(router['id'])

        if check:
            self.check_presence(router, must_present=False)

    @steps_checker.step
    def check_presence(self, router, must_present=True, timeout=0):
        """Verify step to check router is present.

        Args:
            router (dict): router to check presence status
            must_present (bool): flag whether router must present or not
            timeout (int): seconds to wait a result of check

        Raises:
            TimeoutExpired: if check failed after timeout
        """
        def _check_router_presence():
            is_present = bool(self._client.find_all(id=router['id']))
            return waiter.expect_that(is_present, equal_to(must_present))

        waiter.wait(_check_router_presence, timeout_seconds=timeout)

    @steps_checker.step
    def set_gateway(self, router, network, check=True):
        """Step to set router gateway.

        Args:
            router (dict): router
            network (dict): network
            check (bool): flag whether to check step or not
        """
        self._client.set_gateway(router_id=router['id'],
                                 network_id=network['id'])
        if check:
            self.check_gateway_presence(router)

    @steps_checker.step
    def clear_gateway(self, router, check=True):
        """Step to clear router gateway.

        Args:
            router (dict): router
            check (bool): flag whether to check step or not
        """
        self._client.clear_gateway(router_id=router['id'])
        if check:
            self.check_gateway_presence(router, must_present=False)

    @steps_checker.step
    def check_gateway_presence(self, router, must_present=True, timeout=0):
        """Verify step to check router gateway is present.

        Args:
            router (dict): router to check gateway presence status
            must_present (bool): flag whether router must present or not
            timeout (int): seconds to wait a result of check

        Raises:
            TimeoutExpired: if check failed after timeout
        """
        router_id = router['id']

        def _check_gateway_presence():
            router = self._client.get(router_id)
            is_present = router['external_gateway_info'] is not None
            return waiter.expect_that(is_present, equal_to(must_present))

        waiter.wait(_check_gateway_presence, timeout_seconds=timeout)

    @steps_checker.step
    def add_subnet_interface(self, router, subnet, check=True):
        """Step to add router to subnet interface.

        Args:
            router (dict): router
            subnet (dict): subnet
            check (bool): flag whether to check step or not
        """
        self._client.add_subnet_interface(router_id=router['id'],
                                          subnet_id=subnet['id'])
        if check:
            self.check_subnet_interface_presence(router, subnet)

    @steps_checker.step
    def remove_subnet_interface(self, router, subnet, check=True):
        """Step to remove router to subnet interface.

        Args:
            router (dict): router
            subnet (dict): subnet
        """
        self._client.remove_subnet_interface(router_id=router['id'],
                                             subnet_id=subnet['id'])
        if check:
            self.check_subnet_interface_presence(
                router, subnet, must_present=False)

    @steps_checker.step
    def check_subnet_interface_presence(self,
                                        router,
                                        subnet,
                                        must_present=True,
                                        timeout=0):
        """Verify step to check subnet is in router interfaces.

        Args:
            router (dict): router to check
            subnet (dict): subnet to be found in router interfaces
            must_present (bool): flag whether router should contain interface
                to subnet or not
            timeout (int): seconds to wait a result of check

        Raises:
            TimeoutExpired: if check failed after timeout
        """
        def _check_subnet_interface_presence():
            subnet_ids = self._client.get_interfaces_subnets_ids(router['id'])
            is_present = subnet['id'] in subnet_ids
            return waiter.expect_that(is_present, equal_to(must_present))

        waiter.wait(_check_subnet_interface_presence, timeout_seconds=timeout)

    @steps_checker.step
    def add_port_interface(self, router, port, check=True):
        """Step to add router port interface.

        Args:
            router (dict): router
            port (dict): port
            check (bool): flag whether to check step or not
        """
        self._client.add_port_interface(router_id=router['id'],
                                        port_id=port['id'])
        if check:
            self.check_port_interface_presence(router, port)

    @steps_checker.step
    def remove_port_interface(self, router, port, check=True):
        """Step to remove router port interface.

        After this, port can be also deleted.

        Args:
            router (dict): router
            port (dict): port
            check (bool): flag whether to check step or not
        """
        self._client.remove_port_interface(router_id=router['id'],
                                           port_id=port['id'])
        if check:
            self.check_port_interface_presence(
                router, port, must_present=False)

    @steps_checker.step
    def check_port_interface_presence(self,
                                      router,
                                      port,
                                      must_present=True,
                                      timeout=0):
        """Verify step to check port is in router interfaces.

        Args:
            router (dict): router to check
            port (dict): port to be found in router interfaces
            must_present (bool): flag whether router should contain interface
                to port or not
            timeout (int): seconds to wait a result of check

        Raises:
            TimeoutExpired: if check failed after timeout
        """
        def _check_port_interface_presence():
            ports = self._client.get_interfaces_ports(router['id'])
            matcher = is_in(ports)
            if not must_present:
                matcher = is_not(matcher)
            return waiter.expect_that(port, matcher)

        waiter.wait(_check_port_interface_presence, timeout_seconds=timeout)

    @steps_checker.step
    def get_router(self, **kwargs):
        """Step to get router.

        Args:
            **kwargs: filter to match router

        Returns:
            dict: router

        Raises:
            LookupError: if zero or more than one routers found
        """
        return self._client.find(**kwargs)

    @steps_checker.step
    def get_routers(self, check=True):
        """Step to retrieve all routers in current project.

        Args:
            check (bool): flag whether to check step or not

        Returns:
            list: list of retrieved routers
        """
        routers = self._client.list()

        if check:
            assert_that(routers, is_not(empty()))

        return routers

    @steps_checker.step
    def check_router_attrs(self, router, **kwargs):
        """Step to check whether router has expected attributes or not.

        Args:
            router (dict): router dict
            **kwargs: attributes to check

        Raises:
            AssertionError: if check failed
        """
        router_attr = self.get_router(id=router['id'])
        assert_that(router_attr, has_entries(kwargs))

    @steps_checker.step
    def check_routers_count_for_agent(self, agent, expected_count):
        """Step to check routers count for L3 agent.

        Args:
            agent (dict): neutron agent dict to check routers count
            expected_count (int): expected routers count for L3 agent

        Raises:
            AssertionError: if check failed
        """
        routers = self._client.get_routers_on_l3_agent(agent['id'])
        assert_that(routers, has_length(expected_count))

    @steps_checker.step
    def update_router(self, router, check=True, **kwargs):
        """Step to update router attributes.

        Args:
            router (dict): router dict
            check (bool): flag whether to check step or not
            **kwargs: attributes to pass to API

        Raises:
            AssertionError: if check failed
        """
        self._client.update(router['id'], **kwargs)

        if check:
            self.check_router_attrs(router, **kwargs)

    @steps_checker.step
    def check_router_type_not_changed_to_centralized(self, router):
        """Step to check router is not updated from distributed to centralized.

        Args:
            router (dict): router dict

        Raises:
            AssertionError: if BadRequest is not appeared or exception message
                is unexpected.
        """
        exception_message = ("Migration from distributed router to "
                             "centralized is not supported.")

        assert_that(calling(self.update_router).with_args(
            router=router, distributed=False, check=False),
            raises(exceptions.BadRequest, exception_message))

    @steps_checker.step
    def check_type_unchangeable_for_active_router(self, router):
        """Step to check that router type can't be changed for active router.

        Args:
            router (dict): router dict

        Raises:
            AssertionError: if BadRequest is not appeared or exception message
                is unexpected.
        """
        exception_message = (
            "Cannot upgrade active router to distributed. "
            "Please set router admin_state_up to False prior to upgrade")

        assert_that(
            calling(self.update_router).with_args(
                router=router, distributed=True, check=False),
            raises(exceptions.BadRequest, exception_message))

    @steps_checker.step
    def check_negative_create_extra_router(self):
        """Step to check that unable to create routers more than quota.

        Raises:
            AssertionError: if no OverQuotaClient exception occurs or exception
                message is not expected
        """
        exception_message = "Quota exceeded for resources"
        assert_that(
            calling(self.create).with_args(
                next(utils.generate_ids()), check=False),
            raises(exceptions.OverQuotaClient, exception_message),
            "Router has been created though it exceeds the quota or "
            "OverQuotaClient exception with expected error message "
            "has not been appeared")
