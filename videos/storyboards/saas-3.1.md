# Storyboard: SaaS Building Blocks, lesson 3.1

> AI-drafted, not expert-reviewed. Part of the November 2026 content audit (`academy/audits/2026-11-content-audit.md`). Check every fact against the lesson and its claims register before production.

**Pick 2 of 3 for this course.** Three concrete failures (closed tab, hand-typed success URL, expired card) collapse into one rule that juniors get wrong on day one. Stripe's webhook model is stable, so the video will not date quickly.

## Don't Trust the Redirect (lesson 3.1, Subscriptions and payments)

**Why this lesson:** naive version, three failures, one rule. The lesson's own paragraph (03-money.md:24-30) is the script.
**Target viewer:** a developer adding a 'Buy' button to their first SaaS.
**Length:** about 80 s.

| # | Seconds | On screen | Visual / animation | On-screen text (EN) | Voice-over (EN) | Voice-over (AR) |
|---|---|---|---|---|---|---|
| 1 | 0-10 | Three lanes: Browser, Stripe, Beacon DB | 'Buy' click, then redirect, then `UPDATE organizations SET plan = 'pro'` | Pro plan: $29/month | "Beacon launches a 29-dollar Pro plan. Version one: the success page sets the plan to Pro. It works in the demo." | "يطلق Beacon خطة Pro بسعر 29 دولارًا شهريًا. في النسخة الأولى، تحوّل صفحة النجاح الخطة إلى Pro. وكل شيء يعمل في العرض التجريبي." |
| 2 | 10-22 | Browser tab closes mid-redirect | Payment lands in Stripe; the DB lane stays 'Free' | Charged. Still on Free. | "Then real life happens. A customer pays and closes the tab before the redirect finishes. Charged, and still on Free." | "ثم يأتي الواقع. عميل يدفع ويغلق الصفحة قبل اكتمال إعادة التوجيه، فيُخصم المبلغ ويبقى على الخطة المجانية." |
| 3 | 22-32 | A hand types /billing?success=true | DB flips to Pro with no payment | Pro for free | "Someone else spots the success URL and visits it by hand. Pro, without paying." | "وآخر يلاحظ رابط النجاح ويفتحه بنفسه، فيحصل على Pro دون أن يدفع." |
| 4 | 32-44 | Calendar flips three months; card icon cracks | Stripe shows 'renewal failed'; Beacon lane never hears | Card expired. Beacon never knew. | "Three months later a card expires and the renewal fails. Nothing in Beacon finds out, so they keep Pro forever." | "وبعد ثلاثة أشهر تنتهي صلاحية بطاقة ويفشل التجديد، ولا يعلم Beacon بشيء، فيبقى العميل على Pro إلى الأبد." |
| 5 | 44-58 | Redraw: a signed envelope travels from Stripe to Beacon | Signature seal checked; only this arrow may write the plan column; the redirect becomes a dotted 'UX only' line | Webhook = signed POST | "The fix: the redirect is just UX. Stripe tells your server what happened through webhooks, signed HTTP POSTs." | "الحل: إعادة التوجيه مجرد واجهة. يُبلغ Stripe خادمك بما حدث عبر الويب هوك، وهي طلبات HTTP موقَّعة." |
| 6 | 58-70 | A failed delivery retried over days | Retry arrows; the handler returns an error rather than a silent 200 | Fail loudly. Stripe retries. | "Stripe retries a failed delivery for up to three days in live mode, as long as your handler fails loudly instead of returning 200 and dropping the event." | "يعيد Stripe محاولة الإرسال الفاشل حتى ثلاثة أيام في الوضع الحقيقي، بشرط أن يُعلن معالجك الفشل بدل أن يردّ بـ200 ويتجاهل الحدث." |
| 7 | 70-80 | Two boxes: 'Provider = truth', 'Your DB = cached copy' | A sync arrow points one way only | The provider owns the truth about money. | "The payment provider owns the truth about money. Your database holds a cached copy. Open lesson 3.1 to build the handler." | "مزوّد الدفع هو المرجع الموثوق في كل ما يخص المال، وقاعدة بياناتك تحفظ نسخة منه فقط. افتح الدرس 3.1 لتبني المعالج." |

**Closing takeaway:** the payment provider owns the truth about money; webhooks keep your copy in sync, never the other way around.
**Call to action:** open lesson 3.1, Subscriptions and payments.

**Re-check before production:** Stripe's retry window ('up to three days in live mode') against current Stripe docs. For the Arabic audience, add a caption or description note that Stripe test mode is free and that the lesson also covers Polar/Paddle sandboxes (fix #8).
