
from zope.component import getUtility
from zope.interface import implements

from zope.intid.interfaces import IIntIds
from zope.keyreference.interfaces import IKeyReference

class INotification(IKeyReference):
    """
    """

class Notification(object):

    implements(INotification)

    member = None
    userid = u''
    notification_type = None
    message = u''
    params = {}
    section = u''
    read = False
    intid = 0

    def __init__(self, member, notification_type, message, params, section):
        self.member = member
        self.userid = member.getMemberId()
        self.notification_type = notification_type
        self.message = u''
        self.params = params
        self.section = section
        self.read = False
        intids = getUtility(IIntIds)
        self.intid = intids.register(self)

    def __call__(self):
        return self

    def is_read(self):
        return self.read

    def mark_read(self):
        self.read = True

    def mark_unread(self):
        self.read = False

