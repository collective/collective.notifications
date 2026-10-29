Introduction
============

The package allows you to notify users of actions or action requests for
site content and actions.


Installation
============

Download the package from GitHub and extract into your src directory.
Add 'collective.notifications' to your eggs and zcml slugs in buildout.
Include the location (src/collective.notifications) in development slugs too.
Run buildout

In Site Setup -> Add-ons, activate Notifications.
Once it is installed you will see "Notifications" under Add-on Configuration.
This is where you can see and manage site notifications. There is also a
link here to a form that allows admins to send notifications.


Sending Notifications
=====================

To send notifications from code, use NotificationRequestedEvent. Send the
event notification from the place in your code where it is required, using
code similar to this:

::

    from zope.event import notify
    from collective.notification.interfaces import NotificationRequestedEvent
    notify(NotificationRequestedEvent(context,
                                      note,
                                      recipients,
                                      user=user_id,
                                      url=action_url,
                                      external='email',
                                      email_body=email_body,
                                      email_subject=email_subject,
                                      email_content_type=content_type,
                                      first_read=False))

The `context` is the affected object. `note` is a plain text string with the
description of the action that is being notified or needs to be performed;
`recipients` is a list of user ids of all the users that will be notified,
it allows the use of group ids with the prefix "group", so for example
['group:Reviewers', 'group:Staff', 'jsmith', 'jdoe'] would send the
notification to all users of the groups reviewers and staff, as well as to
individual users jsmith and jdoe. The special group "Members" will notify
all portal users.

The last seven parameters are optional: `user` can be the userid of the user
associated with the notification. This is just in case we need a different
user than the currently logged in user, which is the default. `url` will be
used as a site action if provided, otherwise the context url will be used.
`external` refers to external notification services (see below). Currently,
the only service included is 'email'. The parameter can be a list, in which
case the notification is sent using all the listed services. Default is None,
so no external notifications will be sent if this parameter is omitted.
Finally, `first_read`, if True, marks the notification as read for all
recipients after one user reads it. This can be used to send a notification
to a group where multiple users can take action, but can safely ignore the
notification once someone reads it. Default is False. `email_body` is text for
the body of the email sent by the 'email' external service. `note` will be used
if `email_body` is not set. `email_body` should be either html or plain text.
`email_content_type` should be 'text/html' if `email_body` is html.
`email_subject` text for the subject of the email sent by the 'email' external
service.


External Notification Services
==============================

Collective.notifications allowseasy integration with external notification
services. Use the IExternalNotificationService interface for this. If a
class implements this interface and it has a `send` method, it can be used
as a service and included in the `external` parameter when sending a
notification.

Example:

::

    from zope.interface import implements
    from collective.notification.interfaces import IExternalNotificationService

    class TwitterNotifier(object):
        implements(IExternalNotificationService)

        def send(self, notification):
            # send the tweet
            ...

This requires configuring the service as un utility in configure.zcml:

::

    <utility
      provides="collective.notifications.interfaces.IExternalNotificationService"
      factory=".external.TwitterNotifier"
      name="twitter"
    />


Background jobs
===============

When collective.procrastinate is installed (the ``procrastinate`` extra),
notifications are sent by a background job (task
``collective.notifications.notify``, registered under the
``[procrastinate_tasks]`` entry point) queued when the request's transaction
commits, so the request does not wait for e-mail or other external services.
Without it the notification is sent during the request. See
collective.procrastinate's README for running the workers.


Note
====

For inserting the number of pending notifications, the "toolbar.pt" template
from plone.app.layout was overridden using z3c.jbot. Keep this in mind if
your project has its own modifications for this template.
