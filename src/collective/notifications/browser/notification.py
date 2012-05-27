from zope.interface import implements
from zope.interface import Interface

from zope.component import adapts

from collective.notifications.notification import INotification

import transaction


class IBaseNotification(Interface):
    """
    Base Interface for rendering notifications
    """

class BaseNotification(object):
    implements(IBaseNotification)

    adapts(Interface, Interface, INotification)

    def __init__(self, context, request, notification):
        self.context = context
        self.request = request
        self.notification = notification

    def render(self):
        self.update()
        self.mark_notification_as_read()

        return self.pt()

    def update(self):
        raise ("This method should be overriden")

    def mark_notification_as_read(self):
        if not self.notification.is_read():
            self.notification.mark_read()
            transaction.savepoint()
