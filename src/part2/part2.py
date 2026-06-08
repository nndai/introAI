"""Part 2 — Input Convex Neural Networks (ICNN)
Thời lượng mục tiêu: 6 phút (05:00 – 11:00)

Render preview:
    manim -pql src/part2/part2.py Part2Scene
Render chất lượng cao:
    manim -pqh src/part2/part2.py Part2Scene
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
PAPER_ORANGE = "#f0883e"


class Part2Scene(Scene):
    """Scene giải thích Input Convex Neural Networks (ICNN)."""

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
        self.scene1_intro_convexity()
        self.scene2_relu_convexity()
        self.scene3_icnn_architecture()
        self.scene4_energy_based_models()
        self.scene5_lyapunov_stability()
        self.scene6_limitations()

    # ═══════════════════════════════════════════════════════════════════
    # SCENE 1 — Intro Convexity (≈75s)
    # ═══════════════════════════════════════════════════════════════════
    def scene1_intro_convexity(self):
        # 1. Title slide
        title = Text("Chương 1: Optimization & Implicit Layers", font_size=32, color=PAPER_YELLOW)
        subtitle = Text("", font_size=24, color=PAPER_BLUE)
        title_group = VGroup(title, subtitle).arrange(DOWN, buff=0.45).move_to(ORIGIN)
        
        self.play(Write(title), run_time=1.5)
        self.play(FadeIn(subtitle, shift=UP * 0.3), run_time=1.0)
        self.wait(8.0)
        self.play(FadeOut(title_group))

        # 2. Context 2015
        ctx_title = Text("Bối cảnh 2015: Kỷ nguyên Học sâu", font_size=32, color=PAPER_YELLOW)
        ctx_title.to_edge(UP, buff=0.35)

        layer_positions = [-3.5, -1.5, 0.5, 2.5]
        layer_sizes = [3, 4, 4, 2]
        layer_colors = [PAPER_BLUE, PAPER_GREEN, PAPER_GREEN, PAPER_ORANGE]
        nodes = []
        for lx, lsize, lc in zip(layer_positions, layer_sizes, layer_colors):
            col = []
            for ni in range(lsize):
                y = (ni - (lsize - 1) / 2) * 0.6
                c = Circle(radius=0.18, color=lc, fill_color=lc, fill_opacity=0.7, stroke_width=1.5)
                c.move_to([lx, y, 0])
                col.append(c)
            nodes.append(col)

        edges = VGroup()
        for li in range(len(nodes) - 1):
            for n1 in nodes[li]:
                for n2 in nodes[li + 1]:
                    e = Line(n1.get_center(), n2.get_center(),
                             stroke_width=0.8, color=CARD_STROKE, stroke_opacity=0.9)
                    edges.add(e)

        all_nodes = VGroup(*[c for col in nodes for c in col])
        nn_group = VGroup(edges, all_nodes)
        nn_group.move_to([0, 0.2, 0])

        label_lin = Text("Xếp chồng các lớp tuyến tính + phi tuyến", font_size=20, color=TEXT_COLOR)
        label_lin.next_to(nn_group, DOWN, buff=0.45)

        question = Text("Nhúng bài toán tối ưu trực tiếp vào mạng nơ-ron?", font_size=22, color=PAPER_YELLOW)
        question.next_to(label_lin, DOWN, buff=0.35)

        self.play(Write(ctx_title), run_time=1.2)
        self.play(
            LaggedStart(*[Create(n) for col in nodes for n in col], lag_ratio=0.05),
            run_time=1.5
        )
        self.play(Create(edges), run_time=1.5)
        self.play(FadeIn(label_lin, shift=UP * 0.2), run_time=1.0)
        self.wait(10.0)
        self.play(Write(question), run_time=1.2)
        self.wait(12.0)
        self.play(FadeOut(VGroup(ctx_title, nn_group, label_lin, question)))

        # 3. Non-convex vs Convex
        compare_title = Text("Tối ưu hóa Lồi vs Không Lồi", font_size=32, color=PAPER_YELLOW)
        compare_title.to_edge(UP, buff=0.35)

        ax_nc = Axes(
            x_range=[-3, 3, 1], y_range=[-0.5, 4, 1],
            x_length=4.5, y_length=2.5,
            axis_config={"include_tip": False, "stroke_width": 1.5, "color": DIM_TEXT},
        )
        nc_label = Text("Không Lồi (Non-Convex)", font_size=18, color=PAPER_RED)

        ax_c = Axes(
            x_range=[-3, 3, 1], y_range=[-0.5, 4, 1],
            x_length=4.5, y_length=2.5,
            axis_config={"include_tip": False, "stroke_width": 1.5, "color": DIM_TEXT},
        )
        c_label = Text("Lồi (Convex)", font_size=18, color=PAPER_GREEN)

        nc_group = VGroup(ax_nc, nc_label)
        nc_label.next_to(ax_nc, DOWN, buff=0.25)
        c_group = VGroup(ax_c, c_label)
        c_label.next_to(ax_c, DOWN, buff=0.25)

        both = VGroup(nc_group, c_group)
        both.arrange(RIGHT, buff=0.8)
        both.next_to(compare_title, DOWN, buff=0.4)
        both.set_x(0)

        nc_func = lambda x: 0.0875 * (x**4) + 0.0117 * (x**3) - 0.4235 * (x**2) - 0.168 * x + 1.8
        c_func = lambda x: 0.45 * ((x - 0.5) ** 2) + 0.9

        nc_curve = ax_nc.plot(nc_func, x_range=[-2.5, 2.5], color=PAPER_RED, stroke_width=3)
        c_curve = ax_c.plot(c_func, x_range=[-2.5, 2.5], color=PAPER_GREEN, stroke_width=3)

        nc_tracker = ValueTracker(-2.0)
        nc_dot = Dot(color=HIGHLIGHT, radius=0.1)
        nc_dot.add_updater(lambda d: d.move_to(ax_nc.c2p(nc_tracker.get_value(), nc_func(nc_tracker.get_value()))))

        c_tracker = ValueTracker(2.2)
        c_dot = Dot(color=HIGHLIGHT, radius=0.1)
        c_dot.add_updater(lambda d: d.move_to(ax_c.c2p(c_tracker.get_value(), c_func(c_tracker.get_value()))))

        trap_label = Text("Cực tiểu cục bộ!", font_size=15, color=PAPER_RED)
        trap_label.next_to(nc_group, DOWN, buff=0.25)

        global_label = Text("Cực tiểu toàn cục", font_size=15, color=PAPER_GREEN)
        global_label.next_to(c_group, DOWN, buff=0.25)

        self.play(Write(compare_title), run_time=1.0)
        self.play(Create(ax_nc), Create(ax_c), FadeIn(nc_label), FadeIn(c_label), run_time=1.5)
        self.play(Create(nc_curve), Create(c_curve), run_time=2.0)
        self.wait(5.0)

        self.add(nc_dot)
        self.play(nc_tracker.animate.set_value(-1.5), run_time=3.0, rate_func=smooth)
        self.play(FadeIn(trap_label), run_time=1.0)
        self.wait(5.0)

        self.add(c_dot)
        self.play(c_tracker.animate.set_value(0.5), run_time=3.0, rate_func=smooth)
        self.play(FadeIn(global_label), run_time=1.0)
        self.wait(5.0)

        # Illustrate convexity chord definition on the right
        pt1 = ax_c.c2p(-1.2, c_func(-1.2))
        pt2 = ax_c.c2p(1.8, c_func(1.8))
        dot_pt1 = Dot(pt1, color=PAPER_BLUE, radius=0.08)
        dot_pt2 = Dot(pt2, color=PAPER_BLUE, radius=0.08)
        chord = Line(pt1, pt2, color=PAPER_YELLOW, stroke_width=2)
        
        chord_label = Paragraph(
            "Đoạn thẳng nối 2 điểm",
            "luôn nằm trên đồ thị",
            alignment="center",
            font_size=14,
            color=PAPER_YELLOW,
        ).next_to(chord, UP, buff=-0.3).shift(RIGHT * 0.4 + UP * 0.2)

        self.play(FadeIn(dot_pt1), FadeIn(dot_pt2))
        self.play(Create(chord), FadeIn(chord_label), run_time=1.0)
        self.wait(10.0)

        nc_dot.clear_updaters()
        c_dot.clear_updaters()
        self.play(
            FadeOut(VGroup(compare_title, both, nc_curve, c_curve, nc_dot, c_dot, trap_label, global_label, dot_pt1, dot_pt2, chord, chord_label))
        )

    # ═══════════════════════════════════════════════════════════════════
    # SCENE 2 — ReLU & Convexity Rules (≈75s)
    # ═══════════════════════════════════════════════════════════════════
    def scene2_relu_convexity(self):
        # 1. Intro ICNN
        icnn_title = Text("Mạng Nơ-ron Lồi theo Đầu vào", font_size=32, color=PAPER_YELLOW)
        icnn_title.to_edge(UP, buff=0.35)

        icnn_abbr = Text("ICNN", font_size=64, color=PAPER_BLUE)
        icnn_abbr.move_to([0, 0.3, 0])

        question_icnn = Text("Làm thế nào để f(x) lồi đối với x?", font_size=24, color=TEXT_COLOR)
        question_icnn.next_to(icnn_abbr, DOWN, buff=0.55)

        self.play(Write(icnn_title), run_time=1.2)
        self.play(FadeIn(icnn_abbr, scale=0.5), run_time=1.5)
        self.play(Write(question_icnn), run_time=1.2)
        self.wait(8.0)
        self.play(FadeOut(VGroup(icnn_title, icnn_abbr, question_icnn)))

        # 2. ReLU is Convex
        relu_title = Text("Hàm kích hoạt ReLU", font_size=32, color=PAPER_YELLOW)
        relu_title.to_edge(UP, buff=0.35)

        ax_relu = Axes(
            x_range=[-2.5, 2.5, 1], y_range=[-0.5, 2.5, 1],
            x_length=5.0, y_length=2.5,
            axis_config={"include_tip": False, "stroke_width": 1.5, "color": DIM_TEXT},
        )
        ax_relu.next_to(relu_title, DOWN, buff=0.4)
        ax_relu.set_x(0)

        relu_curve = ax_relu.plot(
            lambda x: max(0.0, x),
            x_range=[-2.5, 2.5, 0.01], color=PAPER_BLUE, stroke_width=3.5
        )
        relu_formula = MathTex(r"\text{ReLU}(x) = \max(0, x)", font_size=30, color=PAPER_BLUE)
        relu_formula.next_to(ax_relu, DOWN, buff=0.4)
        relu_formula.set_x(0)

        self.play(Write(relu_title), run_time=1.0)
        self.play(Create(ax_relu), run_time=1.2)
        self.play(Create(relu_curve), run_time=1.5)
        self.play(Write(relu_formula), run_time=1.2)
        self.wait(8.0)
        self.play(FadeOut(VGroup(relu_title, ax_relu, relu_curve, relu_formula)))

        # 3. Convexity Preservation Rules
        rules_title = Text("Nguyên lý Bảo toàn tính Lồi", font_size=32, color=PAPER_YELLOW)
        rules_title.to_edge(UP, buff=0.35)

        rule1_lbl = Text("1. Tổ hợp tuyến tính hệ số không âm:", font_size=18, color=TEXT_COLOR)
        rule1_math = VGroup(
            MathTex(r"f(x) = \sum w_i g_i(x) \quad", font_size=24, color=PAPER_GREEN),
            Text("(với", font_size=16, color=PAPER_GREEN),
            MathTex(r"w_i \geq 0", font_size=20, color=PAPER_GREEN),
            Text("và", font_size=16, color=PAPER_GREEN),
            MathTex(r"g_i", font_size=20, color=PAPER_GREEN),
            Text("lồi)", font_size=16, color=PAPER_GREEN)
        ).arrange(RIGHT, buff=0.08)
        
        rule2_lbl = Text("2. Hợp thành với hàm lồi, không giảm:", font_size=18, color=TEXT_COLOR)
        rule2_math = VGroup(
            MathTex(r"h(x) = f(g(x)) \quad", font_size=24, color=PAPER_BLUE),
            Text("(với", font_size=16, color=PAPER_BLUE),
            MathTex(r"f", font_size=20, color=PAPER_BLUE),
            Text("lồi, không giảm và", font_size=16, color=PAPER_BLUE),
            MathTex(r"g", font_size=20, color=PAPER_BLUE),
            Text("lồi)", font_size=16, color=PAPER_BLUE)
        ).arrange(RIGHT, buff=0.08)
        
        rule3_lbl = Text("3. Ép trọng số mạng nơ-ron ẩn:", font_size=18, color=TEXT_COLOR)
        rule3_math = VGroup(
            MathTex(r"W_i \geq 0 \implies", font_size=24, color=PAPER_YELLOW),
            MathTex(r"f(x)", font_size=20, color=PAPER_YELLOW),
            Text("lồi đối với", font_size=16, color=PAPER_YELLOW),
            MathTex(r"x", font_size=20, color=PAPER_YELLOW)
        ).arrange(RIGHT, buff=0.08)

        rules_band = VGroup(
            rule1_lbl, rule1_math,
            rule2_lbl, rule2_math,
            rule3_lbl, rule3_math
        )
        rules_band.arrange(DOWN, buff=0.25)
        rules_band.next_to(rules_title, DOWN, buff=0.5)
        rules_band.set_x(0)

        self.play(Write(rules_title), run_time=1.2)
        self.play(FadeIn(rule1_lbl, shift=RIGHT * 0.2), FadeIn(rule1_math, shift=RIGHT * 0.2), run_time=1.0)
        self.wait(5.0)
        self.play(FadeIn(rule2_lbl, shift=RIGHT * 0.2), FadeIn(rule2_math, shift=RIGHT * 0.2), run_time=1.0)
        self.wait(5.0)
        self.play(FadeIn(rule3_lbl, shift=RIGHT * 0.2), FadeIn(rule3_math, shift=RIGHT * 0.2), run_time=1.0)
        self.wait(10.0)
        self.play(FadeOut(VGroup(rules_title, rules_band)))

    # ═══════════════════════════════════════════════════════════════════
    # SCENE 3 — ICNN Architecture (≈75s)
    # ═══════════════════════════════════════════════════════════════════
    def scene3_icnn_architecture(self):
        arch_title = Text("Kiến trúc Mạng ICNN", font_size=32, color=PAPER_YELLOW)
        arch_title.to_edge(UP, buff=0.35)

        y_nodes = 0.5
        positions = [
            np.array([-4.0, y_nodes, 0]),
            np.array([-1.3, y_nodes, 0]),
            np.array([1.3, y_nodes, 0]),
            np.array([4.0, y_nodes, 0]),
        ]
        node_colors = [PAPER_GREEN, PAPER_YELLOW, PAPER_YELLOW, PAPER_BLUE]
        node_labels_tex = ["x", "z_1", "z_2", "f(x)"]

        nn_nodes = []
        nn_labels = []
        for pos, col, lbl in zip(positions, node_colors, node_labels_tex):
            c = Circle(radius=0.28, color=col, fill_color=col, fill_opacity=0.7, stroke_width=2)
            c.move_to(pos)
            l = MathTex(lbl, font_size=22, color=TEXT_COLOR)
            l.next_to(c, DOWN, buff=0.15)
            nn_nodes.append(c)
            nn_labels.append(l)

        # Sequential arrows (W)
        seq_arrows = VGroup()
        for i in range(len(nn_nodes) - 1):
            arr = Arrow(nn_nodes[i].get_right(), nn_nodes[i+1].get_left(),
                        buff=0.06, color=PAPER_GREEN, stroke_width=2.5)
            seq_arrows.add(arr)

        # Skip connections from x (node 0) to z1 and z2 (nodes 1, 2)
        skip_arrows = VGroup()
        for target_idx in [1, 2]:
            start = nn_nodes[0].get_bottom() + DOWN * 0.05
            end = nn_nodes[target_idx].get_bottom() + DOWN * 0.05
            path = ArcBetweenPoints(start, end, angle=TAU / 4)
            path.set_color(PAPER_ORANGE)
            path.set_stroke(width=2)
            skip_arrows.add(path)

        w_lbl = MathTex(r"W_i \geq 0", font_size=18, color=PAPER_GREEN)
        w_lbl.next_to(seq_arrows[1], UP, buff=0.1)

        u_lbl = MathTex(r"U_i \in \mathbb{R}", font_size=18, color=PAPER_ORANGE)
        u_lbl.next_to(skip_arrows[1], DOWN, buff=0.1)

        all_nodes_grp = VGroup(*nn_nodes, *nn_labels)
        arch_diagram = VGroup(all_nodes_grp, seq_arrows, skip_arrows, w_lbl, u_lbl)

        formula = MathTex(
            r"z_{i+1} = \text{ReLU}(W_i z_i + U_i x + b_i)",
            font_size=26,
            color=TEXT_COLOR
        )
        formula.next_to(arch_diagram, DOWN, buff=0.5)
        formula.set_x(0)

        self.play(Write(arch_title), run_time=1.0)
        self.play(
            LaggedStart(*[Create(n) for n in nn_nodes], lag_ratio=0.15),
            LaggedStart(*[Write(l) for l in nn_labels], lag_ratio=0.15),
            run_time=2.0
        )
        self.play(
            LaggedStart(*[GrowArrow(arr) for arr in seq_arrows], lag_ratio=0.3),
            run_time=1.5
        )
        self.wait(3.0)
        self.play(Create(skip_arrows), run_time=2.0)
        self.play(FadeIn(w_lbl), FadeIn(u_lbl), run_time=1.0)
        self.wait(4.0)
        self.play(Write(formula), run_time=1.5)
        self.wait(8.0)

        # Show Key Constraints
        self.play(FadeOut(arch_diagram), FadeOut(formula))
        
        wc_title = Text("Ràng buộc của mạng ICNN", font_size=32, color=PAPER_YELLOW)
        wc_title.to_edge(UP, buff=0.35)

        w_text = MathTex(r"W_i \geq 0", font_size=42, color=PAPER_GREEN)
        w_desc = Text("Trọng số ẩn-ẩn: Bắt buộc không âm", font_size=20, color=TEXT_COLOR)
        w_block = VGroup(w_text, w_desc)
        w_block.arrange(DOWN, buff=0.25)

        u_text = MathTex(r"U_i \in \mathbb{R}", font_size=42, color=PAPER_ORANGE)
        u_desc = Text("Trọng số kết nối tắt: Nhận giá trị bất kỳ", font_size=20, color=TEXT_COLOR)
        u_block = VGroup(u_text, u_desc)
        u_block.arrange(DOWN, buff=0.25)

        both_blocks = VGroup(w_block, u_block)
        both_blocks.arrange(DOWN, buff=0.55)
        both_blocks.next_to(wc_title, DOWN, buff=0.5)
        both_blocks.set_x(0)

        self.play(Transform(arch_title, wc_title))
        self.play(FadeIn(w_block, shift=UP * 0.2), run_time=1.2)
        self.wait(5.0)
        self.play(FadeIn(u_block, shift=UP * 0.2), run_time=1.2)
        self.wait(10.0)
        
        self.play(FadeOut(VGroup(arch_title, both_blocks)))

    # ═══════════════════════════════════════════════════════════════════
    # SCENE 4 — Energy-Based Models (≈60s)
    # ═══════════════════════════════════════════════════════════════════
    def scene4_energy_based_models(self):
        ebm_title = Text("Mô hình Năng lượng (Energy-Based Models)", font_size=32, color=PAPER_YELLOW)
        ebm_title.to_edge(UP, buff=0.35)

        energy_formula = MathTex(r"y^* = \arg\min_y\, f(x, y)", font_size=34, color=PAPER_BLUE)
        energy_formula.next_to(ebm_title, DOWN, buff=0.4)
        energy_formula.set_x(0)

        # Setup side-by-side: Grid on left, Curve on right
        # Grid representing Image Completion
        grid = VGroup(*[
            Square(side_length=0.4, fill_color=CARD_BG, fill_opacity=1, stroke_color=CARD_STROKE, stroke_width=1.0)
            for _ in range(25)
        ]).arrange_in_grid(rows=5, cols=5, buff=0.05).shift(LEFT * 3.3 + DOWN * 0.6)

        lbl_grid = VGroup(
            Text("Ảnh bị khuyết", font_size=16, color=PAPER_GREEN),
            MathTex(r"x", font_size=18, color=PAPER_GREEN)
        ).arrange(RIGHT, buff=0.08).next_to(grid, UP, buff=0.15)
        
        # Curve representing energy function
        ax_e = Axes(
            x_range=[-2.5, 2.5, 1], y_range=[0, 3, 1],
            x_length=4.5, y_length=2.2,
            axis_config={"include_tip": False, "stroke_width": 1.5, "color": DIM_TEXT},
        ).shift(RIGHT * 3.3 + DOWN * 0.6)

        y_func = lambda y: 0.5 * y**2 + 0.2
        bowl_curve = ax_e.plot(
            y_func,
            x_range=[-2.2, 2.2], color=PAPER_BLUE, stroke_width=3
        )
        
        min_dot = Dot(ax_e.c2p(0, 0.2), color=PAPER_YELLOW, radius=0.12)
        min_label = MathTex(r"y^*", font_size=22, color=PAPER_YELLOW)
        min_label.next_to(min_dot, UP, buff=0.12)

        # Gradient descent sliding dot
        y_tracker = ValueTracker(1.8)
        gd_dot = Dot(color=PAPER_RED, radius=0.1)
        gd_dot.add_updater(lambda d: d.move_to(ax_e.c2p(y_tracker.get_value(), y_func(y_tracker.get_value()))))

        gd_arrow = Arrow(
            ax_e.c2p(1.8, y_func(1.8)),
            ax_e.c2p(0.2, y_func(0.2)),
            color=PAPER_RED, stroke_width=2, buff=0.05
        )

        desc_text = VGroup(
            MathTex(r"f", font_size=22, color=PAPER_GREEN),
            Text("lồi đối với", font_size=18, color=PAPER_GREEN),
            MathTex(r"y \implies", font_size=22, color=PAPER_GREEN),
            Text("Đảm bảo cực tiểu toàn cục", font_size=18, color=PAPER_GREEN)
        ).arrange(RIGHT, buff=0.08)
        desc_text.next_to(ax_e, DOWN, buff=0.35).shift(LEFT * 3.3) # center under both
        desc_text.set_x(0)

        self.play(Write(ebm_title), run_time=1.0)
        self.play(Write(energy_formula), run_time=1.2)
        self.play(Create(grid), FadeIn(lbl_grid), run_time=1.2)
        self.play(Create(ax_e), Create(bowl_curve), run_time=1.5)
        self.wait(5.0)

        # Highlight missing central part of the grid (corrupted)
        missing_indices = [6, 7, 8, 11, 12, 13, 16, 17, 18]
        for idx in missing_indices:
            grid[idx].set_fill(PAPER_RED, opacity=0.4)
            grid[idx].set_stroke(PAPER_RED, width=1.5)
        self.play(FadeIn(gd_dot), run_time=0.8)
        self.wait(2.0)

        # Slide down while gradually completing the grid pixels
        def update_grid(obj):
            val = y_tracker.get_value()
            fraction = max(0.0, min(1.0, (1.8 - val) / 1.8))
            num_to_restore = int(fraction * len(missing_indices))
            for i in range(num_to_restore):
                grid[missing_indices[i]].set_fill(PAPER_GREEN, opacity=0.6)
                grid[missing_indices[i]].set_stroke(PAPER_GREEN, width=1.0)

        grid.add_updater(update_grid)

        self.play(
            y_tracker.animate.set_value(0.0),
            GrowArrow(gd_arrow),
            run_time=4.0,
            rate_func=smooth
        )
        self.wait(1.0)

        grid.clear_updaters()
        gd_dot.clear_updaters()

        self.play(FadeIn(min_dot), FadeIn(min_label), run_time=1.0)
        self.play(Write(desc_text), run_time=1.2)
        
        for idx in missing_indices:
            grid[idx].set_fill(PAPER_GREEN, opacity=0.6)
            grid[idx].set_stroke(PAPER_GREEN, width=1.0)
        
        self.wait(10.0)
        self.play(
            FadeOut(VGroup(ebm_title, energy_formula, grid, lbl_grid, ax_e, bowl_curve, min_dot, min_label, gd_dot, gd_arrow, desc_text))
        )

    # ═══════════════════════════════════════════════════════════════════
    # SCENE 5 — Lyapunov Stability (≈60s)
    # ═══════════════════════════════════════════════════════════════════
    def scene5_lyapunov_stability(self):
        lyap_title = Text("Tính ổn định Lyapunov", font_size=32, color=PAPER_YELLOW)
        lyap_title.to_edge(UP, buff=0.35)

        # Thiết lập cấu hình hệ trục tọa độ ô lưới
        plane_config = {
            "x_range": [-2, 2, 1],
            "y_range": [-2, 2, 1],
            "x_length": 3.5,
            "y_length": 3.5,
            "background_line_style": {
                "stroke_color": CARD_STROKE,
                "stroke_width": 1,
                "stroke_opacity": 0.4
            },
            "axis_config": {
                "include_tip": False, 
                "stroke_width": 1.5,
                "include_ticks": True,
                "stroke_color": DIM_TEXT
            }
        }

        # ==========================================================
        # ĐỒ THỊ 1: Nominal f_hat (Trường vector không ổn định)
        # ==========================================================
        ax1 = NumberPlane(**plane_config).shift(LEFT * 4.5 + UP * 0.9)
        ax1.add_coordinates() 

        def nominal_field(pos):
            x, y = ax1.p2c(pos)[0], ax1.p2c(pos)[1]
            # Công thức tạo dòng chảy hình yên ngựa/không ổn định
            return np.array([y + 0.3 * x, 0.6 * x, 0])

        vf1 = ArrowVectorField(
            nominal_field,
            x_range=[ax1.get_left()[0], ax1.get_right()[0], 0.45], 
            y_range=[ax1.get_bottom()[1], ax1.get_top()[1], 0.45],
            length_func=lambda norm: 0.22 if norm > 0 else 0,
            colors=[PAPER_BLUE, PAPER_RED]
        )

        title1 = VGroup(
            Text("Động lực danh định", font_size=15, color=PAPER_RED),
            MathTex(r"\hat{f}", font_size=18, color=PAPER_RED)
        ).arrange(RIGHT, buff=0.1).next_to(ax1, UP, buff=0.3)
        
        graph1 = VGroup(ax1, vf1, title1)

        # ==========================================================
        # ĐỒ THỊ 2: Lyapunov Function V (Các đường tròn đồng mức đồng tâm)
        # ==========================================================
        ax2 = NumberPlane(**plane_config).shift(UP * 0.9)
        ax2.add_coordinates()

        contours = VGroup()
        for r in np.linspace(0.4, 1.8, 8):
            radius_in_units = np.linalg.norm(ax2.c2p(r, 0) - ax2.c2p(0, 0))
            color = interpolate_color(ManimColor(PAPER_BLUE), ManimColor(PAPER_YELLOW), (r - 0.4) / 1.4)
            circle = Circle(radius=radius_in_units, color=color, stroke_width=2).move_to(ax2.c2p(0, 0))
            contours.add(circle)

        colorbar = Rectangle(height=3.5, width=0.18).next_to(ax2, RIGHT, buff=0.2)
        colorbar.set_fill(color=[PAPER_BLUE, PAPER_GREEN, PAPER_YELLOW], opacity=0.8)
        colorbar.set_stroke(color=CARD_STROKE, width=1)
        
        title2 = VGroup(
            Text("Hàm Lyapunov", font_size=15, color=PAPER_PURPLE),
            MathTex(r"V", font_size=18, color=PAPER_PURPLE)
        ).arrange(RIGHT, buff=0.1).next_to(ax2, UP, buff=0.3)
        
        graph2 = VGroup(ax2, contours, colorbar, title2)

        # ==========================================================
        # ĐỒ THỊ 3: Stable f (Trường vector xoáy tụ ổn định)
        # ==========================================================
        ax3 = NumberPlane(**plane_config).shift(RIGHT * 4.5 + UP * 0.9)
        ax3.add_coordinates()

        def stable_field(pos):
            x, y = ax3.p2c(pos)[0], ax3.p2c(pos)[1]
            # Công thức xoáy tụ về tâm (0,0)
            return np.array([-0.5 * x + y, -x - 0.5 * y, 0])

        vf3 = ArrowVectorField(
            stable_field,
            x_range=[ax3.get_left()[0], ax3.get_right()[0], 0.45],
            y_range=[ax3.get_bottom()[1], ax3.get_top()[1], 0.45],
            length_func=lambda norm: 0.22 if norm > 0 else 0,
            colors=[PAPER_BLUE, PAPER_GREEN]
        )

        title3 = VGroup(
            Text("Động lực ổn định", font_size=15, color=PAPER_GREEN),
            MathTex(r"f", font_size=18, color=PAPER_GREEN)
        ).arrange(RIGHT, buff=0.1).next_to(ax3, UP, buff=0.3)
        
        graph3 = VGroup(ax3, vf3, title3)

        # ==========================================================
        # PHẦN VĂN BẢN VÀ CÔNG THỨC TOÁN LATEX BÊN DƯỚI
        # ==========================================================
        description = VGroup(
            Text("Học hàm Lyapunov để đảm bảo tính ổn định vững chắc", font_size=18, color=TEXT_COLOR),
            Text("cho các hệ thống động lực học phức tạp bằng mạng nơ-ron sâu", font_size=18, color=TEXT_COLOR)
        ).arrange(DOWN, buff=0.15).shift(DOWN * 1.5)

        main_formula = MathTex(
            r"f(x) = \text{Proj}\left( \hat{f}(x), \{ \dot{V}(x) < 0 \} \right)",
            font_size=28, color=TEXT_COLOR
        ).next_to(description, DOWN, buff=0.35)

        # Mũi tên chỉ từ chữ ICNN lên cụm từ "{ \dot{V}(x) < 0 }"
        pointer_arrow = Arrow(
            start=main_formula.get_bottom() + RIGHT * 1.8 + DOWN * 0.7,
            end=main_formula.get_bottom() + RIGHT * 1.3 + DOWN * 0.1,
            buff=0, stroke_width=3, color=PAPER_YELLOW
        )
        icnn_label = MathTex(r"\text{ICNN}", font_size=24, color=PAPER_YELLOW).next_to(pointer_arrow, DOWN, buff=0.1)

        bottom_part = VGroup(description, main_formula, pointer_arrow, icnn_label)

        # Draw trajectories on top of ax1 (nominal) and ax3 (stable)
        t_vals = np.linspace(0, 3 * np.pi, 80)
        nominal_pts = []
        for t in t_vals:
            r = 0.12 * t
            x_val = r * np.cos(t)
            y_val = r * np.sin(t)
            nominal_pts.append(ax1.c2p(x_val, y_val))
        traj_nominal = VMobject(color=PAPER_RED, stroke_width=3)
        traj_nominal.set_points_as_corners(nominal_pts)
        traj_dot_nominal = Dot(color=PAPER_RED, radius=0.08)

        stable_pts = []
        for t in t_vals:
            rev_t = 3 * np.pi - t
            r = 0.15 * rev_t
            x_val = r * np.cos(t)
            y_val = r * np.sin(t)
            stable_pts.append(ax3.c2p(x_val, y_val))
        traj_stable = VMobject(color=PAPER_GREEN, stroke_width=3)
        traj_stable.set_points_as_corners(stable_pts)
        traj_dot_stable = Dot(color=PAPER_GREEN, radius=0.08)

        # ==========================================================
        # TIẾN HÀNH RENDER
        # ==========================================================
        self.play(Write(lyap_title), run_time=1.0)
        self.play(
            FadeIn(graph1),
            FadeIn(graph2),
            FadeIn(graph3),
            run_time=1.5
        )
        self.play(Write(bottom_part), run_time=1.8)
        self.wait(2.0)

        # Animate trajectory flow on fields
        self.play(
            Create(traj_nominal),
            MoveAlongPath(traj_dot_nominal, traj_nominal),
            run_time=4.0,
            rate_func=linear
        )
        self.wait(1.5)

        self.play(
            Create(traj_stable),
            MoveAlongPath(traj_dot_stable, traj_stable),
            run_time=4.0,
            rate_func=linear
        )
        self.wait(10.0)

        self.play(
            FadeOut(VGroup(lyap_title, graph1, graph2, graph3, bottom_part,
                           traj_nominal, traj_dot_nominal, traj_stable, traj_dot_stable))
        )

    # ═══════════════════════════════════════════════════════════════════
    # SCENE 6 — Limitations & Transition (≈45s)
    # ═══════════════════════════════════════════════════════════════════
    def scene6_limitations(self):
        lim_title = Text("Hạn chế của ICNN", font_size=32, color=PAPER_YELLOW)
        lim_title.to_edge(UP, buff=0.35)

        lim1 = VGroup(
            Text("• Trọng số", font_size=22, color=PAPER_RED),
            MathTex(r"W_i \geq 0", font_size=26, color=PAPER_RED),
            Text("làm giới hạn khả năng biểu diễn", font_size=22, color=PAPER_RED)
        ).arrange(RIGHT, buff=0.1)
        lim2 = Text("• Khó tích hợp linh hoạt vào các kiến trúc hiện đại", font_size=22, color=PAPER_RED)
        lim3 = Text("• Bắt buộc toàn bộ mạng nơ-ron phải lồi", font_size=22, color=PAPER_ORANGE)
        
        next_idea = Text("Nhúng bài toán tối ưu trực tiếp dưới dạng một lớp ẩn (layer)?", font_size=22, color=TEXT_COLOR)
        optnet_label = Text("⇒ OptNet", font_size=26, color=PAPER_YELLOW)

        all_items = VGroup(lim1, lim2, lim3, next_idea, optnet_label)
        all_items.arrange(DOWN, buff=0.45)
        all_items.next_to(lim_title, DOWN, buff=0.55)
        all_items.set_x(0)

        self.play(Write(lim_title), run_time=1.0)
        self.play(FadeIn(lim1, shift=UP * 0.15), run_time=1.0)
        self.wait(6.0)
        self.play(FadeIn(lim2, shift=UP * 0.15), run_time=1.0)
        self.wait(5.0)
        self.play(FadeIn(lim3, shift=UP * 0.15), run_time=1.0)
        self.wait(5.0)
        self.play(FadeIn(next_idea, shift=UP * 0.15), run_time=1.0)
        self.wait(4.0)
        self.play(FadeIn(optnet_label, scale=0.8), run_time=1.2)
        self.wait(8.0)
        self.play(FadeOut(VGroup(lim_title, all_items)))
        self.wait(1.0)
