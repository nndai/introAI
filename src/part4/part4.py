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
PAPER_ORANGE = "#f0883e"

class Part4Scene(Scene):
    """Scene giải thích Deep Equilibrium Models (7 minutes)."""

    def construct(self):
        Text.set_default(
            font="sans-serif",
            font_size=24,
        )

        Paragraph.set_default(
            font="sans-serif",
            font_size=24,
        )

        self.camera.background_color = BG
        
        self.scene1_intro_deq()
        self.scene2_infinite_network()
        self.scene3_fixed_point_cobweb()
        self.scene4_forward_backward()
        self.scene5_results()
        self.scene6_why_fail()

    # ═══════════════════════════════════════════════════════════════════
    # SCENE 1 — Intro DEQ (0:00 - 0:40)
    # ═══════════════════════════════════════════════════════════════════
    def scene1_intro_deq(self):
        title = Text("Chương 1: Optimization & Implicit Layers", font_size=32, color=PAPER_YELLOW)
        subtitle = Text("Deep Equilibrium Models (DEQ)", font_size=24, color=PAPER_BLUE)
        title_group = VGroup(title, subtitle).arrange(DOWN, buff=0.45).move_to(ORIGIN)

        self.play(Write(title), run_time=1.2)
        self.play(FadeIn(subtitle, shift=UP * 0.3), run_time=1.0)
        self.wait(5.0)
        self.play(title_group.animate.to_edge(UP, buff=0.4))

        # Paper details box
        paper_card = RoundedRectangle(
            corner_radius=0.15,
            height=2.2,
            width=10.0,
            stroke_color=CARD_STROKE,
            stroke_width=2,
            fill_color=CARD_BG,
            fill_opacity=0.8
        )
        paper_card.move_to(UP * 0.8)

        paper_title = Text(
            '"Deep Equilibrium Models"',
            font_size=24,
            color=TEXT_COLOR,
            weight=BOLD
        )
        paper_conf = Text("NeurIPS 2019", font_size=20, color=HIGHLIGHT)
        paper_info = VGroup(paper_title, paper_conf).arrange(DOWN, buff=0.25).move_to(paper_card.get_center())

        paper_group = VGroup(paper_card, paper_info)

        # Author cards
        author_names = ["Shaojie Bai", "J. Zico Kolter", "Vladlen Koltun"]
        author_colors = [PAPER_BLUE, PAPER_PURPLE, PAPER_GREEN]
        author_cards = VGroup()

        for name, col in zip(author_names, author_colors):
            card_rect = RoundedRectangle(
                corner_radius=0.1,
                height=1.2,
                width=2.8,
                stroke_color=col,
                stroke_width=2,
                fill_color=CARD_BG,
                fill_opacity=0.9
            )
            card_text = Text(name, font_size=18, color=TEXT_COLOR)
            card_text.move_to(card_rect.get_center())
            author_cards.add(VGroup(card_rect, card_text))

        author_cards.arrange(RIGHT, buff=0.4)
        author_cards.move_to(DOWN * 1.8)

        self.play(Create(paper_card), run_time=1.2)
        self.play(Write(paper_info), run_time=1.5)
        self.wait(6.0)

        self.play(
            LaggedStart(*[FadeIn(card, shift=UP * 0.25) for card in author_cards], lag_ratio=0.18),
            run_time=2.0
        )
        
        self.wait(20.0)
        self.play(FadeOut(VGroup(title_group, paper_group, author_cards)))

    # ═══════════════════════════════════════════════════════════════════
    # SCENE 2 — 3 Forms of Network (0:40 - 2:10)
    # ═══════════════════════════════════════════════════════════════════
    def scene2_infinite_network(self):
        title = Text("3 Dạng kiến trúc: Từ Hữu hạn đến Điểm bất động", font_size=30, color=PAPER_YELLOW)
        title.to_edge(UP, buff=0.35)

        # Draw generic network diagram functions
        def create_layer(color, name, pos, num_circles=3):
            rect_height = max(1.2, num_circles * 0.3 + 0.1)
            rect = RoundedRectangle(height=rect_height, width=0.5, corner_radius=0.1, color=color, fill_opacity=0.3)
            label = MathTex(name, font_size=18).next_to(rect, DOWN, buff=0.1)
            circles = VGroup(*[Circle(radius=0.1, color=color, fill_opacity=0.1) for _ in range(num_circles)]).arrange(DOWN, buff=0.1).move_to(rect.get_center())
            return VGroup(rect, circles, label).move_to(pos)

        # -----------------------------------------------------------------
        # Form 1: Normal network
        # -----------------------------------------------------------------
        normal_title = Text("1. Mạng thông thường", font_size=20, color=TEXT_COLOR)
        normal_formula = MathTex(r"z_{i+1} = \sigma(W_i z_i + b_i)", font_size=24, color=PAPER_BLUE)
        normal_group = VGroup(normal_title, normal_formula).arrange(DOWN, buff=0.2).shift(LEFT * 4.5 + UP * 1.5)

        n_x = create_layer(PAPER_GREEN, "x", LEFT * 6.0 + DOWN * 1.0, 3)
        n_z1 = create_layer(PAPER_YELLOW, "z_1", LEFT * 5.0 + DOWN * 1.0, 4)
        n_zk = create_layer(PAPER_YELLOW, "z_k", LEFT * 3.3 + DOWN * 1.0, 4)
        n_y = create_layer(PAPER_BLUE, "y", LEFT * 2.4 + DOWN * 1.0, 2)

        n_a1 = Arrow(n_x[0].get_right(), n_z1[0].get_left(), buff=0.1, stroke_width=2, max_tip_length_to_length_ratio=0.2)
        n_w0 = MathTex("W_0", font_size=16).next_to(n_a1, UP, buff=0.05)
        n_a2 = Arrow(n_z1[0].get_right(), n_z1[0].get_right() + RIGHT*0.4, buff=0.1, stroke_width=2, max_tip_length_to_length_ratio=0.2)
        n_w1 = MathTex("W_1", font_size=16).next_to(n_a2, UP, buff=0.05)
        n_dots = MathTex(r"\dots", font_size=16).next_to(n_a2, RIGHT, buff=0.1)
        n_a4 = Arrow(n_dots.get_right() + RIGHT*0.1, n_zk[0].get_left(), buff=0.1, stroke_width=2, max_tip_length_to_length_ratio=0.2)
        n_wk = MathTex("W_{k-1}", font_size=16).next_to(n_a4, UP, buff=0.05)
        n_a5 = Arrow(n_zk[0].get_right(), n_y[0].get_left(), buff=0.1, stroke_width=2, max_tip_length_to_length_ratio=0.2)

        normal_diag = VGroup(n_x, n_z1, n_zk, n_y, n_a1, n_w0, n_a2, n_w1, n_dots, n_a4, n_wk, n_a5)

        # -----------------------------------------------------------------
        # Form 2: Infinite network
        # -----------------------------------------------------------------
        inf_title = Text("2. Mạng vô hạn lớp", font_size=20, color=TEXT_COLOR)
        inf_formula = MathTex(r"z_{i+1} = \sigma(W z_i + U x + b)", font_size=24, color=PAPER_GREEN)
        inf_group = VGroup(inf_title, inf_formula).arrange(DOWN, buff=0.2).shift(ORIGIN + UP * 1.5)

        i_x = create_layer(PAPER_GREEN, "x", LEFT * 1.0 + DOWN * 1.0, 3)
        i_z1 = create_layer(PAPER_YELLOW, "z_1", ORIGIN + DOWN * 1.0, 4)
        i_zinf = create_layer(PAPER_YELLOW, r"z_\infty", RIGHT * 1.5 + DOWN * 1.0, 4)
        i_y = create_layer(PAPER_BLUE, "y", RIGHT * 2.5 + DOWN * 1.0, 2)

        i_a1 = Arrow(i_x[0].get_right(), i_z1[0].get_left(), buff=0.1, stroke_width=2, max_tip_length_to_length_ratio=0.2)
        i_w0 = MathTex("U", font_size=16).next_to(i_a1, UP, buff=0.05)
        i_a2 = Arrow(i_z1[0].get_right(), i_z1[0].get_right() + RIGHT*0.4, buff=0.1, stroke_width=2, max_tip_length_to_length_ratio=0.2)
        i_w1 = MathTex("W", font_size=16).next_to(i_a2, UP, buff=0.05)
        i_dots = MathTex(r"\dots", font_size=16).next_to(i_a2, RIGHT, buff=0.1)
        i_a4 = Arrow(i_dots.get_right() + RIGHT*0.1, i_zinf[0].get_left(), buff=0.1, stroke_width=2, max_tip_length_to_length_ratio=0.2)
        i_wk = MathTex("W", font_size=16).next_to(i_a4, UP, buff=0.05)
        i_a5 = Arrow(i_zinf[0].get_right(), i_y[0].get_left(), buff=0.1, stroke_width=2, max_tip_length_to_length_ratio=0.2)

        inj_lines = VGroup()
        u_top = i_x[0].get_top() + UP * 0.6
        inj_lines.add(Line(i_x[0].get_top(), u_top, stroke_width=2))
        u_line = Line(u_top, u_top + RIGHT * 2.5, stroke_width=2)
        inj_lines.add(u_line)
        inj_u_label = MathTex("U", font_size=16).next_to(u_line, UP, buff=0.1).shift(LEFT * 0.5)
        inj_lines.add(inj_u_label)

        for layer in [i_z1, i_zinf]:
            inj_lines.add(Arrow(layer[0].get_top() + UP * 0.54, layer[0].get_top(), buff=0, stroke_width=2, max_tip_length_to_length_ratio=0.15))

        inf_diag = VGroup(i_x, i_z1, i_zinf, i_y, i_a1, i_w0, i_a2, i_w1, i_dots, i_a4, i_wk, i_a5, inj_lines)

        # -----------------------------------------------------------------
        # Form 3: DEQ Model
        # -----------------------------------------------------------------
        deq_title = Text("3. DEQ Model", font_size=20, color=TEXT_COLOR)
        deq_formula = MathTex(r"z^* = \sigma(W z^* + U x + b)", font_size=24, color=HIGHLIGHT)
        deq_group = VGroup(deq_title, deq_formula).arrange(DOWN, buff=0.2).shift(RIGHT * 4.8 + UP * 1.5)

        d_x = create_layer(PAPER_GREEN, "x", RIGHT * 4.0 + DOWN * 1.0, 3)
        d_z = create_layer(PAPER_YELLOW, "z^*", RIGHT * 5.2 + DOWN * 1.0, 4)
        d_y = create_layer(PAPER_BLUE, "y", RIGHT * 6.4 + DOWN * 1.0, 2)

        d_a1 = Arrow(d_x[0].get_right(), d_z[0].get_left(), buff=0.1, stroke_width=2, max_tip_length_to_length_ratio=0.1)
        d_w0 = MathTex("U", font_size=16).next_to(d_a1, UP, buff=0.05)
        d_a2 = Arrow(d_z[0].get_right(), d_y[0].get_left(), buff=0.1, stroke_width=2, max_tip_length_to_length_ratio=0.1)
        
        # Self loop for W
        start_pt = d_z[0].get_top() + RIGHT * 0.1
        p2 = start_pt + UP * 0.5
        p3 = p2 + RIGHT * 0.55
        stab_pt = d_z[0].get_right() + UP * 0.3
        p4 = np.array([p3[0], stab_pt[1], 0])

        loop_path = VGroup(
            Line(start_pt, p2, stroke_width=2),
            Line(p2, p3, stroke_width=2),
            Line(p3, p4, stroke_width=2),
            Arrow(p4, stab_pt, buff=0, stroke_width=2, max_tip_length_to_length_ratio=0.2)
        )
        d_w1 = MathTex("W", font_size=16).next_to(loop_path[2], RIGHT, buff=0.1)

        deq_diag = VGroup(d_x, d_z, d_y, d_a1, d_w0, d_a2, loop_path, d_w1)

        # Separators
        v_line1 = DashedLine(UP * 2.5, DOWN * 3.0, dash_length=0.1, color=DIM_TEXT).shift(LEFT * 1.8)
        v_line2 = DashedLine(UP * 2.5, DOWN * 3.0, dash_length=0.1, color=DIM_TEXT).shift(RIGHT * 3.2)

        self.play(Write(title))
        self.wait(2.0)

        # Show normal network
        self.play(FadeIn(normal_group), run_time=1.0)
        self.play(FadeIn(normal_diag), run_time=2.0)
        self.wait(5.0)

        self.play(Create(v_line1), run_time=1.0)
        
        # Show infinite network
        self.play(FadeIn(inf_group), run_time=1.5)
        self.play(FadeIn(inf_diag), run_time=2.5)
        self.wait(6.0)

        self.play(Create(v_line2), run_time=1.0)

        # Show DEQ model
        self.play(FadeIn(deq_group), run_time=1.5)
        self.play(FadeIn(deq_diag), run_time=2.5)
        self.wait(10.0)

        # Focus on fixed point concept
        fixed_pt_text = Text("Gom tất cả thành 1 lớp tự phản hồi duy nhất!", font_size=24, color=HIGHLIGHT)
        fixed_pt_box = SurroundingRectangle(fixed_pt_text, color=HIGHLIGHT, fill_color=CARD_BG, fill_opacity=0.9, buff=0.2)
        fixed_group = VGroup(fixed_pt_box, fixed_pt_text).move_to(DOWN * 2.8)

        self.play(FadeIn(fixed_group, shift=UP*0.2), run_time=1.5)
        self.wait(12.0)

        self.play(FadeOut(VGroup(
            title, normal_group, normal_diag, inf_group, inf_diag, deq_group, deq_diag, v_line1, v_line2, fixed_group
        )))

    # ═══════════════════════════════════════════════════════════════════
    # SCENE 3 — Fixed Point & Cobweb Diagram (2:10 - 3:40)
    # ═══════════════════════════════════════════════════════════════════
    def scene3_fixed_point_cobweb(self):
        title = Text("Sự hội tụ về Điểm bất động (Fixed Point)", font_size=30, color=PAPER_YELLOW)
        title.to_edge(UP, buff=0.35)

        eq_text = MathTex(r"z^* = f(z^*, x)", font_size=36, color=HIGHLIGHT).next_to(title, DOWN, buff=0.4)

        ax = Axes(
            x_range=[0, 1.1, 0.2], y_range=[0, 1.1, 0.2],
            x_length=5.5, y_length=5.5,
            axis_config={"include_tip": False, "color": DIM_TEXT}
        ).shift(DOWN * 0.5)

        labels = ax.get_axis_labels(x_label=MathTex("z_i"), y_label=MathTex("z_{i+1}"))
        labels[0].set_color(TEXT_COLOR)
        labels[1].set_color(TEXT_COLOR)

        # Line y = z
        y_eq_z = ax.plot(lambda x: x, color=PAPER_GREEN, stroke_width=2.5)
        y_eq_z_label = MathTex("y = z", color=PAPER_GREEN, font_size=24).next_to(ax.c2p(1.0, 1.0), UP+LEFT, buff=0.1)

        # Function curve y = f(z) = r * z * (1 - z) with r = 2.8
        def f(z):
            return 2.8 * z * (1 - z)
            
        curve = ax.plot(f, color=PAPER_BLUE, stroke_width=2.5)
        curve_label = MathTex("y = f(z)", color=PAPER_BLUE, font_size=24).next_to(ax.c2p(0.8, f(0.8)), UP+RIGHT, buff=0.1)

        # Fixed point
        z_star = 1.0 - 1.0/2.8
        pt_star = Dot(ax.c2p(z_star, z_star), color=HIGHLIGHT, radius=0.08)
        star_label = MathTex("z^*", color=HIGHLIGHT, font_size=24).next_to(pt_star, RIGHT, buff=0.2)

        self.play(Write(title), FadeIn(eq_text), run_time=1.5)
        self.play(Create(ax), FadeIn(labels), run_time=1.5)
        self.play(Create(y_eq_z), FadeIn(y_eq_z_label), run_time=1.0)
        self.play(Create(curve), FadeIn(curve_label), run_time=1.5)
        self.wait(5.0)

        # Cobweb Diagram Animation
        z_val = 0.2 # Initial guess x0 = 0.2
        
        cobweb_lines = VGroup()
        
        z0_dot = Dot(ax.c2p(z_val, 0), color=PAPER_ORANGE, radius=0.06)
        z0_label = MathTex("z_0", color=PAPER_ORANGE, font_size=20).next_to(z0_dot, DOWN, buff=0.1)
        self.play(FadeIn(z0_dot), FadeIn(z0_label))
        self.wait(1.0)

        # First few iterations slow, then speed up
        nmax = 12
        for i in range(1, nmax + 1):
            next_z = f(z_val)
            p1 = ax.c2p(z_val, z_val if i > 1 else 0)
            p2 = ax.c2p(z_val, next_z)
            v_line = Line(p1, p2, color=PAPER_ORANGE, stroke_width=2, stroke_opacity=0.7)
            
            p3 = ax.c2p(next_z, next_z)
            h_line = Line(p2, p3, color=PAPER_ORANGE, stroke_width=2, stroke_opacity=0.7)
            
            run_time_speed = 0.8 if i <= 3 else (0.4 if i <= 6 else 0.15)
            
            if i <= 3:
                dot_curve = Dot(p2, color=PAPER_ORANGE, radius=0.05)
                z_i_label = MathTex(f"z_{i}", color=PAPER_ORANGE, font_size=18).next_to(dot_curve, UP if next_z > z_val else DOWN, buff=0.1)
                self.play(Create(v_line), FadeIn(dot_curve), FadeIn(z_i_label), run_time=run_time_speed)
                self.play(Create(h_line), run_time=run_time_speed)
                cobweb_lines.add(v_line, dot_curve, z_i_label, h_line)
            else:
                self.play(Create(v_line), Create(h_line), run_time=run_time_speed)
                cobweb_lines.add(v_line, h_line)
            
            z_val = next_z
            if i <= 2:
                self.wait(0.5)

        self.wait(3.0)

        # Show final fixed point
        self.play(Create(pt_star), FadeIn(star_label), run_time=1.0)
        self.play(Flash(pt_star, color=HIGHLIGHT, line_length=0.3, num_lines=12), run_time=1.5)
        self.wait(12.0)

        self.play(FadeOut(VGroup(
            title, eq_text, ax, labels, y_eq_z, y_eq_z_label, curve, curve_label,
            z0_dot, z0_label, cobweb_lines, pt_star, star_label
        )))

    # ═══════════════════════════════════════════════════════════════════
    # SCENE 4 — Forward & Backward Passes (3:40 - 4:40)
    # ═══════════════════════════════════════════════════════════════════
    def scene4_forward_backward(self):
        title = Text("Lan truyền xuôi & ngược trong DEQ", font_size=30, color=PAPER_YELLOW)
        title.to_edge(UP, buff=0.35)

        fw_box = RoundedRectangle(height=3.5, width=5.5, corner_radius=0.1, stroke_color=PAPER_BLUE, fill_color=CARD_BG, fill_opacity=0.9)
        fw_title = Text("Forward Pass", font_size=24, color=PAPER_BLUE).next_to(fw_box.get_top(), DOWN, buff=0.3)
        fw_subtitle = Text("(Lan truyền xuôi)", font_size=18, color=DIM_TEXT).next_to(fw_title, DOWN, buff=0.1)
        fw_text = Paragraph(
            "Giải bài toán tìm nghiệm:\n"
            "  f(z*, x) - z* = 0\n\n"
            "Sử dụng các thuật toán:\n"
            "Anderson, Broyden...",
            font_size=20, color=TEXT_COLOR, line_spacing=1, alignment="center"
        ).next_to(fw_subtitle, DOWN, buff=0.4).move_to(fw_box.get_center() + DOWN*0.4)
        fw_group = VGroup(fw_box, fw_title, fw_subtitle, fw_text)

        bw_box = RoundedRectangle(height=3.5, width=5.5, corner_radius=0.1, stroke_color=PAPER_GREEN, fill_color=CARD_BG, fill_opacity=0.9)
        bw_title = Text("Backward Pass", font_size=24, color=PAPER_GREEN).next_to(bw_box.get_top(), DOWN, buff=0.3)
        bw_subtitle = Text("(Lan truyền ngược)", font_size=18, color=DIM_TEXT).next_to(bw_title, DOWN, buff=0.1)
        bw_text = Paragraph(
            "Vi phân ẩn (Implicit Diff):\n\n"
            "Không cần đồ thị tính toán\n"
            "của hàng trăm lớp.\n"
            "Chỉ cần z* để tính Gradient.",
            font_size=20, color=TEXT_COLOR, line_spacing=1, alignment="center"
        ).next_to(bw_subtitle, DOWN, buff=0.4).move_to(bw_box.get_center() + DOWN*0.4)
        bw_group = VGroup(bw_box, bw_title, bw_subtitle, bw_text)

        cards = VGroup(fw_group, bw_group).arrange(RIGHT, buff=0.8).move_to(ORIGIN).shift(DOWN * 0.2)

        self.play(Write(title), run_time=1.0)
        self.wait(3.0)

        self.play(FadeIn(fw_group, shift=UP*0.2), run_time=1.5)
        self.wait(10.0)

        self.play(FadeIn(bw_group, shift=UP*0.2), run_time=1.5)
        self.wait(12.0)

        memory_tag = Text("⇒ Tối ưu cực tốt cho BỘ NHỚ", font_size=24, color=HIGHLIGHT)
        memory_tag.next_to(cards, DOWN, buff=0.5)
        self.play(FadeIn(memory_tag), run_time=1.0)
        self.wait(8.0)

        self.play(FadeOut(VGroup(title, cards, memory_tag)))

    # ═══════════════════════════════════════════════════════════════════
    # SCENE 5 — Results / Bar Charts (4:40 - 5:30)
    # ═══════════════════════════════════════════════════════════════════
    def scene5_results(self):
        # 1. Tiêu đề chính của biểu đồ
        title = Text("Hiệu suất thực tế trên Wikitext-103", font_size=30, color=PAPER_YELLOW)
        title.to_edge(UP, buff=0.35)
        self.play(Write(title))

        # 2. Định nghĩa dữ liệu
        categories = [
            "Transformer-XL\nSmall",
            "DEQ-Transformer\nSmall",
            "Transformer-XL\nMedium",
            "DEQ-Transformer\nMedium"
        ]
        
        perplexity_data = [35.8, 32.4, 23.6, 23.2]
        memory_data = [4.8, 1.1, 9.0, 3.3]

        # 3. Cấu hình hệ trục tọa độ BarChart
        chart = BarChart(
            values=perplexity_data,  

            y_range=[0, 40, 5],
            x_length=9.5, 
            y_length=5.0,
            bar_colors=[PAPER_BLUE]*4,
            bar_width=0.35,
        ).shift(DOWN * 0.3)

        if chart.bar_labels is not None:
            for label in chart.bar_labels:
                label.scale(0.65)
                label.set_color(DIM_TEXT)
                label.shift(DOWN * 0.2)

        # Tạo đường lưới ngang nhạt (Gridlines)
        grid_lines = VGroup()
        for y_val in range(5, 41, 5):
            pos = chart.y_axis.number_to_point(y_val)
            line = Line(
                [chart.x_axis.get_start()[0], pos[1], 0],
                [chart.x_axis.get_end()[0], pos[1], 0],
                stroke_width=1,
                stroke_opacity=0.15,
                color=TEXT_COLOR
            )
            grid_lines.add(line)
        
        # Đường trục hoành làm gốc
        baseline = Line(
            chart.x_axis.get_start(),
            chart.x_axis.get_end(),
            stroke_width=2,
            color=TEXT_COLOR,
            stroke_opacity=0.3
        )

        self.play(Create(chart.x_axis), Create(chart.y_axis), run_time=1.0)
        self.play(Create(baseline), Create(grid_lines), run_time=1.0)
        
        if chart.bar_labels is not None:
            self.play(FadeIn(chart.bar_labels))

        # 4. Tự vẽ các cụm cột (Grouped Bars)
        perplexity_bars = VGroup()
        memory_bars = VGroup()
        bar_values_labels = VGroup()

        w = 0.35          
        offset = w / 2 + 0.02  

        for i in range(len(categories)):
            center_x = chart.bars[i].get_x()
            base_y = chart.x_axis.get_start()[1]

            # --- Cột Perplexity ---
            h_perp = chart.y_axis.number_to_point(perplexity_data[i])[1] - base_y
            p_bar = Rectangle(
                width=w, height=h_perp,
                fill_color=PAPER_BLUE, fill_opacity=0.9,
                stroke_width=0
            )
            p_bar.move_to([center_x - offset, base_y + h_perp/2, 0])
            perplexity_bars.add(p_bar)

            p_text = Text(str(perplexity_data[i]), font_size=15, color=TEXT_COLOR)
            p_text.next_to(p_bar, UP, buff=0.1)
            bar_values_labels.add(p_text)

            # --- Cột Memory ---
            h_mem = chart.y_axis.number_to_point(memory_data[i])[1] - base_y
            m_bar = Rectangle(
                width=w, height=h_mem,
                fill_color=PAPER_ORANGE, fill_opacity=0.9,
                stroke_width=0
            )
            m_bar.move_to([center_x + offset, base_y + h_mem/2, 0])
            memory_bars.add(m_bar)

            m_val_str = str(int(memory_data[i])) if memory_data[i].is_integer() else str(memory_data[i])
            m_text = Text(m_val_str, font_size=15, color=TEXT_COLOR)
            m_text.next_to(m_bar, UP, buff=0.1)
            bar_values_labels.add(m_text)

            if chart.bar_labels is None:
                cat_text = Paragraph(categories[i], font_size=14, color=DIM_TEXT, line_spacing=1.2, alignment="center")
                cat_text.move_to([center_x, base_y - 0.4, 0])
                bar_values_labels.add(cat_text)

        self.play(
            AnimationGroup(
                *[GrowFromEdge(bar, DOWN) for bar in perplexity_bars],
                *[GrowFromEdge(bar, DOWN) for bar in memory_bars],
                lag_ratio=0.08
            ),
            run_time=1.5
        )
        self.play(FadeIn(bar_values_labels), run_time=0.4)

        # 5. Tạo Chú thích (Legend)
        legend_p_box = Square(side_length=0.18, fill_color=PAPER_BLUE, fill_opacity=0.9, stroke_width=0)
        legend_p_text = Text("Perplexity", font_size=16, color=TEXT_COLOR)
        legend_p = VGroup(legend_p_box, legend_p_text).arrange(RIGHT, buff=0.15)

        legend_m_box = Square(side_length=0.18, fill_color=PAPER_ORANGE, fill_opacity=0.9, stroke_width=0)
        legend_m_text = Text("Memory (GB)", font_size=16, color=TEXT_COLOR)
        legend_m = VGroup(legend_m_box, legend_m_text).arrange(RIGHT, buff=0.15)

        legend = VGroup(legend_p, legend_m).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        legend.to_edge(UR, buff=1.0).shift(DOWN * 0.4)
        
        self.play(FadeIn(legend))
        self.wait(12.0)

        # Cleanup
        to_fade = VGroup(title, chart.x_axis, chart.y_axis, baseline, grid_lines, perplexity_bars, memory_bars, bar_values_labels, legend)
        if chart.bar_labels is not None:
            to_fade.add(chart.bar_labels)
        self.play(FadeOut(to_fade))

    # ═══════════════════════════════════════════════════════════════════
    # SCENE 6 — Why it failed / DEQ vs MoE (5:30 - 6:50)
    # ═══════════════════════════════════════════════════════════════════
    def scene6_why_fail(self):
        title = Text("Tại sao DEQ không trở thành xu hướng?", font_size=30, color=PAPER_YELLOW)
        title.to_edge(UP, buff=0.35)

        fail_box = RoundedRectangle(height=1.2, width=8.0, corner_radius=0.15, stroke_color=PAPER_RED, fill_color=CARD_BG, fill_opacity=0.9)
        fail_text = Text("Tốc độ chậm gấp 2 lần mạng thông thường!", font_size=26, color=PAPER_RED).move_to(fail_box.get_center())
        fail_group = VGroup(fail_box, fail_text).move_to(UP * 1.5)

        # Scale diagram
        scale_title = Text("Triết lý Thiết kế: DEQ vs Trào lưu hiện đại", font_size=24, color=TEXT_COLOR).move_to(ORIGIN)

        deq_box = RoundedRectangle(height=2.0, width=5.0, corner_radius=0.1, stroke_color=PAPER_GREEN, fill_color=CARD_BG, fill_opacity=0.9)
        deq_text = VGroup(
            Text("Deep Equilibrium Models", font_size=20, color=PAPER_GREEN),
            Paragraph("Ít tham số\nRất nhiều compute/tham số", font_size=18, color=TEXT_COLOR, line_spacing=1, alignment="center")
        ).arrange(DOWN, buff=0.3).move_to(deq_box.get_center())
        deq_group = VGroup(deq_box, deq_text)

        moe_box = RoundedRectangle(height=2.0, width=5.0, corner_radius=0.1, stroke_color=PAPER_BLUE, fill_color=CARD_BG, fill_opacity=0.9)
        moe_text = VGroup(
            Text("Mixture of Experts (MoE)", font_size=20, color=PAPER_BLUE),
            Paragraph("Hàng trăm tỷ tham số\nRất ít compute/tham số", font_size=18, color=TEXT_COLOR, line_spacing=1, alignment="center")
        ).arrange(DOWN, buff=0.3).move_to(moe_box.get_center())
        moe_group = VGroup(moe_box, moe_text)

        compare_group = VGroup(deq_group, moe_group).arrange(RIGHT, buff=1.0).next_to(scale_title, DOWN, buff=0.5)

        closing_text = Text("Bài học: Triết lý kiến trúc phải thuận theo dòng chảy của phần cứng và Scaling.", font_size=20, color=HIGHLIGHT).to_edge(DOWN, buff=0.6)

        self.play(Write(title))
        self.wait(2.0)
        
        self.play(Create(fail_box), Write(fail_text), run_time=1.5)
        self.play(Flash(fail_box, color=PAPER_RED, line_length=0.4), run_time=1.0)
        self.wait(8.0)

        self.play(Write(scale_title), run_time=1.0)
        self.play(FadeIn(deq_group, shift=UP*0.2), run_time=1.2)
        self.wait(5.0)

        self.play(FadeIn(moe_group, shift=UP*0.2), run_time=1.2)
        self.wait(10.0)

        self.play(Write(closing_text), run_time=1.5)
        self.wait(15.0)

        self.play(FadeOut(Group(*self.mobjects)))
