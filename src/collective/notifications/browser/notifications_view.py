from zope.interface import implements
from zope.interface import Interface

from zope import schema

from zope.component import queryMultiAdapter
from zope.component import getUtility

from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.Five.browser import BrowserView

from collective.notifications.utility import INotifications

import json


class INotificationsView(Interface):
    """Interface for the address view
    """

class NotificationsView(BrowserView):
    implements(INotificationsView)

    pt = ViewPageTemplateFile('templates/notifications_view.pt')

    def get_notifications(self, section=None):
        util = getUtility(INotifications)
        pm = getToolByName(self.context, 'portal_membership')
        auth_member = pm.getAuthenticatedMember()

        if section:
            notifications = util.get_notifications_for_member(auth_member,
                                                            section = section)
        else:
            notifications = util.get_notifications_for_member(auth_member)

        return notifications

    def all_notifications(self):
        self.notifications = self.get_notifications()
        return self.pt()

    def section_notifications(self):
        self.notifications = self.get_notifications(section = self.context.id)
        return self.pt()

    def render_notification(self, notification):
        notification_type = notification.notification_type
        view = queryMultiAdapter((self.context, self.request, notification),
                               name=notification_type)

        if view:
            return view.render()


