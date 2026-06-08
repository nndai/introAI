"""Part 1 — Mở bài: Tại sao video này tồn tại
Thời lượng mục tiêu: 5 phút (00:00 – 05:00)

Render preview:
    manim -pql src/part1/part1.py Part1Scene
Render chất lượng cao:
    manim -pqh src/part1/part1.py Part1Scene
"""

from __future__ import annotations

import numpy as np
from manim import *

# ── Color palette ────────────────────────────────────────────────────
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
PAPER_TEAL   = "#39d353"
PAPER_ORANGE = "#f0883e"


class Part1Scene(Scene):
    """Scene mở đầu video — bối cảnh ICLR 2015 và câu hỏi trung tâm."""

    def construct(self):
        self.camera.background_color = BG
        self.scene1_title()
        self.scene2_iclr2015_intro()
        self.scene3_landmark_papers()
        self.scene4_scale_comparison()
        self.scene5_what_changed()
        self.scene6_roadmap()

    # ═══════════════════════════════════════════════════════════════════
    # SCENE 1 — Title card (≈30s)
    # ═══════════════════════════════════════════════════════════════════
    def scene1_title(self):
        title = Text(
            "Xây dựng hệ thống AI\nan toàn và mạnh mẽ",
            font="sans-serif",
            font_size=48,
            color=TEXT_COLOR,
            line_spacing=1.4,
        ).move_to(UP * 0.8)

        subtitle = Text(
            "Giải thích bài nói của Zico Kolter · ICLR 2025",
            font="sans-serif",
            font_size=24,
            color=DIM_TEXT,
        ).next_to(title, DOWN, buff=0.6)

        # decorative line
        line = Line(LEFT * 3, RIGHT * 3, color=ACCENT, stroke_width=2).next_to(
            subtitle, DOWN, buff=0.5
        )

        topics = VGroup(
            Text("Optimization Layers", font_size=20, color=PAPER_BLUE),
            Text("·", font_size=20, color=DIM_TEXT),
            Text("Robustness", font_size=20, color=PAPER_RED),
            Text("·", font_size=20, color=DIM_TEXT),
            Text("Empirical DL", font_size=20, color=PAPER_GREEN),
            Text("·", font_size=20, color=DIM_TEXT),
            Text("AI Safety", font_size=20, color=PAPER_ORANGE),
        ).arrange(RIGHT, buff=0.2).next_to(line, DOWN, buff=0.4)

        self.play(FadeIn(title, shift=UP * 0.3), run_time=1.5)
        self.play(FadeIn(subtitle, shift=UP * 0.2), run_time=1.0)
        self.play(Create(line), run_time=0.6)
        self.play(FadeIn(topics, shift=UP * 0.15), run_time=0.8)
        self.wait(19)
        self.play(
            FadeOut(title), FadeOut(subtitle), FadeOut(line), FadeOut(topics),
            run_time=0.8,
        )

    # ═══════════════════════════════════════════════════════════════════
    # SCENE 2 — ICLR 2015: "A long time ago..." (≈45s)
    # ═══════════════════════════════════════════════════════════════════
    def scene2_iclr2015_intro(self):
        # Header
        header = Text(
            "ICLR 2015", font="sans-serif", font_size=44, color=TITLE_COLOR
        ).to_edge(UP, buff=0.6)
        tagline = Text(
            '"A long time ago..."',
            font="sans-serif",
            font_size=28,
            color=DIM_TEXT,
            slant=ITALIC,
        ).next_to(header, DOWN, buff=0.3)

        self.play(Write(header), run_time=0.8)
        self.play(FadeIn(tagline, shift=UP * 0.15), run_time=0.6)

        # The big number: 31
        big_num = Text("31", font="sans-serif", font_size=120, color=ACCENT)
        big_label = Text(
            "bài báo được chấp nhận",
            font="sans-serif",
            font_size=28,
            color=TEXT_COLOR,
        )
        num_group = VGroup(big_num, big_label).arrange(DOWN, buff=0.3).move_to(ORIGIN)

        self.play(FadeIn(big_num, scale=0.5), run_time=1.0)
        self.play(FadeIn(big_label, shift=UP * 0.2), run_time=0.6)

        # 31 dots appearing
        # dots = VGroup()
        # np.random.seed(42)
        # for i in range(31):
        #     angle = 2 * PI * i / 31
        #     r = 2.5 + 0.3 * np.random.random()
        #     pos = np.array([r * np.cos(angle), r * np.sin(angle), 0])
        #     dot = Dot(pos, radius=0.06, color=PAPER_BLUE).set_opacity(0.7)
        #     dots.add(dot)

        # self.play(
        #     LaggedStartMap(FadeIn, dots, lag_ratio=0.03, scale=0.5),
        #     run_time=1.5,
        # )
        self.wait(32)

        # Store for transition
        self._iclr_group = VGroup(header, tagline, num_group)
        self.play(FadeOut(self._iclr_group), run_time=0.8)

    # ═══════════════════════════════════════════════════════════════════
    # SCENE 3 — Landmark papers (≈90s)
    # ═══════════════════════════════════════════════════════════════════
    def scene3_landmark_papers(self):
        header = Text(
            "Những bài báo thay đổi lịch sử",
            font="sans-serif",
            font_size=36,
            color=TITLE_COLOR,
        ).to_edge(UP, buff=0.5)
        self.play(Write(header), run_time=0.8)

        papers = [
            ("Adam", "Kingma & Ba", "Thuật toán tối ưu\nphổ biến nhất DL", PAPER_BLUE),
            ("Attention", "Bahdanau et al.", "Nền tảng cho\nTransformer & GPT", PAPER_GREEN),
            ("Adversarial\nExamples", "Goodfellow et al.", "Phát hiện điểm yếu\nchí mạng của DNN", PAPER_RED),
            ("VGGNet", "Simonyan &\nZisserman", "Kiến trúc CNN\nchuẩn mực", PAPER_PURPLE),
            ("AlphaGo\nfoundation", "Maddison et al.", "Nền tảng cho\nAlphaGo", PAPER_TEAL),
        ]

        cards = VGroup()
        for name, authors, desc, color in papers:
            card = self._make_paper_card(name, authors, desc, color)
            cards.add(card)

        cards.arrange(RIGHT, buff=0.3).scale_to_fit_width(13).next_to(header, DOWN, buff=0.5)

        for i, card in enumerate(cards):
            self.play(
                FadeIn(card, shift=UP * 0.3),
                run_time=0.5,
            )
            if i == 0:
                self.wait(12.0)  # pause on Adam
            elif i == 1:
                self.wait(14.0)  # pause on Attention
            elif i == 2:
                self.wait(17.0)  # pause on Adversarial
            else:
                self.wait(9.0)

        # Highlight: all from ONE conference
        highlight_box = SurroundingRectangle(
            cards, color=ACCENT, buff=0.2, stroke_width=2, corner_radius=0.1,
        )
        highlight_text = Text(
            "Tất cả từ MỘT hội nghị — chỉ 31 bài báo",
            font="sans-serif",
            font_size=24,
            color=ACCENT,
        ).next_to(highlight_box, DOWN, buff=0.3)

        self.play(Create(highlight_box), Write(highlight_text), run_time=1.0)
        self.wait(10)
        self.play(
            FadeOut(cards), FadeOut(header), FadeOut(highlight_box),
            FadeOut(highlight_text),
            run_time=0.8,
        )

    def _make_paper_card(self, name, authors, desc, color):
        """Create a paper card with name, authors, and description."""
        bg = RoundedRectangle(
            width=2.6, height=3.2, corner_radius=0.12,
            fill_color=CARD_BG, fill_opacity=0.95,
            stroke_color=color, stroke_width=1.5,
        )
        # Color accent bar at top
        accent_bar = Rectangle(
            width=2.6, height=0.08, fill_color=color,
            fill_opacity=1, stroke_width=0,
        ).move_to(bg.get_top() + DOWN * 0.04)

        title = Paragraph(
            *name.split("\n"),
            alignment="center",
            font="sans-serif",
            font_size=18,
            color=color,
        ).move_to(bg.get_center() + UP * 0.9)

        auth = Paragraph(
        *authors.split("\n"),
        alignment="center",
        font="sans-serif",
        font_size=13,
        color=DIM_TEXT,
        ).next_to(title, DOWN, buff=0.2)


        # separator
        sep = Line(LEFT * 0.9, RIGHT * 0.9, color=CARD_STROKE, stroke_width=1).next_to(
            auth, DOWN, buff=0.15
        )

        description = Paragraph(
            *desc.split("\n"),
            alignment="center",
            font="sans-serif",
            font_size=14,
            color=TEXT_COLOR,
            line_spacing=1.3,
        ).next_to(sep, DOWN, buff=0.15)
        return VGroup(bg, accent_bar, title, auth, sep, description)

    # ═══════════════════════════════════════════════════════════════════
    # SCENE 4 — Scale comparison 2015 vs 2025 (≈40s)
    # ═══════════════════════════════════════════════════════════════════
    def scene4_scale_comparison(self):
        header = Text(
            "Chúng ta đã mất gì?",
            font="sans-serif",
            font_size=40,
            color=TITLE_COLOR,
        ).to_edge(UP, buff=0.5)
        self.play(Write(header), run_time=0.8)

        # Bar chart comparison
        bar_2015 = Rectangle(
            width=1.2, height=0.5, fill_color=PAPER_BLUE,
            fill_opacity=0.85, stroke_width=0,
        )
        bar_2025 = Rectangle(
            width=1.2, height=3.75, fill_color=PAPER_ORANGE,
            fill_opacity=0.85, stroke_width=0,
        )

        # Align bars at bottom
        bar_2015.move_to(LEFT * 2.5 + DOWN * 1.5, aligned_edge=DOWN)
        bar_2025.move_to(RIGHT * 2.5 + DOWN * 1.5, aligned_edge=DOWN)

        label_2015 = VGroup(
            Text("ICLR 2015", font="sans-serif", font_size=22, color=PAPER_BLUE),
            Text("31 papers", font="sans-serif", font_size=18, color=DIM_TEXT),
        ).arrange(DOWN, buff=0.1).next_to(bar_2015, DOWN, buff=0.2)

        label_2025 = VGroup(
            Text("ICLR 2025", font="sans-serif", font_size=22, color=PAPER_ORANGE),
            Text("~3700 papers", font="sans-serif", font_size=18, color=DIM_TEXT),
        ).arrange(DOWN, buff=0.1).next_to(bar_2025, DOWN, buff=0.2)

        num_2015 = Text(
            "31", font="sans-serif", font_size=28, color=WHITE
        ).next_to(bar_2015, UP, buff=0.15)
        num_2025 = Text(
            "~3700", font="sans-serif", font_size=28, color=WHITE
        ).next_to(bar_2025, UP, buff=0.15)

        # Grow bars
        self.play(
            GrowFromEdge(bar_2015, DOWN), FadeIn(label_2015), FadeIn(num_2015),
            run_time=1.0,
        )
        self.play(
            GrowFromEdge(bar_2025, DOWN), FadeIn(label_2025), FadeIn(num_2025),
            run_time=1.5,
        )

        # Multiplier text
        mult = Text(
            "× 120", font="sans-serif", font_size=36, color=ACCENT
        ).move_to(ORIGIN + UP * 0.5)
        arrow_l = Arrow(
            bar_2015.get_right() + RIGHT * 0.2 + UP * 0.5,
            mult.get_left() + LEFT * 0.15,
            color=ACCENT, stroke_width=2, buff=0.1,
        )
        arrow_r = Arrow(
            mult.get_right() + RIGHT * 0.15,
            bar_2025.get_left() + LEFT * 0.2 + UP * 0.5,
            color=ACCENT, stroke_width=2, buff=0.1,
        )
        self.play(FadeIn(mult, scale=0.8), Create(arrow_l), Create(arrow_r), run_time=0.8)
        self.wait(8.0)

        # Quote
        quote = Text(
            "Mười năm tuyệt vời cho AI — nhưng có điều gì đó đã mất đi...",
            font="sans-serif",
            font_size=22,
            color=HIGHLIGHT,
            slant=ITALIC,
        ).to_edge(DOWN, buff=0.6)
        self.play(FadeIn(quote, shift=UP * 0.2), run_time=0.8)
        self.wait(18.0)

        all_objs = VGroup(
            header, bar_2015, bar_2025, label_2015, label_2025,
            num_2015, num_2025, mult, arrow_l, arrow_r, quote,
        )
        self.play(FadeOut(all_objs), run_time=0.8)

    # ═══════════════════════════════════════════════════════════════════
    # SCENE 5 — What changed? Scaling era (≈45s)
    # ═══════════════════════════════════════════════════════════════════
    def scene5_what_changed(self):
        header = Text(
            "Kỷ nguyên Scaling",
            font="sans-serif",
            font_size=40,
            color=TITLE_COLOR,
        ).to_edge(UP, buff=0.5)
        self.play(Write(header), run_time=0.8)

        # Scaling curve
        axes = Axes(
            x_range=[2015, 2026, 2],
            y_range=[0, 10, 2],
            x_length=9,
            y_length=4.5,
            tips=False,
            axis_config={"color": DIM_TEXT, "stroke_width": 1.5},
        ).shift(DOWN * 0.3)

        x_labels = VGroup()
        for yr in [2015, 2017, 2019, 2021, 2023, 2025]:
            lbl = Text(str(yr), font="sans-serif", font_size=14, color=DIM_TEXT)
            lbl.next_to(axes.c2p(yr, 0), DOWN, buff=0.15)
            x_labels.add(lbl)

        x_label = Text("Năm", font="sans-serif", font_size=18, color=DIM_TEXT).next_to(
            axes.x_axis, RIGHT, buff=0.2
        )
        y_label = Text(
            "Compute", font="sans-serif", font_size=18, color=DIM_TEXT
        ).next_to(axes.y_axis, UP, buff=0.2)

        # Industry curve (exponential-ish)
        industry_curve = axes.plot(
            lambda x: 0.015 * (x - 2015) ** 2.8,
            x_range=[2015, 2025.5],
            color=PAPER_ORANGE,
        )
        industry_label = Text(
            "Công nghiệp", font="sans-serif", font_size=18, color=PAPER_ORANGE
        ).next_to(axes.c2p(2025, 9), RIGHT, buff=0.15)

        # Academia curve (plateaus)
        academia_curve = axes.plot(
            lambda x: 1.5 + 0.8 * np.log(max(x - 2014, 0.1)),
            x_range=[2015, 2025.5],
            color=PAPER_BLUE,
        )
        academia_label = Text(
            "Học thuật", font="sans-serif", font_size=18, color=PAPER_BLUE
        ).next_to(axes.c2p(2025, 4), RIGHT, buff=0.15)

        self.play(Create(axes), FadeIn(x_labels), Write(x_label), Write(y_label), run_time=1.0)
        self.play(Create(academia_curve), FadeIn(academia_label), run_time=1.2)
        self.play(Create(industry_curve), FadeIn(industry_label), run_time=1.5)

        # Gap annotation
        gap_arrow = DoubleArrow(
            axes.c2p(2025, 3.7), axes.c2p(2025, 9),
            color=ACCENT, stroke_width=2, buff=0.1,
        )
        gap_text = Text(
            "Khoảng cách ngày càng lớn",
            font="sans-serif",
            font_size=16,
            color=ACCENT,
        ).next_to(gap_arrow, UL, buff=0.2)

        self.play(GrowFromCenter(gap_arrow), FadeIn(gap_text), run_time=0.8)
        self.wait(13.0)

        # Question
        question = Text(
            "Làm thế nào nghiên cứu học thuật tìm lại 'tia sáng' đó?",
            font="sans-serif",
            font_size=24,
            color=HIGHLIGHT,
        ).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(question, shift=UP * 0.2), run_time=0.8)
        self.wait(16.0)

        all_objs = VGroup(
            header, axes, x_labels, x_label, y_label,
            industry_curve, industry_label,
            academia_curve, academia_label,
            gap_arrow, gap_text, question,
        )
        self.play(FadeOut(all_objs), run_time=0.8)

    # ═══════════════════════════════════════════════════════════════════
    # SCENE 6 — Roadmap: what's coming (≈45s)
    # ═══════════════════════════════════════════════════════════════════
    def scene6_roadmap(self):
        header = Text(
            "Hành trình 10 năm nghiên cứu",
            font="sans-serif",
            font_size=36,
            color=TITLE_COLOR,
        ).to_edge(UP, buff=0.5)
        self.play(Write(header), run_time=0.8)

        # Timeline
        timeline = Line(LEFT * 5.5, RIGHT * 5.5, color=DIM_TEXT, stroke_width=2).shift(
            DOWN * 0.5
        )
        self.play(Create(timeline), run_time=0.6)

        milestones = [
            ("2015", "Optimization\nLayers", PAPER_BLUE, LEFT * 4),
            ("2017", "Adversarial\nRobustness", PAPER_RED, LEFT * 1.3),
            ("2020", "Empirical\nDL Science", PAPER_GREEN, RIGHT * 1.3),
            ("2023", "AI\nSafety", PAPER_ORANGE, RIGHT * 4),
        ]

        dots_and_labels = []
        for year, topic, color, pos in milestones:
            dot = Dot(
                timeline.get_center() + pos, radius=0.12, color=color
            ).set_z_index(1)

            year_text = Text(
                year, font="sans-serif", font_size=18, color=TEXT_COLOR
            ).next_to(dot, DOWN, buff=0.25)

            topic_text = Paragraph(
                *topic.split("\n"),
                alignment="center",
                font="sans-serif",
                font_size=16,
                color=color,
                line_spacing=1.2,
                
            ).next_to(dot, UP, buff=0.3)

            dots_and_labels.append((dot, year_text, topic_text))

        for i, (dot, year_text, topic_text) in enumerate(dots_and_labels):
            self.play(
                GrowFromCenter(dot),
                FadeIn(year_text, shift=DOWN * 0.15),
                FadeIn(topic_text, shift=UP * 0.15),
                run_time=0.7,
            )
            self.wait(3.5)

        # Highlight Safety with glow
        safety_dot = dots_and_labels[-1][0]
        glow = Circle(
            radius=0.3, color=PAPER_ORANGE, fill_opacity=0.15, stroke_width=2,
        ).move_to(safety_dot)
        self.play(Create(glow), run_time=0.5)
        self.play(
            glow.animate.scale(1.8).set_opacity(0),
            run_time=1.0,
        )

        # Final message
        conclusion = Text(
            "AI Safety — cơ hội lớn nhất cho nghiên cứu học thuật",
            font="sans-serif",
            font_size=24,
            color=GOOD,
        ).to_edge(DOWN, buff=0.6)
        self.play(FadeIn(conclusion, shift=UP * 0.2), run_time=0.8)
        self.wait(6.0)

        # Call to action
        cta = Text(
            "Hãy cùng bắt đầu hành trình này.",
            font="sans-serif",
            font_size=28,
            color=TEXT_COLOR,
        ).move_to(ORIGIN + DOWN * 2.5)
        self.play(
            FadeOut(conclusion),
            FadeIn(cta, shift=UP * 0.2),
            run_time=0.8,
        )
        self.wait(8.0)

        # Fade everything out
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=1.0)
