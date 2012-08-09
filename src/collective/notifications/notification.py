from Persistence import Persistent

from zope.component import getUtility
from zope.interface import implements

from zope.intid.interfaces import IIntIds
from zope.keyreference.interfaces import IKeyReference

from DateTime import DateTime
from datetime import datetime
from datetime import date


def new_condition(self):
    return True

class INotification(IKeyReference):
    """
    """

class Notification(Persistent):

    implements(INotification)

    key_type_id = 'collective.notifications.notification'

    member = None
    userid = u''
    notification_type = None
    message = u''
    params = {}
    section = u''
    read = False
    intid = 0
    expires = None
    date = datetime(2011, 1, 1)

    def condition(self):
        raise

    def __init__(self, member, notification_type, message, params, section, expires=None, condition=None):
        self.member = member
        self.userid = member.getMemberId()
        self.notification_type = notification_type
        self.message = message
        self.params = params
        self.section = section
        self.read = False
        intids = getUtility(IIntIds)
        self.intid = intids.register(self)

        if isinstance(expires, date):
            self.expires = DateTime(expires.strftime("%Y-%m-%d"))
        elif isinstance(expires, datetime):  
            self.expires = DateTime(expires.strftime("%Y-%m-%d %H:%M:%S"))
        else:
            self.expires = expires

        if not condition:
            self.condition = new_condition
        else:
            self.condition = condition

        self.date = datetime.now()

    def __call__(self):
        return self

    def is_read(self):
        return self.read

    def mark_read(self):
        self.read = True

    def mark_unread(self):
        self.read = False

    def is_expired(self):
        expired = False
        if self.expires:
            if self.expires < DateTime():
                expired = True

        return expired

    def is_valid(self):
        return self.condition(self)