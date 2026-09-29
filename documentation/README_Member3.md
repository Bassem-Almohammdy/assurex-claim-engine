# Member 3 — Teachable Machine / Computer Vision
## AssureX Claim Engine — التسليم النهائي

**النموذج المعتمد:** `tm-2026-09-28-v2-final` (وهو **run3** في سجل التدريب، القسم 4)
**آخر تحديث:** 2026-09-29

> هذا الملف هو **المرجع الوحيد** لوثائق الوحدة. يجمع: التشغيل، سجل جولات التدريب الكامل، تقرير التقييم التفصيلي (كان سابقًا `output/evaluation_notes.md`)، القيود المعروفة، وما ينقص قبل التسليم.

---

## 1. الحالة الحالية

| البند | الحالة |
|---|---|
| مولّد البطاقات `generate_claim_cards.py` | جاهز — يحتاج مجلد `fonts/` (موجود) |
| التقسيم | 1050 / 225 / 225 Claim (350 / 75 / 75 لكل فئة)، بلا تسريب — يتحقق منه `tests/test_dataset_integrity.py` |
| صور التدريب | **2100** = 1050 Claim × نسختين (700 لكل فئة) |
| Validation / Test | 225 صورة لكل منهما (75 لكل فئة)، مرسومة بالنسخة `variation=0` |
| عينة المقارنة | 30 صورة (10 لكل فئة)، مأخوذة من Claims الـTest فقط |
| البطاقات | لا تحتوي Python prediction ولا confidence ولا Final Decision ولا اسم الفئة (يتحقق منه `test_generator_never_writes_model_outputs_on_cards`) |
| النموذج المُصدَّر | `model/tm_model/` |
| الدقة Validation / Test / Comparison | **80.89% / 83.11% / 76.67%** |
| هدف SRS (≥ 85% على Test) | **غير محقق** — الفجوة 5 صور من 225، وهي ضمن هامش الخطأ (انظر القسم 8) |
| صور `output/comparison_30/` | النتائج موجودة، **الصور نفسها غير موجودة في هذه الحزمة** — انسخها من جهازك |

---

## 2. هيكل المشروع

```text
generate_claim_cards.py   توليد بطاقات Claim Summary Card من CSV
predict_tm.py             تنبؤ TM على صورة واحدة بصيغة العقد (للـBackend / Member 5)
run_comparison_30.py      تنبؤ TM على عينة الـ30 دفعة واحدة
evaluate_model.py         تقييم شامل على Validation أو Test الكاملتين
build_label_mapping.py    بناء label_mapping.json من labels.txt الحقيقي (إلزامي بعد كل تصدير)
set_model_version.py      تسجيل إعدادات ونتائج كل نسخة في model_version.json
requirements.txt          كل المتطلبات (Pillow / numpy / tensorflow / tf-keras / pytest)
README_Member3.md         هذا الملف
AI_USAGE_Member3.md       إعلان استخدام الذكاء الاصطناعي (SRS 1.8.9 / 15)
.gitignore                يستثني venv* و output/tm_dataset/ و model/tm_model_run*/

fonts/                    DejaVuSans + Bold (مطلوبة للمولّد)
data/splits/              train.csv / validation.csv / test.csv (من Member 2)
model/tm_model/           keras_model.h5, labels.txt, model_version.json  ← النموذج المعتمد
tests/                    test_dataset_integrity / test_predict_contract / test_label_consistency / test_no_windows_paths
screenshots/              لقطات شاشة TM (تُضاف من جهازك)
sample_cards/             15 بطاقة عيّنة (5 لكل فئة) لعرض شكل البطاقة دون توليد الداتا كاملة
documentation/            retraining_history.md, DEVLOG_Member3.md

output/
  manifest.csv                 سجل كل صورة: claim_id, split, claim_status, variation, file_path
  training_log.json            إحصائيات التوليد (عدد الصور لكل مجموعة وفئة)
  label_mapping.json           تعريف الفئات الثابت للنموذج المعتمد (يستهلكه Member 5)
  comparison_30_manifest.json  قائمة الـ30 Claim + الفئة الحقيقية
  comparison_30_results.json   نتائج النموذج على الـ30 (يستهلكه Member 5)
  comparison_30/               صور الـ30 (غير مرفقة في الحزمة — انسخها من جهازك)
  evaluation/
    validation_evaluation.json   التقييم الكامل على Validation + قائمة الأخطاء
    test_evaluation.json         التقييم الكامل على Test + قائمة الأخطاء
    tm_metrics.json              ملخص مصفوفات الالتباس والـPrecision/Recall للمجموعتين
  tm_dataset/                  يُعاد توليده، غير مرفوع لـGit
```

> **تسمية الفئات:** البيانات الأصلية `Valid` / `Invalid` / `Manual Review`، وأسماء الـClasses في Teachable Machine وكل الأكواد هي `Valid_Claim` / `Invalid_Claim` / `Manual_Review` بلا مسافات. استخدمها **حرفيًا** عند إنشاء أي Class جديد. مخرجات `predict_tm.py` تعود دائمًا بالأسماء القانونية (Valid / Invalid / Manual Review).

---

## 3. التشغيل السريع

```bash
pip install -r requirements.txt

# توليد الصور (نسختان لكل Claim = النموذج الحالي)
python3 generate_claim_cards.py --data-dir data/splits --out-dir output --variations 2

# تنبؤ بطاقة واحدة
python3 predict_tm.py --image output/comparison_30/<file>.jpg --claim-id 542

# تقييم كامل + مقارنة الـ30
python3 evaluate_model.py --dataset-dir output/tm_dataset/validation --save-json output/evaluation/validation_evaluation.json
python3 evaluate_model.py --dataset-dir output/tm_dataset/test --save-json output/evaluation/test_evaluation.json
python3 run_comparison_30.py

# الاختبارات
python3 -m pytest tests/ -v
```

> أعِد تشغيل `build_label_mapping.py` بعد أي تصدير جديد من TM. المولّد لا يكتب `label_mapping.json` عمدًا.

---

## 4. سجل جولات التدريب الكامل (Training Log)

عدد كل مجموعة تقييم 225 صورة (75 لكل فئة). أرقام run1–run4 والـBaseline من سجل التجارب المحلي؛ أرقام run3 تطابق ملفات `output/evaluation/*.json` تمامًا.

**إعدادات ثابتة بعد Baseline:** Epochs = 80، Batch Size = 16 (أدنى قيمة متاحة في واجهة TM؛ لا يوجد خيار 8)، Learning Rate = 0.0005، على نفس صور `train/` (2100 صورة).

| الجولة | التصميم / الإعداد | Val | Test | Invalid (Val/Test) | Manual_Review (Val/Test) | Valid (Val/Test) | القرار |
|---|---|---|---|---|---|---|---|
| **Baseline** (`tm-20260925-224736`، v0) | تصميم أولي، Epochs=50 / Batch=16 / LR=0.001 | 73.33% | 74.67% | 52.00 / 66.67 | 77.33 / 77.33 | 90.67 / 80.00 | مرجع البداية |
| محاولات مبكرة غير مُوثَّقة الإعدادات (تشمل `tm-2026-09-27-v1`) | تحسينات بصرية أولى | 78.22% (×2) | 79.11% / 84.44% | 61.33–70.67 / 61.33–80.00 | 78.67–80.00 / 68.00–84.00 | 84.00–94.67 / 89.33–97.33 | رُفضت لعدم توثيق الإعدادات — ومنها جاءت إلزامية `set_model_version.py` |
| **run1** | + راية خطورة لونية كبيرة (`risk_level`, score ≥ 2) | 76.00% | **83.11%** | **85.33 / 97.33** | 68.00 / 68.00 | 74.67 / 84.00 | Invalid ممتازة، Manual_Review تراجعت |
| **run2** | نفس تصميم run1، إعادة تدريب (قياس التذبذب) | 76.00% | 76.89% | 86.67 / 90.67 | 74.67 / 70.67 | 66.67 / 69.33 | أكّد نمط run1 |
| **run3 — ✅ المعتمد** (`tm-2026-09-28-v2-final`) | نفس تصميم run1/2، تكرار ثالث | **80.89%** | **83.11%** | 80.00 / 89.33 | 76.00 / 72.00 | **86.67 / 88.00** | أفضل توازن عبر الفئات الثلاث |
| **run4** | ترجيح مضاعف للإشارتين القويتين في `risk_level` | 69.78% | 72.89% | 89.33 / 97.33 | 70.67 / 68.00 | **49.33 / 53.33** | **مرفوض** — انهيار Valid_Claim؛ أُلغي التعديل |

**القراءة الإحصائية:**
- عبر run1→run3 (نفس الإعدادات والتصميم) تراوحت Invalid_Claim بين 80–87% على Validation: نجاح متكرر وليس صدفة.
- Manual_Review تراجعت في الجولات الثلاث معًا عن Baseline (77.33%) إلى 68–76%: الاتجاه تكرر ثلاث مرات مستقلة، فهو أثر تصميمي لراية الخطورة أكثر منه ضوضاء تدريب.
- محاولة إصلاحه في run4 كسرت Valid_Claim، فتقرر الاعتماد على run3.

**ما تغيّر بين الإصدارات (مختصر):**
- Baseline → v1: التغييرات غير موثّقة.
- v1 → run1–3: تصميم بطاقة جديد (شريط RISK LEVEL، شريط تجاوز الضمان بثلاث درجات، مؤشر نسبة claim/price).
- نمط الخطأ الرئيسي في Baseline/v1: Invalid ↔ Manual_Review. في run3 انخفض لكن ظهر خلط Manual_Review → Invalid (15 حالة على Test).

**مشاكل تقنية سُجّلت أثناء العمل:**
- ترتيب `labels.txt` (Manual_Review, Invalid_Claim, Valid_Claim) يختلف عن الترتيب اليدوي في المولّد → حُلّ بـ`build_label_mapping.py` + `tests/test_label_consistency.py`.
- نماذج TM (Keras 2) لا تُحمَّل على TF ≥ 2.16 بدون `tf-keras` و`TF_USE_LEGACY_KERAS=1` (مضبوط داخل السكربتات).

**محتوى `model/tm_model/model_version.json` الفعلي:**
```json
{
  "version": "tm-2026-09-28-v2-final",
  "trained_on": "2100 images, variations=2, risk-banner design",
  "epochs": 80,
  "learning_rate": 0.0005,
  "batch_size": 16,
  "validation_accuracy": 0.8089,
  "test_accuracy": 0.8311
}
```

---

## 5. التقييم التفصيلي للنموذج المعتمد

**المصدر:** `output/evaluation/validation_evaluation.json`، `test_evaluation.json`، `tm_metrics.json`، و`output/comparison_30_results.json`.

### 5.1 الدقة الإجمالية

| المجموعة | الدقة | Valid | Invalid | Manual Review |
|---|---|---|---|---|
| Validation (225) | 182/225 = **80.89%** | 65/75 = 86.67% | 60/75 = 80.00% | 57/75 = 76.00% |
| Test (225) | 187/225 = **83.11%** | 66/75 = 88.00% | 67/75 = 89.33% | 54/75 = 72.00% |
| Comparison (30) | 23/30 = **76.67%** | 9/10 | 7/10 | 7/10 |

> متطلب SRS (Non-Functional #4): دقة ≥ 85% على مطالبات غير مرئية. النموذج الحالي لم يبلغه (83.11% على Test).
> عينة الـ30 لها هامش خطأ كبير (≈ ±15 نقطة)، فرقمها الأقل من Test **متوقع وليس تناقضًا**. تُستخدم فقط للمقارنة صفًّا بصف مع Python Model (Member 1)؛ المقياس الرسمي هو Test الكاملة.

### 5.2 Confusion Matrix (الصفوف = الحقيقي، الأعمدة = المتوقع)

**Test**

| | Manual Review | Invalid | Valid |
|---|---|---|---|
| Manual Review | 54 | 15 | 6 |
| Invalid | 8 | 67 | 0 |
| Valid | 9 | 0 | 66 |

**Validation**

| | Manual Review | Invalid | Valid |
|---|---|---|---|
| Manual Review | 57 | 11 | 7 |
| Invalid | 15 | 60 | 0 |
| Valid | 10 | 0 | 65 |

### 5.3 Precision / Recall / F1

| الفئة | Test P / R / F1 | Validation P / R / F1 |
|---|---|---|
| Manual Review | 0.761 / 0.720 / 0.740 | 0.695 / 0.760 / 0.726 |
| Invalid | 0.817 / 0.893 / 0.854 | 0.845 / 0.800 / 0.822 |
| Valid | 0.917 / 0.880 / 0.898 | 0.903 / 0.867 / 0.884 |
| Macro-F1 | 0.830 | 0.811 |

### 5.4 نمط الأخطاء

- **لا يوجد خلط مباشر Valid ↔ Invalid إطلاقًا** (0 حالة في المجموعتين)؛ كل خطأ يمر عبر Manual Review.
- الفئة الأضعف **Manual Review** (recall 72% على Test)، وSRS يطلب اكتشاف هذه الحالات بشكل موثوق.
- 11 من 38 خطأ على Test (و18 من 43 على Validation) كانت بثقة ≥ 0.90: الثقة العالية وحدها لا تضمن صحة التنبؤ، فيجب أن يعتمد Member 5 على مقارنة النموذجين وقواعد الضمان لا على ثقة TM منفردة.
- قوائم الأخطاء الكاملة (الملف، الحقيقي، المتوقع، الثقة) داخل `validation_evaluation.json` و`test_evaluation.json`.

---

## 6. تدريب Teachable Machine

1. Image Project → Standard image model، 3 Classes بالأسماء: `Valid_Claim`, `Invalid_Claim`, `Manual_Review`.
2. ارفع فقط `output/tm_dataset/train/<Class>/` (700 صورة لكل Class). لا ترفع validation أو test أو comparison_30.
3. Advanced: Epochs = 80، Batch Size = 16، Learning Rate = 0.0005.
4. Export → Tensorflow → Keras → Download، وضع `keras_model.h5` و`labels.txt` في `model/tm_model/`.
5. شغّل بهذا الترتيب: `build_label_mapping.py` ← `evaluate_model.py` (Validation ثم Test) ← `set_model_version.py`.

---

## 7. صيغة المخرجات (العقد المشترك)

```json
{
  "claim_id": "542",
  "tm_prediction": "Invalid",
  "tm_probabilities": {"Manual Review": 0.362, "Invalid": 0.638, "Valid": 0.0},
  "tm_confidence": 0.638,
  "tm_raw_label": "Invalid_Claim",
  "model_version": "tm-2026-09-28-v2-final"
}
```

> هذا مثال حقيقي من `comparison_30_results.json`: الفئة **الحقيقية** للـClaim 542 هي Manual Review، والنموذج أخطأ فتوقّع Invalid.

للتصنيف من الـBackend مباشرة: `predict(pil_image, claim_id=...)` (يُحمَّل النموذج مرة واحدة). على Member 5 تثبيت `tf-keras` مع `tensorflow`.
زمن التنبؤ (وفق مراجعة 2026-09-29): أول استدعاء يشمل تحميل النموذج (~4.7 ث)، وما بعده ≈ 0.06 ث (شرط SRS: 5 ثوانٍ).

> ملاحظة للفريق: القسمان 5 و6 في الدستور يسميان حقول TM بأسماء مختلفة (`tm_prediction` مقابل `prediction`). الكود يتبع القسم 5، ويجب أن يقرر الفريق الصيغة النهائية.

---

## 8. القيود المعروفة (موثّقة صراحة)

1. **لم يتحقق معيار ≥ 85% على Test** (83.11%، الفجوة 5 صور). لكن الرقم غير حاسم في أي اتجاه: وفق مراجعة 2026-09-29، إعادة توليد صور التقييم وتقييم **النموذج نفسه** أعطت Validation 81.33% / Test 85.78% / Comparison 90.00%. هامش الخطأ ≈ ±5 نقاط لـ225 صورة و≈ ±15 لـ30 صورة، فلا تقل «لم نحقق 85%» ولا «حققناه» بثقة.
2. **Manual_Review أضعف فئة** بعد إدخال راية الخطورة (68–76% مقابل 77.33% في Baseline). لم يُجرَّب بعد أي من الحلّين: رفع Manual_Review إلى 3 نسخ، أو `--variations 3` لكل الفئات.
3. **شريط RISK LEVEL** مؤشر مشتق من حقول البطاقة الخام، ويرتبط بالفئة ارتباطًا قويًا في هذه البيانات (كل بطاقات Invalid الـ500 تظهر HIGH). تفاصيله ومبرر توافقه مع قيود SRS في القسم 8.1؛ وقد يسأل المقيّم عنه، فيُصرَّح به أيضًا في `AI_USAGE_Member3.md`.
4. **Test لم تعد مجموعة محجوبة تمامًا:** تصميم البطاقة عُدّل بعد الاطلاع على أخطاء Validation وTest، وعينة الـ30 مأخوذة منها. واختيار run3 من بين عدة تجارب اعتمادًا جزئيًا على Test يُدخل تحيّز اختيار بسيط؛ الرقم على بيانات غير مرئية قد يكون أقل بقليل. التقييم الحقيقي سيكون على الـHidden Claims.
5. **فرق توزيع بين التدريب والتقييم:** Validation/Test مرسومة بالنسخة `variation=0` (ثيم أزرق) بينما تدرّب النموذج على النسختين 1 و2 فقط (برتقالي/أخضر). قد يخفض هذا الأرقام؛ الحل المقترح `--variations 3` وإعادة التدريب.
6. **إعادة التوليد غير متطابقة بايتيًا:** التسلسل العشوائي مُبذَّر (`random.seed(42)` + seed لكل Claim/نسخة)، لكن `Image.effect_noise` غير مُبذَّر، فتتطابق الصور في المحتوى لا في البكسلات. لذلك يُنصح بتسليم صور التقييم نفسها (`comparison_30/`) وعدم إعادة توليدها.
7. **الـDataset (مسؤولية Member 2):** كل Claims الـInvalid عمر منتجها أكبر من مدة الضمان وبأحد 3 أنواع ضرر فقط (`INVALID_ONLY_DAMAGE_TYPES`)، فالمسألة سهلة نسبيًا بقاعدة واحدة، ولن تكون الأرقام بهذا المستوى على Hidden Claims. يجب إبلاغ Member 2.
8. **البطاقة لا تعرض «المستندات الناقصة»** (SRS Step 7) لأن الـDataset لا يحتوي هذا الحقل — قرار مشترك مع Member 2.
9. Teachable Machine لا يوفر Batch Size = 8؛ أدنى قيمة متاحة 16.

### 8.1 مذكرة تصميمية: شريط RISK LEVEL على البطاقة

**ما هو؟** شريط لوني في أعلى البطاقة يعرض `RISK LEVEL: LOW / MEDIUM / HIGH`، تحسبه الدالة `risk_level()` في `generate_claim_cards.py` من أربع حقول خام موجودة أصلًا على البطاقة نفسها، بمنح نقطة لكل شرط تحقق:

| # | الشرط | الحقل |
|---|---|---|
| 1 | نسبة مبلغ المطالبة إلى سعر الشراء ≥ 0.65 | `claim_amount` / `purchase_price` |
| 2 | عدد الإصلاحات السابقة > 2 | `repair_history` |
| 3 | نوع الضرر أحد: Physical Damage / Unknown / Water Damage | `damage_type` |
| 4 | عمر المنتج تجاوز مدة الضمان | `product_age_months` / `warranty_period_months` |

مجموع النقاط ≥ 2 → HIGH، وواحدة → MEDIUM، وصفر → LOW.

**لماذا نرى أنه لا يخالف قيود المحتوى على البطاقة؟**
نص SRS (Step 7، والبند xx في المتطلبات الوظيفية، والبند 5 في المخرجات) يمنع أن تحتوي البطاقة على **تنبؤ Python Model** أو **درجة الثقة** أو **نتيجة/قرار Claim النهائي**. والشريط لا يتضمن أيًّا منها:

1. **ليس مخرج نموذج.** تُحسب قيمته بقاعدة حسابية ثابتة من بيانات الـClaim نفسها، ولا يُستدعى أي نموذج (لا Python Model ولا Teachable Machine) عند رسمه.
2. **ليس قرارًا ولا اسم فئة.** قيمه (LOW/MEDIUM/HIGH) لا تطابق فئات التصنيف (Valid / Invalid / Manual Review)، ولا تعني قبول المطالبة أو رفضها. القرار النهائي يُبنى لاحقًا في Backend (Member 5) بجمع تنبؤ النموذجين وقواعد الضمان.
3. **لا يقرأ التصنيف الحقيقي.** الدالة لا تستخدم `claim_status` إطلاقًا، وتُطبَّق بالطريقة نفسها على Train وValidation وTest. لذلك لا يوجد تسريب للجواب.
4. **ترميز بصري لبيانات موجودة على البطاقة.** يؤدي الدور نفسه الذي تؤديه عناصر أخرى في البطاقة (شريط الضمان الملوّن، نقاط سجل الإصلاح، شريط نسبة المطالبة إلى السعر): تلخيص بصري لحقول خام، وليس معلومة جديدة من خارج البيانات.
5. **«مستوى الخطورة» مفهوم وارد في SRS نفسه:** البند xlii (Search and Filtering) يذكر `risk level` ضمن حقول البحث والتصفية في التطبيق، أي أنه متغير مشتق مقبول في النظام وليس قرارًا.
6. **موثّق ومُصرَّح به.** تصميمه وحدوده مذكوران هنا وفي `AI_USAGE_Member3.md`، ويتحقق الاختبار `test_generator_never_writes_model_outputs_on_cards` من أن المولّد لا يكتب أي مخرج نموذج على البطاقة.

**تنبيه:** يبقى تفسير «قرار نهائي» في يد المقيّم؛ لذلك نصرّح بالشريط ونوثّق حدوده بدل الاكتفاء بالتبرير. وSRS البند 1.8.7 يمنع «hard-coded test answers»: والشريط لا يحوي أي إجابة اختبار، فالعتبات مقاسة على `train.csv` فقط وتُطبَّق بالقاعدة نفسها على كل الأقسام.

**شفافية بشأن الارتباط بالفئة.** قياس فعلي على الـ1500 Claim (كل الأقسام):

| الفئة الحقيقية | HIGH | MEDIUM | LOW |
|---|---|---|---|
| Invalid (500) | 500 | 0 | 0 |
| Manual Review (500) | 329 | 140 | 31 |
| Valid (500) | 0 | 147 | 353 |

الارتباط القوي سببه أن حقول الـDataset نفسها تفصل بين الفئات بوضوح (كل Invalid فيها بمنتج تجاوز ضمانه ونوع ضرر من ثلاثة أنواع فقط)، والشريط يُظهر هذه الحقول فقط. وهو **لا** يعني أن الشريط يقرأ الجواب. لكن ينبغي تفسير أرقام الدقة في القسمين 4 و5 على ضوء ذلك، فقد تكون أعلى من أدائها على Hidden Claims ذات توزيع مختلف.

---

## 9. إعادة الإنتاج الكاملة من الصفر

```bash
pip install -r requirements.txt

# 1) توليد الصور
python3 generate_claim_cards.py --data-dir data/splits --out-dir output --variations 2

# 2) التدريب على Teachable Machine (يدوي، متصفح) — القسم 6

# 3) ضع keras_model.h5 و labels.txt في model/tm_model/

# 4) طابق الفئات وسجّل النسخة (إلزامي، بهذا الترتيب)
python3 build_label_mapping.py --model-dir model/tm_model --out output/label_mapping.json
python3 evaluate_model.py --dataset-dir output/tm_dataset/validation --model-dir model/tm_model --save-json output/evaluation/validation_evaluation.json
python3 evaluate_model.py --dataset-dir output/tm_dataset/test --model-dir model/tm_model --save-json output/evaluation/test_evaluation.json
python3 set_model_version.py --model-dir model/tm_model \
  --trained-on "2100 images, variations=2, risk-banner design" \
  --epochs 80 --lr 0.0005 --batch-size 16 \
  --val-accuracy <من نتيجة Validation> --test-accuracy <من نتيجة Test> \
  --tag <اسم وصفي>

# 5) تحقق آلي
python3 -m pytest tests/ -v

# 6) مقارنة الـ30
python3 run_comparison_30.py --model-dir model/tm_model --out output/comparison_30_results.json
```

النتيجة المتوقعة بنفس الإعدادات: قريبة من run1/2/3 (76–81% Validation، 77–83% Test). التذبذب بين 76–97% لفئة Invalid_Claim تحديدًا موثّق أعلاه وليس خطأ إن ظهر.

---

## 10. ما ينقص قبل التسليم (لا يستطيع أحد سواك إكماله)

1. نسخ `output/comparison_30/` الأصلية (30 صورة) من جهازك، ولا تعيد توليدها؛ وأي لقطات شاشة: مشروع TM، الفئات الثلاث، Preview، الأخطاء.
2. **دليل مشروع Teachable Machine** — SRS البند 5 يقبل «project link **or permitted project evidence**». أضف هنا ما تيسّر:
   - رابط المشروع على Drive (إن حُفظ): `[أضف الرابط]`
   - رابط النموذج المرفوع (Export Model ← Upload my model): `[أضف الرابط]`
   - ملف المشروع المحمَّل (`.tm`) إن وُجد، ولقطات الشاشة في `screenshots/`
3. ~~سجل التطوير~~ — أُنجز: `documentation/DEVLOG_Member3.md`. راجع تواريخ run1–run4 وعدّلها إن اختلفت.
4. ~~إعلان الذكاء الاصطناعي~~ — أُنجز: `AI_USAGE_Member3.md`. أضف اسمك الكامل، وأي تعديل يدوي أجريتَه على الكود، ثم ادمجه في `AI_USAGE.md` الرئيسي للفريق.
5. نشر `output/tm_dataset/` **الأصلية من جهازك** كملف مضغوط في Drive أو Release مع وضع الرابط هنا (تسليم صور Train/Validation/Test). (عيّنة `sample_cards/` جاهزة بالفعل.)
6. مناقشة مع الفريق: شريط RISK LEVEL، نقص «المستندات الناقصة»، وخاصية الـDataset.
7. الاستعداد لشرح أي دالة في `generate_claim_cards.py` و`predict_tm.py`.
8. (اختياري) تثبيت Seed للضجيج وحفظ صور التقييم، ثم إعادة التدريب بـ`--variations 3`.

---

## 11. ما يُرفع على GitHub

| ✅ ارفعه | ❌ لا ترفعه |
|---|---|
| كل ملفات `.py` في الجذر و`tests/` | `output/tm_dataset/train\|validation\|test/` (يُعاد توليدها) |
| `requirements.txt`, `README_Member3.md`, `AI_USAGE_Member3.md`, `.gitignore` | `venv*/` أو أي بيئة افتراضية |
| `fonts/`, `data/splits/*.csv`, `documentation/` | `model/tm_model_run*/` (أرشيف تجارب محلي؛ الأرقام موثّقة في القسم 4) |
| `model/tm_model/keras_model.h5`, `labels.txt`, `model_version.json` | `preview*.png/jpg`, `*.zip` في الجذر |
| `output/manifest.csv`, `label_mapping.json`, `training_log.json` | — |
| `output/comparison_30/`, `comparison_30_manifest.json`, `comparison_30_results.json` | — |
| `output/evaluation/`, `sample_cards/` | — |

```bash
git checkout -b feat/tm-claim-cards
git add *.py requirements.txt README_Member3.md AI_USAGE_Member3.md .gitignore screenshots/ \
        fonts/ data/splits/ tests/ documentation/ \
        model/tm_model/keras_model.h5 model/tm_model/labels.txt model/tm_model/model_version.json \
        output/manifest.csv output/label_mapping.json output/training_log.json \
        output/comparison_30/ output/comparison_30_manifest.json output/comparison_30_results.json \
        output/evaluation/ sample_cards/
git commit -m "feat(tm): claim card generator, risk-banner design, trained model v2-final (val 80.89%, test 83.11%)"
git push origin feat/tm-claim-cards
```

> حجم `keras_model.h5` الفعلي ≈ 2.4 ميجا. إن تجاوز ~50 ميجا مستقبلًا استخدم Git LFS: `git lfs install && git lfs track "*.h5" && git add .gitattributes`.

---

## 12. تنسيق التسليم للفريق

```text
Module: Teachable Machine / Computer Vision

Input : Claim Summary Card (JPG/PIL) + claim_id
        (التدريب من Common Claim Dataset: train.csv / validation.csv / test.csv من Member 2)

Output: claim_id, tm_prediction, tm_probabilities, tm_confidence, model_version

Files : generate_claim_cards.py
        predict_tm.py
        model/tm_model/keras_model.h5, labels.txt, model_version.json
        output/label_mapping.json
        output/training_log.json
        output/comparison_30/ , output/comparison_30_results.json

Tests : tests/*.py + Validation 225 + Test 225 (غير مستخدمتين في التدريب)
        + عينة مقارنة 30 ضد Python Model. تفاصيل الجولات في README_Member3.md القسم 4.

النتائج النهائية (run3 = model/tm_model المعتمد):
| المجموعة         | الدقة  | Valid  | Manual_Review | Invalid |
| Validation (225) | 80.89% | 86.67% | 76.00%        | 80.00%  |
| Test (225)       | 83.11% | 88.00% | 72.00%        | 89.33%  |
| Comparison (30)  | 76.67% | 9/10   | 7/10          | 7/10    |

Known limitations: لم يتحقق ≥ 85% على Test (الفجوة 5 صور، وضمن هامش الخطأ)؛
Manual Review هي الأضعف (recall 72%)؛ شريط RISK LEVEL قرار تصميمي بانتظار اعتماد الفريق.
التفاصيل: القسمان 5 و8 في هذا الملف.
```

---

## 13. مطابقة مخرجات الوحدة مع SRS (البند 1.10.5 وما يتصل به)

| المطلوب في SRS | الحالة | أين |
|---|---|---|
| Google Teachable Machine project link **or permitted project evidence** | ⏳ ينقصك | القسم 10 البند 2 |
| Screenshots of the three classes (Valid / Invalid / Manual Review) | ⏳ ينقصك | `screenshots/` |
| Training configuration | ✅ | القسمان 4 و6 |
| Number of images per class | ✅ 700 تدريب لكل فئة، 75 Validation، 75 Test | القسم 1 و`output/training_log.json` |
| Training observations | ✅ | القسم 4 |
| Incorrectly classified samples | ✅ | القسم 5.4 و`output/evaluation/*.json` (حقل `errors`) |
| Retraining details | ✅ | القسم 4 و`documentation/retraining_history.md` |
| Exported model + label file + model version | ✅ | `model/tm_model/` |
| Model test screenshots | ⏳ ينقصك | `screenshots/` |
| Sample Claim Summary Cards | ✅ 15 بطاقة | `sample_cards/` |
| Claim Summary Card images: train / validation / test | ⏳ من جهازك (الأصلية، لا المعاد توليدها) | رابط Drive في القسم 10 البند 5 |
| Claim ID ↔ image filename mapping file | ✅ | `output/manifest.csv`، `output/comparison_30_manifest.json` |
| البطاقة بلا Python prediction / confidence / القرار النهائي | ✅ (مع مذكرة RISK LEVEL) | القسم 8.1 |
| Development log (SRS 1.8.3) | ✅ | `documentation/DEVLOG_Member3.md` |
| AI_USAGE declaration (SRS 1.8.9 و15) | ✅ | `AI_USAGE_Member3.md` |
| دقة ≥ 85% على unseen test | ⚠️ 83.11% (ضمن هامش الخطأ) | القسمان 5 و8 |

**فريق المشروع:** محمد الجرادي (Member 1 — نموذج Python ML)، عبد الرحمن الحرفي (Member 2)، باسم (Member 3 — Teachable Machine / Computer Vision)، أحمد الكبش (Member 4)، عبد الرحمن العريقي (Member 5)، محمد الشرعبي (Member 6).
