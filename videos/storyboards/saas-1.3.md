# Storyboard: SaaS Building Blocks, lesson 1.3

> AI-drafted, not expert-reviewed. Part of the November 2026 content audit (`academy/audits/2026-11-content-audit.md`). Check every fact against the lesson and its claims register before production.

**Pick 3 of 3 for this course.** A real, datable incident (Homakov, March 2012) that makes an invisible bug class (mass assignment) concrete, with a one-sentence moral: the server trusted the client to only send what the form showed.

## The Extra Field (lesson 1.3, Authorization)

**Why this lesson:** one real incident and one visible mechanism, plus a rule that carries over to every Beacon endpoint.
**Target viewer:** a junior who protects pages by hiding buttons.
**Length:** about 70 s.

| # | Seconds | On screen | Visual / animation | On-screen text (EN) | Voice-over (EN) | Voice-over (AR) |
|---|---|---|---|---|---|---|
| 1 | 0-10 | Date card, then a simple web form with visible fields | Cursor fills the fields | March 2012 | "In March 2012, a developer named Egor Homakov warned that Rails apps were widely open to mass assignment." | "في مارس 2012 حذّر مطوّر اسمه Egor Homakov من أن تطبيقات Rails معرّضة على نطاق واسع لثغرة الإسناد الجماعي." |
| 2 | 10-22 | Code card: `User.update(params[:user])` | Every request field flows into every column | Any column the request names | "Code like this would set any column the request mentioned, including ones the form never showed." | "شيفرة كهذه تحدّث أي عمود يرد في الطلب، حتى الأعمدة التي لا يعرضها النموذج." |
| 3 | 22-36 | The form, then an X-ray of the request revealing one extra field | The hidden field glows; a key icon lands on a 'rails/rails' repo | One extra field | "When nobody listened, he showed it on GitHub itself. One extra field in a form submission attached his SSH key to the Rails organization, and he pushed a commit to rails/rails." | "ولما لم يؤخذ تحذيره بجدية، أثبته على GitHub نفسه: حقل إضافي واحد في نموذج أضاف مفتاح SSH الخاص به إلى منظمة Rails، فدفع تعديلًا إلى مستودع rails/rails." |
| 4 | 36-46 | Caption over the repo | Text types out | The server trusted the client. | "Nobody forgot a permission check. The server trusted the client to send only what the form showed." | "لم ينسَ أحد فحص الصلاحيات، بل وثق الخادم بأن العميل لن يرسل إلا ما يعرضه النموذج." |
| 5 | 46-58 | Request passes an allow-list gate | Allowed fields pass; the extra field is stamped 'rejected' | Allow-list the fields | "Rails answered with strong parameters: an allow-list of fields the server accepts." | "وجاء رد Rails بالمعاملات القوية: قائمة سماح بالحقول التي يقبلها الخادم." |
| 6 | 58-70 | Three Beacon requests: GET another org's monitor, a member PATCHing role=owner, a viewer deleting a page with the button hidden | Each bounced by the server | User + action + object, every request | "Authorization is a question the server asks on every request, about a specific user, action and object. The answer never comes from the client. Open lesson 1.3." | "التفويض سؤال يطرحه الخادم مع كل طلب: هذا المستخدم، وهذا الإجراء، وهذا الكائن. والإجابة لا تأتي من العميل أبدًا. افتح الدرس 1.3." |

**Closing takeaway:** authorization is checked on the server, on every request, and the answer is never taken from the client.
**Call to action:** open lesson 1.3, Authorization.

**Re-check before production:** the incident details (date, SSH key, commit to rails/rails, GitHub suspending and then reinstating the account) against a primary source such as GitHub's 2012 post. Line 626 states them, but they are not in the course's verified claims. Do not show a real-looking exploit payload; keep the extra field generic.
