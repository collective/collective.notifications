# -*- coding: utf-8 -*-

import unittest2 as unittest

from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles

from plone.registry.interfaces import IRegistry

from zope.component import getUtility

from collective.notifications.config import PROJECTNAME
from collective.notifications.testing import INTEGRATION_TESTING


class InstallTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

    def test_installed(self):
        qi = getattr(self.portal, 'portal_quickinstaller')
        self.assertTrue(qi.isProductInstalled(PROJECTNAME))

    def test_registry_not_lost_on_reinstall(self):
        registry = getUtility(IRegistry)
        self.assertTrue(PROJECTNAME in registry)

        notifications = registry[PROJECTNAME]
        self.assertEqual(notifications, None)

        notifications = {'test_key': "This is a test value"}
        registry[PROJECTNAME] = notifications

        qi = getattr(self.portal, 'portal_quickinstaller')
        qi.reinstallProducts(products=[PROJECTNAME])

        registry = getUtility(IRegistry)
        after_notifications = registry.get(PROJECTNAME, None)
        self.assertEqual(notifications, after_notifications)


class UninstallTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.qi = getattr(self.portal, 'portal_quickinstaller')
        self.qi.uninstallProducts(products=[PROJECTNAME])

    def test_uninstalled(self):
        self.assertFalse(self.qi.isProductInstalled(PROJECTNAME))
