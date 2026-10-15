# Waste Transport Contract (print format)

**For:** Service Quotation · **Module:** Ozone · **Files:** `ozone/ozone/print_format/waste_transport_contract/`

The Madinah Regional Municipality's standard contract for transporting non-hazardous waste (عقد نقل النفايات غير الخطرة), filled from a Service Quotation. It is always printed in Arabic, right to left, on A4.

| Page | Contents |
| --- | --- |
| 1 | Contract data (number, effective and end dates, duration, activity, license, area, municipality), the waste classification (the quotation's waste types and wastes, ticked), the conclusion date in Gregorian and Hijri, the two parties, the container plan (the quotation's container lines with their collection frequency, totals, VAT and the amount in words), the regulation articles, the signatures and the municipality's supervision block |
| 2 | The technical terms, both parties' obligations and the general conditions, as the official form has them; the duration clause states the quotation's own duration |
| 3 | Only when the collection mechanism is a collection room (its name has غرفة / room): the room annex, with the contract data, photo boxes and the room's conditions |

## Data

`ozone/contract_print.py: waste_transport_contract(doc)` (registered in `hooks.py: jinja`) prepares everything in Arabic, whoever prints:

- **Producer (first party):** the quotation's party and contact; its commercial registration, national ID and tax number from the **facility's credentials**, matched by the document type's name (سجل / هوية / ضريب…).
- **Transporter (second party):** the Company; its MWAN license, municipal license and the municipality's qualification certificate (numbers and expiry dates) from the **Company's credentials** (موان / بلدي / تأهيل…). The footer carries the Company's address, registration, tax number, email and phone.
- **Municipality:** the facility's region's Municipality-level region.
- **Hijri dates:** `hijridate`.

Anything not on record prints as a dotted line to fill by hand. The municipality's logo is `ozone/public/images/print/madinah_municipality.jpeg`, embedded as a data URI so the PDF needs no request back to the site; the Company's logo fills the logo circle when it has one.
