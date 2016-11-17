"""
------------
Subnet steps
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

from hamcrest import equal_to

from stepler import base
from stepler.third_party.matchers import expect_that
from stepler.third_party import steps_checker
from stepler.third_party import waiter

__all__ = ["SubnetSteps"]


class SubnetSteps(base.BaseSteps):
    """Subnet steps."""

    @steps_checker.step
    def create(self, subnet_name, network, cidr, check=True, **kwargs):
        """Step to create subnet.

        Args:
            subnet_name (str): subnet name
            network (dict): network to create subnet on
            cidr (str): cidr for subnet (like 192.168.1.0/24"")
            check (bool): flag whether to check step or not
            **kwargs: other arguments to pass to API

        Returns:
            dict: subnet
        """
        subnet = self._client.create(name=subnet_name,
                                     network_id=network['id'],
                                     cidr=cidr,
                                     **kwargs)

        if check:
            self.check_presence(subnet)

        return subnet

    @steps_checker.step
    def delete(self, subnet, check=True):
        """Step to delete subnet.

        Args:
            subnet (dict): subnet
            check (bool): flag whether to check step or not
        """
        self._client.delete(subnet['id'])

        if check:
            self.check_presence(subnet, must_present=False)

    @steps_checker.step
    def check_presence(self, subnet, must_present=True, timeout=0):
        """Verify step to check subnet is present.

        Args:
            subnet (dict): subnet to check presence status
            must_present (bool): flag whether subnet must present or not
            timeout (int): seconds to wait a result of check

        Raises:
            TimeoutExpired: if check failed after timeout
        """
        def _check_subnet_presence():
            is_present = bool(self._client.find_all(id=subnet['id']))
            return expect_that(is_present, equal_to(must_present))

        waiter.wait(_check_subnet_presence, timeout_seconds=timeout)
