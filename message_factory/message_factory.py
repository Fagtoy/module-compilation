# Copyright The IETF Trust 2021, All Rights Reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

__author__ = 'Slavomir Mazur'
__copyright__ = 'Copyright The IETF Trust 2021, All Rights Reserved'
__license__ = 'Apache License, Version 2.0'
__email__ = 'slavomir.mazur@pantheon.tech'

import os
import re
import typing as t

from demo_utils_yc_test import message_factory

from redis_connections.redis_user_notifications_connection import RedisUserNotificationsConnection

GREETINGS = 'Hello from yang-catalog'


class MessageFactory(message_factory.MessageFactory):
    """This class serves to automatically email a group of admin/developers."""

    def __init__(
        self,
        config_path=os.environ['YANGCATALOG_CONFIG_PATH'],
        close_connection_after_message_sending: bool = True,
        redis_user_notifications_connection: t.Optional[RedisUserNotificationsConnection] = None,
    ):
        super().__init__(config_path)
        self._close_connection_after_message_sending = close_connection_after_message_sending
        self._redis_user_notifications_connection = (
            redis_user_notifications_connection or RedisUserNotificationsConnection(config=self.config)
        )

    def send_missing_modules(self, modules_list: list, incorrect_revision_modules: list):
        message = 'Following modules extracted from drafts are missing in YANG Catalog:\n'
        path = os.path.join(
            self._temp_dir,
            'drafts-missing-modules/yangmodels/yang/experimental/ietf-extracted-YANG-modules',
        )
        for module in modules_list:
            message += f'{module}\n'
        message += f'\nAll missing modules have been copied to the directory: {path}'

        if incorrect_revision_modules:
            message += '\n\nFollowing missing modules do not have revision in the correct format:\n'
            for module in incorrect_revision_modules:
                message += f'{module}\n'

        self._post_to_email(message, self._developers_email)

    def send_problematic_draft(
        self,
        email_to: list[str],
        draft_filename: str,
        errors: str,
        draft_name_without_revision: t.Optional[str] = None,
    ):
        subject = f'{GREETINGS}, "{draft_filename}" had errors during an extraction'
        errors = errors.replace('\n', '<br>')
        message = f'During a daily check of IETF drafts, some errors were found in "{draft_filename}":<br><br>{errors}'
        draft_filename_without_format = draft_filename.split('.')[0]
        draft_name_without_revision = (
            draft_name_without_revision
            if draft_name_without_revision
            else re.sub(r'-\d+', '', draft_filename_without_format)
        )
        unsubscribed_emails = self._redis_user_notifications_connection.get_unsubscribed_emails(
            draft_name_without_revision,
        )
        email_to = [email for email in email_to if email not in unsubscribed_emails]
        message_subtype = 'html'
        for email in email_to:
            link_to_view_the_draft = (
                f'<a href="{self._domain_prefix}/yangvalidator?draft={draft_filename_without_format}">'
                'View it on YANG Catalog</a>'
            )
            unsubscribing_link = (
                f'<a href="{self._domain_prefix}/api/notifications/unsubscribe_from_emails/'
                f'{draft_name_without_revision}/{email}">unsubscribe</a>'
            )
            message = f'{message}<br><br>{link_to_view_the_draft} or {unsubscribing_link}'
            self._post_to_email(message, email_to=[email], subject=subject, subtype=message_subtype)
        self.send_test_webex()

    def send_test_webex(self):
        self._post_to_webex(msg='TEST MESSAGE')
