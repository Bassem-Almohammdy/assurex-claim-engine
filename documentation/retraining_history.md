# سجل إعادة تدريب نموذج Teachable Machine (Member 3)

يوثّق هذا الملف الجولات السابقة (مطلوب في SRS: Retraining details + Incorrectly classified samples).
الأرقام مأخوذة من ملفات التقييم الأصلية التي أُزيلت من `output/` بعد تلخيصها هنا.

| الجولة | الإصدار | Validation (225) | Test (225) | Invalid_Claim (val/test) | ملاحظة |
|---|---|---|---|---|---|
| v0 | tm-20260925-224736 | 73.33% | 74.67% | 52.00% / 66.67% | أول نموذج |
| v1 | tm-2026-09-27-v1 | 78.22% | 79.11% | 61.33% / 61.33% | 29 خطأ Invalid→Manual_Review على كل مجموعة تقريبًا |
| v2 (الحالي) | tm-2026-09-28-v2-final | 80.89% | 83.11% | 80.00% / 89.33% | تصميم بطاقة جديد (Risk Banner)، Epochs 80، LR 0.0005، Batch 16 |

## ما تغيّر بين الجولات
- v0 → v1: التغييرات غير موثّقة في المشروع (لا توجد إعدادات محفوظة لـ v0/v1) — أكملها من ذاكرتك أو من سجل TM.
- v1 → v2: تغيير تصميم البطاقة حسب تعليقات `generate_claim_cards.py` (شريط RISK LEVEL، شريط تجاوز الضمان بثلاث درجات، مؤشر نسبة claim/price).
- نمط الخطأ الأساسي في v0/v1: Invalid_Claim ↔ Manual_Review. في v2 انخفض هذا الخلط لكن ظهر خلط Manual_Review → Invalid_Claim (15 حالة على Test).

## مشاكل تقنية سُجّلت أثناء العمل
- ترتيب الفئات في `labels.txt` (Manual_Review, Invalid_Claim, Valid_Claim) مختلف عن الترتيب اليدوي في المولّد → حُلّ بـ `build_label_mapping.py` + اختبار `tests/test_label_consistency.py`.
- نماذج TM (Keras 2) لا تُحمَّل على TF ≥ 2.16 بدون `tf-keras` و`TF_USE_LEGACY_KERAS=1`.
