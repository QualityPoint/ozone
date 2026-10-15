# Authentication

Ozone's own login page, in Arabic and English and in the website's look. It replaces Frappe's
`/login`. It serves **Ozone's team**, who go to the Desk after logging in, and Ozone's **clients**
(producers), who sign up at `/signup` and go to their dashboard: see
[../producer_dashboard/](../producer_dashboard/README.md) (ported from hawya's `naqel` branch). The
structure follows blinktech's (`apps/blinktech/docs/frontend/auth.md`).

## Pages

| Path | View | What it does |
| --- | --- | --- |
| `/login`, `/en/login` | `LoginView` | Login name and password, a two-factor code step, "Email me a login link", "Continue with ‹provider›" |
| `/forgot-password`, `/en/forgot-password` | `ForgotPasswordView` | Emails a password reset link (to Frappe's own `/update-password` page) |
| `/signup`, `/en/signup` | `SignupView` | Name and email: a Lead and its Contact, then Frappe's sign-up (a Website User and the welcome email). See [accounts.md](../producer_dashboard/accounts.md) |

- **Replacing Frappe's page:** the `website_route_rules` in `ozone/hooks.py` take `/login`
  from Frappe. Every Frappe link to the login page lands here: Desk session expiry, the Desk's
  logout, and `/desk` while logged out.
- **Language:** like every page, the language is in the address. Frappe's links lead to
  `/login`, so they open in Arabic, and the language switch goes to `/en/login`, keeping the
  query.
- **Old reset link:** `/login#forgot`, the hash of Frappe's old reset form, goes to the reset
  page.
- **Not indexed:** the pages aren't in `meta.json`. The server marks them `noindex`, and the
  sitemap leaves them out. Each has its own tab title (`auth.login.pageTitle`, set from the
  route's `meta.title`).

## Look

Both use the `auth` layout (`layouts/AuthLayout.vue`), one of the documents' pages:

- **The page:** white with silver shards (`BrandSilverBackground`), between the green and red
  top band and the green bottom band (`BrandStripe`).
- **The form** (`AuthCard`): one of the documents' white panels, with the red section tag
  ("حساب أوزون", "Ozone account"), and rounded fields with a green focus ring (`BaseInput`).
  Results show in a notice: red for errors, green for success (`BaseNotice`).
- **The panel beside it** (desktop only): the trucks' slogan, the tagline pill, and the
  website's truck (`BrandTruck`, shared with the hero), parked on the bottom band. It's still,
  with no motion.
- **The header:** the logo, "Back to website", the theme toggle and the language switch.

The website's header has an account link (`AccountLink`). Its icon goes to the login page, or
to the Desk when Frappe's cookies say a staff member is logged in. On phones it's a row in the
menu instead.

## Frappe behaviour we match

Checked against `frappe/templates/includes/login/login.js` and `frappe/auth.py`, as in
blinktech:

| Frappe behaviour | Here |
| --- | --- |
| `?redirect-to=` (same site only) | Followed after login. Without it, staff go to `/desk` and anyone else to the website (`postLoginUrl`) |
| Already logged in on `/login` | The router guard sends the visitor on the same way. It asks the server first: the `user_id` and `system_user` cookies outlive an expired session |
| Login name: email or `Administrator`, plus username or mobile number when enabled in System Settings | The field only has to be filled in. Its label follows the settings ("Email", "Email or username"…) |
| Two-factor (`verification` and `tmp_id` in the response) | A code step that sends `otp` and `tmp_id`. A wrong code shows "Incorrect verification code" |
| Expired password (`message: "Password Reset"`) | "Your password has expired…": Frappe has emailed a reset link |
| Error text | The server's `_server_messages` when present (account locked, IP not allowed…), else a translated default. The bare `message` ("Incorrect password" vs "User disabled or missing") is never shown, because it would reveal whether an account exists |
| Login link and reset: the same answer whether or not the email exists | Yes |

## Only enabled options are shown

The page asks `ozone.api.auth.get_login_options` what's enabled, and hides the rest:

| Option | Where to enable it (Desk) | On ozone.local (2026-10-13) |
| --- | --- | --- |
| Password login | System Settings → *Disable Username/Password Login* off | ✅ on |
| Email login link | System Settings → *Login with email link* | ✅ on, but no outgoing email ([known-issues.md](known-issues.md)) |
| Username or mobile number as the login name | System Settings → *Allow Login using User Name* / *Mobile Number* | ❌ off |
| Two-factor | System Settings → *Enable Two Factor Auth* | ❌ off |
| Google / other OAuth | Social Login Key: enable, plus client ID and secret | ❌ none |

**Emails** (login link, password reset, two-factor setup) need an outgoing **Email Account**.

## Code

| Piece | File |
| --- | --- |
| API calls (Frappe core + ours), `DESK_PATH` | `src/services/auth.ts` |
| Login state from Frappe's cookies, confirmed by the server | `src/composables/useSession.ts` (no store: nothing else needs one) |
| Error messages, email check, safe redirects, where a login goes, cached options | `src/components/auth/authHelpers.ts` (tested) |
| The form's panel | `src/components/auth/AuthCard.vue` |
| Routes in both languages, and the guest-only guard | `src/router/routes.ts` (`authPaths` in `config/site.ts`), `src/router/guards.ts` |
| Server | `ozone/api/auth.py` (endpoints: session user, login options, social login), `ozone/auth.py` (enabled providers) |

- **After a password login,** the page does a full load of the destination. The Desk is
  outside this app, and the load picks up the new session's CSRF token.
- **OAuth:** the buttons link to `ozone.api.auth.social_login?provider=…`, which makes a fresh
  state token and redirects. An authorize URL embedded in the page would expire after 10
  minutes.
- **CSRF:** the page sends the token from its boot data (`csrfHeaders()` in
  `services/http.ts`). The dev server turns the check off.

## Not handled

- **Sign up** is the page's, but Frappe decides: with Website Settings → *Disable Signup* on (as on
  naqel.local), `/signup` says it isn't available and the login page shows no sign-up link.
- **LDAP login.**
- **Two-factor setup by QR code:** on the first two-factor login, Frappe emails the
  authenticator QR code, which needs an outgoing Email Account.
- **Frappe's `/update-password` page,** where reset links lead, keeps Frappe's look.
