# -*- coding: utf-8 -*-

from zope import schema

#from z3c.form.browser.textlines import TextLinesFieldWidget
from zope.interface import Interface

from plone.app.registry.browser import controlpanel

from collective.notifications import _



class INotificationsSettings(Interface):
    """ Interface for the control panel form.
    """

    notification_types = schema.Set(
            title=_(u'Notification types'),
            required=True,
            default=set(),
            value_type=schema.TextLine(title=_(u'Notification types')),)


class NotificationsSettingsEditForm(controlpanel.RegistryEditForm):
    schema = INotificationsSettings
    label = _(u'Notifications Settings')
    description = _(u'Settings for the collective.notifications package')

    #def updateFields(self):
        #super(NotificationsSettingsEditForm, self).updateFields()
        #self.fields['sections'].widgetFactory = TextLinesFieldWidget

    #def updateWidgets(self):
        #super(NotificationsSettingsEditForm, self).updateWidgets()
        #self.widgets['sections'].rows = 8
        #self.widgets['sections'].style = u'width: 30%;'


class NotificationsSettingsControlPanel(controlpanel.ControlPanelFormWrapper):
    form = NotificationsSettingsEditForm
