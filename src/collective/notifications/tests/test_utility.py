# -*- coding: utf-8 -*-

import unittest2 as unittest

from zope.component import getUtility
from zope.intid.interfaces import IIntIds

from plone.registry.interfaces import IRegistry

from Products.CMFCore.utils import getToolByName

from collective.notifications.config import PROJECTNAME

from collective.notifications.notification import Notification

from collective.notifications.utility import INotifications

from collective.notifications.testing import INTEGRATION_TESTING

from DateTime import DateTime


class UtilityTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        self.utility = getUtility(INotifications)

        self.pm = getToolByName(self.portal, 'portal_membership')


    def test_notifying_a_user(self):
        auth_member = self.pm.getAuthenticatedMember()
        type = "type 1"
        message = "This is the message"
        params = {}
        section = "section 1"

        self.utility.notify_member(auth_member,
                                   type,
                                   message,
                                   params,
                                   section)

        registry = getUtility(IRegistry)
        notifications = registry.get(PROJECTNAME, None)

        user_notifications = notifications.get(auth_member.getMemberId(), {})

        self.assertNotEqual(user_notifications, {})

        section_notifications = user_notifications.get(section, [])

        self.assertNotEqual(section_notifications, [])

        notification = section_notifications[0]

        self.assertTrue(isinstance(notification, Notification))

    def test_notification_start_as_unread(self):
        auth_member = self.pm.getAuthenticatedMember()
        type = "type 1"
        message = "This is the message"
        params = {}
        section = "section 1"

        self.utility.notify_member(auth_member,
                                   type,
                                   message,
                                   params,
                                   section)

        registry = getUtility(IRegistry)
        notifications = registry.get(PROJECTNAME, None)

        user_notifications = notifications.get(auth_member.getMemberId(), {})
        section_notifications = user_notifications.get(section, [])
        notification = section_notifications[0]

        self.assertFalse(notification.is_read())

    def test_mark_notification_as_read(self):
        auth_member = self.pm.getAuthenticatedMember()
        type = "type 1"
        message = "This is the message"
        params = {}
        section = "section 1"

        for i in range(0,9):
            self.utility.notify_member(auth_member,
                                       type,
                                       message,
                                       params,
                                       section)

        registry = getUtility(IRegistry)
        notifications = registry.get(PROJECTNAME, None)

        user_notifications = notifications.get(auth_member.getMemberId(), {})
        section_notifications = user_notifications.get(section, [])

        intids = []
        for i in range(0,9):
            notification = section_notifications[i]

            self.assertFalse(notification.is_read())

            intids.append(notification.intid)

        self.utility.mark_notifications_as_read(intids)

        # It shouldn't be needed to get the registry again, but we'll just
        # make sure everything works as expected
        notifications = registry.get(PROJECTNAME, None)

        user_notifications = notifications.get(auth_member.getMemberId(), {})
        section_notifications = user_notifications.get(section, [])

        for i in range(0,9):
            notification = section_notifications[i]

            self.assertTrue(notification.is_read())

    def test_get_notifications_for_member(self):
        auth_member = self.pm.getAuthenticatedMember()
        type = "type 1"
        message = "This is the message"
        params = {}
        section = "section 1"

        for i in range(0,4):
            self.utility.notify_member(auth_member,
                                       type,
                                       message,
                                       params,
                                       section)

        section = "section 2"

        for i in range(0,2):
            self.utility.notify_member(auth_member,
                                       type,
                                       message,
                                       params,
                                       section)

        section = "section 3"

        for i in range(0,6):
            self.utility.notify_member(auth_member,
                                       type,
                                       message,
                                       params,
                                       section)

        notifications = self.utility.get_notifications_for_member(auth_member)
        self.assertEqual(len(notifications), 12)

        notifications = self.utility.get_notifications_for_member(auth_member,
                                                         section="section 1")
        self.assertEqual(len(notifications), 4)
        notifications = self.utility.get_notifications_for_member(auth_member,
                                                         section="section 2")
        self.assertEqual(len(notifications), 2)
        notifications = self.utility.get_notifications_for_member(auth_member,
                                                         section="section 3")
        self.assertEqual(len(notifications), 6)



    def test_unread_count_for_member(self):
        auth_member = self.pm.getAuthenticatedMember()
        type = "type 1"
        message = "This is the message"
        params = {}
        section = "section 1"

        for i in range(0,4):
            self.utility.notify_member(auth_member,
                                       type,
                                       message,
                                       params,
                                       section)

        section = "section 2"

        for i in range(0,2):
            self.utility.notify_member(auth_member,
                                       type,
                                       message,
                                       params,
                                       section)

        unread_count = self.utility.get_unread_count_for_member(auth_member)

        self.assertEqual(unread_count[0], ("section 1", 4))
        self.assertEqual(unread_count[1], ("section 2", 2))

        section = "section 3"

        for i in range(0,6):
            self.utility.notify_member(auth_member,
                                       type,
                                       message,
                                       params,
                                       section)

        notifications = self.utility.get_notifications_for_member(auth_member,
                                                                  'section 1')
        self.utility.mark_notifications_as_read([notifications[3].intid])


        notifications = self.utility.get_notifications_for_member(auth_member,
                                                                  'section 2')
        self.utility.mark_notifications_as_read([i.intid for
                                                 i in notifications])

        unread_count = self.utility.get_unread_count_for_member(auth_member)

        self.assertEqual(unread_count[0], ("section 1", 3))
        self.assertEqual(unread_count[1], ("section 2", 0))
        self.assertEqual(unread_count[2], ("section 3", 6))


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
