# coding=utf-8
from zope.component.hooks import getSite

from .config import NOTIFICATION_KEY
from .config import MAIN
from .interfaces import INotificationStorage

try:
    from collective.notifications.tasks import clear_read_unread_notifications_for_user
    from collective.notifications.tasks import queue_job
    from collective.notifications.tasks import remove_notifications
    from celery.utils.log import get_task_logger
    logger = get_task_logger(__name__)
except ImportError:
    queue_job = None
    import logging
    logger = logging.getLogger('collective.notifications')


def runJob(notification_uid):
    site = getSite()
    storage = INotificationStorage(site)
    notification = storage.get_notification(notification_uid)
    notification.notify()
    notification.notify_external()


def queueJob(notification_uid):
    """
    queue a job async if available.
    otherwise, just run normal
    """
    if queue_job:
        queue_job.delay(notification_uid)
    else:
        runJob(notification_uid)


def clearNotificationsForUser(users, uids):
    site = getSite()
    storage = INotificationStorage(site)
    if not isinstance(users, list):
        users = [users]
    if not isinstance(uids, list):
        uids = [uids]
    for user in users:
        notifications = storage.get_notifications_for_user(user)
        for notification, read in notifications[:]:
            if notification in uids:
                notifications.remove((notification, read))


def markReadForUsers(users, uids):
    site = getSite()
    storage = INotificationStorage(site)
    if not isinstance(users, list):
        users = [users]
    if not isinstance(uids, list):
        uids = [uids]
    for user in users:
        notifications = storage.get_notifications_for_user(user)
        for index, notification in enumerate(notifications):
            notification_uid, read = notification
            if notification_uid in uids:
                notifications[index] = (notification_uid, True)


def markUnreadForUsers(users, uids):
    site = getSite()
    storage = INotificationStorage(site)
    if not isinstance(users, list):
        users = [users]
    if not isinstance(uids, list):
        uids = [uids]
    for user in users:
        notifications = storage.get_notifications_for_user(user)
        for index, notification in enumerate(notifications):
            notification_uid, read = notification
            if notification_uid in uids:
                notifications[index] = (notification_uid, False)


def queueClearReadUnreadNotificationsForUser(users, uids, action):
    """
    queue clearing notifications, marking unread or
    marking read for users async if available.
    otherwise, just run normal
    """
    if clear_read_unread_notifications_for_user:
        clear_read_unread_notifications_for_user.delay(users, uids, action)
    else:
        if action == 'clear':
            clearNotificationsForUser(users, uids)
        elif action == 'read':
            markReadForUsers(users, uids)
        elif action == 'unread':
            markUnreadForUsers(users, uids)


def removeNotifications(uids):
    site = getSite()
    storage = INotificationStorage(site)
    if not isinstance(uids, list):
        uids = [uids]
    for uid in uids:
        notification = storage.get_notification(uid)
        if notification:
            for user in notification.recipients:
                storage.clear_notifications_for_users(user, uid)
            del storage.annotations[NOTIFICATION_KEY][MAIN][uid]


def queueRemoveNotifications(uids):
    """
    queue removing notifications async if available.
    otherwise, just run normal
    """
    if remove_notifications:
        remove_notifications.delay(uids)
    else:
        removeNotifications(uids)
