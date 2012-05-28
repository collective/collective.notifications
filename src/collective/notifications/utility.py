from zope.interface import implements
from zope.interface import Interface
from zope.component import getUtility

from zope.intid.interfaces import IIntIds

from plone.registry.interfaces import IRegistry

from collective.notifications.config import PROJECTNAME
from collective.notifications.notification import Notification


class INotifications(Interface):

    def notify(notification):
        """
        This method will add a notification to the notifications registry
        """

    def notify_member(self, member, type, message, params, section=None):
        """
        This method will notify a given member, a notification with the
        given message, type and params, into the given section
        """

    def get_notifications_for_member(member, section=None):
        """
        This method will search the registry and it will return a notification
        for the requested member
        """

    def get_unread_count_for_member(member):
        """
        This method will return a list of tuples, with the number of unread
        notifications for each section
        """

    def mark_notifications_as_read(notifications_ids):
        """
        This method gets a list of notification ids and mark them as read
        """

class Notifications(object):
    """
    This utility will handle the notifications. Adding them to the registry
    and getting them.
    """

    implements(INotifications)

    def notify(self, notification):

        # First, let's create our notification object
        member = notification['member']
        notification_type = notification['type']
        message = notification['message']
        params = notification['params']
        section = notification['section']

        new_notification = Notification(member,
                                        notification_type,
                                        message,
                                        params,
                                        section)

        # Now, we are going to get existing notifications for this member and
        # for this section
        userid = new_notification.userid

        registry = getUtility(IRegistry)
        notifications = registry.get(PROJECTNAME)

        if not notifications:
            notifications = {}

        member_notifications = notifications.get(userid, {})

        section_notification = member_notifications.get(section, [])

        # Save the notification at the beginning of the list
        section_notification.insert(0, new_notification)

        # Finally, store back everything
        member_notifications[section] = section_notification
        notifications[userid] = member_notifications
        registry[PROJECTNAME] = notifications

    def notify_member(self, member, type, message, params, section=None):

        notification = {}
        notification['member'] = member
        notification['type'] = type
        notification['message'] = message
        notification['params'] = params

        if section:
            notification['section'] = section
        else:
            notification['section'] = 'global'

        self.notify(notification)

    def get_notifications_for_member(self, member, section=None):

        registry = getUtility(IRegistry)
        notifications = registry.get(PROJECTNAME, {})

        if not notifications:
            notifications = {}

        userid = member.getMemberId()

        member_notifications = notifications.get(userid, {})

        if section:
            notifications = member_notifications.get(section, [])
        else:
            notifications = []
            for i in member_notifications.keys():
                notifications.extend(member_notifications[i])

        return notifications

    def get_unread_count_for_member(self, member):

        registry = getUtility(IRegistry)
        notifications = registry.get(PROJECTNAME, None)

        if not notifications:
            notifications = {}

        userid = member.getMemberId()

        member_notifications = notifications.get(userid, {})

        unread_count = []
        for section in member_notifications.keys():
            number = 0
            for notification in member_notifications[section]:
                if notification.is_read():
                    # New (unread) notifications are added in the beginning
                    # of the list, so there's no point to keep looking for
                    # notifications, once we found one that is already read.
                    # So we just stop here
                    break

                number += 1

            unread_count.append((section, number))

        return unread_count

    def mark_notifications_as_read(self, notifications_ids):

        intids = getUtility(IIntIds)
        for id in notifications_ids:
            notification = intids.queryObject(id)
            if notification:
                notification.mark_read()
