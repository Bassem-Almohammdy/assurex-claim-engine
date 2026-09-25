# AssureX Claim Engine

تطبيق ويب مبني بلغة Python يهدف إلى أتمتة تقييم مطالبات الضمان (Warranty Claims) باستخدام نموذج تصنيف Python ونموذج Google Teachable Machine بشكل مستقل، ثم مقارنة نتائجهما مع قواعد الضمان للوصول إلى قرار نهائي: Valid Claim / Invalid Claim / Manual Review.

## فكرة المشروع
يحلل النظام تفاصيل المنتج، معلومات الشراء، وصف العطل، تاريخ الإصلاحات، وشروط الضمان، ثم:
1. يصنّف المطالبة عبر نموذج Python (Machine Learning).
2. يولّد بطاقة ملخص بصرية للمطالبة (Claim Summary Card) ويصنّفها عبر Google Teachable Machine.
3. يقارن النتيجتين ويطبّق قواعد الضمان للوصول إلى القرار النهائي.

## الفريق والمسؤوليات
| العضو | الدور |
|---|---|
| Member 1 | AI / ML Lead |
| Member 2 | Dataset |
| Member 3 | Teachable Machine / Computer Vision |
| Member 4 | OCR / استخراج البيانات من المستندات |
| Member 5 | Backend / Rules Engine |
| Member 6 | Frontend / Testing |
## هيكل المشروع
