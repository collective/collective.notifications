# -*- coding: utf-8 -*-

from random import choice
import unittest2 as unittest

from zope.component import getUtility
from zope.intid.interfaces import IIntIds

from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles

from plone.registry.interfaces import IRegistry

from Products.CMFCore.utils import getToolByName

from collective.notifications.config import PROJECTNAME

from collective.notifications.notification import Notification

from collective.notifications.utility import INotifications

from collective.notifications.testing import INTEGRATION_TESTING

from DateTime import DateTime


def condition(self):
    return self.params['condition']

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

        self.assertEqual(unread_count, {"section 1": 4,
                                        "section 2": 2})

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

        self.assertEqual(unread_count, {"section 1": 3,
                                        "section 2": 0,
                                        "section 3": 6})

    def test_notifying_a_user_using_user_id(self):
        auth_member = self.pm.getAuthenticatedMember()
        type = "type 1"
        message = "This is the message"
        params = {}
        section = "section 1"

        member_id = auth_member.getUserId()

        self.utility.notify_member(member_id,
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

    def test_notifications_expire(self):
        auth_member = self.pm.getAuthenticatedMember()
        type = "type 1"
        expired_message = "Expired"
        non_expired_message = "Non expired"
        params = {}
        section = "section 1"
        expires = DateTime()

        member_id = auth_member.getUserId()

        self.utility.notify_member(member_id,
                                   type,
                                   expired_message,
                                   params,
                                   section,
                                   expires - 5)

        self.utility.notify_member(member_id,
                                   type,
                                   non_expired_message,
                                   params,
                                   section,
                                   expires + 5)

        # We can see that both notifications exist
        registry = getUtility(IRegistry)
        notifications = registry.get(PROJECTNAME, None)

        user_notifications = notifications.get(auth_member.getMemberId(), {})

        self.assertNotEqual(user_notifications, {})

        section_notifications = user_notifications.get(section, [])

        self.assertNotEqual(section_notifications, [])

        notification = section_notifications[0]

        self.assertTrue(isinstance(notification, Notification))
        self.assertEquals(notification.message, "Non expired")

        notification = section_notifications[1]

        self.assertTrue(isinstance(notification, Notification))
        self.assertEquals(notification.message, "Expired")

        # But if we use our utility methods to get the notifications, then expired ones are filtered out
        notifications = self.utility.get_notifications_for_member(auth_member)
        self.assertEquals(len(notifications), 1)
        self.assertTrue(isinstance(notifications[0], Notification))
        self.assertEquals(notifications[0].message, "Non expired")

        # If we specify the section, then we get the same output
        notifications = self.utility.get_notifications_for_member(auth_member, section="section 1")
        self.assertEquals(len(notifications), 1)
        self.assertTrue(isinstance(notifications[0], Notification))
        self.assertEquals(notifications[0].message, "Non expired")

        count = self.utility.get_unread_count_for_member(auth_member)
        self.assertEquals(len(count), 1)
        self.assertEquals(count, {'section 1': 1})

    def test_notify_role(self):
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

        regtool = getToolByName(self.portal, 'portal_registration')
        # Let's create some users that belong to specific roles
        username = "user1"
        email = "user1@none.com"
        properties = {'username' : username,'fullname' : username.encode("utf-8"),'email' : email,}
        user1 = regtool.addMember(username, username, ['Reviewer',], properties=properties)

        username = "user2"
        email = "user2@none.com"
        properties = {'username' : username,'fullname' : username.encode("utf-8"),'email' : email,}
        user2 = regtool.addMember(username, username, ['Reviewer',], properties=properties)

        username = "user3"
        email = "user3@none.com"
        properties = {'username' : username,'fullname' : username.encode("utf-8"),'email' : email,}
        user3 = regtool.addMember(username, username, ['Reviewer', 'Manager'], properties=properties)

        username = "user4"
        email = "user4@none.com"
        properties = {'username' : username,'fullname' : username.encode("utf-8"),'email' : email,}
        user4 = regtool.addMember(username, username, ['Manager',], properties=properties)

        username = "user5"
        email = "user5@none.com"
        properties = {'username' : username,'fullname' : username.encode("utf-8"),'email' : email,}
        user5 = regtool.addMember(username, username, ['Editor',], properties=properties)

        username = "user6"
        email = "user6@none.com"
        properties = {'username' : username,'fullname' : username.encode("utf-8"),'email' : email,}
        user6 = regtool.addMember(username, username, properties=properties)

        # Now, let's send a notification for just the reviewers
        type = "type 1"
        message = "None"
        params = {}
        section = "section 1"

        self.utility.notify_role('Reviewer',
                                 type,
                                 message,
                                 params,
                                 section)

        # user1, user2, and user3 should have gotten the notification, but user4, user5 and user6 not.
        notifications = self.utility.get_notifications_for_member(user1)
        self.assertEquals(len(notifications), 1)
        self.assertTrue(isinstance(notifications[0], Notification))

        notifications = self.utility.get_notifications_for_member(user2)
        self.assertEquals(len(notifications), 1)
        self.assertTrue(isinstance(notifications[0], Notification))

        notifications = self.utility.get_notifications_for_member(user3)
        self.assertEquals(len(notifications), 1)
        self.assertTrue(isinstance(notifications[0], Notification))
        
        notifications = self.utility.get_notifications_for_member(user4)
        self.assertEquals(len(notifications), 0)
        notifications = self.utility.get_notifications_for_member(user5)
        self.assertEquals(len(notifications), 0)
        notifications = self.utility.get_notifications_for_member(user6)
        self.assertEquals(len(notifications), 0)

        # Now, let's send a notification for just the Managers
        type = "type 1"
        message = "None"
        params = {}
        section = "section 1"

        self.utility.notify_role('Manager',
                                 type,
                                 message,
                                 params,
                                 section)

        # user1, user2, user5 and user6 should not have gotten the notification, and user3 and user4 should.
        notifications = self.utility.get_notifications_for_member(user1)
        self.assertEquals(len(notifications), 1)
        self.assertTrue(isinstance(notifications[0], Notification))

        notifications = self.utility.get_notifications_for_member(user2)
        self.assertEquals(len(notifications), 1)
        self.assertTrue(isinstance(notifications[0], Notification))

        notifications = self.utility.get_notifications_for_member(user3)
        self.assertEquals(len(notifications), 2)
        self.assertTrue(isinstance(notifications[0], Notification))
        self.assertTrue(isinstance(notifications[1], Notification))

        notifications = self.utility.get_notifications_for_member(user4)
        self.assertEquals(len(notifications), 1)
        self.assertTrue(isinstance(notifications[0], Notification))

        notifications = self.utility.get_notifications_for_member(user5)
        self.assertEquals(len(notifications), 0)
        notifications = self.utility.get_notifications_for_member(user6)
        self.assertEquals(len(notifications), 0)

        # Now, let's send a notification for both roles
        type = "type 1"
        message = "None"
        params = {}
        section = "section 1"

        self.utility.notify_role(['Reviewer', 'Manager'],
                                 type,
                                 message,
                                 params,
                                 section)

        # All of them should have gotten the notifications, but user5 and user6.
        notifications = self.utility.get_notifications_for_member(user1)
        self.assertEquals(len(notifications), 2)
        self.assertTrue(isinstance(notifications[0], Notification))
        self.assertTrue(isinstance(notifications[1], Notification))

        notifications = self.utility.get_notifications_for_member(user2)
        self.assertEquals(len(notifications), 2)
        self.assertTrue(isinstance(notifications[0], Notification))
        self.assertTrue(isinstance(notifications[1], Notification))

        notifications = self.utility.get_notifications_for_member(user3)
        self.assertEquals(len(notifications), 3)
        self.assertTrue(isinstance(notifications[0], Notification))
        self.assertTrue(isinstance(notifications[1], Notification))
        self.assertTrue(isinstance(notifications[2], Notification))

        notifications = self.utility.get_notifications_for_member(user4)
        self.assertEquals(len(notifications), 2)
        self.assertTrue(isinstance(notifications[0], Notification))
        self.assertTrue(isinstance(notifications[1], Notification))
        
        notifications = self.utility.get_notifications_for_member(user5)
        self.assertEquals(len(notifications), 0)
        notifications = self.utility.get_notifications_for_member(user6)
        self.assertEquals(len(notifications), 0)

    def test_notifications_condition(self):
        auth_member = self.pm.getAuthenticatedMember()
        type = "type 1"
        message = "Message"
        params = {'condition': True}
        section = "section 1"

        member_id = auth_member.getUserId()

        self.utility.notify_member(member_id,
                                   type,
                                   message,
                                   params,
                                   section,
                                   condition=condition)

        params = {'condition': False}

        self.utility.notify_member(member_id,
                                   type,
                                   message,
                                   params,
                                   section,
                                   condition=condition)

        # We can see that both notifications exist
        registry = getUtility(IRegistry)
        notifications = registry.get(PROJECTNAME, None)

        user_notifications = notifications.get(auth_member.getMemberId(), {})

        self.assertNotEqual(user_notifications, {})

        section_notifications = user_notifications.get(section, [])

        self.assertNotEqual(section_notifications, [])

        notification = section_notifications[0]

        self.assertTrue(isinstance(notification, Notification))
        self.assertEquals(notification.params, {'condition': False})

        notification = section_notifications[1]

        self.assertTrue(isinstance(notification, Notification))
        self.assertEquals(notification.params, {'condition': True})

        # But if we use our utility methods to get the notifications, then 
        # the one with the False condition is filtered out
        notifications = self.utility.get_notifications_for_member(auth_member)
        self.assertEquals(len(notifications), 1)
        self.assertTrue(isinstance(notifications[0], Notification))
        self.assertEquals(notifications[0].params, {'condition': True})

        # If we specify the section, then we get the same output
        notifications = self.utility.get_notifications_for_member(auth_member, section="section 1")
        self.assertEquals(len(notifications), 1)
        self.assertTrue(isinstance(notifications[0], Notification))
        self.assertEquals(notifications[0].params, {'condition': True})

        # Also check that it doesn't get counted as unread notification
        unread_count = self.utility.get_unread_count_for_member(auth_member)

        self.assertEqual(unread_count, {"section 1": 1})

    def test_notifications_returned_in_order(self):
        auth_member = self.pm.getAuthenticatedMember()
        type = "type 1"
        message = "This is the message"
        params = {}
        sections = ["section 1", "section 2", "section 3"]

        for i in range(0, 20):
            section = choice(sections)
            self.utility.notify_member(auth_member,
                                       type,
                                       "%s %s" %(message, i),
                                       params,
                                       section)

        notifications = self.utility.get_notifications_for_member(auth_member)
        self.assertEqual(len(notifications), 20)

        for i in range(0, 20):
            self.assertEquals(notifications[i].message, "%s %s" %(message, i))


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
