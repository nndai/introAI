"""Part 9 — AI Safety: Automated Jailbreaks
Thời lượng mục tiêu: 5 phút (49:00 – 54:00 trong video mới)

Render preview:
    manim -pql src/part9/part9.py Part9Scene
Render chất lượng cao:
    manim -pqh src/part9/part9.py Part9Scene
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


class Part9Scene(Scene):
    """Explainer cho phần AI Safety và automated jailbreaks."""

    def construct(self):
        Text.set_default(font="sans-serif", font_size=24)
        Paragraph.set_default(font="sans-serif", font_size=24)
        self.camera.background_color = BG

        self.scene1_safety_turn()
        self.scene3_refusal_vs_suffix()
        self.scene3b_manual_vs_automated()
        self.scene4_suffix_optimization()
        self.scene5_transfer_and_takeaway()
        self.scene2_safety_is_larger_than_robustness()

    # ═══════════════════════════════════════════════════════════════════
    # SCENE 1 — Why safety becomes central (≈170s)
    # ═══════════════════════════════════════════════════════════════════
    def scene1_safety_turn(self):
        title = Text("AI Safety: hướng nghiên cứu chiến lược", font_size=36, color=TITLE_COLOR)
        self._fit_width(title, 12.2)
        subtitle = Text(
            "Model mạnh hơn nhanh hơn dự đoán, vulnerability nhỏ không còn nhỏ nữa",
            font_size=24,
            color=TEXT_COLOR,
        )
        self._fit_width(subtitle, 12.0)
        intro = VGroup(title, subtitle).arrange(DOWN, buff=0.35).move_to(ORIGIN)

        self.play(Write(title), run_time=1.0)
        self.play(FadeIn(subtitle, shift=UP * 0.2), run_time=0.8)
        self.wait(6.0)

        field_status = self._small_card("Field status", "safety là vấn đề\nrất lớn", PAPER_RED)
        academic_role = self._small_card("Academic role", "cần nghiên cứu\nnhưng còn thiếu", PAPER_BLUE)
        strategic_impact = self._small_card("Strategic impact", "ảnh hưởng tương lai\nAI systems", PAPER_GREEN)
        strategic = VGroup(field_status, academic_role, strategic_impact).arrange(RIGHT, buff=0.35).move_to(DOWN * 1.55)

        self.play(FadeIn(field_status, shift=UP * 0.15), run_time=0.8)
        self.wait(6.0)
        self.play(FadeIn(academic_role, shift=UP * 0.15), run_time=0.8)
        self.wait(6.0)
        self.play(FadeIn(strategic_impact, shift=UP * 0.15), run_time=0.8)
        self.wait(7.0)
        self.play(FadeOut(VGroup(intro, strategic)), run_time=0.8)

        axis = Axes(
            x_range=[2020, 2026, 1],
            y_range=[0, 10, 2],
            x_length=9.5,
            y_length=3.8,
            axis_config={"include_tip": False, "stroke_width": 1.6, "color": DIM_TEXT},
            tips=False,
        ).shift(DOWN * 0.35)
        labels = axis.get_axis_labels(
            Text("year", font_size=18, color=DIM_TEXT),
            Text("capability", font_size=18, color=DIM_TEXT),
        )

        curve = axis.plot(
            lambda x: 1.0 + 8.2 / (1 + np.exp(-1.45 * (x - 2023.0))),
            x_range=[2020.1, 2025.9],
            color=PAPER_BLUE,
            stroke_width=4,
        )

        chatgpt_dot = Dot(axis.c2p(2022.9, 5.1), radius=0.09, color=PAPER_ORANGE)
        chatgpt_label = Text("ChatGPT\n2022", font_size=18, color=PAPER_ORANGE, line_spacing=0.9)
        chatgpt_label.next_to(chatgpt_dot, UP + LEFT, buff=0.18)

        risk_band = Rectangle(
            width=9.5,
            height=0.95,
            fill_color=PAPER_RED,
            fill_opacity=0.13,
            stroke_width=0,
        ).move_to(axis.c2p(2023, 8.3))
        risk_text = Text("high-risk zone", font_size=19, color=PAPER_RED)
        risk_text.next_to(risk_band, RIGHT, buff=0.12)

        question = Paragraph(
            "Robustness từng là bài toán kỹ thuật.",
            "Khi model đủ mạnh, nó trở thành vấn đề safety.",
            alignment="center",
            font_size=23,
            color=TEXT_COLOR,
            line_spacing=1.2,
        ).to_edge(DOWN, buff=0.45)

        self.play(Create(axis), FadeIn(labels), run_time=1.2)
        self.play(Create(curve), run_time=2.6)
        self.play(FadeIn(chatgpt_dot, scale=0.6), FadeIn(chatgpt_label), run_time=0.8)
        self.wait(34.0)
        self.play(FadeIn(risk_band), FadeIn(risk_text), Write(question), run_time=1.5)
        self.wait(49.0)
        self.play(FadeOut(VGroup(axis, labels, curve, chatgpt_dot, chatgpt_label, risk_band, risk_text, question)))

    # ═══════════════════════════════════════════════════════════════════
    # SCENE 2 — Safety is not only robustness (≈12s)
    # ═══════════════════════════════════════════════════════════════════
    def scene2_safety_is_larger_than_robustness(self):
        title = Text("AI Safety ≠ chỉ là robustness", font_size=34, color=TITLE_COLOR)
        self._fit_width(title, 12.2)
        title.to_edge(UP, buff=0.45)

        center = Circle(radius=1.05, color=PAPER_ORANGE, fill_color=CARD_BG, fill_opacity=0.85)
        center_text = Text("AI\nSafety", font_size=28, color=PAPER_ORANGE, line_spacing=0.8)
        center_group = VGroup(center, center_text).move_to(ORIGIN)

        topics = [
            ("Robustness", "khó bị thao túng", PAPER_BLUE, UP * 2.05),
            ("Jailbreak", "lách safeguard", PAPER_RED, RIGHT * 3.55 + UP * 0.75),
            ("Unlearning", "forget chọn lọc", PAPER_PURPLE, RIGHT * 2.8 + DOWN * 1.78),
            ("Misuse", "dùng sai mục đích", PAPER_YELLOW, LEFT * 2.8 + DOWN * 1.78),
            ("Alignment", "đúng intention", PAPER_GREEN, LEFT * 3.55 + UP * 0.75),
        ]

        nodes = VGroup()
        edges = VGroup()
        for name, desc, color, pos in topics:
            node = self._topic_node(name, desc, color).move_to(pos)
            nodes.add(node)
            direction = pos - center_group.get_center()
            direction = direction / np.linalg.norm(direction)
            edges.add(Line(
                center_group.get_center() + direction * 1.1,
                pos,
                color=CARD_STROKE,
                stroke_width=2,
            ))

        note = Text(
            "Automated jailbreaks chỉ là điểm khởi đầu.",
            font_size=22,
            color=TEXT_COLOR,
        ).to_edge(DOWN, buff=0.45)

        self.play(Write(title), run_time=0.6)
        self.play(FadeIn(center_group, scale=0.8), run_time=0.6)
        self.play(Create(edges), LaggedStart(*[FadeIn(n, shift=UP * 0.15) for n in nodes], lag_ratio=0.08), run_time=1.4)
        self.wait(3.0)

        robustness_box = SurroundingRectangle(nodes[0], color=PAPER_BLUE, buff=0.15, stroke_width=2.5)
        not_equal = Text("only one slice", font_size=20, color=PAPER_BLUE).next_to(robustness_box, DOWN, buff=0.12)
        self.play(Create(robustness_box), FadeIn(not_equal), run_time=0.6)
        self.wait(2.0)
        self.play(Write(note), run_time=0.7)
        self.wait(2.0)
        self.play(FadeOut(VGroup(title, center_group, nodes, edges, note, robustness_box, not_equal)))

    # ═══════════════════════════════════════════════════════════════════
    # SCENE 3 — Refusal vs adversarial suffix (≈66s)
    # ═══════════════════════════════════════════════════════════════════
    def scene3_refusal_vs_suffix(self):
        title = Text("Automated jailbreak: query + adversarial suffix", font_size=32, color=TITLE_COLOR)
        self._fit_width(title, 12.0)
        title.to_edge(UP, buff=0.4)

        caveat = Paragraph(
            "Older-model demo; current reasoning models are much more robust.",
            "Work was done before the later organizational connection mentioned in the talk.",
            alignment="center",
            font_size=17,
            color=PAPER_GREEN,
        ).next_to(title, DOWN, buff=0.18)
        self._fit_width(caveat, 11.0)

        left = self._chat_panel(
            "Normal query",
            "Restricted request",
            "Refuse:\n\"I can't help with that.\"",
            PAPER_BLUE,
            GOOD,
        ).shift(LEFT * 3.18 + DOWN * 0.02)

        right = self._chat_panel(
            "Query + suffix",
            "Restricted request\n+ qx7 }## alp ...",
            "Comply:\n\"Sure, here is how...\"",
            PAPER_RED,
            PAPER_RED,
        ).shift(RIGHT * 3.18 + DOWN * 0.02)

        self.play(Write(title), FadeIn(caveat, shift=DOWN * 0.1), run_time=0.9)
        self.wait(37.0)
        self.play(FadeIn(left, shift=RIGHT * 0.25), run_time=1.2)
        self.wait(8.0)
        self.play(FadeIn(right, shift=LEFT * 0.25), run_time=1.2)
        self.wait(9.0)

        suffix_box = SurroundingRectangle(right[3], color=PAPER_RED, buff=0.12, stroke_width=2)
        arrow = Arrow(
            left.get_right() + RIGHT * 0.04 + UP * 0.25,
            right.get_left() + LEFT * 0.04 + UP * 0.25,
            buff=0.1,
            color=PAPER_ORANGE,
            stroke_width=2.4,
        )
        arrow_label = self._arrow_label("append tokens", PAPER_ORANGE, width=1.72, height=0.42)
        arrow_label.next_to(arrow, UP, buff=0.08)
        arrows = VGroup(
            arrow,
            arrow_label,
        )
        self.play(Create(suffix_box), FadeIn(arrows), run_time=1.0)
        self.wait(8.0)
        self.play(FadeOut(VGroup(title, caveat, left, right, suffix_box, arrows)))

    # ═══════════════════════════════════════════════════════════════════
    # SCENE 3B — Manual prompt tricks vs automated suffix search (≈12s)
    # ═══════════════════════════════════════════════════════════════════
    def scene3b_manual_vs_automated(self):
        title = Text("Điểm mới: suffix được tìm tự động", font_size=32, color=TITLE_COLOR)
        self._fit_width(title, 12.2)
        title.to_edge(UP, buff=0.45)

        manual = VGroup(
            self._small_card("Manual jailbreak", "role-play\nstory wrapper", PAPER_PURPLE),
            self._small_card("Human prompt", "người nghĩ prompt\ncho khéo", PAPER_PURPLE),
        ).arrange(DOWN, buff=0.28).move_to(LEFT * 3.4 + DOWN * 0.15)

        automated = VGroup(
            self._small_card("Automated search", "query cố định\n+ suffix", PAPER_ORANGE),
            self._small_card("Optimization", "objective rõ ràng\ncandidate tokens", PAPER_ORANGE),
        ).arrange(DOWN, buff=0.28).move_to(RIGHT * 3.4 + DOWN * 0.15)

        divider = VGroup(
            Line(UP * 1.8, DOWN * 1.8, color=CARD_STROKE, stroke_width=1.6),
            Text("không phải", font_size=17, color=DIM_TEXT).move_to(UP * 0.35),
            Text("mà là", font_size=17, color=DIM_TEXT).move_to(DOWN * 0.35),
        )

        note = Paragraph(
            "Ý chính: không cần con người bịa prompt tinh vi.",
            "Ta biến jailbreak thành một bài toán optimization.",
            alignment="center",
            font_size=22,
            color=TEXT_COLOR,
        ).to_edge(DOWN, buff=0.4)

        self.play(Write(title), run_time=0.5)
        self.play(FadeIn(manual, shift=RIGHT * 0.2), FadeIn(divider), run_time=0.8)
        self.wait(3.0)
        self.play(FadeIn(automated, shift=LEFT * 0.2), run_time=0.8)
        self.wait(2.4)
        self.play(Write(note), run_time=0.8)
        self.wait(2.4)
        self.play(FadeOut(VGroup(title, manual, automated, divider, note)), run_time=0.5)

    # ═══════════════════════════════════════════════════════════════════
    # SCENE 4 — Optimization view (≈78s)
    # ═══════════════════════════════════════════════════════════════════
    def scene4_suffix_optimization(self):
        title = Text("Automated jailbreak = discrete optimization", font_size=32, color=TITLE_COLOR)
        self._fit_width(title, 12.2)
        title.to_edge(UP, buff=0.4)

        model = self._model_box("Open-source\nmodel").move_to(LEFT * 4.65 + UP * 0.75)
        prompt = self._small_card("Fixed query", "yêu cầu bị cấm", PAPER_BLUE).move_to(LEFT * 4.65 + DOWN * 1.45)
        suffix = self._token_grid(rows=2, cols=8).move_to(LEFT * 0.95 + DOWN * 1.45)
        suffix_label = Text("adversarial suffix", font_size=20, color=PAPER_ORANGE).next_to(suffix, DOWN, buff=0.18)
        candidate_note = self._arrow_label("try many\ncandidate tokens", PAPER_PURPLE, width=2.35, height=0.72)
        candidate_note.next_to(suffix, UP, buff=0.28)

        flow1 = Arrow(prompt.get_right(), suffix.get_left(), buff=0.18, color=DIM_TEXT)
        flow2 = Arrow(
            candidate_note.get_top() + UP * 0.08 + LEFT * 0.65,
            model.get_bottom() + DOWN * 0.08 + RIGHT * 0.35,
            buff=0.1,
            color=DIM_TEXT,
        )

        prob_panel, comply_bar, refuse_bar = self._probability_panel()
        VGroup(prob_panel, comply_bar, refuse_bar).move_to(RIGHT * 3.75 + UP * 0.12)
        flow3 = Arrow(model.get_right() + UP * 0.22, prob_panel.get_left() + UP * 0.22, buff=0.14, color=DIM_TEXT, stroke_width=2.3)
        gradient_arrows = self._gradient_arrows(suffix)

        equation = VGroup(
            Text("Objective:", font_size=21, color=TEXT_COLOR),
            Text("maximize P(comply)", font_size=26, color=PAPER_ORANGE),
        ).arrange(RIGHT, buff=0.3).to_edge(DOWN, buff=0.35)

        self.play(Write(title), run_time=0.8)
        self.play(FadeIn(prompt), FadeIn(model), run_time=1.0)
        self.play(Create(flow1), FadeIn(suffix), FadeIn(suffix_label), run_time=1.1)
        self.play(Create(flow2), Create(flow3), FadeIn(prob_panel), run_time=1.1)
        self.wait(20.0)
        self.play(Write(equation), run_time=1.0)
        self.wait(2.0)

        self.play(FadeIn(candidate_note, shift=DOWN * 0.1), LaggedStart(*[GrowArrow(a) for a in gradient_arrows], lag_ratio=0.06), run_time=1.3)
        self.wait(6.0)

        for i in range(3):
            new_suffix = self._token_grid(rows=2, cols=8).move_to(suffix)
            new_suffix.set_color_by_gradient(PAPER_PURPLE, PAPER_ORANGE, PAPER_RED)
            comply_height = [0.9, 1.75, 2.55][i]
            refuse_height = [2.35, 1.45, 0.75][i]
            new_comply = Rectangle(
                width=0.52,
                height=comply_height,
                fill_color=PAPER_RED,
                fill_opacity=0.85,
                stroke_width=0,
            ).move_to(comply_bar.get_bottom() + UP * comply_height / 2)
            new_refuse = Rectangle(
                width=0.52,
                height=refuse_height,
                fill_color=GOOD,
                fill_opacity=0.85,
                stroke_width=0,
            ).move_to(refuse_bar.get_bottom() + UP * refuse_height / 2)
            self.play(
                Transform(suffix, new_suffix),
                Transform(comply_bar, new_comply),
                Transform(refuse_bar, new_refuse),
                run_time=1.0,
            )
            self.wait(4.0)

        threshold = DashedLine(
            prob_panel.get_left() + RIGHT * 0.6 + UP * 0.45,
            prob_panel.get_right() + LEFT * 0.35 + UP * 0.45,
            color=PAPER_YELLOW,
            dash_length=0.09,
            stroke_width=2,
        )
        threshold_label = Text("P(comply) > P(refuse)", font_size=18, color=PAPER_YELLOW)
        threshold_label.next_to(threshold, UP, buff=0.1)

        takeaway = Paragraph(
            "Không cần viết sẵn toàn bộ target answer.",
            "Chỉ cần kéo model qua ngưỡng comply,",
            "phần còn lại đến từ internal knowledge.",
            alignment="center",
            font_size=19,
            color=TEXT_COLOR,
            line_spacing=0.9,
        ).to_edge(DOWN, buff=0.25)

        self.wait(3.0)
        self.play(Create(threshold), FadeIn(threshold_label), run_time=0.8)
        self.wait(6.0)
        self.play(Transform(equation, takeaway), run_time=1.0)
        self.wait(20.0)
        self.play(FadeOut(VGroup(title, model, prompt, suffix, suffix_label, candidate_note, flow1, flow2, flow3, prob_panel, comply_bar, refuse_bar, gradient_arrows, equation, threshold, threshold_label)))

    # ═══════════════════════════════════════════════════════════════════
    # SCENE 5 — Transfer and bridge to broader safety (≈50s)
    # ═══════════════════════════════════════════════════════════════════
    def scene5_transfer_and_takeaway(self):
        title = Text("Điểm bất ngờ: zero-shot transfer", font_size=32, color=TITLE_COLOR)
        self._fit_width(title, 12.2)
        title.to_edge(UP, buff=0.4)

        open_model = self._model_box("Open-source\nmodel").move_to(LEFT * 4.1 + UP * 0.55)
        suffix = self._small_card("Optimized suffix", "tìm trên\nopen model", PAPER_ORANGE).move_to(LEFT * 4.1 + DOWN * 1.3)
        closed_models = VGroup(
            self._model_box("Closed\nmodel A"),
            self._model_box("Closed\nmodel B"),
            self._model_box("Closed\nmodel C"),
        ).arrange(DOWN, buff=0.35).move_to(RIGHT * 3.8)

        arrows = VGroup()
        for cm in closed_models:
            arrows.add(Arrow(suffix.get_right(), cm.get_left(), buff=0.15, color=PAPER_PURPLE, stroke_width=3))

        zero_shot = Text("zero-shot transfer", font_size=22, color=PAPER_PURPLE)
        zero_shot.next_to(arrows, UP, buff=0.25)

        progress = VGroup(
            self._small_card("Today", "reasoning models\nrobust hơn", PAPER_GREEN),
            self._small_card("Lesson", "vulnerability nhỏ\nvẫn đáng nghiên cứu", PAPER_RED),
        ).arrange(RIGHT, buff=0.3).move_to(UP * 2.0)

        lesson = Paragraph(
            "Tối ưu trên open model, nhưng suffix vẫn có thể transfer sang closed models.",
            "Đó là lý do vulnerability nhỏ trong model mạnh có thể thành vấn đề safety lớn.",
            alignment="center",
            font_size=22,
            color=TEXT_COLOR,
        ).to_edge(DOWN, buff=0.35)

        self.play(Write(title), run_time=0.8)
        self.play(FadeIn(open_model), FadeIn(suffix), run_time=1.0)
        self.play(LaggedStart(*[FadeIn(m, shift=LEFT * 0.2) for m in closed_models], lag_ratio=0.15), run_time=1.2)
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.12), FadeIn(zero_shot), run_time=1.3)
        self.wait(15.0)
        self.play(FadeIn(progress, shift=UP * 0.15), run_time=1.0)
        self.wait(8.0)
        self.play(Write(lesson), run_time=1.2)
        self.wait(12.0)
        self.play(FadeOut(VGroup(title, open_model, suffix, closed_models, arrows, zero_shot, progress, lesson)), run_time=0.8)

    # ═══════════════════════════════════════════════════════════════════
    # Helpers
    # ═══════════════════════════════════════════════════════════════════
    def _topic_node(self, name: str, desc: str, color: str) -> VGroup:
        box = RoundedRectangle(
            width=2.35,
            height=1.0,
            corner_radius=0.12,
            fill_color=CARD_BG,
            fill_opacity=0.96,
            stroke_color=color,
            stroke_width=1.8,
        )
        accent_bar = Rectangle(
            width=2.35,
            height=0.055,
            fill_color=color,
            fill_opacity=1,
            stroke_width=0,
        ).move_to(box.get_top() + DOWN * 0.0275)
        name_text = Text(name, font_size=19, color=color)
        self._fit_width(name_text, 2.0)
        desc_text = Text(desc, font_size=13.5, color=DIM_TEXT)
        self._fit_width(desc_text, 2.0)
        text = VGroup(name_text, desc_text).arrange(DOWN, buff=0.08).move_to(box.get_center() + DOWN * 0.02)
        return VGroup(box, accent_bar, text)

    def _chat_panel(self, heading: str, user_text: str, bot_text: str, accent: str, bot_color: str) -> VGroup:
        panel = RoundedRectangle(
            width=5.15,
            height=4.25,
            corner_radius=0.14,
            fill_color=CARD_BG,
            fill_opacity=0.96,
            stroke_color=accent,
            stroke_width=1.7,
        )
        accent_bar = Rectangle(
            width=5.15,
            height=0.065,
            fill_color=accent,
            fill_opacity=1,
            stroke_width=0,
        ).move_to(panel.get_top() + DOWN * 0.0325)
        head = Text(heading, font_size=21, color=accent).move_to(panel.get_top() + DOWN * 0.38)
        self._fit_width(head, 4.6)

        user_bubble = self._bubble(user_text, PAPER_BLUE, width=4.35, height=1.05)
        user_bubble.move_to(panel.get_center() + UP * 0.65)

        bot_bubble = self._bubble(bot_text, bot_color, width=4.35, height=1.18)
        bot_bubble.move_to(panel.get_center() + DOWN * 0.85)

        return VGroup(panel, accent_bar, head, user_bubble, bot_bubble)

    def _bubble(self, text: str, color: str, width: float, height: float) -> VGroup:
        box = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=0.18,
            fill_color=color,
            fill_opacity=0.14,
            stroke_color=color,
            stroke_width=1.4,
        )
        msg = Paragraph(
            *text.split("\n"),
            alignment="center",
            font_size=16,
            color=TEXT_COLOR,
            line_spacing=0.92,
        )
        self._fit_width(msg, width - 0.42)
        msg.move_to(box)
        return VGroup(box, msg)

    def _model_box(self, text: str) -> VGroup:
        box = RoundedRectangle(
            width=2.35,
            height=1.22,
            corner_radius=0.14,
            fill_color=CARD_BG,
            fill_opacity=0.96,
            stroke_color=PAPER_BLUE,
            stroke_width=1.8,
        )
        accent_bar = Rectangle(
            width=2.35,
            height=0.055,
            fill_color=PAPER_BLUE,
            fill_opacity=1,
            stroke_width=0,
        ).move_to(box.get_top() + DOWN * 0.0275)
        nodes = VGroup()
        for x in [-0.52, 0, 0.52]:
            nodes.add(Circle(radius=0.08, color=PAPER_BLUE, fill_color=PAPER_BLUE, fill_opacity=0.75).shift(RIGHT * x))
        links = VGroup(
            Line(nodes[0].get_center(), nodes[1].get_center(), color=CARD_STROKE, stroke_width=1.3),
            Line(nodes[1].get_center(), nodes[2].get_center(), color=CARD_STROKE, stroke_width=1.3),
        )
        mini_net = VGroup(links, nodes).move_to(box.get_top() + DOWN * 0.32)
        label = Paragraph(*text.split("\n"), alignment="center", font_size=16.5, color=TEXT_COLOR, line_spacing=0.92)
        self._fit_width(label, 2.0)
        label.move_to(box.get_center() + DOWN * 0.18)
        return VGroup(box, accent_bar, mini_net, label)

    def _small_card(self, title: str, body: str, color: str) -> VGroup:
        box = RoundedRectangle(
            width=2.65,
            height=1.28,
            corner_radius=0.12,
            fill_color=CARD_BG,
            fill_opacity=0.96,
            stroke_color=color,
            stroke_width=1.7,
        )
        accent_bar = Rectangle(
            width=2.65,
            height=0.055,
            fill_color=color,
            fill_opacity=1,
            stroke_width=0,
        ).move_to(box.get_top() + DOWN * 0.0275)
        t = Paragraph(*title.split("\n"), alignment="center", font_size=17, color=color, line_spacing=0.9)
        self._fit_width(t, 2.24)
        b = Paragraph(*body.split("\n"), alignment="center", font_size=14.5, color=TEXT_COLOR, line_spacing=0.92)
        self._fit_width(b, 2.18)
        content = VGroup(t, b).arrange(DOWN, buff=0.11).move_to(box.get_center() + DOWN * 0.02)
        return VGroup(box, accent_bar, content)

    def _token_grid(self, rows: int, cols: int) -> VGroup:
        rng = np.random.default_rng(9)
        symbols = ["qx", "}", "##", "alp", "7", "\\", "tok", "!!", "mu", "z", "++", "vr", "ka", "9", "?", "ne"]
        cells = VGroup()
        for r in range(rows):
            for c in range(cols):
                token = symbols[(r * cols + c + int(rng.integers(0, 4))) % len(symbols)]
                box = RoundedRectangle(
                    width=0.55,
                    height=0.42,
                    corner_radius=0.07,
                    fill_color=CARD_BG,
                    fill_opacity=0.98,
                    stroke_color=PAPER_ORANGE,
                    stroke_width=1.2,
                )
                text = Text(token, font_size=12.5, color=TEXT_COLOR)
                self._fit_width(text, 0.42)
                cell = VGroup(box, text).move_to(RIGHT * c * 0.62 + DOWN * r * 0.5)
                cells.add(cell)
        cells.arrange_in_grid(rows=rows, cols=cols, buff=(0.08, 0.08))
        return cells

    def _probability_panel(self) -> VGroup:
        panel = RoundedRectangle(
            width=3.3,
            height=3.6,
            corner_radius=0.14,
            fill_color=CARD_BG,
            fill_opacity=0.96,
            stroke_color=CARD_STROKE,
            stroke_width=1.6,
        )
        title = Text("Response probability", font_size=19, color=TEXT_COLOR)
        title.move_to(panel.get_top() + DOWN * 0.32)

        base_y = panel.get_bottom()[1] + 0.55
        comply_bar = Rectangle(width=0.52, height=0.35, fill_color=PAPER_RED, fill_opacity=0.85, stroke_width=0)
        refuse_bar = Rectangle(width=0.52, height=2.65, fill_color=GOOD, fill_opacity=0.85, stroke_width=0)
        comply_bar.move_to([panel.get_center()[0] - 0.55, base_y + 0.35 / 2, 0])
        refuse_bar.move_to([panel.get_center()[0] + 0.55, base_y + 2.65 / 2, 0])

        comply_label = Text("comply", font_size=15, color=PAPER_RED).next_to(comply_bar, DOWN, buff=0.18)
        refuse_label = Text("refuse", font_size=15, color=GOOD).next_to(refuse_bar, DOWN, buff=0.18)
        y_axis = Line(
            [panel.get_left()[0] + 0.45, base_y, 0],
            [panel.get_left()[0] + 0.45, panel.get_top()[1] - 0.65, 0],
            color=DIM_TEXT,
            stroke_width=1.3,
        )
        return VGroup(panel, title, y_axis, comply_label, refuse_label), comply_bar, refuse_bar

    def _gradient_arrows(self, grid: VGroup) -> VGroup:
        arrows = VGroup()
        for i, cell in enumerate(grid):
            if i % 2 == 0:
                start = cell.get_top() + UP * 0.22
                end = cell.get_top() + UP * 0.03
                arrows.add(Arrow(start, end, buff=0, color=PAPER_PURPLE, stroke_width=2, max_tip_length_to_length_ratio=0.25))
        return arrows

    def _wide_callout(self, title: str, body: str, color: str) -> VGroup:
        box = RoundedRectangle(
            width=11.3,
            height=1.15,
            corner_radius=0.14,
            fill_color=CARD_BG,
            fill_opacity=0.97,
            stroke_color=color,
            stroke_width=1.8,
        )
        accent_bar = Rectangle(
            width=11.3,
            height=0.06,
            fill_color=color,
            fill_opacity=1,
            stroke_width=0,
        ).move_to(box.get_top() + DOWN * 0.03)
        title_text = Text(title, font_size=19, color=color)
        body_text = Paragraph(*self._wrap_text(body, 72), alignment="center", font_size=17, color=TEXT_COLOR, line_spacing=0.92)
        self._fit_width(body_text, 10.2)
        text = VGroup(title_text, body_text).arrange(DOWN, buff=0.08).move_to(box.get_center() + DOWN * 0.02)
        return VGroup(box, accent_bar, text)

    def _arrow_label(self, text: str, color: str, width: float = 2.0, height: float = 0.5) -> VGroup:
        box = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=0.1,
            fill_color=BG,
            fill_opacity=0.94,
            stroke_color=color,
            stroke_width=1.2,
        )
        label = Paragraph(*text.split("\n"), alignment="center", font_size=14, color=color, line_spacing=0.9)
        self._fit_width(label, width - 0.24)
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
