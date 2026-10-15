# Who a producer is

All of it lives in one module, `ozone/producer.py`. Nothing else decides it.

## The chain

```
User (Website User) ── Contact (user) ── links ──▶ Lead
         └──────────── Customer.portal_users ────▶ Customer
```

| Step | Rule | Source |
| --- | --- | --- |
| User type | A user is a System User only if one of their roles has Desk access. ERPNext's **Customer** role has none | `frappe/core/doctype/user/user.py: set_system_user`, `erpnext/setup/install.py` |
| User ↔ Contact | Frappe gives every User a Contact, or reuses the one with their email, and sets `Contact.user` | `user.py: create_contact`, `contact.py: set_user` |
| **Customer** | The Customer whose **Portal Users** table lists the user. This is ERPNext's portal rule | `erpnext/controllers/website_list_for_contact.py: get_parents_for_user` |
| **Lead** | If there is no Customer: the open Lead linked to the user's Contact. Frappe's own portal rule ("a related lead or contact") | `frappe/contacts/doctype/address/address.py: has_website_permission` |

- `get_producer(user)` returns `{doctype, name, title, parties}`. It returns `None` for guests,
  staff, and Website Users nobody has linked yet.
- A disabled Customer doesn't count. A **Converted** Lead doesn't either: its Customer does.

## Parties: whose records a producer sees

| Producer | `parties` |
| --- | --- |
| A Lead | `[(Lead, L)]` |
| A Customer | `[(Customer, C), (Lead, C.lead_name)]` |

ERPNext leaves Lead-stage records on the Lead. For example, a Quotation keeps
`quotation_to = Lead` after the order (`quotation.py: _make_customer`), and the Customer keeps
its origin in `lead_name`. So a converted producer still sees its history, and nothing is
rewritten.

How each DocType names its owner is in [access.md](access.md).
