# Known Issues and Open Items

Status as of 2026-10-13.

## Open

### 1. Content to confirm before publishing (high)

The site describes the operation file's plan as Ozone's service. Its fleet, camp and tracking
are stated in the future tense there ("Ozone will buy…"), so confirm with Ozone that they can be
presented as current, and that the MWAN statement in `why.features` stands
([README.md](README.md#to-confirm-before-publishing)). The 25-page technical offer isn't a
source ([README.md](README.md#content-sources)).

### 2. Contact details are empty (setup)

Ozone Settings is empty on ozone.local. Until it's filled in, the footer has no contact
column and the contact section has no buttons ([server.md](server.md#ozone-settings)).

### 3. No outgoing email (setup)

ozone.local has no outgoing Email Account, yet *Login with email link* is on in System
Settings. "Email me a login link" and password reset answer "sent", by design the same whether
or not the account exists, but nothing is delivered. Add an Email Account on each site, or
turn the email link off ([auth.md](auth.md#only-enabled-options-are-shown)).

### 4. The Ozone sidebar's Home row is relabelled on ozone.local (local)

A site-level sidebar customization, created on 2026-10-13, shows the Home row as "Ozone" with
a truck icon. It's site data, not app code. Reset the sidebar's customization in the Desk if
it isn't wanted.

## Not issues

- **Headless screenshots catch animations half-way.** Chrome's headless screenshot doesn't wait
  for CSS transitions. Take them with `--force-prefers-reduced-motion`
  ([how-to.md](how-to.md#check-responsiveness)).
- **frappe-ui's Inter font files are in the build.** Browsers download a font only when
  something uses it, and the site's text uses Almarai and Montserrat, so they aren't fetched.
- **An unknown top-level path is Frappe's 404**, not the SPA's: only `/`, `/en` and
  `/en/<path>` are routed to it, as in blinktech ([architecture.md](architecture.md#routing)).
