# AI Usage Declaration — Member 3 (Teachable Machine / Computer Vision)

**Project:** AssureX Claim Engine — **Module:** Claim Summary Cards + Google Teachable Machine model
**Team member:** باسم [الاسم الكامل] (Member 3)
**Declaration date:** 2026-09-29

> هذا الملف إعلان الوحدة وفق SRS البند 1.8.9 والبند 15. عند تجميع المستودع يُدمج في `AI_USAGE.md` الرئيسي للفريق تحت عنوان «Member 3».

---

## 1. Tool name (اسم الأداة)

**Claude** (Anthropic) — عبر واجهة المحادثة (claude.ai / تطبيق الجوال).

لم تُستخدم أي أداة ذكاء اصطناعي أخرى في هذه الوحدة. لم تُستخدم صور مولّدة بالذكاء الاصطناعي: بطاقات Claim Summary Card كلها ترسمها السكربتات برمجيًا من بيانات CSV.

## 2. Purpose of use (الغرض)

1. توليد سكربتات Python للوحدة (توليد البطاقات، التنبؤ، التقييم، ربط الفئات، تسجيل النسخة، الاختبارات).
2. مراجعة الوحدة مقابل SRS وكشف الأخطاء الوثائقية.
3. صياغة الوثائق: `README_Member3.md`، `documentation/DEVLOG_Member3.md`، وهذا الملف.
4. مساعدة الطالب في قراءة نتائج التقييم وفهم أسباب الأخطاء.

## 3. Prompt or type of assistance requested (نوع المساعدة المطلوبة)

- **Code generation:** طلب سكربتات تحقق شروط SRS (2100 صورة تدريب، نسختان لكل Claim، عدم وضع أي تنبؤ أو ثقة أو قرار على البطاقة، فصل Train/Validation/Test).
- **Code review / bug fixing:** طلب مراجعة الاتساق بين ترتيب الفئات في `labels.txt` و`label_mapping.json`، وتوافق تحميل نماذج TM القديمة (Keras 2) مع TensorFlow الحديث.
- **Documentation drafting:** صياغة README وسجل التطوير وتنظيم مجلد `output/`.
- **Analysis:** تلخيص مصفوفات الالتباس وقياسات Precision/Recall.

## 4. Files or modules affected (الملفات المتأثرة)

| الملف | طبيعة مساهمة Claude |
|---|---|
| `generate_claim_cards.py` | كتابة السكربت (رسم البطاقات، الثيمات، `risk_level`) |
| `predict_tm.py` | كتابة السكربت (تحميل النموذج المحلي، التنبؤ بصيغة العقد) |
| `evaluate_model.py`, `run_comparison_30.py` | كتابة السكربتات |
| `build_label_mapping.py`, `set_model_version.py` | كتابة السكربتات |
| `tests/test_dataset_integrity.py`, `test_predict_contract.py`, `test_label_consistency.py`, `test_no_windows_paths.py` | كتابة الاختبارات |
| `README_Member3.md`, `documentation/*`, `AI_USAGE_Member3.md` | صياغة الوثائق بناءً على نتائج الطالب وملفات المشروع |
| مراجعة 2026-09-29 | تعديلات محدودة قام بها Claude بطلب من الطالب: حذف إحالات في التعليقات إلى وثيقة غير موجودة، تحويل مسارات ويندوز في ملفي JSON، إضافة `test_no_windows_paths.py`، تصحيح `requirements.txt`، توليد `sample_cards/`، تنظيم `output/evaluation/` |

**غير متأثر بالذكاء الاصطناعي:** تدريب نموذج Teachable Machine نفسه (نفّذه الطالب يدويًا في متصفح TM). النموذج المحلي `model/tm_model/keras_model.h5` هو التصدير الفعلي من TM.

**لا توجد استدعاءات لأي API ذكاء اصطناعي خارجي** داخل الكود (لا `requests` ولا `openai` ولا `anthropic`)، والتنبؤ يتم محليًا بالنموذج المُصدَّر. بذلك يتحقق شرط SRS: القرار النهائي لا يُنتَج عبر API توليدي خارجي.

## 5. Modifications performed by the team (ما فعله الطالب)

- **شغّل السكربتات بنفسه** وولّد صور البطاقات (2100 تدريب + 225 Validation + 225 Test + 30 مقارنة).
- **درّب نموذج Teachable Machine بنفسه** في عدة جولات (انظر `README_Member3.md` القسم 4) وضبط Epochs وBatch Size وLearning Rate.
- **اتخذ قرارات التصميم:**
  - لما كانت دقة النموذج الأول أقل من 75% وفشلت عدة محاولات لرفعها، قرر تغيير تصميم البطاقة (أُضيف شريط RISK LEVEL وأشرطة بصرية للتجاوز)، ونُفّذ التغيير في `generate_claim_cards.py` بمساعدة Claude.
  - جرّب في `run4` تغيير الأوزان وقيم مؤشر الخطورة، فانهارت دقة Valid_Claim (إلى ≈ 49–53%)، فرفضه وتراجع إلى تصميم `run3`.
  - اختار `run3` كنموذج معتمد بعد مقارنة الجولات.
- **راجع مخرجات Claude** (الأكواد والنتائج) بنفسه قبل اعتمادها.

## 6. Testing completed by the team (الاختبارات)

- تقييم النموذج على Validation (225) وTest (225) الكاملتين، وعلى عينة المقارنة (30 Claim من Test)؛ النتائج في `output/evaluation/` و`output/comparison_30_results.json`.
- تكرار التدريب 3 مرات بنفس الإعدادات (run1–run3) لقياس التذبذب.
- تشغيل الاختبارات الآلية: `python3 -m pytest tests/ -v` (سلامة البيانات وعدم التسريب، عقد التنبؤ، اتساق الفئات، عدم وجود مسارات ويندوز).
- فحص بصري لعيّنات البطاقات للتأكد من عدم ظهور تنبؤ أو ثقة أو قرار نهائي عليها.

## 7. Team member who verified the output (من تحقق)

**باسم [الاسم الكامل]** — Member 3.

## 8. Design decision disclosure — شريط RISK LEVEL

شريط `RISK LEVEL` على البطاقة مؤشر مشتق بقاعدة حسابية من حقول البطاقة الخام، وليس مخرج نموذج ولا قرارًا نهائيًا. تفاصيله وحدوده في `README_Member3.md` القسم 8.1، ويُصرَّح به هنا لأنه نُفّذ بمساعدة Claude ويرتبط بالفئات ارتباطًا قويًا في هذه البيانات.
