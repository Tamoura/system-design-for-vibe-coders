# Storyboard: Digital Practice, lesson 11.2

> AI-drafted, not expert-reviewed. Written on 2026-11-22, after the course was drafted, not as part of its writing. Check every fact against the lesson (`dprac/modules/11-govern.md`) and its claims register (`academy/claims/dprac.md`) before production.

**Pick 3 of 3 for this course.** One number in a web address, changed by one, shows another courier's pay. It is a one-second reveal that anyone can follow, it needs no outside statistics, and it leads straight into the lesson's two habits: a fifteen-minute threat model before building, and a test that fixes the whole class of bug, not one page. Every detail comes from the lesson.

## Change one number, see someone else's pay

**Lesson:** 11.2 Security and risk in everyday practice
**Why this lesson:** It turns security from "the security team's job" into an everyday habit of every team, with a concrete bug, a named weakness (broken access control), a risk register entry with an owner, and a fix that protects every future page.
**Target viewer:** A new engineer, tester or reviewer who reads pull requests and assumes passing tests mean a change is safe.
**Length:** about 85 seconds

## Scenes

**1. 0-10 s - A routine review**
- On screen: Yasmin's screen shows a pull request on the Courier Payouts team: "Add weekly earnings page". A browser bar shows an address ending in a courier's ID number, drawn as a placeholder such as ".../earnings/1041".
- Visual/animation: A row of green ticks: "All tests passed".
- On-screen text: "Qafila is fictional. All figures are illustrative, not benchmarks."
- VO (EN): "Yasmin is reviewing a pull request from a newer engineer. It adds a page showing a courier's weekly earnings. The page's address ends with the courier's ID number. Every test is green."
- VO (AR): "تراجع ياسمين طلب دمج (pull request) من مهندس أحدث عهدًا في الفريق. يضيف الطلب صفحة تعرض أرباح المندوب الأسبوعية، وينتهي عنوان الصفحة برقم تعريف المندوب. والاختبارات كلها ناجحة."

**2. 10-22 s - Plus one**
- On screen: In her test environment, Yasmin's cursor changes the last digit of the ID by one.
- Visual/animation: The page reloads with a different courier: a name, weekly earnings and the last digits of a bank account, all blurred placeholder values.
- On-screen text: "Changed the ID by one. Saw another courier's earnings, name and bank digits."
- VO (EN): "In her test environment she changes the number by one. Now she sees another courier's earnings, their name and the last digits of their bank account. The code passed every test, because every test used the right courier."
- VO (AR): "في بيئة الاختبار لديها، تغيّر الرقم بواحد، فترى أرباح مندوب آخر واسمه وآخر أرقام حسابه المصرفي. نجحت الشيفرة في كل الاختبارات، لأن كل اختبار استعمل المندوب الصحيح."

**3. 22-34 s - The weakness has a name**
- On screen: A phone and a server with a dotted line between them labelled "trust boundary". The phone sends "show earnings for 1042". The server checks "logged in? yes" and skips a second, missing check: "is this your record?"
- Visual/animation: Four labels pin onto the picture: "Asset: couriers' earnings and bank details", "Threat: a curious courier, or an outsider with one login", "Vulnerability: the page trusts the ID in the address", "Control: a server-side ownership check".
- On-screen text: "Broken access control: it checks that you are logged in, not that you may see this record."
- VO (EN): "The weakness has a name: broken access control. The system checks that you are logged in, but not that you may see this record. The server must not simply believe what the phone sends."
- VO (AR): "لهذا الضعف اسم: كسر التحكم في الوصول (broken access control). يتحقق النظام من أنك مسجِّل دخولك، لكنه لا يتحقق من أنه يحق لك رؤية هذا السجل تحديدًا. ولا ينبغي للخادم أن يصدّق ببساطة كل ما يرسله الهاتف."

**4. 34-46 s - Found by luck**
- On screen: A stopwatch: "Fix: one hour". A dice icon beside it: "Finding it: luck". Behind them, Dana's risk list: "14 rows, most written after incidents".
- Visual/animation: The payments partner's questionnaire slides in with one highlighted line: "How do development teams identify security risks in new features? Provide two recent examples."
- On-screen text: "Most risks were written down after the incident, not before the build."
- VO (EN): "The fix took an hour. Finding it took luck. That same month, the payments partner's questionnaire asked how teams find security risks in new features. Dana's risk list had fourteen rows, most written after incidents. She told Maha every team needed a cheap, repeatable way to ask what could go wrong."
- VO (AR): "استغرق الإصلاح ساعة، أما اكتشاف الخلل فكان بالحظ. وفي الشهر نفسه سأل استبيان شريك المدفوعات: كيف تحدد الفرق المخاطر الأمنية في الميزات الجديدة؟ كانت قائمة المخاطر لدى دانة تضم أربعة عشر صفًا، كُتب معظمها بعد حوادث. فقالت لمها إن كل فريق يحتاج إلى طريقة رخيصة قابلة للتكرار ليسأل: ما الذي قد يسوء؟"

**5. 46-60 s - Fifteen minutes before building**
- On screen: Four question cards in a row: "What are we working on? · What can go wrong? · What are we going to do about it? · Did we do a good enough job?" Under the second card, six small prompt words fan out: "Spoofing · Tampering · Repudiation · Information disclosure · Denial of service · Elevation of privilege" (STRIDE).
- Visual/animation: A 15-minute timer runs while a sketch of the earnings page is drawn and the "Information disclosure" card lights up over it.
- On-screen text: "Touches money, personal data, logins or access? Spend fifteen minutes on a threat model first."
- VO (EN): "That way is a threat model: four questions, asked before you build. What are we working on? What can go wrong? What will we do about it? Did we do a good enough job? A six-word prompt list, STRIDE, helps with the second. If a change touches money, personal data, logins or access, spend fifteen minutes on it first."
- VO (AR): "وهذه الطريقة هي نمذجة التهديدات (threat modelling): أربعة أسئلة تطرحها قبل أن تبني. على ماذا نعمل؟ ما الذي قد يسوء؟ ماذا سنفعل حياله؟ هل أحسنّا العمل بما يكفي؟ وتساعد قائمة من ست كلمات تُسمّى STRIDE في السؤال الثاني. فإن مسّ التغيير المال أو البيانات الشخصية أو تسجيل الدخول أو صلاحيات الوصول، فاقضِ فيه خمس عشرة دقيقة أولًا."

**6. 60-72 s - Rate it, treat it, own it**
- On screen: A risk register entry fills in line by line: "R-112: Courier earnings visible to other couriers · Likelihood High · Impact High · Treatment: Reduce (server-side ownership check; test for another courier's record; bank digits removed from page) · Owner: Courier Payouts team lead · Due: fix deployed within 2 days".
- Visual/animation: Four treatment chips sit beside it, "Reduce · Avoid · Transfer · Accept"; "Reduce" lights up. The "Owner" field glows: it names the team's lead, not "security".
- On-screen text: "Every risk gets a single owner and a date."
- VO (EN): "Then rate it and treat it. Easy to try, personal and financial data: high and high. The team reduced it with a server-side check and removed the bank digits from the page. The register entry names one owner, the team's own lead, not the security team."
- VO (AR): "ثم قيّم الخطر وعالجه. سهل التجربة، ويمسّ بيانات شخصية ومالية: احتمال مرتفع وأثر مرتفع. فقلّل الفريق الخطر بتحقق على الخادم، وأزال أرقام الحساب المصرفي من الصفحة. ويسمّي القيد في سجل المخاطر (risk register) مالكًا واحدًا هو قائد الفريق نفسه، لا فريق الأمن."

**7. 72-85 s - Closing card**
- On screen: A single test card, "Ask for another courier's record → expect a refusal", drops into a "service template" box. Copies flow out to many endpoints that take an ID.
- Visual/animation: A paper memo labelled "Remember to check ownership" fades; the test card stays lit.
- On-screen text: "Ask 'what can go wrong?' before you build, and give every risk an owner."
- VO (EN): "Yasmin's fix included a test that asks for another courier's record and expects a refusal. Dana had it added to the service template, for every endpoint that takes an ID. A test is fixed once; a memo is fixed until someone forgets. Open lesson 11.2 and threat model your next change."
- VO (AR): "تضمّن إصلاح ياسمين اختبارًا يطلب سجل مندوب آخر ويتوقع الرفض. وطلبت دانة إضافته إلى قالب الخدمة، لكل نقطة نهاية تستقبل رقم تعريف. فالاختبار يُصلح الأمر مرة واحدة، أما المذكّرة فتُصلحه حتى ينسى أحدهم. افتح الدرس 11.2 وابدأ نمذجة التهديدات لتغييرك القادم."

## Takeaway and call to action
Takeaway: security is an everyday habit of every team: ask "what can go wrong?" before you build, rate and treat each risk, give it one owner and a date, and turn every finding into a test that covers the whole class. CTA: open lesson 11.2 and run the four-question threat model on a small feature.

## Re-check before production
- The bug, the one-hour fix, the 14-row risk list, the partner's question and register entry R-112 come from the lesson's "Why it matters", "The essentials", "The risk register" and "Expert view" (`dprac/modules/11-govern.md`). The lesson gives no real ID numbers; the "1041/1042" in scenes 1 and 3 are on-screen placeholders and every name, amount and bank digit shown must be an obvious placeholder, blurred.
- The four questions are attributed in the lesson to the Threat Modeling Manifesto and STRIDE to Microsoft, both "as reported" (claims register dprac-11-005 and dprac-11-006, not yet checked). The video names neither source; if a source is added on screen, keep "as reported".
- Leave out the Verizon DBIR figures (31% and 13%; dprac-11-003 and dprac-11-012). They are "reported" only and describe that report's dataset, not Qafila's risk.
- The payments partner is unnamed in the lesson; show no real bank, payment company or card scheme on screen or in the questionnaire graphic.
- The access-key scare that led Qafila to hire Dana is told in lesson 8.3, not 11.2, so it is not used here. If production wants it as a cold open, take its wording from `dprac/modules/08-teams.md` ("misused for a few hours before it was revoked") and add 8.3 to this storyboard's sources.
- In the Arabic VO, STRIDE stays in Latin letters without parentheses; "Courier Payouts" follows the Arabic lesson («فريق مستحقات المندوبين») if it is shown on screen.
- Keep the "Qafila is fictional; figures illustrative" label on screen for the whole of scene 1 and as a small footer in scenes 2, 4 and 6.
