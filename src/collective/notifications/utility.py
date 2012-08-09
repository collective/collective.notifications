from Products.CMFCore.utils import getToolByName

from zope.interface import implements
from zope.interface import Interface
from zope.component import getUtility

from zope.site.hooks import getSite

from zope.intid.interfaces import IIntIds

from plone.registry.interfaces import IRegistry

from collective.notifications.config import PROJECTNAME
from collective.notifications.notification import Notification


class INotifications(Interface):

    def notify(notification):
        """
        This method will add a notification to the notifications registry
        """

    def notify_member(member, type, message, params, section=None, expires=None):
        """
        This method will notify a given member, a notification with the
        given message, type and params, into the given section
        """

    def notify_broadcast(type, message, params, section=None, expires=None):
        """
        This method will send a notification for all members in the site using
        the 'notify_member' method
        """

    def notify_role(roles, type, message, params, section=None, expires=None):
        """
        This method will send a notification for all members that belong to the
        specified roles.
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
        if isinstance(member, basestring):
            portal = getSite()
            pm = getToolByName(portal, 'portal_membership')
            member = pm.getMemberById(member)

        notification_type = notification['type']
        message = notification['message']
        params = notification['params']
        section = notification['section']
        expires = notification['expires']
        condition = notification['condition']

        new_notification = Notification(member,
                                        notification_type,
                                        message,
                                        params,
                                        section,
                                        expires,
                                        condition)

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

    def notify_member(self, member, type, message, params, section=None, expires=None, condition=None):

        notification = {}
        notification['member'] = member
        notification['type'] = type
        notification['message'] = message
        notification['params'] = params
        notification['expires'] = expires
        notification['condition'] = condition

        if section:
            notification['section'] = section
        else:
            notification['section'] = 'global'

        self.notify(notification)

    def notify_broadcast(self, type, message, params, section=None, expires=None, condition=None):
        portal = getSite()

        pm = getToolByName(portal, 'portal_membership')
        members = pm.listMembers()

        for member in members:
            self.notify_member(member, type, message, params, section, expires, condition)

    def notify_role(self, roles, type, message, params, section=None, expires=None, condition=None):
        portal = getSite()
        pm = getToolByName(portal, 'portal_membership')

        if isinstance(roles, basestring):
            roles = [roles]

        members = []
        for role in roles:
            members += [member for member in pm.listMembers() 
                        if member.has_role(role) and member not in members]

        for member in members:
            self.notify_member(member, type, message, params, section, expires, condition)

    def get_notifications_for_member(self, member, section=None):

        registry = getUtility(IRegistry)
        notifications = registry.get(PROJECTNAME, {})

        if not notifications:
            notifications = {}

        try:
            userid = member.getMemberId()
        except AttributeError:
            # This might happen when asking for anonymous
            return []

        member_notifications = notifications.get(userid, {})

        notifications = []
        for i in member_notifications.keys():
            if section and section != i:
                continue
            non_expired_and_valid = [i for i in member_notifications[i] 
                                     if not i.is_expired() and i.is_valid()]
            notifications.extend(non_expired_and_valid)

        notifications.sort(key=lambda x:x.date)
        return notifications

    def get_unread_count_for_member(self, member):

        notifications = self.get_notifications_for_member(member)

        unread_count = {}
        for notification in notifications:
            number = unread_count.get(notification.section)
            if not number:
                number = unread_count[notification.section] = 0
                
            if notification.is_read():
                continue
            
            number += 1 
            unread_count[notification.section] = number

        return unread_count

    def mark_notifications_as_read(self, notifications_ids):

        intids = getUtility(IIntIds)
        for id in notifications_ids:
            notification = intids.queryObject(id)
            if notification:
                notification.mark_read()
