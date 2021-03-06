"""
---------------------
Volume snapshot tests
---------------------
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

import pytest

from stepler.third_party import utils


@pytest.mark.usefixtures('any_one')
class TestAnyOne(object):
    """Tests for any user."""

    @pytest.mark.idempotent_id('c8a507e8-ff2a-4e4d-b476-edacae26fed6',
                               any_one='admin')
    @pytest.mark.idempotent_id('934c3816-b68b-4844-829c-889670d42c22',
                               any_one='user')
    def test_create_volume_snapshot(self, volume, create_snapshot):
        """**Scenario:** Create volume snapshot.

        **Setup:**

        #. Create volume

        **Steps:**

        #. Create snapshot
        #. Check that snapshot created

        **Teardown:**

        #. Delete snapshot
        #. Delete volume
        """
        snapshot_name = next(utils.generate_ids('snapshot'))
        create_snapshot(snapshot_name)

    @pytest.mark.idempotent_id('51654e7a-bda4-4a3b-a75a-8788cbff3eae',
                               any_one='admin')
    @pytest.mark.idempotent_id('7270841e-2d58-45cd-9ef0-46c92c116c87',
                               any_one='user')
    def test_create_volume_snapshot_with_long_name(self, volume,
                                                   volumes_steps_ui):
        """**Scenario:** Create volume snapshot with name lenght > 255.

        **Setup:**

        #. Create volume

        **Steps:**

        #. Check that snapshot's name on snapshot's creation form can
            contain max 255 symbols

        **Teardown:**

        #. Delete volume
        """
        volumes_steps_ui.check_snapshot_creation_form_name_field_max_length(
            volume.name, 255)

    @pytest.mark.idempotent_id('0daeefa1-b562-4dae-97fb-fc7534794189',
                               any_one='admin')
    @pytest.mark.idempotent_id('f6823214-bef0-4af2-9000-5fcaed74fdfd',
                               any_one='user')
    def test_create_volume_snapshot_with_description(self, volume,
                                                     create_snapshot):
        """**Scenario:** Create volume snapshot with description.

        **Setup:**

        #. Create volume

        **Steps:**

        #. Create volume snapshot with description
        #. Check that snapshot created
        #. Check that description is correct

        **Teardown:**

        #. Delete snapshot
        #. Delete volume
        """
        snapshot_name = next(utils.generate_ids('snapshot'))
        snapshot_description = next(utils.generate_ids('snapshot_description'))
        create_snapshot(snapshot_name, description=snapshot_description)

    @pytest.mark.idempotent_id('a1750859-a173-4e1a-9acb-3ad40c6c486a',
                               any_one='admin')
    @pytest.mark.idempotent_id('2c64d9c8-573f-4ecc-a401-d349916168c9',
                               any_one='user')
    def test_create_volume_snapshot_with_max_length_description(
            self, create_snapshot):
        """**Scenario:** Create volume snapshot with description lenght == max.

        **Setup:**

        #. Create volume

        **Steps:**

        #. Create snapshot with long (255 symbols) description
        #. Check that snapshot is created
        #. Check that snapshot description is correct

        **Teardown:**

        #. Delete snapshot
        #. Delete volume
        """
        snapshot_name = next(utils.generate_ids('snapshot'))
        snapshot_description = next(utils.generate_ids('description',
                                                       length=255))
        create_snapshot(snapshot_name, description=snapshot_description)

    @pytest.mark.idempotent_id('b16ba9bf-7d09-462c-ae99-e1ec4653c40d',
                               any_one='admin')
    @pytest.mark.idempotent_id('8afdf0b3-f28a-4806-b527-d671a4f67df5',
                               any_one='user')
    def test_edit_volume_snapshot(self, snapshot, volumes_steps_ui):
        """Verify that user can edit volume snapshot."""
        new_snapshot_name = snapshot.name + '(updated)'
        with snapshot.put(name=new_snapshot_name):
            volumes_steps_ui.update_snapshot(snapshot.name, new_snapshot_name)

    @pytest.mark.idempotent_id('be29711c-2ce8-4f95-b77b-5380dcb968c6',
                               any_one='admin')
    @pytest.mark.idempotent_id('24f94a1a-2615-4311-9f9e-0da03d7087db',
                               any_one='user')
    def test_volume_snapshots_pagination(self, volumes_steps_ui,
                                         create_snapshots, update_settings):
        """Verify that snapshots pagination works right and back."""
        snapshot_names = list(utils.generate_ids(prefix='snapshot', count=3))
        create_snapshots(snapshot_names)
        update_settings(items_per_page=1)
        volumes_steps_ui.check_snapshots_pagination(snapshot_names)

    @pytest.mark.idempotent_id('0dd311c9-c9cf-4860-a5a3-be01d3d209d2',
                               any_one='admin')
    @pytest.mark.idempotent_id('b0e4146d-5ffa-4a27-a522-e7c3266324f2',
                               any_one='user')
    def test_create_volume_from_snapshot(self, snapshot, volumes_steps_ui):
        """Verify that user cat create volume from snapshot."""
        volumes_steps_ui.create_volume_from_snapshot(snapshot.name)
        volumes_steps_ui.delete_volume(snapshot.name)
