"""Part 10 — Unlearning & Anti-distillation Sampling
Thời lượng mục tiêu: 6 phút (54:00 – 60:00 trong video mới)

Render preview:
    manim -pql src/part10/part10.py Part10Scene
Render chất lượng cao:
    manim -pqh src/part10/part10.py Part10Scene
"""

from __future__ import annotations

import numpy as np
from manim import *

# ── Color palette: đồng bộ với các part trước ────────────────────────
BG           = "#0d1117"
TITLE_COLOR  = "#58a6ff"
ACCENT       = "#f0883e"
ACCENT2      = "#a371f7"
GOOD         = "#3fb950"
TEXT_COLOR   = "#e6edf3"
DIM_TEXT     = "#8b949e"
CARD_BG      = "#161b22"
CARD_STROKE  = "#30363d"
HIGHLIGHT    = "#ffa657"
PAPER_BLUE   = "#58a6ff"
PAPER_GREEN  = "#3fb950"
PAPER_RED    = "#f85149"
PAPER_YELLOW = "#d29922"
PAPER_PURPLE = "#a371f7"
PAPER_ORANGE = "#f0883e"
PAPER_TEAL   = "#39d353"


class Part10Scene(Scene):
    """Explainer cho gỡ học, TOFU benchmark và anti-distillation sampling."""

    def construct(self):
        Text.set_default(font="sans-serif", font_size=24)
        Paragraph.set_default(font="sans-serif", font_size=24)
        self.camera.background_color = BG

        self.scene1_unlearning_motivation()
        self.scene2_tofu_benchmark()
        self.scene3_forget_utility_tradeoff()
        self.scene4_anti_distillation_intuition()
        self.scene5_pareto_frontier()

    # ═══════════════════════════════════════════════════════════════════
    # SCENE 1 — Unlearning motivation (≈42s)
    # ═══════════════════════════════════════════════════════════════════
    def scene1_unlearning_motivation(self):
        title = Text("Unlearning: không chỉ bảo model im lặng", font_size=34, color=TITLE_COLOR)
        self._fit_width(title, 12.2)
        title.to_edge(UP, buff=0.45)

        model = self._large_model("Model đã học").move_to(LEFT * 3.65)
        model[3].next_to(model[0], UP, buff=0.1)

        knowledge = VGroup(
            self._knowledge_chip("lập trình", PAPER_BLUE),
            self._knowledge_chip("toán", PAPER_GREEN),
            self._knowledge_chip("sinh học", PAPER_PURPLE),
            self._knowledge_chip("kiến thức nguy hiểm", PAPER_RED),
            self._knowledge_chip("văn học", PAPER_ORANGE),
        ).arrange(DOWN, buff=0.1).scale(0.86).move_to(model[0].get_center())

        patch = self._small_card(
            "Vá ở cuối",
            "Fine-tune để\nnói từ chối.",
            PAPER_BLUE,
        ).move_to(RIGHT * 3.25 + UP * 1.15)

        remove = self._small_card(
            "Unlearning thật sự",
            "Loại bỏ kiến thức\nkhỏi bên trong.",
            PAPER_RED,
        ).move_to(RIGHT * 3.25 + DOWN * 1.15)

        arrow_patch = Arrow(model.get_right(), patch.get_left(), buff=0.12, color=PAPER_BLUE, stroke_width=2.4)
        arrow_remove = Arrow(model.get_right(), remove.get_left(), buff=0.12, color=PAPER_RED, stroke_width=2.4)

        note = Paragraph(
            "Nếu kiến thức vẫn nằm trong tham số,",
            "một jailbreak tốt có thể kéo nó ra lại.",
            alignment="center",
            font_size=23,
            color=TEXT_COLOR,
        ).to_edge(DOWN, buff=0.4)

        self.play(Write(title), run_time=0.9)
        self.play(FadeIn(model, scale=0.9), run_time=0.9)
        self.play(FadeOut(VGroup(model[1], model[2])), run_time=0.45)
        self.play(LaggedStart(*[FadeIn(k, shift=UP * 0.12) for k in knowledge], lag_ratio=0.1), run_time=1.4)
        self.wait(6.0)
        self.play(GrowArrow(arrow_patch), FadeIn(patch), run_time=1.0)
        self.wait(4.5)
        self.play(GrowArrow(arrow_remove), FadeIn(remove), run_time=1.0)
        self.wait(4.0)
        self.play(Write(note), run_time=1.2)
        self.wait(7.0)
        self.play(FadeOut(VGroup(title, model, knowledge, patch, remove, arrow_patch, arrow_remove, note)))

    # ═══════════════════════════════════════════════════════════════════
    # SCENE 2 — TOFU benchmark (≈66s)
    # ═══════════════════════════════════════════════════════════════════
    def scene2_tofu_benchmark(self):
        title = Text("TOFU: benchmark sạch cho unlearning", font_size=34, color=TITLE_COLOR)
        self._fit_width(title, 12.2)
        title.to_edge(UP, buff=0.42)

        ad_hoc = self._small_card(
            "Kiểm tra tùy biến",
            "Hỏi vài câu nhạy cảm\nrồi xem model đáp gì.",
            PAPER_RED,
        ).move_to(LEFT * 4.35 + UP * 1.55)

        authors = self._author_cloud(count=28).scale(0.92).move_to(LEFT * 4.0 + DOWN * 0.7)
        authors_label = Text("200 fictional authors", font_size=21, color=PAPER_PURPLE).next_to(authors, UP, buff=0.22)

        base_model = self._large_model("Base model\nkhông biết họ", width=2.55, height=1.8, font_size=15).move_to(LEFT * 0.25 + UP * 1.35)
        learned_model = self._large_model("Fine-tune\nbiết 200 tác giả", width=2.55, height=1.8, font_size=15).move_to(RIGHT * 3.55 + UP * 1.35)
        forget_model = self._large_model("Unlearn\nmột nhóm nhỏ", width=2.55, height=1.8, font_size=15).move_to(RIGHT * 3.55 + DOWN * 1.35)

        arrow1 = Arrow(authors.get_right(), base_model.get_left(), buff=0.14, color=DIM_TEXT, stroke_width=2.2)
        arrow2 = Arrow(base_model.get_right(), learned_model.get_left(), buff=0.14, color=PAPER_GREEN, stroke_width=2.2)
        arrow3 = Arrow(learned_model.get_bottom(), forget_model.get_top(), buff=0.14, color=PAPER_RED, stroke_width=2.2)

        keep_group = self._legend_item("retain set", PAPER_GREEN).move_to(RIGHT * 1.25 + DOWN * 2.6)
        forget_group = self._legend_item("forget set", PAPER_RED).next_to(keep_group, RIGHT, buff=0.5)

        explanation = Paragraph(
            "Vì các tác giả là hư cấu, model không thể biết sẵn.",
            "Ta kiểm soát được chính xác nó học gì, rồi kiểm tra nó quên gì.",
            alignment="center",
            font_size=22,
            color=TEXT_COLOR,
        ).to_edge(DOWN, buff=0.35)

        self.play(Write(title), run_time=0.9)
        self.play(FadeIn(ad_hoc, shift=DOWN * 0.15), run_time=0.9)
        self.wait(8.0)
        self.play(FadeIn(authors), FadeIn(authors_label), FadeOut(ad_hoc), run_time=1.2)
        self.wait(3.5)
        self.play(GrowArrow(arrow1), FadeIn(base_model), run_time=1.0)
        self.wait(4.0)
        self.play(GrowArrow(arrow2), FadeIn(learned_model), run_time=1.1)
        self.wait(4.5)
        self.play(GrowArrow(arrow3), FadeIn(forget_model), FadeIn(keep_group), FadeIn(forget_group), run_time=1.2)
        self.wait(6.0)
        self.play(Write(explanation), run_time=1.4)
        self.wait(11.0)
        self.play(FadeOut(VGroup(title, ad_hoc, authors, authors_label, base_model, learned_model, forget_model, arrow1, arrow2, arrow3, keep_group, forget_group, explanation)))

    # ═══════════════════════════════════════════════════════════════════
    # SCENE 3 — Forget quality vs utility (≈80s)
    # ═══════════════════════════════════════════════════════════════════
    def scene3_forget_utility_tradeoff(self):
        title = Text("Bài toán khó: forget đúng thứ, giữ đúng capability", font_size=32, color=TITLE_COLOR)
        self._fit_width(title, 12.2)
        title.to_edge(UP, buff=0.4)

        axes = Axes(
            x_range=[0, 10, 2],
            y_range=[0, 10, 2],
            x_length=6.7,
            y_length=4.2,
            axis_config={"include_tip": False, "stroke_width": 1.5, "color": DIM_TEXT},
        ).move_to(LEFT * 1.1 + DOWN * 0.15)
        x_label = Text("forget quality", font_size=18, color=TEXT_COLOR).next_to(axes.x_axis, DOWN, buff=0.28)
        y_label = Text("utility", font_size=18, color=TEXT_COLOR).next_to(axes.y_axis, LEFT, buff=0.22).rotate(PI / 2)

        bad_points = VGroup()
        coords = [(1.4, 8.6), (2.1, 7.9), (3.2, 6.2), (4.6, 4.7), (5.8, 3.3), (6.7, 2.1)]
        for x, y in coords:
            bad_points.add(Dot(axes.c2p(x, y), radius=0.07, color=PAPER_RED))

        no_forget = self._annotated_dot(axes, 1.0, 9.0, "no unlearning", PAPER_BLUE, UP + LEFT)
        retrain = self._annotated_dot(axes, 8.6, 8.4, "retrain\nbaseline", PAPER_GREEN, UP + RIGHT)

        trade_line = VMobject(color=PAPER_RED, stroke_width=2.5)
        trade_line.set_points_smoothly([axes.c2p(x, y) for x, y in coords])

        metrics = VGroup(
            self._metric_card("Forget quality", "forget đúng\nforget set", PAPER_RED),
            self._metric_card("Utility", "giữ chất lượng\nretain set", PAPER_GREEN),
        ).arrange(DOWN, buff=0.22).move_to(RIGHT * 3.85 + UP * 0.9)

        side = self._wide_callout(
            "Trade-off tệ",
            "Nhiều phương pháp hoặc giữ utility nhưng forget kém, hoặc forget tốt bằng cách làm hỏng model.",
            PAPER_RED,
        ).move_to(RIGHT * 3.85 + DOWN * 1.15)

        self.play(Write(title), run_time=0.9)
        self.play(Create(axes), FadeIn(x_label), FadeIn(y_label), run_time=1.1)
        self.play(FadeIn(metrics, shift=LEFT * 0.15), run_time=0.8)
        self.play(FadeIn(no_forget), run_time=0.9)
        self.wait(10.0)
        self.play(FadeIn(retrain), run_time=0.9)
        self.wait(9.0)
        self.play(LaggedStart(*[FadeIn(p, scale=0.5) for p in bad_points], lag_ratio=0.12), Create(trade_line), run_time=1.6)
        self.wait(14.0)
        self.play(FadeIn(side, shift=LEFT * 0.2), run_time=1.0)
        self.wait(10.0)
        self.play(FadeOut(VGroup(title, axes, x_label, y_label, bad_points, no_forget, retrain, trade_line, metrics, side)))

    # ═══════════════════════════════════════════════════════════════════
    # SCENE 4 — Anti-distillation intuition (≈81s)
    # ═══════════════════════════════════════════════════════════════════
    def scene4_anti_distillation_intuition(self):
        title = Text("Anti-distillation: mẫu đúng nhưng khó học theo", font_size=33, color=TITLE_COLOR)
        self._fit_width(title, 12.2)
        title.to_edge(UP, buff=0.4)

        teacher = self._large_model("Teacher\nmodel", width=2.75, height=1.95, font_size=16).move_to(LEFT * 4.1 + UP * 0.75)
        student = self._large_model("Student\nmodel", width=2.75, height=1.95, font_size=16).move_to(RIGHT * 4.1 + UP * 0.75)

        normal_samples = VGroup(
            self._sample_card("normal samples", "đúng, dễ học lại", PAPER_BLUE),
            self._sample_card("distillation", "student cải thiện", PAPER_BLUE),
        ).arrange(DOWN, buff=0.22).move_to(ORIGIN + UP * 1.02)

        anti_samples = VGroup(
            self._sample_card("anti samples", "vẫn giải đúng", PAPER_ORANGE),
            self._sample_card("anti-distill", "kém giá trị train", PAPER_ORANGE),
        ).arrange(DOWN, buff=0.22).move_to(ORIGIN + DOWN * 1.16)

        arrows_normal = VGroup(
            Arrow(teacher.get_right(), normal_samples.get_left(), buff=0.15, color=PAPER_BLUE),
            Arrow(normal_samples.get_right(), student.get_left(), buff=0.15, color=PAPER_BLUE),
        )
        arrows_anti = VGroup(
            Arrow(teacher.get_right() + DOWN * 0.55, anti_samples.get_left(), buff=0.15, color=PAPER_ORANGE),
            Arrow(anti_samples.get_right(), student.get_left() + DOWN * 0.55, buff=0.15, color=PAPER_ORANGE),
        )

        cross = Cross(student, stroke_color=PAPER_RED, stroke_width=5).scale(0.55).move_to(student.get_center() + DOWN * 0.65)
        label = Text("ít cải thiện", font_size=19, color=PAPER_RED).next_to(cross, DOWN, buff=0.13)

        note = Paragraph(
            "Không phải phản đối mã nguồn mở:",
            "mục tiêu là giữ một khoảng trễ để phân tích rủi ro.",
            alignment="center",
            font_size=22,
            color=TEXT_COLOR,
        ).to_edge(DOWN, buff=0.35)

        self.play(Write(title), run_time=0.9)
        self.play(FadeIn(teacher), FadeIn(student), run_time=1.0)
        self.play(FadeIn(normal_samples), LaggedStart(*[GrowArrow(a) for a in arrows_normal], lag_ratio=0.1), run_time=1.2)
        self.wait(14.0)
        self.play(FadeIn(anti_samples), LaggedStart(*[GrowArrow(a) for a in arrows_anti], lag_ratio=0.1), run_time=1.2)
        self.wait(17.0)
        self.play(Create(cross), FadeIn(label), run_time=0.8)
        self.wait(8.0)
        self.play(Write(note), run_time=1.3)
        self.wait(8.0)
        self.play(FadeOut(VGroup(title, teacher, student, normal_samples, anti_samples, arrows_normal, arrows_anti, cross, label, note)))

    # ═══════════════════════════════════════════════════════════════════
    # SCENE 5 — Pareto frontier (≈95s)
    # ═══════════════════════════════════════════════════════════════════
    def scene5_pareto_frontier(self):
        title = Text("Mục tiêu lấy mẫu: đúng với teacher, kém hữu ích cho student", font_size=30, color=TITLE_COLOR)
        self._fit_width(title, 12.2)
        title.to_edge(UP, buff=0.38)

        axes = Axes(
            x_range=[0, 100, 20],
            y_range=[0, 100, 20],
            x_length=7.2,
            y_length=4.4,
            axis_config={"include_tip": False, "stroke_width": 1.5, "color": DIM_TEXT},
        ).move_to(LEFT * 0.75 + DOWN * 0.1)
        x_label = Text("teacher accuracy", font_size=18, color=TEXT_COLOR).next_to(axes.x_axis, DOWN, buff=0.25)
        y_label = Text("student accuracy", font_size=18, color=TEXT_COLOR).next_to(axes.y_axis, LEFT, buff=0.22).rotate(PI / 2)

        objective = VGroup(
            self._objective_card("Teacher likelihood", "mẫu tự nhiên,\nhợp lý", PAPER_BLUE),
            Text("+", font_size=26, color=DIM_TEXT),
            self._objective_card("Student harm", "ít giúp\nstudent học", PAPER_ORANGE),
        ).arrange(RIGHT, buff=0.18).move_to(ORIGIN + UP * 1.25)
        token_note = Paragraph(
            "Mỗi token phải ước lượng tác động huấn luyện hạ nguồn.",
            "Các thủ thuật vi phân giúp tính xấp xỉ hiệu quả.",
            alignment="center",
            font_size=20,
            color=TEXT_COLOR,
        ).next_to(objective, DOWN, buff=0.28)

        temp_curve = axes.plot(
            lambda x: 12 + 0.58 * x,
            x_range=[20, 92],
            color=PAPER_BLUE,
            stroke_width=3,
        )
        anti_curve = VMobject(color=PAPER_ORANGE, stroke_width=3.4)
        anti_points = [axes.c2p(x, y) for x, y in [(20, 6), (38, 7), (55, 8), (70, 10), (88, 18)]]
        anti_curve.set_points_smoothly(anti_points)

        temp_label = Text("temperature sampling", font_size=18, color=PAPER_BLUE).next_to(temp_curve, UP, buff=0.2)
        anti_label = Text("anti-distillation", font_size=18, color=PAPER_ORANGE).next_to(anti_curve, DOWN, buff=0.18)

        temp_note = self._wide_callout(
            "Temperature sampling",
            "Teacher accuracy giảm, nhưng student vẫn học được từ dữ liệu đó.",
            PAPER_BLUE,
        ).move_to(RIGHT * 3.95 + UP * 1.35)

        point_70 = Dot(axes.c2p(70, 10), radius=0.09, color=PAPER_ORANGE)
        callout = self._wide_callout(
            "GSM8K: basic math",
            "Teacher vẫn đúng khoảng 70%, nhưng gần như vô dụng để train student.",
            PAPER_ORANGE,
        ).move_to(RIGHT * 3.95 + DOWN * 0.45)

        target = VGroup(
            Arrow(axes.c2p(83, 58), axes.c2p(70, 10), buff=0.12, color=PAPER_YELLOW),
            self._arrow_label("lower-left target\nteacher OK, student low", PAPER_YELLOW, width=2.45, height=0.72),
        )
        target[1].next_to(target[0], UP, buff=0.12)

        target_zone = DashedVMobject(
            SurroundingRectangle(point_70, color=PAPER_YELLOW, buff=0.35, corner_radius=0.12),
            num_dashes=18,
        )

        self.play(Write(title), run_time=0.9)
        self.play(FadeIn(objective, shift=DOWN * 0.15), Write(token_note), run_time=1.3)
        self.wait(16.0)
        self.play(FadeOut(VGroup(objective, token_note)), run_time=0.6)
        self.play(Create(axes), FadeIn(x_label), FadeIn(y_label), run_time=1.1)
        self.play(Create(temp_curve), FadeIn(temp_label), run_time=1.2)
        self.wait(4.0)
        self.play(FadeIn(temp_note, shift=LEFT * 0.15), run_time=1.0)
        self.wait(7.0)
        self.play(Create(anti_curve), FadeIn(anti_label), run_time=1.2)
        self.wait(7.0)
        self.play(FadeIn(point_70, scale=0.5), Create(target_zone), FadeIn(target), run_time=1.0)
        self.wait(7.0)
        self.play(FadeOut(temp_note), run_time=0.5)
        self.play(FadeIn(callout, shift=LEFT * 0.2), run_time=1.0)
        self.wait(16.0)
        final_intuition = self._wide_callout(
            "Trực giác chính",
            "Sample vẫn đủ đúng để dùng, nhưng kém giá trị để sao chép capability.",
            PAPER_GREEN,
        ).move_to(RIGHT * 3.95 + DOWN * 1.95)
        self.play(FadeIn(final_intuition, shift=UP * 0.15), run_time=1.0)
        self.wait(32.0)
        self.play(FadeOut(VGroup(title, axes, x_label, y_label, temp_curve, anti_curve, temp_label, anti_label, temp_note, point_70, target_zone, target, callout, final_intuition)))

    # ═══════════════════════════════════════════════════════════════════
    # SCENE 6 — Takeaway and bridge (≈35s)
    # ═══════════════════════════════════════════════════════════════════
    def scene6_takeaway(self):
        title = Text("Hai bài học cho an toàn AI", font_size=36, color=TITLE_COLOR)
        title.to_edge(UP, buff=0.55)

        left = self._lesson_card(
            "1. Unlearning",
            "Muốn model không tiết lộ kiến thức,\nđôi khi phải loại bỏ kiến thức thật sự.",
            PAPER_PURPLE,
        ).move_to(LEFT * 3.1)

        right = self._lesson_card(
            "2. Anti-distillation",
            "Muốn chia sẻ năng lực có kiểm soát,\ncần nghĩ cả chuyện người khác học lại từ mẫu.",
            PAPER_ORANGE,
        ).move_to(RIGHT * 3.1)

        bridge = Paragraph(
            "Unlearning hỏi: làm sao để model forget thật sự?",
            "Anti-distillation hỏi: làm sao để mẫu vẫn đúng nhưng khó học lại?",
            "Cả hai đều là bài toán kiểm soát năng lực, không chỉ kiểm soát câu trả lời.",
            alignment="center",
            font_size=22,
            color=TEXT_COLOR,
        ).to_edge(DOWN, buff=0.45)

        next_part = Text("Mẫu vẫn đủ đúng để dùng, nhưng kém giá trị để sao chép năng lực.", font_size=23, color=PAPER_GREEN)
        self._fit_width(next_part, 12.0)
        next_part.next_to(bridge, UP, buff=0.4)

        self.play(Write(title), run_time=0.9)
        self.play(FadeIn(left, shift=UP * 0.2), FadeIn(right, shift=UP * 0.2), run_time=1.2)
        self.wait(14.0)
        self.play(Write(bridge), run_time=1.4)
        self.wait(9.0)
        self.play(FadeIn(next_part, shift=UP * 0.15), run_time=0.8)
        self.wait(9.0)
        self.play(FadeOut(VGroup(title, left, right, bridge, next_part)), run_time=0.8)

    # ═══════════════════════════════════════════════════════════════════
    # Helpers
    # ═══════════════════════════════════════════════════════════════════
    def _large_model(self, label: str, width: float = 3.0, height: float = 2.1, font_size: float = 18) -> VGroup:
        box = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=0.16,
            fill_color=CARD_BG,
            fill_opacity=0.96,
            stroke_color=PAPER_BLUE,
            stroke_width=1.8,
        )
        layers = VGroup()
        xs = [-0.28 * width, 0, 0.28 * width]
        for li, x in enumerate(xs):
            for j in range(3):
                y = (j - 1) * 0.15 * height
                dot = Circle(
                    radius=0.055,
                    color=PAPER_BLUE,
                    fill_color=PAPER_BLUE,
                    fill_opacity=0.75,
                    stroke_width=1,
                ).move_to(box.get_center() + RIGHT * x + UP * (y + 0.18 * height))
                layers.add(dot)
        links = VGroup()
        dots = list(layers)
        for a in dots[:3]:
            for b in dots[3:6]:
                links.add(Line(a.get_center(), b.get_center(), color=CARD_STROKE, stroke_width=0.7))
        for a in dots[3:6]:
            for b in dots[6:]:
                links.add(Line(a.get_center(), b.get_center(), color=CARD_STROKE, stroke_width=0.7))

        text = Paragraph(*label.split("\n"), alignment="center", font_size=font_size, color=TEXT_COLOR, line_spacing=0.9)
        self._fit_width(text, width - 0.4)
        text.move_to(box.get_center() + DOWN * (0.25 * height))
        return VGroup(box, links, layers, text)

    def _knowledge_chip(self, text: str, color: str) -> VGroup:
        box = RoundedRectangle(
            width=2.05,
            height=0.38,
            corner_radius=0.12,
            fill_color=color,
            fill_opacity=0.15,
            stroke_color=color,
            stroke_width=1.2,
        )
        label = Text(text, font_size=14, color=TEXT_COLOR)
        self._fit_width(label, 1.78)
        return VGroup(box, label)

    def _small_card(self, title: str, body: str, color: str) -> VGroup:
        box = RoundedRectangle(
            width=3.0,
            height=1.42,
            corner_radius=0.13,
            fill_color=CARD_BG,
            fill_opacity=0.96,
            stroke_color=color,
            stroke_width=1.7,
        )
        accent_bar = Rectangle(
            width=3.0,
            height=0.06,
            fill_color=color,
            fill_opacity=1,
            stroke_width=0,
        ).move_to(box.get_top() + DOWN * 0.03)
        t = Paragraph(*title.split("\n"), alignment="center", font_size=18, color=color, line_spacing=0.9)
        self._fit_width(t, 2.55)
        b = Paragraph(*body.split("\n"), alignment="center", font_size=15, color=TEXT_COLOR, line_spacing=0.95)
        self._fit_width(b, 2.5)
        content = VGroup(t, b).arrange(DOWN, buff=0.12).move_to(box.get_center() + DOWN * 0.03)
        return VGroup(box, accent_bar, content)

    def _author_cloud(self, count: int) -> VGroup:
        rng = np.random.default_rng(10)
        cloud = VGroup()
        for i in range(count):
            x = rng.uniform(-1.55, 1.55)
            y = rng.uniform(-1.1, 1.1)
            color = PAPER_RED if i < 5 else PAPER_GREEN
            dot = Dot([x, y, 0], radius=0.055, color=color)
            cloud.add(dot)
        hull = RoundedRectangle(
            width=3.65,
            height=2.75,
            corner_radius=0.16,
            fill_color=CARD_BG,
            fill_opacity=0.55,
            stroke_color=PAPER_PURPLE,
            stroke_width=1.5,
        )
        return VGroup(hull, cloud)

    def _legend_item(self, text: str, color: str) -> VGroup:
        dot = Dot(radius=0.06, color=color)
        label = Text(text, font_size=16, color=TEXT_COLOR)
        return VGroup(dot, label).arrange(RIGHT, buff=0.12)

    def _annotated_dot(self, axes: Axes, x: float, y: float, label: str, color: str, direction) -> VGroup:
        dot = Dot(axes.c2p(x, y), radius=0.085, color=color)
        text = Paragraph(*label.split("\n"), alignment="center", font_size=15, color=color, line_spacing=0.9)
        text.next_to(dot, direction, buff=0.12)
        return VGroup(dot, text)

    def _wide_callout(self, title: str, body: str, color: str) -> VGroup:
        box = RoundedRectangle(
            width=4.35,
            height=1.7,
            corner_radius=0.14,
            fill_color=CARD_BG,
            fill_opacity=0.97,
            stroke_color=color,
            stroke_width=1.8,
        )
        accent_bar = Rectangle(
            width=4.35,
            height=0.065,
            fill_color=color,
            fill_opacity=1,
            stroke_width=0,
        ).move_to(box.get_top() + DOWN * 0.0325)
        title_text = Text(title, font_size=19, color=color)
        self._fit_width(title_text, 3.8)
        body_text = Paragraph(*self._wrap_text(body, 34), alignment="center", font_size=15, color=TEXT_COLOR, line_spacing=0.9)
        self._fit_width(body_text, 3.85)
        text = VGroup(title_text, body_text).arrange(DOWN, buff=0.1).move_to(box.get_center() + DOWN * 0.03)
        return VGroup(box, accent_bar, text)

    def _sample_card(self, title: str, body: str, color: str) -> VGroup:
        box = RoundedRectangle(
            width=2.5,
            height=0.94,
            corner_radius=0.12,
            fill_color=CARD_BG,
            fill_opacity=0.96,
            stroke_color=color,
            stroke_width=1.5,
        )
        accent_bar = Rectangle(
            width=2.5,
            height=0.05,
            fill_color=color,
            fill_opacity=1,
            stroke_width=0,
        ).move_to(box.get_top() + DOWN * 0.025)
        t = Paragraph(*title.split("\n"), alignment="center", font_size=15, color=color, line_spacing=0.9)
        self._fit_width(t, 2.12)
        b = Paragraph(*body.split("\n"), alignment="center", font_size=13, color=TEXT_COLOR, line_spacing=0.88)
        self._fit_width(b, 2.12)
        content = VGroup(t, b).arrange(DOWN, buff=0.06).move_to(box.get_center() + DOWN * 0.02)
        return VGroup(box, accent_bar, content)

    def _metric_card(self, title: str, body: str, color: str) -> VGroup:
        box = RoundedRectangle(
            width=2.8,
            height=1.04,
            corner_radius=0.12,
            fill_color=CARD_BG,
            fill_opacity=0.97,
            stroke_color=color,
            stroke_width=1.5,
        )
        accent_bar = Rectangle(
            width=2.8,
            height=0.055,
            fill_color=color,
            fill_opacity=1,
            stroke_width=0,
        ).move_to(box.get_top() + DOWN * 0.0275)
        title_text = Text(title, font_size=16, color=color)
        self._fit_width(title_text, 2.35)
        body_text = Paragraph(*body.split("\n"), alignment="center", font_size=13.5, color=TEXT_COLOR, line_spacing=0.9)
        content = VGroup(title_text, body_text).arrange(DOWN, buff=0.06).move_to(box.get_center() + DOWN * 0.02)
        return VGroup(box, accent_bar, content)

    def _objective_card(self, title: str, body: str, color: str) -> VGroup:
        box = RoundedRectangle(
            width=2.85,
            height=1.18,
            corner_radius=0.13,
            fill_color=CARD_BG,
            fill_opacity=0.97,
            stroke_color=color,
            stroke_width=1.6,
        )
        accent_bar = Rectangle(
            width=2.85,
            height=0.055,
            fill_color=color,
            fill_opacity=1,
            stroke_width=0,
        ).move_to(box.get_top() + DOWN * 0.0275)
        title_text = Paragraph(*title.split("\n"), alignment="center", font_size=16, color=color, line_spacing=0.9)
        self._fit_width(title_text, 2.35)
        body_text = Paragraph(*body.split("\n"), alignment="center", font_size=13.5, color=TEXT_COLOR, line_spacing=0.9)
        content = VGroup(title_text, body_text).arrange(DOWN, buff=0.08).move_to(box.get_center() + DOWN * 0.02)
        return VGroup(box, accent_bar, content)

    def _lesson_card(self, title: str, body: str, color: str) -> VGroup:
        box = RoundedRectangle(
            width=5.25,
            height=2.25,
            corner_radius=0.16,
            fill_color=CARD_BG,
            fill_opacity=0.96,
            stroke_color=color,
            stroke_width=1.8,
        )
        accent_bar = Rectangle(
            width=5.25,
            height=0.075,
            fill_color=color,
            fill_opacity=1,
            stroke_width=0,
        ).move_to(box.get_top() + DOWN * 0.0375)
        t = Text(title, font_size=24, color=color)
        self._fit_width(t, 4.5)
        b = Paragraph(*body.split("\n"), alignment="center", font_size=18, color=TEXT_COLOR, line_spacing=0.95)
        self._fit_width(b, 4.55)
        content = VGroup(t, b).arrange(DOWN, buff=0.2).move_to(box.get_center() + DOWN * 0.03)
        return VGroup(box, accent_bar, content)

    def _arrow_label(self, text: str, color: str, width: float = 2.2, height: float = 0.65) -> VGroup:
        box = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=0.12,
            fill_color=BG,
            fill_opacity=0.94,
            stroke_color=color,
            stroke_width=1.2,
        )
        label = Paragraph(*text.split("\n"), alignment="center", font_size=14, color=color, line_spacing=0.88)
        self._fit_width(label, width - 0.25)
        label.move_to(box)
        return VGroup(box, label)

    def _wrap_text(self, text: str, max_chars: int) -> list[str]:
        words = text.split()
        lines: list[str] = []
        current: list[str] = []
        length = 0
        for word in words:
            extra = len(word) + (1 if current else 0)
            if current and length + extra > max_chars:
                lines.append(" ".join(current))
                current = [word]
                length = len(word)
            else:
                current.append(word)
                length += extra
        if current:
            lines.append(" ".join(current))
        return lines

    def _fit_width(self, mob: Mobject, max_width: float) -> Mobject:
        if mob.width > max_width:
            mob.scale_to_fit_width(max_width)
        return mob
