from zope.event import notify

from .base import BaseTestCase
from .. import pasync
from ..interfaces import INotificationStorage
from ..interfaces import NotificationRequestedEvent


class TestQueuedNotification(BaseTestCase):
    """With collective.procrastinate installed the inbox update is a task.

    The test layer runs it inline (eager).
    """

    def test_notification_reaches_inbox_through_the_task(self):
        self.assertIsNotNone(pasync.queue_job)
        notify(NotificationRequestedEvent(self.portal, "hello", ['user1']))
        storage = INotificationStorage(self.portal)
        [notification] = list(storage.get_notifications())
        self.assertEqual(
            list(storage.get_notifications_for_user('user1')),
            [(notification.uid, False)])
