from celery.utils.log import get_task_logger
from collective.celery import task


logger = get_task_logger(__name__)


@task(name="notify")
def queue_job(notification_uid):
    from collective.notifications.pasync import runJob
    logger.warn('Sending notification')
    runJob(notification_uid)


@task(name="clear-read-unread-notifications-for-user")
def clear_read_unread_notifications_for_user(users, uids, action):
    from collective.notifications.pasync import clearNotificationsForUser
    from collective.notifications.pasync import markReadForUsers
    from collective.notifications.pasync import markUnreadForUsers

    if action == 'clear':
        logger.warn('Clearing notifications for user')
        clearNotificationsForUser(users, uids)
    elif action == 'read':
        logger.warn('Marking notifications as read for user')
        markReadForUsers(users, uids)
    elif action == 'unread':
        logger.warn('Marking notifications as unread for user')
        markUnreadForUsers(users, uids)


@task(name="remove-notifications")
def remove_notifications(uids):
    from collective.notifications.pasync import removeNotifications

    logger.warn('Removing notifications')
    removeNotifications(uids)
