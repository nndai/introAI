"""Part 11 — Safety Pretraining
Thời lượng mục tiêu: 5 phút (60:00 – 65:00 trong video mới)

Render preview:
    manim -pql src/part11/part11.py Part11Scene
Render chất lượng cao:
    manim -pqh src/part11/part11.py Part11Scene
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
DISPLAY_GREEN = "#56d364"
PAPER_RED    = "#f85149"
PAPER_YELLOW = "#d29922"
PAPER_PURPLE = "#a371f7"
PAPER_ORANGE = "#f0883e"
PAPER_TEAL   = "#39d353"


class Part11Scene(Scene):
    """Explainer cho safety pretraining: đưa an toàn vào từ đầu."""

    def construct(self):
        Text.set_default(font="sans-serif", font_size=24)
        Paragraph.set_default(font="sans-serif", font_size=24)
        self.camera.background_color = BG

        self.scene1_old_pipeline_problem()
        self.scene2_safety_question()
        self.scene3_context_matters()
        self.scene2_safety_from_the_start()
        self.scene4_alignment_fragility()
        self.scene5_harmbench_ablation()
        self.scene6_takeaway()

    # ═══════════════════════════════════════════════════════════════════
    # SCENE 1 — The old pipeline is a patch at the end (≈62s)
    # ═══════════════════════════════════════════════════════════════════
    def scene1_old_pipeline_problem(self):
        title = Text("Old pipeline: pretrain mọi thứ, rồi vá ở cuối", font_size=34, color=TITLE_COLOR)
        self._fit_width(title, 12.2)
        title.to_edge(UP, buff=0.42)

        data = self._data_pile("Web data", ["useful", "biased", "harmful", "random"], LEFT * 5.1 + UP * 0.12)
        pretrain = self._process_box("Pretraining", "learn patterns\nfrom the web", PAPER_BLUE).move_to(LEFT * 2.0 + UP * 0.12)
        base_model = self._model_box("Base model\nbiết rất nhiều").move_to(RIGHT * 1.1 + UP * 0.12)
        rlhf = self._process_box("Instruction tuning\n+ RLHF", "một lượt nhỏ\nở cuối", DISPLAY_GREEN).move_to(RIGHT * 4.2 + UP * 0.12)

        arrows = VGroup(
            Arrow(data.get_right(), pretrain.get_left(), buff=0.08, color=DIM_TEXT, stroke_width=2.2),
            Arrow(pretrain.get_right(), base_model.get_left(), buff=0.08, color=DIM_TEXT, stroke_width=2.2),
            Arrow(base_model.get_right(), rlhf.get_left(), buff=0.08, color=DIM_TEXT, stroke_width=2.2),
        )

        red_memory = self._memory_chip("harmful knowledge vẫn nằm trong tham số", PAPER_RED)
        red_memory.move_to(base_model.get_center() + DOWN * 1.55)
        leak_arrow = Arrow(base_model.get_bottom(), red_memory.get_top(), buff=0.12, color=PAPER_RED)

        note = Paragraph(
            "Cách cũ giống như dạy model đọc cả Internet,",
            "rồi cuối cùng mới nhắc: \"đừng generate nội dung nguy hiểm\".",
            alignment="center",
            font_size=23,
            color=TEXT_COLOR,
        ).to_edge(DOWN, buff=0.38)

        self.play(Write(title), run_time=0.9)
        self.play(FadeIn(data), run_time=1.0)
        self.play(GrowArrow(arrows[0]), FadeIn(pretrain), run_time=0.9)
        self.play(GrowArrow(arrows[1]), FadeIn(base_model), run_time=0.9)
        self.wait(24.0)
        self.play(GrowArrow(arrows[2]), FadeIn(rlhf), run_time=0.9)
        self.wait(19.0)
        self.play(GrowArrow(leak_arrow), FadeIn(red_memory, shift=UP * 0.15), run_time=1.0)
        self.wait(8.0)
        self.play(Write(note), run_time=1.4)
        self.wait(6.0)
        self.play(FadeOut(VGroup(title, data, pretrain, base_model, rlhf, arrows, red_memory, leak_arrow, note)))

    # ═══════════════════════════════════════════════════════════════════
    # SCENE 2A — Safety should be in pretraining, not only final alignment
    # ═══════════════════════════════════════════════════════════════════
    def scene2_safety_question(self):
        title = Text("Câu hỏi: safety có thể nằm ngay từ đầu không?", font_size=33, color=TITLE_COLOR)
        self._fit_width(title, 12.2)
        title.to_edge(UP, buff=0.42)

        old = VGroup(
            self._process_box("Old approach", "learn first\npatch later", PAPER_RED),
            self._process_box("Final alignment", "instruction tuning\n+ RLHF", DISPLAY_GREEN),
        ).arrange(RIGHT, buff=0.85).move_to(UP * 1.15)
        new = VGroup(
            self._process_box("Safety pretraining", "safety built into\nthe learning path", PAPER_BLUE),
            self._process_box("Early refusal", "không đợi\nđến cuối", PAPER_PURPLE),
        ).arrange(RIGHT, buff=0.85).move_to(DOWN * 1.25)

        arrow = Arrow(UP * 0.35, DOWN * 0.55, buff=0, color=PAPER_ORANGE, stroke_width=2.5)
        arrow.move_to(RIGHT * 4.82 + DOWN * 0.05)
        label = self._arrow_label("đưa safety\nvào pipeline", PAPER_ORANGE, width=2.0, height=0.72)
        label.next_to(arrow, RIGHT, buff=0.16)

        self.play(Write(title), run_time=0.7)
        self.play(FadeIn(old, shift=UP * 0.15), run_time=0.9)
        self.wait(8.0)
        self.play(GrowArrow(arrow), FadeIn(label), FadeIn(new, shift=UP * 0.15), run_time=1.2)
        self.wait(9.0)
        self.play(FadeOut(VGroup(title, old, new, arrow, label)), run_time=0.7)

    # ═══════════════════════════════════════════════════════════════════
    # SCENE 2 — Build safety into the whole training path (≈20s)
    # ═══════════════════════════════════════════════════════════════════
    def scene2_safety_from_the_start(self):
        title = Text("Safety pretraining: safety đi xuyên suốt pipeline", font_size=33, color=TITLE_COLOR)
        self._fit_width(title, 12.2)
        title.to_edge(UP, buff=0.42)

        stages = VGroup(
            self._stage_card("1", "Data filtering", "loại phần rõ ràng\nnguy hiểm", PAPER_GREEN),
            self._stage_card("2", "Contextualize", "rephrase nội dung\nxấu trong context", PAPER_BLUE),
            self._stage_card("3", "Early refusal", "học refusal\nngay từ sớm", PAPER_PURPLE),
            self._stage_card("4", "Guardrail tags", "tag harmful\ncontent", PAPER_ORANGE),
            self._stage_card("5", "Backtracking", "gặp harmful tag\nthì backtrack", PAPER_RED),
        ).arrange(RIGHT, buff=0.24).move_to(DOWN * 0.05)

        arrows = VGroup()
        for left, right in zip(stages[:-1], stages[1:]):
            arrows.add(Arrow(left.get_right(), right.get_left(), buff=0.08, color=DIM_TEXT, stroke_width=2))

        message = Paragraph(
            "Ý tưởng không phải là xóa sạch mọi điều xấu.",
            "Ý tưởng là dạy model contextualize chúng trong khung safety.",
            alignment="center",
            font_size=23,
            color=TEXT_COLOR,
        ).to_edge(DOWN, buff=0.38)

        self.play(Write(title), run_time=0.9)
        self.play(FadeIn(stages[0], shift=UP * 0.15), run_time=0.8)
        for i in range(1, len(stages)):
            self.play(GrowArrow(arrows[i - 1]), FadeIn(stages[i], shift=UP * 0.15), run_time=0.65)
        self.wait(7.0)
        self.play(Write(message), run_time=1.4)
        self.wait(8.0)
        self.play(FadeOut(VGroup(title, stages, arrows, message)))

    # ═══════════════════════════════════════════════════════════════════
    # SCENE 3 — Safest-only data can be worse (≈30s)
    # ═══════════════════════════════════════════════════════════════════
    def scene3_context_matters(self):
        title = Text("Safest-only data chưa chắc tốt hơn", font_size=33, color=TITLE_COLOR)
        title.to_edge(UP, buff=0.42)

        left = self._comparison_panel(
            "Safest-only",
            "model thiếu context",
            "không hiểu ranh giới\ncủa harmful content",
            PAPER_RED,
        ).move_to(LEFT * 3.55)

        right = self._comparison_panel(
            "Contextualized data",
            "model hiểu boundary",
            "harmful content được\nđóng khung an toàn",
            PAPER_GREEN,
        ).move_to(RIGHT * 3.55)

        middle = self._arrow_label("khác với\nencourage harmful content", PAPER_RED, width=2.35, height=0.72)
        middle.move_to(ORIGIN + DOWN * 0.02)

        analogy = Paragraph(
            "Giống giáo dục con người: ta vẫn dạy về nguy hiểm,",
            "nhưng không ném trẻ em vào diễn đàn ngẫu nhiên trên Internet.",
            alignment="center",
            font_size=23,
            color=TEXT_COLOR,
        ).to_edge(DOWN, buff=0.38)

        self.play(Write(title), run_time=0.9)
        self.play(FadeIn(left, shift=RIGHT * 0.2), run_time=1.0)
        self.wait(7.5)
        self.play(FadeIn(middle), run_time=0.8)
        self.play(FadeIn(right, shift=LEFT * 0.2), run_time=1.0)
        self.wait(7.5)
        self.play(Write(analogy), run_time=1.4)
        self.wait(9.0)
        self.play(FadeOut(VGroup(title, left, right, middle, analogy)))

    # ═══════════════════════════════════════════════════════════════════
    # SCENE 4 — Alignment can be fine-tuned away (≈64s)
    # ═══════════════════════════════════════════════════════════════════
    def scene4_alignment_fragility(self):
        title = Text("Alignment ở cuối rất dễ bị fine-tune out", font_size=34, color=TITLE_COLOR)
        self._fit_width(title, 12.2)
        title.to_edge(UP, buff=0.42)

        aligned = self._model_box("Aligned\nbase model").move_to(LEFT * 4.55 + UP * 1.02)
        benign = self._process_box("Fine-tune GSM8K", "benign task\nchỉ cần trả lời", PAPER_BLUE).move_to(ORIGIN + UP * 1.0)
        helpful = self._model_box("Helpful-only\nforgets refusal").move_to(RIGHT * 4.55 + UP * 1.02)

        safe_base = self._model_box("Safe LMR", stroke=PAPER_GREEN).move_to(LEFT * 4.55 + DOWN * 1.38)
        benign2 = self._process_box("Same fine-tune", "vẫn học task", PAPER_BLUE).move_to(ORIGIN + DOWN * 1.38)
        safer = self._model_box("Less harmful\nafter fine-tune", stroke=PAPER_GREEN).move_to(RIGHT * 4.55 + DOWN * 1.38)

        top_arrows = VGroup(
            Arrow(aligned.get_right(), benign.get_left(), buff=0.15, color=DIM_TEXT),
            Arrow(benign.get_right(), helpful.get_left(), buff=0.15, color=PAPER_RED),
        )
        bottom_arrows = VGroup(
            Arrow(safe_base.get_right(), benign2.get_left(), buff=0.15, color=DIM_TEXT),
            Arrow(benign2.get_right(), safer.get_left(), buff=0.15, color=PAPER_GREEN),
        )

        warning = self._arrow_label("refusal\nfine-tune out", PAPER_RED, width=1.82, height=0.56)
        warning.move_to(RIGHT * 2.25 + UP * 2.18)
        stable = self._arrow_label("safety\nsâu hơn", PAPER_GREEN, width=1.65, height=0.56)
        stable.move_to(RIGHT * 2.22 + DOWN * 2.68)

        self.play(Write(title), run_time=0.9)
        self.play(FadeIn(aligned), FadeIn(benign), FadeIn(helpful), run_time=1.0)
        self.play(LaggedStart(*[GrowArrow(a) for a in top_arrows], lag_ratio=0.12), FadeIn(warning), run_time=1.2)
        self.wait(28.0)
        self.play(FadeIn(safe_base), FadeIn(benign2), FadeIn(safer), run_time=1.0)
        self.play(LaggedStart(*[GrowArrow(a) for a in bottom_arrows], lag_ratio=0.12), FadeIn(stable), run_time=1.2)
        self.wait(31.0)
        self.play(FadeOut(VGroup(title, aligned, benign, helpful, safe_base, benign2, safer, top_arrows, bottom_arrows, warning, stable)))

    # ═══════════════════════════════════════════════════════════════════
    # SCENE 5 — HarmBench style ablation chart (≈46s)
    # ═══════════════════════════════════════════════════════════════════
    def scene5_harmbench_ablation(self):
        title = Text("HarmBench ablation: thành phần nào giảm harmfulness?", font_size=33, color=TITLE_COLOR)
        self._fit_width(title, 12.2)
        title.to_edge(UP, buff=0.42)

        axes = Axes(
            x_range=[0, 6, 1],
            y_range=[0, 100, 20],
            x_length=8.4,
            y_length=4.3,
            axis_config={"include_tip": False, "stroke_width": 1.5, "color": DIM_TEXT},
        ).move_to(UP * 0.05)
        y_label = Text("HarmBench score", font_size=18, color=TEXT_COLOR).next_to(axes.y_axis, LEFT, buff=0.2).rotate(PI / 2)

        labels = ["all\ndata", "safest\nonly", "rephrase", "native\nrefusal", "tag +\nbacktrack"]
        values = [55, 68, 38, 24, 10]
        colors = [PAPER_BLUE, PAPER_RED, PAPER_PURPLE, PAPER_GREEN, PAPER_ORANGE]

        bars = VGroup()
        bar_labels = VGroup()
        value_labels = VGroup()
        max_bar_height = 3.35
        for i, (label, value, color) in enumerate(zip(labels, values, colors), start=1):
            bar = Rectangle(
                width=0.72,
                height=max_bar_height * value / 100,
                fill_color=color,
                fill_opacity=0.85,
                stroke_width=0,
            )
            bar.move_to(axes.c2p(i, 0) + UP * bar.height / 2)
            bars.add(bar)

            bar_label = Paragraph(*label.split("\n"), alignment="center", font_size=14, color=TEXT_COLOR, line_spacing=0.8)
            bar_label.next_to(bar, DOWN, buff=0.18)
            bar_labels.add(bar_label)

            value_label = Text(str(value), font_size=16, color=color).next_to(bar, UP, buff=0.08)
            value_labels.add(value_label)

        odd_note = self._wide_callout(
            "Điểm lạ",
            "Safest-only data có thể tệ hơn, vì model không học cách contextualize harmful content.",
            PAPER_RED,
        ).scale(0.86).to_edge(DOWN, buff=0.28)

        final_note = Text("Kết hợp các bước: harmfulness giảm mạnh", font_size=23, color=PAPER_GREEN)
        final_note.to_edge(DOWN, buff=0.55)

        self.play(Write(title), run_time=0.9)
        self.play(Create(axes), FadeIn(y_label), run_time=1.0)
        self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.12), run_time=1.6)
        self.play(FadeIn(bar_labels), FadeIn(value_labels), run_time=0.9)
        self.wait(18.0)
        self.play(FadeIn(odd_note, shift=UP * 0.2), run_time=1.0)
        self.wait(11.0)
        self.play(FadeOut(odd_note), FadeIn(final_note, shift=UP * 0.15), run_time=0.9)
        self.wait(11.0)
        self.play(FadeOut(VGroup(title, axes, y_label, bars, bar_labels, value_labels, final_note)))

    # ═══════════════════════════════════════════════════════════════════
    # SCENE 6 — Takeaway (≈12s)
    # ═══════════════════════════════════════════════════════════════════
    def scene6_takeaway(self):
        title = Text("Safety pretraining: bài học chính", font_size=36, color=TITLE_COLOR)
        title.to_edge(UP, buff=0.55)

        lessons = VGroup(
            self._lesson("Không chỉ final patch", "safety phải vào từ đầu", PAPER_BLUE),
            self._lesson("Context + refusal", "học boundary và từ chối sớm", PAPER_GREEN),
            self._lesson("Guardrail tags", "phát hiện rồi backtrack", PAPER_ORANGE),
        ).arrange(DOWN, buff=0.35).move_to(ORIGIN + UP * 0.1)

        bridge = Paragraph(
            "Safety pretraining cố gắng đưa context, refusal,",
            "và guardrails vào ngay từ đầu pipeline.",
            alignment="center",
            font_size=23,
            color=TEXT_COLOR,
        ).to_edge(DOWN, buff=0.4)

        self.play(Write(title), run_time=0.6)
        self.play(LaggedStart(*[FadeIn(item, shift=UP * 0.15) for item in lessons], lag_ratio=0.12), run_time=1.1)
        self.wait(5.0)
        self.play(Write(bridge), run_time=1.0)
        self.wait(5.0)
        self.play(FadeOut(VGroup(title, lessons, bridge)), run_time=0.6)

    # ═══════════════════════════════════════════════════════════════════
    # Helpers
    # ═══════════════════════════════════════════════════════════════════
    def _data_pile(self, title: str, items: list[str], pos) -> VGroup:
        box = RoundedRectangle(
            width=2.7,
            height=2.65,
            corner_radius=0.16,
            fill_color=CARD_BG,
            fill_opacity=0.96,
            stroke_color=PAPER_PURPLE,
            stroke_width=1.7,
        )
        accent_bar = Rectangle(
            width=2.7,
            height=0.07,
            fill_color=PAPER_PURPLE,
            fill_opacity=1,
            stroke_width=0,
        ).move_to(box.get_top() + DOWN * 0.035)
        title_text = Text(title, font_size=20, color=PAPER_PURPLE)
        chips = VGroup()
        colors = [PAPER_GREEN, PAPER_YELLOW, PAPER_RED, DIM_TEXT]
        for item, color in zip(items, colors):
            chips.add(self._chip(item, color))
        chips.arrange(DOWN, buff=0.12)
        content = VGroup(title_text, chips).arrange(DOWN, buff=0.22).move_to(box)
        return VGroup(box, accent_bar, content).move_to(pos)

    def _process_box(self, title: str, body: str, color: str) -> VGroup:
        box = RoundedRectangle(
            width=2.75,
            height=1.52,
            corner_radius=0.14,
            fill_color=CARD_BG,
            fill_opacity=0.96,
            stroke_color=color,
            stroke_width=1.7,
        )
        accent_bar = Rectangle(
            width=2.75,
            height=0.065,
            fill_color=color,
            fill_opacity=1,
            stroke_width=0,
        ).move_to(box.get_top() + DOWN * 0.0325)
        title_text = Paragraph(*title.split("\n"), alignment="center", font_size=16, color=color, line_spacing=0.9)
        self._fit_width(title_text, 2.38)
        body_text = Paragraph(*body.split("\n"), alignment="center", font_size=13, color=TEXT_COLOR, line_spacing=1.12)
        content = VGroup(title_text, body_text).arrange(DOWN, buff=0.13).move_to(box.get_center() + DOWN * 0.04)
        return VGroup(box, accent_bar, content)

    def _model_box(self, label: str, stroke: str = PAPER_BLUE) -> VGroup:
        box = RoundedRectangle(
            width=2.55,
            height=1.55,
            corner_radius=0.15,
            fill_color=CARD_BG,
            fill_opacity=0.96,
            stroke_color=stroke,
            stroke_width=1.8,
        )
        accent_bar = Rectangle(
            width=2.55,
            height=0.065,
            fill_color=stroke,
            fill_opacity=1,
            stroke_width=0,
        ).move_to(box.get_top() + DOWN * 0.0325)
        nodes = VGroup()
        for x in [-0.42, 0, 0.42]:
            nodes.add(Circle(radius=0.06, color=stroke, fill_color=stroke, fill_opacity=0.75).shift(RIGHT * x))
        links = VGroup(
            Line(nodes[0].get_center(), nodes[1].get_center(), color=CARD_STROKE, stroke_width=1),
            Line(nodes[1].get_center(), nodes[2].get_center(), color=CARD_STROKE, stroke_width=1),
        )
        net = VGroup(links, nodes).move_to(box.get_top() + DOWN * 0.35)
        text = Paragraph(*label.split("\n"), alignment="center", font_size=15, color=TEXT_COLOR, line_spacing=1.02)
        text.move_to(box.get_center() + DOWN * 0.2)
        self._fit_width(text, 2.15)
        return VGroup(box, accent_bar, net, text)

    def _memory_chip(self, text: str, color: str) -> VGroup:
        box = RoundedRectangle(
            width=3.35,
            height=0.55,
            corner_radius=0.16,
            fill_color=color,
            fill_opacity=0.14,
            stroke_color=color,
            stroke_width=1.4,
        )
        label = Text(text, font_size=15, color=TEXT_COLOR)
        self._fit_width(label, 3.0)
        return VGroup(box, label)

    def _chip(self, text: str, color: str) -> VGroup:
        box = RoundedRectangle(
            width=1.75,
            height=0.34,
            corner_radius=0.1,
            fill_color=color,
            fill_opacity=0.16,
            stroke_color=color,
            stroke_width=1.1,
        )
        label = Text(text, font_size=13, color=TEXT_COLOR)
        return VGroup(box, label)

    def _stage_card(self, number: str, title: str, body: str, color: str) -> VGroup:
        box = RoundedRectangle(
            width=2.25,
            height=2.22,
            corner_radius=0.15,
            fill_color=CARD_BG,
            fill_opacity=0.96,
            stroke_color=color,
            stroke_width=1.7,
        )
        accent_bar = Rectangle(
            width=2.25,
            height=0.07,
            fill_color=color,
            fill_opacity=1,
            stroke_width=0,
        ).move_to(box.get_top() + DOWN * 0.035)
        badge = Circle(radius=0.22, color=color, fill_color=color, fill_opacity=0.2)
        badge_text = Text(number, font_size=18, color=color).move_to(badge)
        title_text = Paragraph(*title.split("\n"), alignment="center", font_size=16, color=color, line_spacing=0.9)
        self._fit_width(title_text, 1.95)
        body_text = Paragraph(*body.split("\n"), alignment="center", font_size=12.5, color=TEXT_COLOR, line_spacing=1.05)
        content = VGroup(VGroup(badge, badge_text), title_text, body_text).arrange(DOWN, buff=0.16).move_to(box.get_center() + DOWN * 0.03)
        return VGroup(box, accent_bar, content)

    def _comparison_panel(self, title: str, subtitle: str, body: str, color: str) -> VGroup:
        box = RoundedRectangle(
            width=3.85,
            height=3.0,
            corner_radius=0.16,
            fill_color=CARD_BG,
            fill_opacity=0.96,
            stroke_color=color,
            stroke_width=1.8,
        )
        accent_bar = Rectangle(
            width=3.85,
            height=0.075,
            fill_color=color,
            fill_opacity=1,
            stroke_width=0,
        ).move_to(box.get_top() + DOWN * 0.0375)
        icon = Circle(radius=0.42, color=color, fill_color=color, fill_opacity=0.12)
        mark = Text("!", font_size=32, color=color).move_to(icon)
        title_text = Paragraph(*title.split("\n"), alignment="center", font_size=21, color=color, line_spacing=0.95)
        self._fit_width(title_text, 3.2)
        sub_text = Paragraph(*subtitle.split("\n"), alignment="center", font_size=16, color=DIM_TEXT, line_spacing=0.95)
        self._fit_width(sub_text, 3.2)
        body_text = Paragraph(*body.split("\n"), alignment="center", font_size=15, color=TEXT_COLOR, line_spacing=1.08)
        self._fit_width(body_text, 3.25)
        content = VGroup(VGroup(icon, mark), title_text, sub_text, body_text).arrange(DOWN, buff=0.13).move_to(box.get_center() + DOWN * 0.02)
        return VGroup(box, accent_bar, content)

    def _wide_callout(self, title: str, body: str, color: str) -> VGroup:
        box = RoundedRectangle(
            width=11.3,
            height=1.25,
            corner_radius=0.14,
            fill_color=CARD_BG,
            fill_opacity=0.97,
            stroke_color=color,
            stroke_width=1.8,
        )
        title_text = Text(title, font_size=20, color=color)
        body_text = Paragraph(*self._wrap_text(body, 62), alignment="center", font_size=17, color=TEXT_COLOR, line_spacing=0.82)
        text = VGroup(title_text, body_text).arrange(DOWN, buff=0.08).move_to(box)
        return VGroup(box, text)

    def _arrow_label(self, text: str, color: str, width: float = 2.25, height: float = 0.72) -> VGroup:
        box = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=0.12,
            fill_color=BG,
            fill_opacity=0.92,
            stroke_color=color,
            stroke_width=1.2,
        )
        label = Paragraph(*text.split("\n"), alignment="center", font_size=15, color=color, line_spacing=0.86)
        self._fit_width(label, width - 0.28)
        label.move_to(box)
        return VGroup(box, label)

    def _lesson(self, title: str, body: str, color: str) -> VGroup:
        box = RoundedRectangle(
            width=8.6,
            height=0.95,
            corner_radius=0.14,
            fill_color=CARD_BG,
            fill_opacity=0.96,
            stroke_color=color,
            stroke_width=1.6,
        )
        accent_bar = Rectangle(
            width=0.08,
            height=0.95,
            fill_color=color,
            fill_opacity=1,
            stroke_width=0,
        ).move_to(box.get_left() + RIGHT * 0.04)
        title_text = Text(title, font_size=19, color=color)
        self._fit_width(title_text, 3.2)
        body_text = Text(body, font_size=17, color=TEXT_COLOR)
        self._fit_width(body_text, 4.4)
        content = VGroup(title_text, body_text).arrange(RIGHT, buff=0.35).move_to(box)
        return VGroup(box, accent_bar, content)

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
