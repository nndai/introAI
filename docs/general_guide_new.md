# Hướng dẫn chung làm video (Manim) — Phiên bản mới

## Mục tiêu

- **Không** làm lại video gốc 1:1. Tạo video **giải thích lại** kiến thức một cách **dễ hiểu, trực quan**.
- Phong cách: **3Blue1Brown** / video giải thích toán học Trung Quốc.
- Thời lượng: **~70 phút (1h10p)**. Ngôn ngữ: **tiếng Việt**, xưng "chúng ta".

## Khác biệt so với video gốc

| Video gốc (Zico Kolter @ ICLR 2025) | Video mới |
|--------------------------------------|-----------|
| Talk/keynote, kể chuyện cá nhân | Explainer giáo dục, giải thích kỹ thuật |
| Slide tĩnh + người nói | Animation Manim động, sơ đồ |
| Khán giả đã biết nền tảng | Dẫn dắt từ cơ bản |

## Nguyên tắc 3Blue1Brown

1. **Trực giác trước, công thức sau**
2. **Một ý tại một thời điểm**
3. **Animation là ngôn ngữ chính** — hình ảnh tự kể chuyện
4. **Build-up dần dần** trên cùng hình minh hoạ
5. **Kết nối các khái niệm** — ý mới liên quan ý trước
6. **Màu sắc có ý nghĩa** nhất quán xuyên video

## Kiến thức cốt lõi cần truyền tải

1. Bối cảnh ICLR 2015 & vai trò nghiên cứu học thuật
2. Input Convex Neural Networks
3. OptNet / Optimization Layers
4. Deep Equilibrium Models
5. Adversarial Examples
6. Certified Robustness — Convex Relaxation
7. Randomized Smoothing
8. Khoa học thực nghiệm DL (Edge of Stability, Disagreement ≈ Error, Agreement on the Line)
9. AI Safety — Automated Jailbreaks
10. Unlearning (TOFU benchmark)
11. Anti-distillation Sampling
12. Safety Pretraining

## Quy trình

1. Đọc `docs/subtitles_en.txt` nắm ý chính. Xem `docs/parts_video_new.md` cho cấu trúc mới.
2. Viết script: `src/partX/partX_script.txt`, tốc độ 140-160 từ/phút.
3. Storyboard: mỗi concept = chuỗi animation. Ưu tiên hình học, sơ đồ luồng, morph, zoom.
4. Code Manim: `src/partX/partX.py`. Font tiếng Việt, color palette nhất quán.
5. Render: `manim -pql` (preview) độ phân giải thấp 480p 30fps để xem trước, tôi sẽ tự render độ phân giải cao sau.
6. Voiceover + phụ đề tiếng Việt khớp timing.

## Checklist

- [ ] Kiến thức chính xác về mặt kỹ thuật (không sai sót nội dung) — sai kiến thức = 0 điểm
- [ ] Giải thích dễ hiểu, trực quan
- [ ] Tổng ≈ 70 phút (1h10p)
- [ ] Animation build-up dần dần, color palette nhất quán
- [ ] Voiceover rõ ràng + phụ đề tiếng Việt

## Ghi chú quan trọng

- **"Kiến thức chính xác" = nội dung kỹ thuật phải đúng**, không có sai sót về mặt khoa học.
- **Không** yêu cầu giống 100% video gốc — cách giải thích, ví dụ, thứ tự trình bày hoàn toàn tự do.
- Dùng `subtitles_en.txt` làm **nguồn tham khảo** để hiểu ý tác giả, không phải để dịch/copy.
- Được phép thêm ví dụ, phép so sánh, intuition riêng — miễn không sai lệch kỹ thuật.
- Độ dài mỗi part cần chính xác theo `docs/parts_video_new.md`.