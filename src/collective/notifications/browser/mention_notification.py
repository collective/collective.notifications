from zope.interface import implements

from zope.component import getMultiAdapter
from zope.component import getUtility

from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from collective.notifications.browser.notification import IBaseNotification
from collective.notifications.browser.notification import BaseNotification


class IMentionNotification(IBaseNotification):
    """Interface for the "mention" notification type
    """

class MentionNotification(BaseNotification):
    implements(IMentionNotification)

    pt = ViewPageTemplateFile('templates/mention_notification_view.pt')

    def update(self):
        pm = getToolByName(self.context, 'portal_membership')
        pu = getToolByName(self.context, 'portal_url')

        portal = pu.getPortalObject()
        portal_url = portal.absolute_url()

        user_id = self.notification.params['mentioner']
        location_path = self.notification.params['location']

        self.location = portal.restrictedTraverse(location_path)

        personal_info = pm.getMemberInfo(user_id)

        self.mentioner = personal_info.get('fullname', user_id)

        home = pm.getHomeUrl(user_id, verifyPermission=1)

        self.mentioner_home = home or '%s/author/%s' % (portal_url, user_id)


