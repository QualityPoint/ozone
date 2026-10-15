# How accounts come to exist

## Ozone invites, from the Desk

No ozone code is involved. Both ways are Frappe's or ERPNext's own.

| Producer is | In the Desk | What follows |
| --- | --- | --- |
| A Customer | Customer → **Portal Users** → add the user | ERPNext adds the Customer role and links the user's Contact (`customer.py: link_portal_users_to_contacts`) |
| A Lead | The Lead's Contact → **Invite as User** | Frappe creates a Website User and emails it (`contact.py: invite_user`) |

## The producer signs up, on the website

The **Create an account** page appears only when Website Settings → *Disable Signup* is off. It
calls `ozone.api.auth.sign_up`, which wraps Frappe's `sign_up` and makes the producer a
**Lead**.

1. If sign-up is off, or the email already has a user, Frappe's answer is returned as it is,
   and no Lead is made.
2. `create_signup_lead` (`ozone/auth.py`) runs:
   - If the email belongs to a **Customer's** contact, it makes no Lead. Access is the
     Ozone's call (Portal Users), and until then the producer sees the not-linked page.
   - If a **Lead** with that email exists, it reuses it.
   - Otherwise it makes a Lead, with **one** Contact for the email.
3. Frappe's `sign_up` creates the User and emails the activation link.

Everything runs in one request, so if Frappe refuses, the Lead is rolled back with it.

### Why the Lead comes first

On ozone.local, CRM Settings → *Auto Creation of Contact* is on, so a new Lead makes its own
Contact (`lead.py: before_insert`). Frappe makes the user's Contact only if none has that email.
With the Lead first, Frappe finds its Contact and sets `user` on it, and there is no second
Contact.

## Lead → Customer

ERPNext converts a Lead when its quotation becomes an order (`quotation.py: _make_customer`).

| Who | Does what |
| --- | --- |
| ERPNext | Re-links the Lead's Contacts and Addresses (`customer.py: link_address_and_contact`) |
| ozone | Re-links the Lead's Facilities (`overrides/customer.py`) |
| ozone | Adds the Lead's website users to the Customer's Portal Users (`producer.py: carry_lead_users`). The rows are inserted directly, as ERPNext's own patch `migrate_supplier_portal_users` does |

Both ozone steps run on Customer `after_insert`. The producer's account then resolves to the
Customer, and still sees its Lead-stage records ([identity.md](identity.md#parties-whose-records-a-producer-sees)).

## Accounts made elsewhere

An account made in the Desk (or by a social login) has no Lead. The first time it opens the dashboard,
the user store calls `ozone.api.auth.start_producer`, which makes its Lead exactly as a sign-up does
(`create_signup_lead`: an existing Lead with the email is reused, the account's existing Contact is
linked rather than duplicated, and the Lead has no owner, since ERPNext refuses one equal to its email).
The account then starts at the facility form. Only an email already on a Customer's contact stays on the
"being linked" page: the transporter adds the user to that Customer's Portal Users.
