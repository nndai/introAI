# Kịch bản Video Mới — Giải thích "Building Safe and Robust AI Systems"

Phong cách 3Blue1Brown. Tổng: **~70 phút (1h10p)**. 12 Parts.

## Tổng quan

| Chương | Parts | Thời lượng | Chủ đề |
|--------|-------|------------|--------|
| Mở bài | Part 1 | 5 phút | Giới thiệu & bối cảnh |
| Chương 1 | Part 2–4 | 18 phút | Optimization & Implicit Layers |
| Chương 2 | Part 5–7 | 17 phút | Adversarial Robustness |
| Chương 3 | Part 8 | 9 phút | Khoa học thực nghiệm DL |
| Chương 4 | Part 9–11 | 16 phút | AI Safety |
| Kết luận | Part 12 | 5 phút | Tổng kết |

---

## Part 1 — Mở bài (5 phút) [00:00–05:00]

**Ý chính**: ICLR 2015 chỉ 31 bài báo nhưng sinh ra Adam, Attention, Adversarial Examples, VGG, nền tảng AlphaGo. Câu hỏi: nghiên cứu học thuật còn tạo ảnh hưởng lớn được không?

**Visual**: Timeline 2015→2025, 31 chấm sáng highlight bài landmark, so sánh quy mô hội nghị.

---

## Part 2 — Input Convex Neural Networks (6 phút) [05:00–11:00]

**Ý chính**: Hàm lồi là gì, tại sao lồi → dễ tối ưu. ReLU là lồi; trọng số dương → mạng lồi theo input. Ứng dụng: energy models, Lyapunov stability. Hạn chế: không plug vào kiến trúc thông thường.

**Visual**: Hàm lồi vs không lồi (2D), chồng ReLU, surface 3D 1 đáy vs nhiều đáy, quỹ đạo Lyapunov hội tụ.

---

## Part 3 — OptNet: Optimization trong Neural Network (5 phút) [11:00–16:00]

**Ý chính**: Layer giải bài toán tối ưu thay vì chỉ nhân ma trận. Output = nghiệm tối ưu. Tổng quát hoá linear+ReLU. Nhúng hard constraints. Ví dụ: Sudoku, lưới điện. Hạn chế: quá chuyên biệt.

**Visual**: Vùng ràng buộc C + đường đồng mức f + điểm nghiệm trượt, so sánh layer thường vs optimization layer, visual Sudoku.

---

## Part 4 — Deep Equilibrium Models (7 phút) [16:00–23:00]

**Ý chính**: Mạng hữu hạn → vô hạn lớp (weight tying + input injection). Hội tụ về điểm bất động z*=f(z*,x). Forward=root finding, Backward=implicit diff. Hiệu quả bộ nhớ. **Tại sao thất bại**: chậm gấp 2; xu hướng = nhiều params ít compute (MoE) — DEQ ngược lại.

**Visual**: Stack layers → vô hạn (morph), đồ thị y=f(z) cắt y=z (cobweb diagram), so sánh bộ nhớ, DEQ vs MoE trade-off.

---

## Part 5 — Adversarial Examples (6 phút) [23:00–29:00]

**Ý chính**: Nhiễu nhỏ imperceptible → phân loại sai. Panda→gibbon (FGSM 2015). Nguyên nhân: hàm phi tuyến biến vùng lồi → vùng méo mó. Defense ad hoc đều bị phá (Carlini). Cần certified methods.

**Visual**: Ảnh + nhiễu → label sai, decision boundary 2D phức tạp, vùng lồi qua ReLU → méo mó, timeline defense bị phá.

---

## Part 6 — Certified Robustness: Convex Relaxation (5 phút) [29:00–34:00]

**Ý chính**: Chứng minh không perturbation nào lừa được mạng. Qua ReLU → phi lồi → nới lỏng bằng convex hull → upper bound loss. Hoạt động MNIST (≤3% error), khó scale ImageNet.

**Visual**: ReLU exact region vs convex hull, input→relaxed region qua layers→bound output, loss thực vs upper bound.

---

## Part 7 — Randomized Smoothing (6 phút) [34:00–40:00]

**Ý chính**: Thêm Gaussian noise, phân loại nhiều lần, bỏ phiếu đa số. Smoothing san phẳng spike. Certified trong L2 ball. Scale được ImageNet. **Thất bại thực tế**: trade-off tệ — robust nhỏ nhưng accuracy giảm nhiều. Không ai dùng.

**Visual**: Ảnh + noise → nhiều bản → bỏ phiếu, boundary gồ ghề → mịn, biểu đồ radius vs accuracy trade-off.

---

## Part 8 — Khoa học thực nghiệm Deep Learning (9 phút) [40:00–49:00]

**Ý chính**:
- **Edge of Stability**: sharpness tăng đến 2/η rồi dừng, loss vẫn giảm non-monotonic (trái lý thuyết).
- **Disagreement ≈ Error**: 2 classifier khác init → tỷ lệ bất đồng ≈ tỷ lệ lỗi (liên quan calibration).
- **Agreement on the Line**: in-dist vs out-dist accuracy/agreement nằm trên đường thẳng → ước lượng OOD performance không cần label (ví dụ: xe tự lái trên tuyết).

**Visual**: Đồ thị sharpness+loss vs iterations, scatter y=x disagreement=error, accuracy/agreement lines trùng nhau.

---

## Part 9 — AI Safety: Automated Jailbreaks (5 phút) [49:00–54:00]

**Ý chính**: ChatGPT (2022) → model mạnh + không robust = nguy hiểm. Safety ≠ chỉ robustness. Jailbreak: query + adversarial suffix → model comply. Gradient descent tối ưu suffix trên open-source → transfer sang closed model. Đã khắc phục trên reasoning models.

**Visual**: Prompt → refusal vs prompt+suffix → comply, token grid + gradient arrows, P(comply) tăng dần, transfer diagram.

---

## Part 10 — Unlearning & Anti-distillation (6 phút) [54:00–60:00]

**Unlearning**: Model biết quá nhiều → quên chọn lọc. TOFU: 200 tác giả giả, fine-tune học, thử unlearn, đánh giá. Trade-off tệ giữa forget quality và utility.

**Anti-distillation**: Teacher sinh sample mà student không học được. Trade off likelihood vs "độ vô dụng". Teacher đúng ~70% nhưng student không học gì.

**Visual**: Forget quality vs utility scatter, Pareto frontier student vs teacher accuracy.

---

## Part 11 — Safety Pretraining (5 phút) [60:00–65:00]

**Ý chính**: Train internet data → RLHF cuối = "vá lỗi". Fine-tune benign → alignment mất. Giải pháp: lọc data (nhưng không hết), contextualize nội dung xấu, refusal training sớm, guardrail tags + backtrack. Chỉ train data "an toàn nhất" → thực ra tệ hơn.

**Visual**: Pipeline cũ vs mới (safety xuyên suốt), bar chart harmfulness theo method, fine-tune comparison.

---

## Part 12 — Kết luận (5 phút) [65:00–70:00]

**Ý chính**: Nhìn lại optimization→robustness→empirical science→safety. AI Safety = cơ hội lớn nhất cho academia. Thông điệp: tìm "ICLR 2015 tiếp theo". Quote Herb Simon 1965.

**Visual**: Timeline tổng hợp 2015→2025, impact vs effort diagram, spark animation kết.

---

## Bảng thời lượng

| Part | Tên | Thời lượng | Tích luỹ |
|------|-----|------------|----------|
| 1 | Mở bài | 5:00 | 05:00 |
| 2 | Input Convex Neural Networks | 6:00 | 11:00 |
| 3 | OptNet | 5:00 | 16:00 |
| 4 | Deep Equilibrium Models | 7:00 | 23:00 |
| 5 | Adversarial Examples | 6:00 | 29:00 |
| 6 | Convex Relaxation | 5:00 | 34:00 |
| 7 | Randomized Smoothing | 6:00 | 40:00 |
| 8 | Khoa học thực nghiệm DL | 9:00 | 49:00 |
| 9 | Automated Jailbreaks | 5:00 | 54:00 |
| 10 | Unlearning & Anti-distillation | 6:00 | 60:00 |
| 11 | Safety Pretraining | 5:00 | 65:00 |
| 12 | Kết luận | 5:00 | 70:00 |

## Ghi chú

- Chênh ±1 phút/Part OK, miễn tổng ≈ 70 phút (1h10p).
- Không có Q&A — nội dung hay được tích hợp vào Part liên quan.
- Mỗi Part là một phần của video tổng hợp, vì vậy làm sao để các part nối liền nhau 1 cách hợp lý và logic
