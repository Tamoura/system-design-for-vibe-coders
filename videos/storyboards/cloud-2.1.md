# Storyboard: Cloud & DevOps: Zero to Hero, lesson 2.1

> AI-drafted, not expert-reviewed. Part of the November 2026 content audit (`academy/audits/2026-11-content-audit.md`). Check every fact against the lesson and its claims register before production.

**Pick 2 of 3 for this course.** It turns a counter-intuitive fact (deleting a file in a later layer does not remove it from an earlier one) into a visual that prose cannot match, plus a second beat on tags that move and digests that don't. These are stable OCI fundamentals.

## The secret you deleted is still in the image

**Why this lesson:** Most learners believe `RUN rm .env` removes the secret. Stacked transparent layers show why it doesn't, and lead to the rule: name images by digest.

**Target viewer:** A developer who has written a Dockerfile or two but never inspected image layers.

**Length:** about 80 seconds.

| # | Seconds | On screen | Visual metaphor / animation | On-screen text (EN) | Voice-over (EN) | Voice-over (AR) |
|---|---|---|---|---|---|---|
| 1 | 0-10 | A Dockerfile with `FROM python:latest` and `COPY . .`; a size badge reads 1.3 GB | Badge inflates like a balloon | "It runs. Ship it?" | Yousef's first container runs. It's 1.3 GB, starts from python:latest, and copies the whole repo in. | الحاوية الأولى التي بناها يوسف تعمل. حجمها 1.3 غيغابايت، تبدأ من python:latest، وتنسخ المستودع كله. |
| 2 | 10-22 | Image shown as a stack of transparent sheets, one per build step | Sheets drop one on top of another | "An image = a stack of layers" | An image is a stack of layers, one per build step, each sitting on top of the last. | الصورة طبقات فوق بعضها، طبقة لكل خطوة بناء، وكل واحدة فوق التي قبلها. |
| 3 | 22-34 | `COPY . .` drops a red `.env` file into layer 2 | A small file falls onto a sheet | "COPY . . grabbed .env" | `COPY . .` quietly copied a local .env file with a database password. | الأمر COPY . . نسخ بصمت ملف .env محليًا فيه كلمة مرور قاعدة بيانات. |
| 4 | 34-46 | A later sheet `RUN rm .env` covers it with an opaque patch | Viewed from above, the file vanishes | "Deleted?" | A later step deletes it. Looking from the top, it's gone. | خطوة لاحقة تحذفه. ومن الأعلى يبدو أنه اختفى. |
| 5 | 46-58 | Camera peels the stack back; layer 2 still holds the red file | Sheets fan apart sideways | "Still in the earlier layer" | But layers are never edited. Peel the stack back and the password is still there for anyone who pulls the image. | لكن الطبقات لا تُعدَّل أبدًا. افصل الطبقات وستجد كلمة المرور ما زالت هناك لكل من يسحب الصورة. |
| 6 | 58-70 | A sticky note `mobile-api:staging` hops between two images; then a welded fingerprint `sha256:...` locks onto one | Sticky note moves; fingerprint stamp | "Tags move. Digests don't." | Second surprise: two pipelines pushed to the same tag, and staging ran whichever came last. A tag is a sticky note. A digest is a fingerprint. | مفاجأة ثانية: خطّان للنشر دفعا إلى الوسم نفسه، فشغّلت بيئة الاختبار آخر ما وصل. الوسم ورقة لاصقة، أما البصمة (digest) فثابتة لا تتغيّر. |
| 7 | 70-80 | Closing card: a small image with a lock icon and a digest | Image shrinks and locks | "Never copy secrets in. Build once. Deploy the digest." | Never copy secrets into any layer. Build once, and deploy that exact digest. Open lesson 2.1 to find the leak yourself. | لا تنسخ الأسرار إلى أي طبقة. ابنِ مرة واحدة وانشر البصمة نفسها. افتح الدرس 2.1 لتكتشف التسريب بنفسك. |

**Closing takeaway:** A file removed in a later layer still exists in the earlier one, and a tag can move while a digest always means the same bytes.

**Call to action:** Open lesson 2.1 and do the layer-secret hunt exercise.

**Re-check before production:** Keep the numbers (1.3 GB, nine-minute build) as the scenario's own figures. Confirm that the digest is shown in the `name@sha256:` form. Do not reuse the Knight Capital beat from this lesson, because other videos already use it.
