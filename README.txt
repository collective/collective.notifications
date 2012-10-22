************************
collective.notifications
************************

.. contents:: Table of Contents

Introduction
------------

This product intends to imitate the functionality of the notification system from `Facebook`_.
It provides a mechanism to create and store notifications per-user.

Usage
-----

After activating the product from the add-on configlet, you should get a viewlet on top with the number of notifications your current user has.
Clicking here will send you to a view showing all notifications.
In order to notifications to be sent, there are a bunch of content rules actions provided that you can use.

Developers
----------

Creating your notification
^^^^^^^^^^^^^^^^^^^^^^^^^^

If you want to create your own notifications, you just need to:

Register your notification in your configure.zcml as an adapter::

        <adapter
            factory=".my_notification.MyNotification"
            provides=".my_notification.IMyNotification"
            name="my_notification"
            />

Your notification class (MyNotification) must inherit from collective.notifications.browser.notification.BaseNotification and its interface (IMyNotifications) must inherit from collective.notifications.browser.notification.IBaseNotification

If you need to obtain information from the notification, you should do this in the "update" method from your class.

In addition, the template showing the notification should be a ViewPageTemplate assigned to the pt class attribute.

For additional details or examples, check the notifications inside the "browser" folder from this package.

Sending the notification
^^^^^^^^^^^^^^^^^^^^^^^^

In order to send your notifications to users, you need to use the provided utility::

        from zope.component import getUtility
        from collective.notifications.utility import INotifications

        utility = getUtility(INotifications)

        to_notify = "user1"
        notif_type = "my_notification"
        msg = u""
        params = {}

        utility.notify_member(to_notify,
                              notif_type,
                              msg,
                              params)

to_notify is the member you want to notify, this can be a userid, or the member object.
notif_type is the name of the notification you gave before in the adapter.
msg would contain any message you want the notification to contain.
params is a dict containing additional key:values you want to have in your notification.

In addition, you can use "notify_broadcast" in order to send the notification to all members from site, and "notify_role", where you can specify a role to notify and all members that belong to that role would get the notification.

Check the INotification interface for additional information.

TODO
----

 - Create a viewlet that will show notifications number.
 - Create a bunch of generalized notifications.
 - Create content rules actions.
 - Provide a plone:notification zcml directive to register notifications, instead of the adapter.


.. _`Facebook`: http://facebook.com