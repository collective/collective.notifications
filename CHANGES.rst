1.5 (unreleased)
================

- Nothing changed yet.


1.4 (2021-09-10)
================

- Call `.notify()` inside the async task if there.

- Add package name to task name.


1.3 (2021-06-24)
================

- Restore python 2.7 support.


1.2 (2020-01-07)
================

- Do not crash @@site-notifications control panel if notification doesn't have a user


1.1 (2019-12-30)
================

- Encode message body appropriately


1.0 (2019-12-10)
================

- Remove support for plone.app.async.

- Add python 3 support

- Support supplying separate text for email notifications.

- Don't fail if there is no site from email address configured.


0.5
===

- Add tests.

- #2612401: Don't fail if the user can't be found.
  [JL 2019-02-28]

- #2745054: Show Notifications menu item if there are read notifications and no
  unread notifications.
  [JL 2019-05-29]

- #2745050: Only send one notification to a user.
  [JL 2019-05-29]

- #2755049: If notification url does not start with http append it to portal_url on display.
  [JL 2019-05-30]

- #2755049: Use relative path for url generated from context item.
  [JL 2019-08-02]

- #2755049: Fix test.
  [JL 2019-08-02]

- #2978679: Support custom email subject and body.
  [JL 2019-10-14]
