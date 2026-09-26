# Member 3 — Teachable Machine / Computer Vision Lead
## AssureX Claim Engine — دليل العمل التفصيلي

هذا الدليل يشرح كل خطوة عليك تنفيذها بدءًا من البيانات المرفوعة وحتى تسليم
عملك للفريق ورفعه على GitHub.

---

## 1. ما الذي تم إنجازه لك في هذه الحزمة

- سكربت `generate_claim_cards.py`: يقرأ ملفات `train.csv` / `validation.csv`
  / `test.csv` (بياناتك المُقسَّمة من Member 2: 1050 / 225 / 225، توزيع
  متوازن تمامًا 350/350/350 و75/75/75) ويحوّل كل Claim إلى صورة **Claim
  Summary Card** احترافية.
- تم **تشغيل السكربت فعليًا** وتوليد الصور كاملة، وهي موجودة داخل
  `output/tm_dataset/`.
- الالتزامات التي تم ضبطها تلقائيًا في السكربت (حسب دستور المشروع):
  - لا يوجد أي Python prediction / confidence / Final Decision داخل أي بطاقة.
  - كل بطاقة تحمل نفس `claim_id`.
  - **2 نسخة بصرية (Variation)** لكل Claim في التدريب فقط (ثيمات ألوان
    مختلفة + إزاحة بسيطة + تشويش خفيف) بدون تكرار حرفي للصورة.
  - إجمالي صور التدريب = **2100 صورة بالضبط** (1050 × 2) → يحقق الحد الأدنى
    المطلوب (2100).
  - Validation وTest صور منفصلة تمامًا عن التدريب (صورة واحدة لكل Claim،
    لم تُستخدم إطلاقًا في التدريب) — تُستخدم فقط للاختبار داخل واجهة
    Teachable Machine وللتوثيق.
  - تم تجهيز **30 صورة** (10 لكل فئة) من مجموعة Test فقط، غير مستخدمة في
    التدريب، داخل `output/comparison_30/` — هذه هي عيّنة المقارنة النهائية
    المطلوبة في السرد (SRS) لمقارنة Python Model مقابل TM Model.

### محتويات الحزمة

```text
generate_claim_cards.py     السكربت الرئيسي (يمكن إعادة تشغيله لتوليد variations إضافية)
predict_tm.py                سكربت تجربة النموذج بعد تصديره من Teachable Machine
evaluate_model.py            سكربت تقييم النموذج على Validation/Test الكاملتين (225+225 صورة)
requirements.txt             المتطلبات (Pillow لإنشاء البطاقات، tensorflow فقط عند التجربة المحلية)
data/splits/                 نسخة من ملفات train.csv / validation.csv / test.csv
output/
  tm_dataset/
    train/Valid_Claim/          700 claim × 2 صور = 1400 صورة
    train/Invalid_Claim/        700 claim × 2 صور = 1400 صورة
    train/Manual_Review/        700 claim × 2 صور = 1400 صورة
    validation/<3 مجلدات>/      75+75+75 صورة (Holdout - لا تُرفع للتدريب)
    test/<3 مجلدات>/            75+75+75 صورة (Holdout - لا تُرفع للتدريب)
  comparison_30/               30 صورة (10 لكل فئة) لاختبار المقارنة النهائي
  manifest.csv                 سجل كل صورة: claim_id, split, class, variation, path
  comparison_30_manifest.json  قائمة الـ30 Claim المستخدمة بالمقارنة + الفئة الحقيقية
  label_mapping.json           تعريف الفئات الثابت (index ↔ اسم الفئة ↔ اسم المجلد)
  training_log.json            إحصائيات التوليد (عدد الصور لكل فئة، تحقق الحد الأدنى)
```

> ملاحظة تسمية: الفئات الأصلية في البيانات هي `Valid` / `Invalid` /
> `Manual Review`، وتم استخدام أسماء مجلدات آمنة بدون مسافات
> (`Valid_Claim`, `Invalid_Claim`, `Manual_Review`) لأن Teachable Machine
> والعديد من أدوات الملفات لا تتعامل جيدًا مع المسافات/الأسماء المركّبة في
> أسماء Classes. **استخدم هذه الأسماء بالضبط كأسماء Classes داخل TM** حتى
> يبقى الـmapping ثابتًا مع بقية الفريق (احفظ `label_mapping.json` كمرجع).

---

## 2. الخطوات التي عليك تنفيذها أنت الآن

### الخطوة 1 — (اختياري) تشغيل السكربت على جهازك للتأكد

```bash
pip install -r requirements.txt
python3 generate_claim_cards.py --data-dir data/splits --out-dir output --variations 2
```

الصور جاهزة بالفعل في الحزمة، لكن نفّذ هذا فقط إن أردت التأكد أو توليد
variations أكثر (مثلاً `--variations 3`) لتقوية تعميم النموذج لاحقًا.

### الخطوة 2 — إنشاء مشروع على Google Teachable Machine

1. افتح: **https://teachablemachine.withgoogle.com/train**
2. اختر **Image Project** → **Standard image model**.
3. أنشئ **3 Classes** بنفس الأسماء بالضبط:
   - `Valid_Claim`
   - `Invalid_Claim`
   - `Manual_Review`

### الخطوة 3 — رفع صور التدريب فقط

لكل Class، اسحب وأفلت **مجلد التدريب المطابق فقط** (وليس Validation ولا
Test):

| Class في TM | المجلد الذي تسحبه |
|---|---|
| Valid_Claim | `output/tm_dataset/train/Valid_Claim/` (1400 صورة) |
| Invalid_Claim | `output/tm_dataset/train/Invalid_Claim/` (1400 صورة) |
| Manual_Review | `output/tm_dataset/train/Manual_Review/` (1400 صورة) |

⚠️ **لا ترفع مجلدات validation أو test أو comparison_30 إلى التدريب** —
هذه محجوزة للاختبار فقط، ورفعها للتدريب يُعتبر Data Leakage ويخالف قاعدة
"فصل Training/Validation/Testing" في الدستور.

### الخطوة 4 — إعدادات التدريب (Advanced)

اضغط **Advanced** قبل التدريب وضَع (نقطة بداية جيدة، يمكنك تجربة غيرها
وتوثيق ما جرّبت):

- Epochs: 50
- Batch Size: 16
- Learning Rate: 0.001

ثم اضغط **Train Model** وانتظر حتى تكتمل (Teachable Machine تعمل داخل
المتصفح، فلا تُغلق الصفحة أثناء التدريب).

### الخطوة 5 — اختبار النموذج قبل التصدير

استخدم قسم **Preview** في نفس الصفحة، وجرّب رفع عدد من صور
`output/tm_dataset/validation/` (صور لم يرها النموذج إطلاقًا). سجّل:

- هل التصنيفات صحيحة تقريبًا؟
- هل هناك فئة معينة يخطئ بها كثيرًا (مثلاً يخلط Manual Review مع Invalid)؟

وثّق هذه الملاحظات — ستحتاجها في "توثيق Incorrect Predictions" المطلوب
منك بالدستور.

### الخطوة 6 — تصدير النموذج

1. اضغط **Export Model**.
2. اختر تبويب **Tensorflow**.
3. اختر **Keras** (وليس TensorFlow.js ولا TensorFlow Lite، لأن باقي
   المشروع Python/Backend).
4. اضغط **Download my model** — سيُنزَّل ملف مضغوط يحتوي:
   - `keras_model.h5`
   - `labels.txt`

### الخطوة 7 — وضع النموذج داخل هيكل المشروع

```text
model/
└── tm_model/
    ├── keras_model.h5
    └── labels.txt
```

### الخطوة 8 — تجربة محلية بـ `predict_tm.py`

```bash
pip install tensorflow numpy
python3 predict_tm.py --image output/comparison_30/<اسم_صورة>.jpg --model-dir model/tm_model
```

يجب أن يعطيك JSON يحتوي `tm_prediction` و`tm_probabilities` و
`tm_confidence` و`model_version` — وهذه بالضبط الحقول التي يحتاجها
Member 5 (راجع جدول العقد المشترك في الدستور).

### الخطوة 9 — تشغيل مقارنة الـ30 Claim (تحضيرًا للتسليم النهائي)

شغّل `predict_tm.py` على الصور الثلاثين في `output/comparison_30/`، واحفظ
النتائج (مثلاً في `output/comparison_30_results.json`) لمقارنتها لاحقًا
بنتائج Member 1 (Python Model) عند تنفيذ خطوة "Model Prediction and
Confidence Comparison" في الـSRS.

---

## 3. ما الذي يجب رفعه على GitHub، ومتى، وكيف

### متى ترفع؟

ترفع **بعد** أن يكون لديك:
- نموذج مُدرَّب ومُصدَّر فعليًا (وليس قبل ذلك — لا ترفع كود بلا نتيجة تدريب
  حقيقية، فالدستور يمنع "Commit وحيد لمجموعة تغييرات كبيرة" بلا معنى).
- نتائج اختبار Preview موثّقة.
- تشغيل ناجح لـ `predict_tm.py` على الأقل على عينة واحدة.

### ماذا ترفع بالضبط (وماذا **لا** ترفع)

| ✅ ارفعه | ❌ لا ترفعه |
|---|---|
| `generate_claim_cards.py` | مجلد `tm_dataset/train` كاملاً (196 ميجا صور — يُثقل الريبو) |
| `predict_tm.py` | مجلد `tm_dataset/validation` و`tm_dataset/test` بالكامل |
| `requirements.txt` | — |
| `manifest.csv` | — |
| `label_mapping.json` | — |
| `training_log.json` | — |
| `output/comparison_30/` (2.6 ميجا فقط — صغير ومطلوب للفريق) | — |
| `output/comparison_30_manifest.json` و`comparison_30_results.json` | — |
| `evaluate_model.py` | — |
| `output/validation_evaluation.json`، `output/validation_full_report.json`، `output/test_full_report.json` | — |
| `output/evaluation_notes.md` | — |
| `model/tm_model/keras_model.h5` و`labels.txt` (عادة بضع ميجابايت، مقبول في Git عادي) | إن تجاوز حجم الموديل ~50-100 ميجا، استخدم Git LFS بدل رفعه مباشرة |
| `README_Member3.md` | — |

**السبب:** GitHub وDستور الفريق لا يمنعان رفع صور، لكن رفع عشرات الآلاف
من صور Training يُبطئ الـclone لكل الفريق دون فائدة حقيقية — البيانات
الأصلية (`train.csv`) وسكربت التوليد كافيان لإعادة إنتاج نفس الصور بالضبط
(السكربت يستخدم `seed` ثابت). أضف مجلد الصور الكبير إلى `.gitignore`.

### أوامر Git التفصيلية

```bash
# 1) تأكد أنك على فرع خاص بمهمتك (لا تعمل مباشرة على main)
git checkout -b feat/tm-claim-cards

# 2) أنشئ .gitignore يستثني الصور الكبيرة
cat >> .gitignore << 'EOF'
output/tm_dataset/train/
output/tm_dataset/validation/
output/tm_dataset/test/
EOF

# 3) أضف الملفات المطلوبة فقط
git add generate_claim_cards.py predict_tm.py evaluate_model.py requirements.txt \
        output/manifest.csv output/label_mapping.json output/training_log.json \
        output/comparison_30/ output/comparison_30_manifest.json output/comparison_30_results.json \
        output/validation_evaluation.json output/validation_full_report.json output/test_full_report.json \
        output/evaluation_notes.md \
        model/tm_model/keras_model.h5 model/tm_model/labels.txt \
        README_Member3.md .gitignore

# 4) Commit برسالة واضحة (حسب تنسيق الدستور)
git commit -m "feat(tm): add claim card generator, trained TM model and full evaluation (val 73.33%, test 74.67%)"

# 5) ارفع الفرع
git push origin feat/tm-claim-cards

# 6) افتح Pull Request للمراجعة قبل الدمج مع main
```

> إن كان حجم `keras_model.h5` كبيرًا جدًا (أكبر من ~50 ميجا) ولم يقبله
> GitHub، استخدم Git LFS:
> `git lfs install && git lfs track "*.h5" && git add .gitattributes`
> قبل تنفيذ باقي الأوامر.

---

## 4. تنسيق التسليم للفريق (حسب "قاعدة التسليم بين الأعضاء")

عند انتهائك، سلّم بهذا الشكل بالضبط (كما ينص الدستور):

```text
Module: Teachable Machine / Computer Vision

Input: Common Claim Dataset (train.csv/validation.csv/test.csv من Member 2)

Output:
tm_prediction
tm_probabilities
tm_confidence
model_version

Files:
generate_claim_cards.py
predict_tm.py
model/tm_model/keras_model.h5
model/tm_model/labels.txt
output/label_mapping.json
output/training_log.json
output/comparison_30/  (30 صورة اختبار مقارنة)

Test:
تم اختبار النموذج على مجموعتي Validation وTest الكاملتين (225 صورة لكل منهما،
لم تُستخدما في التدريب) + عينة المقارنة النهائية (30 صورة) + Preview داخل
Teachable Machine.

النتائج:
| المجموعة | الدقة الإجمالية | Valid_Claim | Manual_Review | Invalid_Claim |
|---|---|---|---|---|
| Validation (225) | 73.33% | 90.67% | 77.33% | 52.00% |
| Test (225) | 74.67% | 80.00% | 77.33% | 66.67% |
| Comparison (30) | 80.00% | 9/10 | 8/10 | 7/10 |

أضعف فئة في الحالتين هي Invalid_Claim (يُخلط غالبًا مع Manual_Review).
التفاصيل الكاملة والتوصية موثقة في: `output/evaluation_notes.md`
```

---

## 5. ما الذي ينقص لإكمال المهمة بالكامل (تحتاج فعله أنت خارج هذه البيئة)

هذه الخطوات تتطلب متصفحًا وحسابًا فعليًا على Google، ولا يمكن تنفيذها هنا:

1. **رفع صور التدريب فعليًا وتدريب النموذج** على
   teachablemachine.withgoogle.com (الخطوات 2-6 أعلاه).
2. **تصدير النموذج** وتنزيله على جهازك.
3. **تحديد إعدادات التدريب النهائية** بعد التجربة (Epochs/Batch/LR) إن
   احتجت تعديلها عن القيم الافتراضية المقترحة.
4. **التنسيق مع Member 2** للتأكد أن `train.csv/validation.csv/test.csv`
   المرفوعة هي **النسخة النهائية المعتمدة** من الفريق (وليست نسخة مبدئية
   ستتغير لاحقًا) — لأن أي تغيير لاحق في الـDataset يعني إعادة توليد كل
   الصور وإعادة التدريب.
5. **التنسيق مع Member 6** إن كان سيتم إنشاء الـClaim Summary Card داخل
   التطبيق نفسه (Live) وليس فقط كملفات ثابتة للتدريب — في هذه الحالة نفس
   دالة `render_card()` يمكن استدعاؤها من الـBackend مباشرة لإنشاء بطاقة
   لأي Claim جديد في وقت التشغيل الفعلي.
