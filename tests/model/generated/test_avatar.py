import unittest

from bunq.sdk.client import ApiClient
from bunq.sdk.model.generated.endpoint import Avatar
from bunq.sdk.model.generated.endpoint import AttachmentPublic
from bunq.sdk.model.generated.endpoint import AttachmentPublicContent
from tests.api_context_handler import ApiContextHandler
from tests.config import Config


class AvatarTest(unittest.TestCase):
    """
    Tests:
        Avatar
        AttachmentPublic
        AttachmentPublicContent
    """

    @classmethod
    def setUpClass(cls):
        cls._FIRST_INDEX = 0
        cls._PATH_TO_ATTACHMENT = '/Users/khellemun/bunq/sdk_python/tests' \
                                  '/assets'
        cls._READ_FILE_BYTES = 'rb'
        cls._CONTENT_TYPE = Config.get_attachment_content_type()
        cls._ATTACHMENT_DESCRIPTION = Config.get_attachment_description()
        cls._ATTACHMENT_PATH_IN = Config.get_attachment_path_in()
        cls._API_CONTEXT = ApiContextHandler.get_api_context()

    def test_avatar_creation(self):
        """
        Tests the creation of an avatar by uploading a picture via
        AttachmentPublic and setting it as avatar via the uuid
        """

        custom_header = {
            ApiClient.HEADER_ATTACHMENT_DESCRIPTION:
                self._ATTACHMENT_DESCRIPTION,
            ApiClient.HEADER_CONTENT_TYPE: self._CONTENT_TYPE
        }
        attachment_public_uuid = AttachmentPublic \
            .create(self._API_CONTEXT, self.attachment_contents, custom_header)

        avatar_map = {
            Avatar.FIELD_ATTACHMENT_PUBLIC_UUID: attachment_public_uuid
        }
        avatar_uuid = Avatar.create(self._API_CONTEXT, avatar_map)
        attachment_uuid_after = Avatar.get(self._API_CONTEXT, avatar_uuid) \
            .image[self._FIRST_INDEX].attachment_public_uuid

        file_contents_received = AttachmentPublicContent.list(
            self._API_CONTEXT, attachment_uuid_after
        )
        self.assertEqual(self.attachment_contents, file_contents_received)

    @property
    def attachment_contents(self):
        """
        :rtype: bytes
        """

        with open(self._PATH_TO_ATTACHMENT + self._ATTACHMENT_PATH_IN,
                  self._READ_FILE_BYTES) as f:
            return f.read()
