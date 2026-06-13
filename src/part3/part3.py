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

class Part3V2Scene(Scene):
    """Scene giải thích OptNet — Optimization in the Loop (5 minutes)."""

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
        
        self.scene1_intro_optnet()
        self.scene2_opt_layer_sliding()
        self.scene3_relu_opt()
        self.scene4_hard_constraints()
        self.scene5_ilya_quote()
        self.scene6_limitations()

    # ═══════════════════════════════════════════════════════════════════
    # SCENE 1 — Intro OptNet (0:00 - 0:40)
    # ═══════════════════════════════════════════════════════════════════
    def scene1_intro_optnet(self):
        title = Text("Chương 1: Optimization & Implicit Layers", font_size=32, color=PAPER_YELLOW)
        subtitle = Text("OptNet — Optimization in the loop", font_size=24, color=PAPER_BLUE)
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
            '"OptNet: Differentiable Optimization as a Layer in Neural Networks"',
            font_size=20,
            color=TEXT_COLOR,
            weight=BOLD
        )
        paper_conf = Text("International Conference on Machine Learning (ICML) 2017", font_size=18, color=HIGHLIGHT)
        paper_info = VGroup(paper_title, paper_conf).arrange(DOWN, buff=0.25).move_to(paper_card.get_center())

        paper_group = VGroup(paper_card, paper_info)

        # Author cards
        author_names = ["Brandon Amos", "Priya Donti", "Po-Wei Wang", "Zico Kolter"]
        author_colors = [PAPER_BLUE, PAPER_PURPLE, PAPER_GREEN, PAPER_ORANGE]
        author_cards = VGroup()

        for name, col in zip(author_names, author_colors):
            card_rect = RoundedRectangle(
                corner_radius=0.1,
                height=1.2,
                width=2.5,
                stroke_color=col,
                stroke_width=2,
                fill_color=CARD_BG,
                fill_opacity=0.9
            )
            card_text = Text(name, font_size=18, color=TEXT_COLOR)
            card_text.move_to(card_rect.get_center())
            author_cards.add(VGroup(card_rect, card_text))

        author_cards.arrange(RIGHT, buff=0.35)
        author_cards.move_to(DOWN * 1.8)

        self.play(Create(paper_card), run_time=1.2)
        self.play(Write(paper_info), run_time=1.5)
        self.wait(6.0)

        self.play(
            LaggedStart(*[FadeIn(card, shift=UP * 0.25) for card in author_cards], lag_ratio=0.18),
            run_time=2.0
        )
        # Total wait ~30s matching script
        self.wait(20.0)
        self.play(FadeOut(VGroup(title_group, paper_group, author_cards)))

    # ═══════════════════════════════════════════════════════════════════
    # SCENE 2 — Optimization Layer Math & Sliding (0:40 - 1:40)
    # ═══════════════════════════════════════════════════════════════════
    def scene2_opt_layer_sliding(self):
        math_title = Text("Cơ chế hoạt động của Optimization Layer", font_size=30, color=PAPER_YELLOW)
        math_title.to_edge(UP, buff=0.35)

        # 2D plane setup
        ax = Axes(
            x_range=[-0.5, 6.5, 1], y_range=[-0.5, 5.5, 1],
            x_length=5.0, y_length=4.5,
            axis_config={"include_tip": False, "stroke_width": 1.5, "color": DIM_TEXT},
        )
        ax.shift(LEFT * 3.2 + DOWN * 0.4)

        alpha = ValueTracker(0)

        # Dynamic coordinates
        C1 = np.array([3.8, 4.0])
        C2 = np.array([4.8, 1.5])
        
        base_v = np.array([(1, 1), (3.5, 0.8), (4, 2.5), (2.5, 4.0), (1, 3.2)])
        shift_vec = np.array([-1.2, -0.6])

        def get_closest_point(verts, p):
            min_dist = float('inf')
            closest = None
            y_scale = 3.0
            for i in range(len(verts)):
                a = verts[i]
                b = verts[(i + 1) % len(verts)]
                ap = p - a
                ab = b - a
                dot_ap_ab = ap[0]*ab[0] + y_scale * ap[1]*ab[1]
                dot_ab_ab = ab[0]*ab[0] + y_scale * ab[1]*ab[1]
                t = dot_ap_ab / max(dot_ab_ab, 1e-8)
                t = max(0.0, min(1.0, t))
                cp = a + t * ab
                dx = p[0] - cp[0]
                dy = p[1] - cp[1]
                d = np.sqrt(dx*dx + y_scale * dy*dy)
                if d < min_dist:
                    min_dist = d
                    closest = cp
            return closest

        # Formula text on the right
        formula_box = RoundedRectangle(
            corner_radius=0.12,
            height=2.8,
            width=5.5,
            stroke_color=CARD_STROKE,
            stroke_width=2,
            fill_color=CARD_BG,
            fill_opacity=0.9
        )
        formula_box.shift(RIGHT * 3.4 + UP * 0.8)

        eq_title = Text("Bài toán trong Lớp Ẩn", font_size=20, color=PAPER_YELLOW)
        eq_title.next_to(formula_box.get_top(), DOWN, buff=0.25)

        eq_math = MathTex(
            r"z_{i+1} = \underset{x \in \mathcal{C}(z_i)}{\operatorname{argmin}} \; f(x, z_i)",
            font_size=26,
            color=TEXT_COLOR
        )
        eq_math.move_to(formula_box.get_center() + DOWN * 0.05)

        input_group = VGroup(
            VGroup(Text("• Đầu vào ", font_size=18, color=TEXT_COLOR), MathTex(r"z_i", font_size=24, color=TEXT_COLOR), Text(" điều khiển:", font_size=18, color=TEXT_COLOR)).arrange(RIGHT, buff=0.05),
            VGroup(Text("   - Vùng ràng buộc ", font_size=18, color=PAPER_BLUE), MathTex(r"\mathcal{C}(z_i)", font_size=24, color=PAPER_BLUE)).arrange(RIGHT, buff=0.05),
            VGroup(Text("   - Hàm mục tiêu ", font_size=18, color=PAPER_RED), MathTex(r"f(x, z_i)", font_size=24, color=PAPER_RED)).arrange(RIGHT, buff=0.05)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        
        output_group = VGroup(
            Text("• Đầu ra ", font_size=18, color=TEXT_COLOR), 
            MathTex(r"z_{i+1}", font_size=24, color=HIGHLIGHT), 
            Text(" trượt liên tục", font_size=18, color=TEXT_COLOR)
        ).arrange(RIGHT, buff=0.05)

        explanation = VGroup(input_group, output_group).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        explanation.next_to(formula_box, DOWN, buff=0.4)
        explanation.align_to(formula_box, LEFT)

        self.play(Write(math_title), run_time=1.0)
        self.play(Create(ax), run_time=1.0)
        self.play(Create(formula_box), Write(eq_title), Write(eq_math), run_time=1.5)
        self.wait(4.0)

        # Polygon and elements
        poly = Polygon(*[ax.c2p(x, y) for x, y in base_v], fill_color=PAPER_BLUE, fill_opacity=0.3, stroke_color=PAPER_BLUE, stroke_width=2.5)
        
        def update_poly(p):
            a = alpha.get_value()
            verts = base_v + shift_vec * a
            new_p = Polygon(*[ax.c2p(x, y) for x, y in verts], fill_color=PAPER_BLUE, fill_opacity=0.3, stroke_color=PAPER_BLUE, stroke_width=2.5)
            p.become(new_p)
            
        poly.add_updater(update_poly)

        center_dot = Dot(color=PAPER_RED, radius=0.08)
        def update_center(d):
            a = alpha.get_value()
            c_pos = C1 * (1 - a) + C2 * a
            d.move_to(ax.c2p(c_pos[0], c_pos[1]))
        center_dot.add_updater(update_center)

        center_label = MathTex(r"f(x, z_i)", font_size=20, color=PAPER_RED)
        def update_center_label(l):
            l.next_to(center_dot, UR, buff=0.1)
        center_label.add_updater(update_center_label)

        poly_label = MathTex(r"\mathcal{C}(z_i)", font_size=22, color=PAPER_BLUE)
        def update_poly_label(l):
            a = alpha.get_value()
            verts = base_v + shift_vec * a
            l.move_to(ax.c2p(verts[2][0] + 0.5, verts[2][1] + 0.2))
        poly_label.add_updater(update_poly_label)

        argmin_dot = Dot(color=HIGHLIGHT, radius=0.09)
        def update_argmin(d):
            a = alpha.get_value()
            c_pos = C1 * (1 - a) + C2 * a
            verts = base_v + shift_vec * a
            p_pos = get_closest_point(verts, c_pos)
            d.move_to(ax.c2p(p_pos[0], p_pos[1]))
        argmin_dot.add_updater(update_argmin)

        ellipses = VGroup()
        def update_ellipses(ells):
            a = alpha.get_value()
            c_pos = C1 * (1 - a) + C2 * a
            verts = base_v + shift_vec * a
            p_pos = get_closest_point(verts, c_pos)
            
            c_screen = ax.c2p(c_pos[0], c_pos[1])
            
            dx = c_pos[0] - p_pos[0]
            dy = c_pos[1] - p_pos[1]
            R = np.sqrt(dx*dx + 3.0 * dy*dy)
            
            a_screen = R * ax.x_axis.get_unit_size()
            b_screen = (R / np.sqrt(3.0)) * ax.y_axis.get_unit_size()
            
            new_ells = VGroup()
            for factor, col, width, op in [(0.4, PAPER_YELLOW, 1.5, 0.45), 
                                          (1.0, HIGHLIGHT, 2.5, 1.0), 
                                          (1.6, PAPER_ORANGE, 1.5, 0.45)]:
                ell = Ellipse(width=max(0.01, 2 * a_screen * factor), height=max(0.01, 2 * b_screen * factor), color=col, stroke_width=width)
                ell.set_stroke(opacity=op)
                ell.move_to(c_screen)
                new_ells.add(ell)
            ells.become(new_ells)
        
        ellipses.add_updater(update_ellipses)

        # Show initial state
        self.play(FadeIn(explanation[0]), run_time=1.5)
        self.play(Create(poly), FadeIn(poly_label), run_time=1.5)
        self.play(Create(center_dot), FadeIn(center_label), run_time=1.0)
        self.wait(1.0)
        
        # Show contours
        self.add(ellipses)
        self.play(Create(argmin_dot), FadeIn(explanation[1]), run_time=1.5)
        
        # Flash the optimal point
        self.play(Flash(argmin_dot, color=HIGHLIGHT, line_length=0.25, num_lines=10), run_time=1.2)
        self.wait(5.0)

        # SLIDING ANIMATION (Đầu vào thay đổi -> Hàm mục tiêu & Ràng buộc trượt)
        self.play(
            alpha.animate.set_value(1.0),
            run_time=6.0,
            rate_func=smooth
        )
        self.wait(15.0)

        poly.clear_updaters()
        center_dot.clear_updaters()
        argmin_dot.clear_updaters()
        center_label.clear_updaters()
        poly_label.clear_updaters()
        ellipses.clear_updaters()

        self.play(
            FadeOut(VGroup(
                math_title, ax, poly, center_dot, argmin_dot, ellipses,
                center_label, poly_label,
                formula_box, eq_title, eq_math, explanation
            ))
        )

    # ═══════════════════════════════════════════════════════════════════
    # SCENE 3 — ReLU as an Optimization Problem (1:40 - 2:30)
    # ═══════════════════════════════════════════════════════════════════
    def scene3_relu_opt(self):
        relu_title = Text("Góc nhìn tối ưu của hàm ReLU", font_size=30, color=PAPER_YELLOW)
        relu_title.to_edge(UP, buff=0.35)

        # 1D axes
        ax_1d = NumberLine(
            x_range=[-3, 3, 1], length=7,
            color=DIM_TEXT, include_numbers=True, font_size=20
        )
        ax_1d.move_to(UP * 0.5)

        constraint_line = Line(
            ax_1d.n2p(0), ax_1d.n2p(3.5),
            color=PAPER_GREEN, stroke_width=6
        )
        constraint_label = Text("Vùng ràng buộc cứng: y >= 0", font_size=18, color=PAPER_GREEN)
        constraint_label.next_to(constraint_line, DOWN, buff=0.5)

        x_tracker = ValueTracker(2.5)
        
        x_dot = Dot(color=PAPER_BLUE, radius=0.1)
        x_label = MathTex(r"x", font_size=24, color=PAPER_BLUE)
        def update_x_dot(d):
            d.move_to(ax_1d.n2p(x_tracker.get_value()))
            x_label.next_to(d, UP, buff=0.15)
        x_dot.add_updater(update_x_dot)

        y_dot = Dot(color=HIGHLIGHT, radius=0.12)
        y_label = MathTex(r"y^*", font_size=24, color=HIGHLIGHT)
        def update_y_dot(d):
            val = max(0, x_tracker.get_value())
            d.move_to(ax_1d.n2p(val) + UP * 0.05)
            y_label.next_to(d, UP, buff=0.2)
        y_dot.add_updater(update_y_dot)

        dist_line = Line(color=PAPER_RED, stroke_width=2)
        def update_dist_line(l):
            val = max(0, x_tracker.get_value())
            if x_tracker.get_value() < 0:
                l.put_start_and_end_on(ax_1d.n2p(val), ax_1d.n2p(x_tracker.get_value()))
                l.set_opacity(1.0)
            else:
                l.set_opacity(0.0)
        dist_line.add_updater(update_dist_line)

        formulas = VGroup(
            VGroup(
                Text("Standard Layer: ", font_size=20, color=TEXT_COLOR),
                MathTex(r"y = \max(0, x)", font_size=26, color=PAPER_BLUE)
            ).arrange(RIGHT, buff=0.2),
            VGroup(
                Text("Optimization Layer: ", font_size=20, color=TEXT_COLOR),
                MathTex(r"y^* = \underset{y \geq 0}{\operatorname{argmin}} \; \frac{1}{2} (y - x)^2", font_size=26, color=HIGHLIGHT)
            ).arrange(RIGHT, buff=0.2)
        ).arrange(DOWN, buff=0.6, aligned_edge=LEFT)
        formulas.move_to(DOWN * 1.8)

        self.play(Write(relu_title), run_time=1.0)
        self.play(Create(ax_1d), run_time=1.2)
        self.wait(5.0)

        self.play(FadeIn(formulas[0]), run_time=1.0)
        self.wait(5.0)

        self.play(FadeIn(formulas[1]), run_time=1.5)
        self.play(Create(constraint_line), FadeIn(constraint_label), run_time=1.5)
        self.wait(3.0)

        # Cập nhật tọa độ chuẩn trước khi hiện để không bị nhảy từ gốc tọa độ
        update_x_dot(x_dot)
        update_y_dot(y_dot)
        update_dist_line(dist_line)
  
        # Hiện x, y*, và line trước
        self.play(FadeIn(VGroup(x_dot, x_label, y_dot, y_label, dist_line)), run_time=1.0)
        
        # Chờ 1s trước khi bắt đầu chuyển động
        self.wait(1.0)

        # Trượt x từ dương sang âm
        self.play(x_tracker.animate.set_value(1.0), run_time=2.0)
        self.wait(1.0)
        self.play(x_tracker.animate.set_value(-2.0), run_time=3.0, rate_func=smooth)
        self.wait(2.0)
        self.play(x_tracker.animate.set_value(-0.5), run_time=2.0)
        self.wait(10.0)

        x_dot.clear_updaters()
        y_dot.clear_updaters()
        dist_line.clear_updaters()
        
        self.play(FadeOut(VGroup(
            relu_title, ax_1d, constraint_line, constraint_label,
            x_dot, x_label, y_dot, y_label, dist_line, formulas
        )))

    # ═══════════════════════════════════════════════════════════════════
    # SCENE 4 — Hard Constraints & Sudoku (2:30 - 3:30)
    # ═══════════════════════════════════════════════════════════════════
    def scene4_hard_constraints(self):
        title = Text("Ràng buộc cứng (Hard Constraints)", font_size=30, color=PAPER_YELLOW)
        title.to_edge(UP, buff=0.35)

        # Soft vs Hard Box
        box_soft = RoundedRectangle(height=2.0, width=5.0, corner_radius=0.1, stroke_color=PAPER_RED, fill_color=CARD_BG, fill_opacity=0.9)
        box_hard = RoundedRectangle(height=2.0, width=5.0, corner_radius=0.1, stroke_color=PAPER_GREEN, fill_color=CARD_BG, fill_opacity=0.9)
        
        soft_group = VGroup(
            box_soft,
            Text("Soft Constraints (Loss Function)", font_size=20, color=PAPER_RED).next_to(box_soft.get_top(), DOWN, buff=0.15),
            Text("Mạng học cách xấp xỉ xác suất.\nThi thoảng vẫn vi phạm luật.", font_size=18, color=TEXT_COLOR, line_spacing=1).move_to(box_soft.get_center() + DOWN*0.2)
        )
        
        hard_group = VGroup(
            box_hard,
            Text("Hard Constraints (OptNet)", font_size=20, color=PAPER_GREEN).next_to(box_hard.get_top(), DOWN, buff=0.15),
            Text("Được mã hóa thành quy luật thép.\nTuyệt đối không vi phạm.", font_size=18, color=TEXT_COLOR, line_spacing=1).move_to(box_hard.get_center() + DOWN*0.2)
        )

        compare_group = VGroup(soft_group, hard_group).arrange(RIGHT, buff=0.8).move_to(UP * 1.5)

        # Sudoku Grid Example
        grid = NumberPlane(
            x_range=[0, 3, 1], y_range=[0, 3, 1],
            x_length=3, y_length=3,
            background_line_style={"stroke_color": DIM_TEXT, "stroke_width": 2, "stroke_opacity": 0.8}
        ).move_to(DOWN * 1.5)

        nums = VGroup(
            Text("5", font_size=28, color=TEXT_COLOR).move_to(grid.c2p(0.5, 2.5)),
            Text("3", font_size=28, color=TEXT_COLOR).move_to(grid.c2p(1.5, 2.5)),
            Text("1", font_size=28, color=TEXT_COLOR).move_to(grid.c2p(0.5, 1.5)),
            Text("8", font_size=28, color=TEXT_COLOR).move_to(grid.c2p(2.5, 0.5)),
        )

        # Red violation
        violation = Text("5", font_size=28, color=PAPER_RED).move_to(grid.c2p(2.5, 2.5))
        cross = Cross(violation, stroke_color=PAPER_RED, stroke_width=4, scale_factor=0.6)

        sudoku_label = Text("Ứng dụng: Giải Sudoku logic", font_size=22, color=HIGHLIGHT).next_to(grid, RIGHT, buff=0.8).shift(UP * 0.5)
        power_label = Text("Tối ưu hóa Lưới điện thông minh", font_size=22, color=PAPER_BLUE).next_to(sudoku_label, DOWN, buff=0.5)

        self.play(Write(title), run_time=1.0)
        self.play(FadeIn(soft_group, shift=UP*0.2), run_time=1.2)
        self.wait(10.0)
        
        self.play(FadeIn(hard_group, shift=UP*0.2), run_time=1.2)
        self.wait(6.0)

        self.play(Create(grid), FadeIn(nums), run_time=1.5)
        self.wait(4.0)

        # Show violation
        self.play(Write(violation), run_time=0.8)
        self.wait(1.0)
        self.play(Create(cross), run_time=0.8)
        self.wait(5.0)

        # Replace with correct
        correct = Text("7", font_size=28, color=PAPER_GREEN).move_to(grid.c2p(2.5, 2.5))
        self.play(FadeOut(violation), FadeOut(cross), FadeIn(correct), run_time=1.0)
        
        self.play(Write(sudoku_label), run_time=1.0)
        self.wait(5.0)
        self.play(Write(power_label), run_time=1.0)
        self.wait(10.0)

        self.play(FadeOut(VGroup(title, compare_group, grid, nums, correct, sudoku_label, power_label)))


    # ═══════════════════════════════════════════════════════════════════
    # SCENE 5 — Ilya's Quote (3:30 - 4:10)
    # ═══════════════════════════════════════════════════════════════════
    def scene5_ilya_quote(self):
        anec_title = Text("Sự kỳ vọng từ giới học giả", font_size=30, color=PAPER_YELLOW)
        anec_title.to_edge(UP, buff=0.35)

        ilya_card = RoundedRectangle(
            corner_radius=0.15,
            height=3.5,
            width=4.0,
            stroke_color=PAPER_BLUE,
            stroke_width=2.5,
            fill_color=CARD_BG,
            fill_opacity=0.9
        )
        ilya_card.shift(LEFT * 3.5 + DOWN * 0.2)

        ilya_title = Text("Ilya Sutskever", font_size=24, color=PAPER_BLUE, weight=BOLD)
        ilya_subtitle = Text("Co-founder, OpenAI", font_size=18, color=DIM_TEXT)
        ilya_desc = Paragraph(
            "Một trong những bộ óc\nhọc sâu vĩ đại nhất.",
            font_size=18,
            color=TEXT_COLOR,
            line_spacing=1,
            alignment="center"
        )
        ilya_content = VGroup(ilya_title, ilya_subtitle, ilya_desc).arrange(DOWN, buff=0.35)
        ilya_content.move_to(ilya_card.get_center())

        bubble = RoundedRectangle(
            corner_radius=0.2,
            height=2.2,
            width=6.0,
            stroke_color=PAPER_ORANGE,
            stroke_width=2.5,
            fill_color=CARD_BG,
            fill_opacity=0.9
        )
        bubble.shift(RIGHT * 2.8 + UP * 0.4)

        bubble_tail = Polygon(
            [2.8 - 3.0, 0.4, 0], [2.8 - 3.0, 0.1, 0], [2.8 - 3.2, 0.25, 0],
            fill_color=PAPER_ORANGE, fill_opacity=1.0, stroke_color=PAPER_ORANGE
        )
        bubble_tail.next_to(bubble, LEFT, buff=0.01)

        quote_en = Text(
            '"This will be as big as ResNets"',
            font_size=22,
            color=PAPER_ORANGE,
            weight=BOLD
        )
        quote_vi = Text(
            '"Kiến trúc này sẽ lớn mạnh ngang tầm ResNet"',
            font_size=18,
            color=TEXT_COLOR,
            weight=BOLD
        )
        quote_group = VGroup(quote_en, quote_vi).arrange(DOWN, buff=0.25)
        quote_group.move_to(bubble.get_center())

        self.play(Write(anec_title), run_time=1.0)
        self.play(Create(ilya_card), Write(ilya_content), run_time=1.5)
        self.wait(10.0)

        self.play(Create(bubble), Create(bubble_tail), run_time=1.2)
        self.play(Write(quote_group), run_time=1.5)
        self.wait(18.0)

        self.play(FadeOut(VGroup(anec_title, ilya_card, ilya_content, bubble, bubble_tail, quote_group)))

    # ═══════════════════════════════════════════════════════════════════
    # SCENE 6 — Limitations & DEQ Transition (4:10 - 5:00)
    # ═══════════════════════════════════════════════════════════════════
    def scene6_limitations(self):
        end_title = Text("Rào cản thực tế & Chuyển giao", font_size=30, color=PAPER_YELLOW)
        end_title.to_edge(UP, buff=0.35)

        lim_box = RoundedRectangle(
            corner_radius=0.15,
            height=3.8,
            width=9,
            stroke_color=PAPER_RED,
            stroke_width=2,
            fill_color=CARD_BG,
            fill_opacity=0.9
        ).move_to(UP * 0.8)

        lim_title = Text("Tại sao OptNet không phổ biến?", font_size=22, color=PAPER_RED)
        lim_title.next_to(lim_box.get_top(), DOWN, buff=0.25)

        lims_list = Paragraph(
            "1. Chi phí tính toán khổng lồ:\n"
            "   - Phải giải bài toán lồi hoàn chỉnh ở mỗi lớp,\n"
            "     cho mỗi bước Forward và Backward pass.\n\n"
            "2. Triết lý ngược với Scaling hiện đại:\n"
            "   - AI hiện đại: Hàng tỷ tham số, tính toán đơn giản (Transformer).\n"
            "   - OptNet: Rất ít tham số, tính toán cực kỳ phức tạp và tuần tự.",
            font_size=19,
            color=TEXT_COLOR,
            line_spacing=1
        )
        lims_list.next_to(lim_title, DOWN, buff=0.3)
        lims_list.align_to(lim_box, LEFT).shift(RIGHT * 0.4)

        transition_text = Text(
            "Làm thế nào để tìm được điểm cân bằng toán học, mà lại xử lý gọn nhẹ vấn đề tài nguyên?",
            font_size=20,
            color=DIM_TEXT
        )
        transition_text.move_to(DOWN * 1.8)

        deq_text = Text(
            "⇒ Deep Equilibrium Models",
            font_size=24,
            color=PAPER_YELLOW
        )
        deq_text.move_to(DOWN * 2.8)

        self.play(Write(end_title), run_time=1.0)
        self.wait(3.0)
        self.play(Create(lim_box), Write(lim_title), run_time=1.5)
        self.play(FadeIn(lims_list, shift=UP * 0.2), run_time=2.0)
        self.wait(18.0)

        self.play(Write(transition_text), run_time=1.2)
        self.wait(8.0)
        self.play(FadeIn(deq_text, scale=0.9), run_time=1.2)
        self.wait(10.0)

        self.play(FadeOut(VGroup(end_title, lim_box, lim_title, lims_list, transition_text, deq_text)))
        self.wait(1.5)
