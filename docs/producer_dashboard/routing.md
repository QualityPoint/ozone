# Where a login goes

| Who | After logging in | On `/dashboard` | On `/desk` |
| --- | --- | --- | --- |
| Guest | — | The login page, then back | Frappe → the login page |
| Staff | `redirect-to`, else `/desk` | `/desk` | The Desk |
| Producer | The page saved at sign-up, else `redirect-to`, **unless it is a Desk page**, else the dashboard **in the login page's language** | The dashboard | Frappe refuses ("Not Permitted") |
| Website User not linked yet | Same as a producer | Linked on arrival (`start_producer` makes its Lead), then the facility form; the not-linked page only for an email on a Customer's contact | Frappe refuses |

## Why a Desk `redirect-to` is skipped for producers

Frappe sends anyone who reaches a Desk page while logged out to
`/login?redirect-to=/desk/…`. That includes a browser where staff were logged in before. A
producer following it would land on a Desk page that refuses them. `landingUrl`
(`components/auth/authHelpers.ts`) is the one rule, used both after a login and by the guard on
the login pages:
- Staff take the first redirect, else the Desk.
- Producers take the first redirect outside the Desk (`isDeskPath`: `/desk`, `/app`), else their
  dashboard.

## What Frappe does, and what ozone adds

| Frappe | Source | ozone |
| --- | --- | --- |
| A Website User's login answer carries `home_page = get_default_path()` | `frappe/auth.py: set_user_info` | The SPA **never follows it** (`postLoginUrl`) |
| `get_default_path` picks from the apps whose `add_to_apps_screen` `has_permission` passes | `frappe/apps.py` | ozone's entry uses `erpnext.check_app_permission`, which is False for Website Users |
| The home page after other logins (email link, OAuth, password reset) | `frappe/website/utils.py: get_home_page` | The hook `get_website_user_home_page` returns `dashboard` for Website Users (`ozone/auth.py`) |
| `/desk` throws for Website Users | `frappe/www/desk.py` | — |

## Every app on the apps screen must hide from Website Users

`get_default_path()` is the only app left in a producer's list, if any app is left. An app with
no `has_permission` keeps a Desk route there, so Frappe's own pages (`/update-password`, and a
login from Frappe's page) would send the producer to a Desk page that refuses them.

| App | `has_permission` |
| --- | --- |
| erpnext, hrms | Their own: False for Website Users |
| naqel | `erpnext.check_app_permission` |
| ozone | `erpnext.check_app_permission` |

With all of them hidden, a producer's `get_default_path()` is `None`, and Frappe falls back to the
home page: `dashboard`. A new app installed on the site needs the same.

**Careful:** Frappe's Desk boot (`frappe/boot.py: get_app_data`) calls each `has_permission`
without catching errors, unlike the apps screen. A path that doesn't import breaks the Desk for
**every** user. After changing one, check that `/desk` opens. With `bench start`, also check that
the web process has reloaded the module.

