# Storyboard: Secure AI & Application Security: Zero to Hero, lesson 3.3

> AI-drafted, not expert-reviewed. Part of the November 2026 content audit (`academy/audits/2026-11-content-audit.md`). Check every fact against the lesson and its claims register before production.

**Pick 2 of 3 for this course.** A one-action attack anyone can picture (10233 becomes 10234) and a timeless takeaway: hiding a button is not access control.

## Change one number: broken access control
**Lesson:** 3.3 Authorisation: broken access control, IDOR and multi-tenancy
**Why this lesson:** The attack is a single visible keystroke, and it separates authentication from authorisation cleanly.
**Target viewer:** a developer, PM or system owner who builds or owns a multi-customer web app.
**Length:** about 75 s

| # | Sec | On screen | Visual metaphor / animation | On-screen text (EN) | Voice-over EN | Voice-over AR |
|---|---|---|---|---|---|---|
| 1 | 0-10 | A tester logged in as an Uploader at Company A, viewing invoice /api/invoices/10233/pdf | A browser address bar zooms in | Signed in. Company A. | A tester signs in as a normal user at Company A and opens one of the company's invoices. | مختبِرة تسجّل الدخول كمستخدمة عادية في الشركة (أ) وتفتح إحدى فواتير شركتها. |
| 2 | 10-20 | The digits tick from 10233 to 10234 | An odometer clicks forward | +1 | She changes one number in the address. | تغيّر رقمًا واحدًا في العنوان. |
| 3 | 20-32 | Company B's invoice opens: supplier names, amounts, bank details | One folder swaps for another company's folder | Company B's invoice | And downloads Company B's invoice, with supplier names, amounts and bank details. | فتنزّل فاتورة الشركة (ب)، بأسماء الموردين والمبالغ والتفاصيل المصرفية. |
| 4 | 32-44 | Two doors: 'Who are you?' (green tick) and 'Is this yours?' (missing) | A building where the front door is guarded but every inner door is open | Authentication worked. Authorisation was missing. | Login worked every time. What was missing was the question: is this record yours? | تسجيل الدخول نجح في كل مرة، أما الغائب فهو السؤال: هل هذا السجلّ لك؟ |
| 5 | 44-56 | A hidden 'Approve payment' button; then a direct request to that endpoint is accepted | A curtain is pulled over a door that is still unlocked | Hiding a button is not access control | The approve button was hidden from her role, but the server still accepted the request. | زرّ الموافقة كان مخفيًّا عن دورها، لكن الخادم ظلّ يقبل الطلب. |
| 6 | 56-68 | A server-side checklist: function, object, property; deny by default | Three locks click shut on the server, not the screen | Check on the server, every request | Check on the server, on every request: may this role do this, to this object, and to these fields? | تحقّق على الخادم مع كل طلب: هل يحقّ لهذا الدور هذا الفعل، على هذا السجلّ، وفي هذه الحقول؟ |
| 7 | 68-75 | End card: Noura's rule, then a test showing another tenant being refused | A red 'refused' stamp | Prove another user is refused | No endpoint ships without a test that proves another user is refused. Open lesson 3.3. | لا تُطلق أي نقطة وصول دون اختبار يثبت أن المستخدم الآخر يُرفض. افتح الدرس 3.3. |

**Closing takeaway:** Hiding a button is not access control; decide on the server, deny by default.
**Call to action:** Open lesson 3.3 and build the access-control matrix.
**Re-check before production:** this is a staging test with test companies, so do not present it as a real breach; keep OWASP rank numbers (A01, 2025) out of the script; leave out the Optus aside, which the lesson itself hedges.
