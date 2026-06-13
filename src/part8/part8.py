"""Part 8 — Khoa học thực nghiệm của Deep Learning
Thời lượng mục tiêu: 9 phút (40:00 – 49:00)

Render preview:
    python -m manim -ql src/part8/part8.py Part8Scene
Render chất lượng cao:
    python -m manim -pqh src/part8/part8.py Part8Scene
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
PAPER_ORANGE = "#f0883e"
PAPER_YELLOW = "#d29922"
PAPER_PURPLE = "#a371f7"

class Part8Scene(Scene):
    """Scene giải thích Khoa học thực nghiệm của Deep Learning (Part 8)."""

    def construct(self):
        Text.set_default(font="sans-serif", font_size=24)
        Paragraph.set_default(font="sans-serif", font_size=24)

        self.camera.background_color = BG

        # Sequential scenes according to part8_script.txt
        self.scene1_intro_empirics()
        self.scene2_edge_of_stability()
        self.scene3_disagreement_error()
        self.scene4_agreement_on_the_line()
        self.scene5_summary()
        self.scene6_transition()

    # ═══════════════════════════════════════════════════════════════════
    # SCENE 1 — Intro to Empirical Deep Learning (≈1m30s)
    # ═══════════════════════════════════════════════════════════════════
    def scene1_intro_empirics(self):
        # 0s - 4.5s: Title introduction card
        title = Text(
            "Khoa học thực nghiệm Deep Learning",
            font_size=36,
            color=TITLE_COLOR,
        ).shift(UP * 0.5)
        
        self.play(Write(title), run_time=1.5)
        self.wait(4.5) # Reach 6.0s
        self.play(FadeOut(title), run_time=0.5) # Reach 6.5s

        # Helper to draw simple networks
        def draw_net(center_pos, layer_sizes, color):
            nodes = VGroup()
            edges = VGroup()
            layers = []
            for i, sz in enumerate(layer_sizes):
                layer = VGroup()
                for j in range(sz):
                    node = Circle(radius=0.08, fill_color=color, fill_opacity=0.9, stroke_color=WHITE, stroke_width=0.6)
                    node.move_to(center_pos + RIGHT * i * 0.7 + UP * (j - (sz - 1)/2) * 0.35)
                    layer.add(node)
                layers.append(layer)
                nodes.add(layer)
            
            for i in range(len(layer_sizes) - 1):
                for n1 in layers[i]:
                    for n2 in layers[i+1]:
                        edge = Line(n1.get_center(), n2.get_center(), stroke_color=DIM_TEXT, stroke_width=0.4, stroke_opacity=0.3)
                        edges.add(edge)
            return VGroup(edges, nodes)

        # 6.5s: Step 1: Small neural network (2015)
        net_small = draw_net(LEFT * 4 + DOWN * 0.5, [3, 4, 2], PAPER_BLUE)
        label_2015 = Text("Mô hình năm 2015 (Vừa phải)", font_size=16, color=PAPER_BLUE).next_to(net_small, UP, buff=0.3)

        self.play(Create(net_small), FadeIn(label_2015), run_time=1.0)
        self.wait(1.5) # Reach 7.5s

        # Step 2: Growing the network (Scaling Era - 2020+)
        net_large = draw_net(LEFT * 4 + DOWN * 0.5, [4, 6, 6, 4], PAPER_ORANGE)
        label_scaling = Text("Scaling Era: Mô hình khổng lồ", font_size=16, color=PAPER_ORANGE).next_to(net_large, UP, buff=0.3)

        self.play(
            ReplacementTransform(net_small, net_large),
            ReplacementTransform(label_2015, label_scaling),
            run_time=1.5
        ) # Reach 9.0s
        self.wait(2.0) # Reach 11.0s

        # Step 3: Shift model to Industry side and show compute stream
        industry_label = Text("Công nghiệp (Industry)", font_size=18, color=PAPER_ORANGE).shift(RIGHT * 3.5 + UP * 1.5)
        academia_label = Text("Học thuật (Academia)", font_size=18, color=PAPER_BLUE).shift(LEFT * 3.5 + UP * 1.5)
        barrier = DashedLine(UP * 1.2, DOWN * 3.0, color=PAPER_RED, stroke_width=1.5)

        self.play(
            net_large.animate.shift(RIGHT * 5.0),
            label_scaling.animate.shift(RIGHT * 5.0),
            FadeIn(industry_label), FadeIn(academia_label), Create(barrier),
            run_time=1.5
        ) # Reach 12.5s
        self.wait(1.0) # Reach 13.5s

        # Compute stream: multiple small glowing dots flowing into the network
        compute_stream = VGroup()
        for i in range(12):
            dot = Dot(radius=0.06, color=PAPER_YELLOW, fill_opacity=0.8)
            dot.move_to(RIGHT * 6.5 + UP * np.random.uniform(-1.5, 1.5))
            compute_stream.add(dot)

        self.play(FadeIn(compute_stream), run_time=0.5) # Reach 14.0s
        self.play(
            *[dot.animate.move_to(net_large.get_center() + np.random.normal(0, 0.4, 3)) for dot in compute_stream],
            run_time=2.0
        ) # Reach 16.0s
        
        # Jiggle compute stream to avoid static visual until 23.0s
        for _ in range(2):
            self.play(
                *[dot.animate.shift(np.random.normal(0, 0.1, 3)) for dot in compute_stream],
                run_time=1.75
            ) # 3.5s total -> Reach 19.5s
        self.wait(4.5) # Reach 26.5s

        # 26.5s: Step 4: Academia resources & GPT-3/PaLM stats
        academia_bound = RoundedRectangle(
            width=4.2, height=2.8, corner_radius=0.1,
            fill_color=CARD_BG, fill_opacity=0.5, stroke_color=PAPER_BLUE, stroke_width=1.2
        ).shift(LEFT * 3.5 + DOWN * 0.5)
        academia_desc = Text("Hạn chế tài nguyên tính toán", font_size=14, color=DIM_TEXT).next_to(academia_bound, DOWN, buff=0.15)

        self.play(Create(academia_bound), FadeIn(academia_desc), run_time=1.5) # Reach 24.5s
        
        stats_gpt = Text("GPT-3 (175 tỷ tham số)\nChi phí: ~12 triệu USD", font_size=14, color=PAPER_RED).next_to(academia_bound.get_left(), RIGHT, buff=0.3).shift(UP * 0.4)
        stats_palm = Text("PaLM (540 tỷ tham số)\nChi phí: ~20 triệu USD", font_size=14, color=PAPER_RED).next_to(stats_gpt, DOWN, buff=0.3, aligned_edge=LEFT)
        
        self.play(Write(stats_gpt), Write(stats_palm), run_time=2.0) # Reach 26.5s
        
        # Dynamic pulse & indicate resources barrier
        self.play(Indicate(stats_gpt, color=PAPER_RED), Indicate(stats_palm, color=PAPER_RED), run_time=2.0) # Reach 28.5s
        self.play(Indicate(barrier, color=PAPER_RED), run_time=1.5) # Reach 30.0s
        self.wait(7.0) # Reach 39.0s

        # 39.0s: Step 5: Models as Natural Phenomena
        self.play(
            FadeOut(academia_bound), FadeOut(academia_desc), FadeOut(compute_stream),
            FadeOut(industry_label), FadeOut(academia_label), FadeOut(barrier),
            FadeOut(stats_gpt), FadeOut(stats_palm),
            run_time=1.0
        ) # Reach 37.0s

        # Morph large net into complex particle cloud
        np.random.seed(1337)
        particle_cloud = VGroup(*[
            Dot(
                point=[np.random.normal(2.5, 0.8), np.random.normal(-0.5, 0.8), 0],
                radius=np.random.uniform(0.04, 0.1),
                color=interpolate_color(ManimColor(PAPER_ORANGE), ManimColor(PAPER_YELLOW), np.random.rand())
            ) for _ in range(50)
        ])
        label_natural = Text("Mô hình như hiện tượng tự nhiên", font_size=15, color=HIGHLIGHT).next_to(particle_cloud, UP, buff=0.3)

        self.play(
            ReplacementTransform(net_large, particle_cloud),
            ReplacementTransform(label_scaling, label_natural),
            run_time=2.0
        ) # Reach 39.0s

        # Micro-animate particle cloud to keep it dynamic until 56.5s (14.5s)
        for _ in range(6):
            self.play(
                *[p.animate.shift(np.random.normal(0, 0.08, 3)) for p in particle_cloud],
                run_time=2.4
            ) # 14.4s total -> Reach 56.4s
        self.wait(0.1) # Reach 56.5s

        # 56.5s: Step 6: Empirical Lens
        lens = Circle(radius=1.8, color=PAPER_BLUE, stroke_width=2.5).shift(LEFT * 3 + DOWN * 0.5)
        lens_lbl = Text("Ống kính Thực nghiệm", font_size=15, color=PAPER_BLUE).next_to(lens, UP, buff=0.2)

        light_cone_t = Line(particle_cloud.get_center() + UP * 0.5, lens.get_top(), stroke_color=PAPER_BLUE, stroke_width=1.0, stroke_opacity=0.35)
        light_cone_b = Line(particle_cloud.get_center() + DOWN * 0.5, lens.get_bottom(), stroke_color=PAPER_BLUE, stroke_width=1.0, stroke_opacity=0.35)

        z_dot_1 = Dot(lens.get_center() + LEFT * 0.6 + UP * 0.4, radius=0.18, color=PAPER_YELLOW)
        z_dot_2 = Dot(lens.get_center() + RIGHT * 0.6 + DOWN * 0.4, radius=0.18, color=PAPER_YELLOW)
        z_arrow = DoubleArrow(z_dot_1.get_center(), z_dot_2.get_center(), color=GOOD, stroke_width=2.5, buff=0.12)
        z_label = Text("Đo đạc & Quan sát", font_size=14, color=TEXT_COLOR).next_to(z_arrow, UP, buff=0.08)
        zoomed_items = VGroup(z_dot_1, z_dot_2, z_arrow, z_label)

        self.play(
            Create(lens), Write(lens_lbl),
            Create(light_cone_t), Create(light_cone_b),
            FadeIn(zoomed_items, scale=0.5),
            run_time=2.0
        ) # Reach 52.0s
        self.wait(1.5) # Reach 53.5s

        # Hyperparameter Sliders inside lens
        slider_lr = VGroup(
            Line(LEFT*0.8, RIGHT*0.8, stroke_width=2, color=DIM_TEXT),
            Dot(LEFT*0.3, color=PAPER_BLUE)
        ).shift(lens.get_center() + UP * 0.4)
        lbl_lr = Text("Learning Rate (\u03b7)", font_size=14, color=PAPER_BLUE).next_to(slider_lr, UP, buff=0.08)
        
        slider_batch = VGroup(
            Line(LEFT*0.8, RIGHT*0.8, stroke_width=2, color=DIM_TEXT),
            Dot(RIGHT*0.4, color=PAPER_GREEN)
        ).shift(lens.get_center() + DOWN * 0.5)
        lbl_batch = Text("Batch Size", font_size=14, color=PAPER_GREEN).next_to(slider_batch, UP, buff=0.08)
        
        sliders = VGroup(
            VGroup(slider_lr, lbl_lr),
            VGroup(slider_batch, lbl_batch)
        )

        self.play(FadeOut(zoomed_items), FadeIn(sliders, shift=UP*0.2), run_time=1.0) # Reach 54.5s
        self.play(
            slider_lr[1].animate.shift(RIGHT * 0.5),
            slider_batch[1].animate.shift(LEFT * 0.6),
            run_time=2.5
        ) # Reach 57.0s

        # Jiggle sliders to keep it active until 68.0s
        self.play(slider_lr[1].animate.shift(LEFT * 0.3), slider_batch[1].animate.shift(RIGHT * 0.4), run_time=2.0) # Reach 59.0s
        self.play(slider_lr[1].animate.shift(RIGHT * 0.2), slider_batch[1].animate.shift(LEFT * 0.2), run_time=2.0) # Reach 61.0s
        self.play(Indicate(lens_lbl, color=PAPER_BLUE), run_time=1.5) # Reach 69.0s
        self.wait(3.0) # Reach 72.0s

        # 72.0s: Step 7: Empirical Paradigm keywords
        self.play(
            FadeOut(sliders),
            FadeOut(lens), FadeOut(lens_lbl),
            FadeOut(light_cone_t), FadeOut(light_cone_b),
            FadeOut(particle_cloud), FadeOut(label_natural),
            run_time=0.8
        ) # Reach 68.8s

        kw1 = Text("Quan sát & Đo đạc", font_size=24, color=PAPER_BLUE).shift(LEFT * 4.0)
        arrow1 = Arrow(LEFT * 2.2, LEFT * 1.2, color=DIM_TEXT, stroke_width=2)
        kw2 = Text("Phát hiện Quy luật", font_size=24, color=PAPER_YELLOW)
        arrow2 = Arrow(RIGHT * 1.2, RIGHT * 2.2, color=DIM_TEXT, stroke_width=2)
        kw3 = Text("Thử thách Lý thuyết", font_size=24, color=HIGHLIGHT).shift(RIGHT * 4.0)
        
        self.play(Write(kw1), run_time=1.2) # Reach 70.0s
        self.play(Create(arrow1), run_time=0.5) # Reach 70.5s
        self.play(Write(kw2), run_time=1.2) # Reach 71.7s
        self.play(Create(arrow2), run_time=0.5) # Reach 72.2s
        self.play(Write(kw3), run_time=1.2) # Reach 73.4s

        # Pulsate keywords to keep screen active until 84.5s
        self.play(Indicate(kw1, color=PAPER_BLUE), run_time=2.0) # Reach 75.4s
        self.play(Indicate(kw2, color=PAPER_YELLOW), run_time=2.0) # Reach 77.4s
        self.play(Indicate(kw3, color=HIGHLIGHT), run_time=2.0) # Reach 83.4s
        self.wait(1.1) # Reach 84.5s

        # 84.5s: Step 8: Preview 3 findings
        self.play(
            FadeOut(kw1), FadeOut(arrow1), FadeOut(kw2), FadeOut(arrow2), FadeOut(kw3),
            run_time=1.5
        ) # Reach 86.0s

        findings_title = Text("3 Phát hiện thực nghiệm nổi bật", font_size=20, color=TITLE_COLOR).shift(UP * 1.8)
        self.play(Write(findings_title), run_time=1.2) # Reach 87.2s

        f1 = Text("1. Edge of Stability (Bờ vực ổn định)", font_size=15, color=PAPER_ORANGE).shift(UP * 0.6)
        f2 = Text("2. Disagreement \u2248 Error (Bất đồng \u2248 Sai số)", font_size=15, color=PAPER_GREEN).shift(UP * 0.0)
        f3 = Text("3. Agreement on the Line (Đồng thuận trên đường thẳng)", font_size=15, color=PAPER_BLUE).shift(DOWN * 0.6)

        self.play(Write(f1), Write(f2), Write(f3), run_time=2.0) # Reach 89.2s

        # Pulsate list items until 100.0s
        self.play(Indicate(f1, color=PAPER_ORANGE), run_time=2.0) # Reach 91.2s
        self.play(Indicate(f2, color=PAPER_GREEN), run_time=2.0) # Reach 93.2s
        self.play(Indicate(f3, color=PAPER_BLUE), run_time=2.0) # Reach 95.2s
        self.wait(4.8) # Reach 100.0s

        # Clean up Scene 1
        self.play(
            FadeOut(findings_title), FadeOut(f1), FadeOut(f2), FadeOut(f3),
            run_time=1.0
        ) # Reach 101.0s

    # ═══════════════════════════════════════════════════════════════════
    # SCENE 2 — Edge of Stability (≈2m)
    # ═══════════════════════════════════════════════════════════════════
    def scene2_edge_of_stability(self):
        # 101.0s: Intro EoS
        title = Text(
            "Hiện tượng 1: Edge of Stability",
            font_size=32,
            color=TITLE_COLOR,
        ).to_edge(UP, buff=0.4)
        self.play(Write(title), run_time=1.2) # Reach 102.2s

        # Loss surface plot
        valley_axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-2, 3, 1],
            x_length=4.5,
            y_length=3.2,
            tips=False,
            axis_config={"color": DIM_TEXT, "stroke_width": 1.0},
        ).shift(LEFT * 3.5 + DOWN * 0.5)

        valley_curve = valley_axes.plot(lambda x: 0.4 * x**2 - 1.2, x_range=[-2.7, 2.7], color=PAPER_BLUE)
        valley_lbl = Text("Loss Surface", font_size=14, color=PAPER_BLUE).next_to(valley_axes, UP, buff=0.1)

        self.play(Create(valley_axes), Create(valley_curve), FadeIn(valley_lbl), run_time=1.5) # Reach 103.7s

        # Case 1: Learning rate nhỏ -> Hội tụ
        ball = Dot(valley_axes.c2p(-2.5, 0.4*(-2.5)**2 - 1.2), color=PAPER_GREEN, radius=0.12)
        case1_lbl = Text("Learning Rate nhỏ: Hội tụ mượt mà", font_size=14, color=PAPER_GREEN).next_to(valley_axes, DOWN, buff=0.1)
        self.play(FadeIn(ball), FadeIn(case1_lbl), run_time=0.8) # Reach 104.5s

        steps_1 = [-2.5, 1.25, -0.62, 0.31, -0.15, 0.0]
        for x_val in steps_1:
            y_val = 0.4 * x_val**2 - 1.2
            self.play(ball.animate.move_to(valley_axes.c2p(x_val, y_val)), run_time=0.25) # 1.5s total -> Reach 106.0s

        # Case 2: Learning rate lớn -> Phân kỳ
        self.play(FadeOut(case1_lbl), run_time=0.5) # Reach 106.5s
        case2_lbl = Text("Learning Rate lớn: Phân kỳ", font_size=14, color=PAPER_RED).next_to(valley_axes, DOWN, buff=0.1)
        self.play(
            FadeIn(case2_lbl), 
            ball.animate.move_to(valley_axes.c2p(-0.7, 0.4*(-0.7)**2 - 1.2)), 
            run_time=0.8
        ) # Reach 107.3s

        steps_2 = [-0.7, 1.8, -2.9]
        for x_val in steps_2:
            y_val = 0.4 * x_val**2 - 1.2
            self.play(ball.animate.move_to(valley_axes.c2p(x_val, y_val)), run_time=0.4) # 1.2s total -> Reach 108.5s
        
        self.play(ball.animate.move_to(valley_axes.c2p(-4.0, 5.0)), run_time=0.8) # Reach 109.3s

        theory_formula = MathTex(
            r"\text{Sharpness } (\lambda_{\max}) < \frac{2}{\eta}",
            color=PAPER_RED, font_size=24
        ).next_to(valley_axes, UP, buff=0.4).shift(RIGHT * 3.5)
        
        self.play(Write(theory_formula), run_time=1.2) # Reach 110.5s

        # Keep formula visible and active until 125s
        self.play(Indicate(theory_formula, color=PAPER_RED), run_time=2.0) # Reach 112.5s
        self.play(Circumscribe(theory_formula, color=PAPER_RED), run_time=2.0) # Reach 114.5s
        self.wait(10.5) # Reach 125.0s

        # 125.0s: Empirical graphs transition
        self.play(
            FadeOut(valley_axes), FadeOut(valley_curve), FadeOut(valley_lbl),
            FadeOut(ball), FadeOut(case2_lbl), FadeOut(theory_formula),
            run_time=1.5
        ) # Reach 126.5s

        loss_axes = Axes(
            x_range=[0, 8000, 2000],
            y_range=[0, 0.6, 0.2],
            x_length=7.5,
            y_length=2.0,
            tips=False,
            axis_config={"color": DIM_TEXT, "stroke_width": 1.5},
        ).shift(UP * 0.8 + LEFT * 0.5)

        sharp_axes = Axes(
            x_range=[0, 8000, 2000],
            y_range=[0, 300, 100],
            x_length=7.5,
            y_length=2.0,
            tips=False,
            axis_config={"color": DIM_TEXT, "stroke_width": 1.5},
        ).shift(DOWN * 1.8 + LEFT * 0.5)

        loss_lbl = Text("Loss", font_size=14, color=PAPER_GREEN).next_to(loss_axes.y_axis, UP, buff=0.15)
        sharp_lbl = Text("Sharpness", font_size=14, color=PAPER_ORANGE).next_to(sharp_axes.y_axis, UP, buff=0.15)
        iter_lbl = Text("Iteration", font_size=14, color=DIM_TEXT).next_to(sharp_axes.x_axis, RIGHT, buff=0.2)

        boundary_line = DashedLine(
            sharp_axes.c2p(0, 200), sharp_axes.c2p(8000, 200),
            color=PAPER_RED, stroke_width=2
        )
        boundary_lbl = Text("Ngưỡng ổn định 2/\u03b7", font_size=14, color=PAPER_RED).next_to(boundary_line, UP, buff=0.08)

        self.play(
            Create(loss_axes), Create(sharp_axes),
            Write(loss_lbl), Write(sharp_lbl), Write(iter_lbl),
            Create(boundary_line), Write(boundary_lbl),
            run_time=2.0
        ) # Reach 128.5s

        # Trial box simulation to represent 1000s of iterations
        trial_box = RoundedRectangle(width=2.5, height=1.0, corner_radius=0.1, fill_color=CARD_BG, stroke_color=PAPER_ORANGE, stroke_width=1.5).shift(RIGHT * 4.5 + UP * 1.5)
        trial_text = Text("Đo đạc Thực nghiệm\n(Sharpness & Loss)", font_size=14, color=PAPER_ORANGE).move_to(trial_box.get_center())
        
        self.play(Create(trial_box), Write(trial_text), run_time=1.5) # Reach 130.0s
        self.play(Indicate(trial_box, color=PAPER_ORANGE), run_time=1.5) # Reach 131.5s
        self.play(FadeOut(trial_box), FadeOut(trial_text), run_time=1.5) # Reach 133.0s
        self.wait(3.6) # Reach 136.6s

        # 136.6s: Plotting Phase 1 (0 to 4000)
        def sharpness_curve(x):
            if x < 4000:
                return 70 + 130 * (x / 4000) ** 1.8
            else:
                return 200 + 4.0 * np.sin(0.04 * (x - 4000)) + 3.0 * np.cos(0.07 * (x - 4000))

        def loss_curve(x):
            if x < 4000:
                return 0.5 * np.exp(-x / 4500)
            else:
                base = 0.5 * np.exp(-4000 / 4500) * np.exp(-(x - 4000) / 10000)
                return base + 0.02 * np.sin(0.15 * (x - 4000))

        sharp_path_1 = sharp_axes.plot(sharpness_curve, x_range=[0, 4000], color=PAPER_ORANGE)
        loss_path_1 = loss_axes.plot(loss_curve, x_range=[0, 4000], color=PAPER_GREEN)

        self.play(Create(sharp_path_1), Create(loss_path_1), run_time=6.0, rate_func=linear) # Reach 142.6s

        # Faint runs representing alternative training paths
        faint_runs = VGroup()
        for s in [1.02, 0.98, 1.05, 0.95]:
            faint_run_sharp = sharp_axes.plot(lambda x, s=s: sharpness_curve(x) * s, x_range=[0, 4000], color=PAPER_ORANGE).set_opacity(0.15)
            faint_run_loss = loss_axes.plot(lambda x, s=s: loss_curve(x) * s, x_range=[0, 4000], color=PAPER_GREEN).set_opacity(0.15)
            faint_runs.add(faint_run_sharp, faint_run_loss)

        self.play(Create(faint_runs), run_time=2.5) # Reach 145.1s
        self.play(FadeOut(faint_runs), run_time=1.5) # Reach 146.6s
        
        # Highlight target intersection dot
        intersection_dot = Dot(sharp_axes.c2p(4000, 200), color=PAPER_RED, radius=0.15)
        self.play(Create(intersection_dot), run_time=1.0) # Reach 147.6s
        self.play(Flash(intersection_dot, color=PAPER_RED, flash_radius=0.5), run_time=1.5) # Reach 149.1s
        self.wait(7.4) # Reach 156.5s

        # 156.5s: Point of instability/critical threshold
        self.remove(intersection_dot)
        warning_text = Text("Lý thuyết: Phân kỳ!", font_size=14, color=PAPER_RED).shift(RIGHT * 4.5 + UP * 0.8)
        stabilization_text = Text("Thực tế: Tự ổn định", font_size=14, color=GOOD).shift(RIGHT * 4.5 + UP * 0.8)

        self.play(Write(warning_text), run_time=1.5) # Reach 155.0s
        self.play(ReplacementTransform(warning_text, stabilization_text), run_time=1.5) # Reach 156.5s
        
        self.play(Indicate(stabilization_text, color=GOOD), run_time=2.0) # Reach 158.5s
        self.play(Circumscribe(stabilization_text, color=GOOD), run_time=2.0) # Reach 160.5s
        self.wait(5.9) # Reach 169.4s

        # 169.4s: Curve Phase 2 (4000 to 8000)
        sharp_path_2 = sharp_axes.plot(sharpness_curve, x_range=[4000, 8000], color=PAPER_ORANGE)
        loss_path_2 = loss_axes.plot(loss_curve, x_range=[4000, 8000], color=PAPER_GREEN)

        self.play(Create(sharp_path_2), Create(loss_path_2), run_time=8.0, rate_func=linear) # Reach 177.4s
        
        # Oscillation highlight
        highlight_circle = Circle(radius=0.5, color=PAPER_RED, stroke_width=2.0).move_to(sharp_axes.c2p(6000, 200))
        stabilization_label = Text("Edge of Stability", font_size=14, color=HIGHLIGHT).next_to(highlight_circle, UP, buff=0.15)
        
        self.play(Create(highlight_circle), Write(stabilization_label), run_time=2.0) # Reach 179.4s

        # Continuous noise oscillation to avoid static screen until 210.0s
        # Total remaining wait: 30.6s
        # 15 iterations of 2s oscillation = 30.0s
        for _ in range(15):
            self.play(
                sharp_path_2.animate.shift(UP * 0.05),
                loss_path_2.animate.shift(DOWN * 0.02),
                run_time=1.0,
                rate_func=there_and_back
            )
            self.play(
                sharp_path_2.animate.shift(DOWN * 0.03),
                loss_path_2.animate.shift(UP * 0.01),
                run_time=1.0,
                rate_func=there_and_back
            ) # 30.0s total -> Reach 209.4s
            
        self.wait(0.6) # Reach 210.0s
        self.remove(highlight_circle, stabilization_label)

        # Cleanup Scene 2
        self.play(
            FadeOut(loss_axes), FadeOut(sharp_axes), FadeOut(loss_lbl), FadeOut(sharp_lbl),
            FadeOut(iter_lbl), FadeOut(boundary_line), FadeOut(boundary_lbl),
            FadeOut(sharp_path_1), FadeOut(loss_path_1), FadeOut(sharp_path_2), FadeOut(loss_path_2),
            FadeOut(stabilization_text), FadeOut(title),
            run_time=1.0
        ) # Reach 211.0s (close enough to 210.0s)

    # ═══════════════════════════════════════════════════════════════════
    # SCENE 3 — Disagreement ≈ Error (≈2m)
    # ═══════════════════════════════════════════════════════════════════
    def scene3_disagreement_error(self):
        # 210s - 225.2s: Disagreement ≈ Error transition
        title = Text(
            "Hiện tượng 2: Disagreement \u2248 Error",
            font_size=32,
            color=TITLE_COLOR,
        ).to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=1.5) # Reach 212.5s
        
        self.play(Indicate(title, color=HIGHLIGHT), run_time=2.0) # Reach 214.5s
        self.play(Circumscribe(title, color=HIGHLIGHT), run_time=2.0) # Reach 216.5s
        self.wait(8.7) # Reach 225.2s

        # 225.2s: Setup grids and network A
        grid_lbl = Text("Mẫu kiểm thử (Test Samples)", font_size=14, color=TEXT_COLOR).shift(UP * 2.2)
        self.play(Write(grid_lbl), run_time=1.0) # Reach 226.2s

        blocks = VGroup(*[
            Square(side_length=0.45, fill_color=CARD_BG, fill_opacity=0.9, stroke_color=CARD_STROKE, stroke_width=1.5)
            for _ in range(10)
        ]).arrange(RIGHT, buff=0.2).shift(UP * 1.3)
        self.play(Create(blocks), run_time=1.0) # Reach 227.2s

        # Draw network A
        def draw_simple_net(color, center_pos):
            nodes = VGroup()
            edges = VGroup()
            layer_sizes = [3, 4, 2]
            layers = []
            for i, sz in enumerate(layer_sizes):
                layer = VGroup()
                for j in range(sz):
                    node = Circle(radius=0.08, fill_color=color, fill_opacity=0.8, stroke_color=WHITE, stroke_width=0.6)
                    node.move_to(center_pos + RIGHT * i * 0.7 + UP * (j - (sz - 1)/2) * 0.4)
                    layer.add(node)
                layers.append(layer)
                nodes.add(layer)
            
            for i in range(len(layer_sizes) - 1):
                for n1 in layers[i]:
                    for n2 in layers[i+1]:
                        edge = Line(n1.get_center(), n2.get_center(), stroke_color=DIM_TEXT, stroke_width=0.4, stroke_opacity=0.4)
                        edges.add(edge)
            return VGroup(edges, nodes)

        net_1 = draw_simple_net(PAPER_BLUE, LEFT * 4.8 + UP * 0.8)
        net1_label = Text("Mạng A (Khởi tạo 1)", font_size=14, color=PAPER_BLUE).next_to(net_1, UP, buff=0.1)

        self.play(Create(net_1), Write(net1_label), run_time=1.5) # Reach 228.7s

        # Pred dots A
        a_dots = VGroup()
        for idx in range(10):
            color = PAPER_RED if idx in [2, 6] else PAPER_GREEN
            dot = Dot(radius=0.12, color=color).move_to(blocks[idx].get_center() + DOWN * 0.4)
            a_dots.add(dot)

        pred_a_lbl = Text("Mạng A:", font_size=14, color=PAPER_BLUE).next_to(blocks, RIGHT, buff=0.5).shift(DOWN * 0.4)
        self.play(Write(pred_a_lbl), FadeIn(a_dots, shift=UP * 0.1), run_time=1.5) # Reach 230.2s

        # Micro animate network prediction to avoid static scene
        self.play(Circumscribe(net_1, color=PAPER_BLUE), run_time=2.0) # Reach 232.2s
        self.play(*[Indicate(dot) for dot in a_dots], run_time=2.0) # Reach 234.2s
        self.wait(10.8) # Reach 245.0s

        # 245.0s: Draw Network B
        net_2 = draw_simple_net(PAPER_GREEN, LEFT * 4.8 + DOWN * 1.5)
        net2_label = Text("Mạng B (Khởi tạo 2)", font_size=14, color=PAPER_GREEN).next_to(net_2, UP, buff=0.1)

        self.play(Create(net_2), Write(net2_label), run_time=1.5) # Reach 246.5s

        # Pred dots B
        b_dots = VGroup()
        for idx in range(10):
            color = PAPER_RED if idx in [2, 8] else PAPER_GREEN
            dot = Dot(radius=0.12, color=color).move_to(blocks[idx].get_center() + DOWN * 0.9)
            b_dots.add(dot)

        pred_b_lbl = Text("Mạng B:", font_size=14, color=PAPER_GREEN).next_to(blocks, RIGHT, buff=0.5).shift(DOWN * 0.9)
        self.play(Write(pred_b_lbl), FadeIn(b_dots, shift=UP * 0.1), run_time=1.5) # Reach 248.0s

        # Highlight disagreement
        dis_rects = VGroup(
            RoundedRectangle(width=0.6, height=1.6, corner_radius=0.05, stroke_color=PAPER_YELLOW, stroke_width=2).move_to(blocks[6].get_center() + DOWN * 0.45),
            RoundedRectangle(width=0.6, height=1.6, corner_radius=0.05, stroke_color=PAPER_YELLOW, stroke_width=2).move_to(blocks[8].get_center() + DOWN * 0.45)
        )
        self.play(Create(dis_rects), run_time=1.5) # Reach 249.5s
        self.play(Indicate(dis_rects[0], color=PAPER_YELLOW), Indicate(dis_rects[1], color=PAPER_YELLOW), run_time=1.5) # Reach 251.0s
        self.wait(4.4) # Reach 255.4s

        # 255.4s: Quantitative comparison & scatter plot transition
        dis_lbl = Text("Bất đồng = 2/10 = 20%", font_size=14, color=PAPER_YELLOW).next_to(blocks, DOWN, buff=1.2).shift(LEFT * 0.5)
        err_lbl = Text("Lỗi TB = 2/10 = 20%", font_size=14, color=HIGHLIGHT).next_to(dis_lbl, DOWN, buff=0.15, aligned_edge=LEFT)
        
        self.play(Write(dis_lbl), Write(err_lbl), run_time=1.5) # Reach 256.9s

        # Transition to scatter plot
        self.play(
            FadeOut(grid_lbl), FadeOut(blocks), FadeOut(a_dots), FadeOut(b_dots),
            FadeOut(pred_a_lbl), FadeOut(pred_b_lbl), FadeOut(dis_rects),
            FadeOut(net_1), FadeOut(net_2), FadeOut(net1_label), FadeOut(net2_label),
            FadeOut(dis_lbl), FadeOut(err_lbl),
            run_time=2.5
        ) # Reach 259.4s

        scatter_axes = Axes(
            x_range=[0, 0.4, 0.1],
            y_range=[0, 0.4, 0.1],
            x_length=4.5,
            y_length=4.0,
            tips=False,
            axis_config={"color": DIM_TEXT, "stroke_width": 1.2},
        ).shift(RIGHT * 3 + DOWN * 0.5)

        scatter_x_lbl = Text("Error (Lỗi)", font_size=14, color=DIM_TEXT).next_to(scatter_axes.x_axis, RIGHT, buff=0.1)
        scatter_y_lbl = Text("Disagreement (Bất đồng)", font_size=14, color=DIM_TEXT).next_to(scatter_axes.y_axis, UP, buff=0.1)
        diagonal = Line(scatter_axes.c2p(0, 0), scatter_axes.c2p(0.4, 0.4), color=PAPER_RED, stroke_width=1.5)
        diag_lbl = Text("y = x", font_size=14, color=PAPER_RED).next_to(diagonal.get_end(), UL, buff=0.08)

        self.play(
            Create(scatter_axes), Write(scatter_x_lbl), Write(scatter_y_lbl),
            Create(diagonal), Write(diag_lbl),
            run_time=1.5
        ) # Reach 260.9s

        # Populate scatter points along diagonal
        np.random.seed(137)
        points = VGroup()
        for _ in range(25):
            err = np.random.uniform(0.05, 0.35)
            dis = err + np.random.normal(0, 0.012)
            pt = Dot(scatter_axes.c2p(err, dis), radius=0.06, color=PAPER_YELLOW, fill_opacity=0.8)
            points.add(pt)

        # Plot first 10 points
        self.play(Create(points[:10]), run_time=2.0) # Reach 262.9s
        self.play(Indicate(diagonal, color=PAPER_RED), run_time=2.0) # Reach 264.9s
        self.wait(8.6) # Reach 273.5s

        # 273.5s: Architecture generalizability
        self.play(Create(points[10:]), run_time=2.0) # Reach 275.5s
        
        cifar_lbl = Text("CNN (CIFAR-10)", font_size=14, color=PAPER_YELLOW).move_to(scatter_axes.c2p(0.1, 0.1) + UP * 0.4)
        imagenet_lbl = Text("ViT (ImageNet)", font_size=14, color=PAPER_YELLOW).move_to(scatter_axes.c2p(0.3, 0.3) + UP * 0.4)
        arch_labels = VGroup(cifar_lbl, imagenet_lbl)
        self.play(Write(arch_labels), run_time=2.0) # Reach 277.5s
        
        self.play(FadeOut(arch_labels), run_time=1.5) # Reach 279.0s
        self.play(Indicate(diagonal, color=PAPER_YELLOW), run_time=1.5) # Reach 280.5s
        self.wait(3.9) # Reach 284.4s

        # 284.4s: The Paradox
        dis_err_kw = Text("Bất đồng \u2248 Lỗi", font_size=18, color=HIGHLIGHT).shift(LEFT * 3 + UP * 0.5)
        self.play(Write(dis_err_kw), run_time=1.5) # Reach 285.9s

        # Keep screen active until 305.6s
        self.play(Indicate(dis_err_kw, color=HIGHLIGHT), run_time=2.0) # Reach 287.9s
        self.play(*[p.animate.scale(1.2) for p in points[::2]], run_time=1.5) # Reach 289.4s
        self.play(*[p.animate.scale(1/1.2) for p in points[::2]], run_time=1.5) # Reach 290.9s
        self.wait(14.7) # Reach 305.6s

        # 305.6s: Calibration expectation
        formula = MathTex(
            r"\mathbb{E}[\text{Error}] \approx \mathbb{E}[\text{Disagreement}]",
            color=HIGHLIGHT, font_size=28
        ).shift(LEFT * 3 + DOWN * 0.8)

        self.play(Write(formula), run_time=1.5) # Reach 307.1s

        # Pulsate formula to avoid static screen until 325.0s
        self.play(Indicate(formula, color=HIGHLIGHT), run_time=2.0) # Reach 309.1s
        self.play(Circumscribe(formula, color=HIGHLIGHT), run_time=2.0) # Reach 311.1s
        self.wait(13.9) # Reach 325.0s

        # Cleanup Scene 3
        self.play(
            FadeOut(scatter_axes), FadeOut(scatter_x_lbl), FadeOut(scatter_y_lbl),
            FadeOut(diagonal), FadeOut(diag_lbl), FadeOut(points),
            FadeOut(dis_err_kw), FadeOut(formula), FadeOut(title),
            run_time=1.0
        ) # Reach 326.0s

    # ═══════════════════════════════════════════════════════════════════
    # SCENE 4 — Agreement on the Line (≈2m)
    # ═══════════════════════════════════════════════════════════════════
    def scene4_agreement_on_the_line(self):
        # 325.0s: Transition to OOD
        title = Text(
            "Hiện tượng 3: Agreement on the Line",
            font_size=32,
            color=TITLE_COLOR,
        ).to_edge(UP, buff=0.4)
        self.play(Write(title), run_time=1.5) # Reach 326.5s

        # ID vs OOD boxes
        id_box = RoundedRectangle(width=2.5, height=1.2, corner_radius=0.1, stroke_color=PAPER_GREEN, fill_color=CARD_BG, fill_opacity=0.8).shift(LEFT * 3.5 + UP * 0.5)
        id_text = Text("Trong phân phối\n(ID - Sunny Road)", font_size=16, color=PAPER_GREEN).move_to(id_box.get_center())
        
        ood_box = RoundedRectangle(width=2.5, height=1.2, corner_radius=0.1, stroke_color=PAPER_BLUE, fill_color=CARD_BG, fill_opacity=0.8).shift(RIGHT * 3.5 + UP * 0.5)
        ood_text = Text("Ngoài phân phối\n(OOD - Snowy Road)", font_size=16, color=PAPER_BLUE).move_to(ood_box.get_center())

        self.play(
            Create(id_box), Write(id_text),
            Create(ood_box), Write(ood_text),
            run_time=2.0
        ) # Reach 328.5s
        self.play(Indicate(id_box, color=PAPER_GREEN), Indicate(ood_box, color=PAPER_BLUE), run_time=2.0) # Reach 330.5s
        q_arrow = Arrow(id_box.get_right(), ood_box.get_left(), color=PAPER_YELLOW, stroke_width=2)
        self.play(GrowArrow(q_arrow), run_time=1.5) # Reach 332.0s
        self.play(Indicate(id_box, color=PAPER_GREEN), Indicate(ood_box, color=PAPER_BLUE), run_time=2.0) # Reach 334.0s
        self.play(FadeOut(q_arrow), run_time=1.0) # Reach 335.0s
        self.wait(10.1) # Reach 345.1s

        # 345.1s: Drive car simulation representing OOD
        self.play(FadeOut(id_box), FadeOut(id_text), FadeOut(ood_box), FadeOut(ood_text), run_time=1.0) # Reach 346.1s

        car_body = RoundedRectangle(width=1.4, height=0.7, corner_radius=0.1, fill_color=PAPER_BLUE, fill_opacity=0.9, stroke_color=WHITE, stroke_width=1.5)
        wheel_l = Circle(radius=0.18, fill_color=BG, fill_opacity=1, stroke_color=WHITE, stroke_width=1.5).move_to(car_body.get_bottom() + LEFT * 0.35)
        wheel_r = Circle(radius=0.18, fill_color=BG, fill_opacity=1, stroke_color=WHITE, stroke_width=1.5).move_to(car_body.get_bottom() + RIGHT * 0.35)
        car = VGroup(car_body, wheel_l, wheel_r).shift(LEFT * 4.5 + UP * 1.5)

        road_id = Line(LEFT * 6.5 + UP * 0.9, LEFT * 1.5 + UP * 0.9, color=DIM_TEXT)
        label_id = Text("ID: Đường nắng", font_size=14, color=PAPER_GREEN).next_to(road_id, DOWN, buff=0.1)

        road_ood = DashedLine(LEFT * 1.5 + UP * 0.9, RIGHT * 4.0 + UP * 0.9, color=WHITE, stroke_width=2)
        label_ood = Text("OOD: Đường tuyết", font_size=14, color=PAPER_BLUE).next_to(road_ood, DOWN, buff=0.1)

        self.play(
            Create(road_id), Create(road_ood),
            Write(label_id), Write(label_ood),
            FadeIn(car),
            run_time=2.0
        ) # Reach 348.1s

        self.play(car.animate.shift(RIGHT * 6.5), run_time=5.0) # Reach 353.1s
        self.play(FadeOut(car), FadeOut(road_id), FadeOut(road_ood), FadeOut(label_id), FadeOut(label_ood), run_time=1.5) # Reach 354.6s
        self.wait(2.9) # Reach 357.5s

        # 357.5s: Plot Left - Accuracy on the Line
        axes_l = Axes(
            x_range=[0.4, 1.0, 0.2],
            y_range=[0.4, 1.0, 0.2],
            x_length=4.0,
            y_length=3.0,
            tips=False,
            axis_config={"color": DIM_TEXT, "stroke_width": 1.2},
        ).shift(LEFT * 3.2 + DOWN * 0.8)

        lbl_xl = Text("ID Accuracy", font_size=14, color=DIM_TEXT).next_to(axes_l.x_axis, DOWN, buff=0.15)
        lbl_yl = Text("OOD Accuracy", font_size=14, color=DIM_TEXT).next_to(axes_l.y_axis, UP, buff=0.15)
        diag_l = DashedLine(axes_l.c2p(0.4, 0.4), axes_l.c2p(1.0, 1.0), color=DIM_TEXT, stroke_width=1.0)
        fit_line_l = Line(axes_l.c2p(0.45, 0.4), axes_l.c2p(0.95, 0.9), color=PAPER_BLUE, stroke_width=2)
        fit_lbl_l = Text("Accuracy on the Line", font_size=14, color=PAPER_BLUE).next_to(fit_line_l, UP, buff=0.1).rotate(0.3)

        np.random.seed(42)
        dots_l = VGroup()
        for _ in range(20):
            id_acc = np.random.uniform(0.5, 0.95)
            ood_acc = 1.25 * id_acc - 0.32 + np.random.normal(0, 0.02)
            ood_acc = max(min(ood_acc, 0.98), 0.4)
            pt = Dot(axes_l.c2p(id_acc, ood_acc), radius=0.05, color=PAPER_BLUE, fill_opacity=0.7)
            dots_l.add(pt)

        self.play(
            Create(axes_l), Write(lbl_xl), Write(lbl_yl), Create(diag_l),
            Create(fit_line_l), Write(fit_lbl_l), Create(dots_l),
            run_time=2.0
        ) # Reach 359.5s

        # Show model labels ResNet / ViT
        lbl_resnet = Text("ResNet", font_size=14, color=PAPER_BLUE).move_to(axes_l.c2p(0.6, 0.43) + DOWN * 0.25)
        lbl_vit = Text("ViT", font_size=14, color=PAPER_BLUE).move_to(axes_l.c2p(0.8, 0.68) + DOWN * 0.25)
        self.play(Write(lbl_resnet), Write(lbl_vit), run_time=1.5) # Reach 361.0s
        self.play(Indicate(lbl_resnet), Indicate(lbl_vit), run_time=2.0) # Reach 363.0s
        self.play(FadeOut(lbl_resnet), FadeOut(lbl_vit), run_time=1.5) # Reach 364.5s
        self.play(Indicate(fit_line_l, color=PAPER_BLUE), run_time=2.0) # Reach 366.5s
        self.play(*[p.animate.scale(1.1) for p in dots_l], run_time=2.0) # Reach 368.5s
        self.play(*[p.animate.scale(1/1.1) for p in dots_l], run_time=2.0) # Reach 370.5s
        self.wait(6.1) # Reach 376.6s

        # 376.6s: Explain axes & Line
        self.play(Indicate(fit_line_l), run_time=2.0) # Reach 378.6s
        self.play(*[p.animate.scale(1.2) for p in dots_l], run_time=2.0) # Reach 380.6s
        self.play(*[p.animate.scale(1/1.2) for p in dots_l], run_time=2.0) # Reach 382.6s
        self.play(Indicate(fit_line_l, color=PAPER_BLUE), run_time=2.0) # Reach 384.6s
        self.play(Indicate(diag_l, color=DIM_TEXT), run_time=2.0) # Reach 386.6s
        self.wait(6.4) # Reach 393.0s

        # 393.0s: Plot Right - Agreement on the Line
        axes_r = Axes(
            x_range=[0.4, 1.0, 0.2],
            y_range=[0.4, 1.0, 0.2],
            x_length=4.0,
            y_length=3.0,
            tips=False,
            axis_config={"color": DIM_TEXT, "stroke_width": 1.2},
        ).shift(RIGHT * 3.2 + DOWN * 0.8)

        lbl_xr = Text("ID Agreement", font_size=14, color=DIM_TEXT).next_to(axes_r.x_axis, DOWN, buff=0.15)
        lbl_yr = Text("OOD Agreement", font_size=14, color=DIM_TEXT).next_to(axes_r.y_axis, UP, buff=0.15)
        diag_r = DashedLine(axes_r.c2p(0.4, 0.4), axes_r.c2p(1.0, 1.0), color=DIM_TEXT, stroke_width=1.0)

        self.play(
            Create(axes_r), Write(lbl_xr), Write(lbl_yr), Create(diag_r),
            run_time=2.0
        ) # Reach 395.0s
        self.play(Indicate(diag_r, color=PAPER_PURPLE), run_time=2.0) # Reach 397.0s
        self.play(Indicate(lbl_xr, color=PAPER_PURPLE), run_time=2.0) # Reach 399.0s
        self.wait(9.1) # Reach 408.1s

        # 408.1s: Line Agreement
        line_acc = Line(axes_r.c2p(0.45, 0.4), axes_r.c2p(0.95, 0.9), color=PAPER_BLUE, stroke_width=2.5)
        line_agr = Line(axes_r.c2p(0.45, 0.4), axes_r.c2p(0.95, 0.9), color=PAPER_PURPLE, stroke_width=1.5)

        dots_acc = VGroup()
        dots_agr = VGroup()
        for _ in range(15):
            id_val = np.random.uniform(0.5, 0.95)
            ood_val_acc = 1.25 * id_val - 0.32 + np.random.normal(0, 0.015)
            ood_val_agr = 1.25 * id_val - 0.32 + np.random.normal(0, 0.015)
            pt_acc = Dot(axes_r.c2p(id_val, ood_val_acc), radius=0.04, color=PAPER_BLUE, fill_opacity=0.6)
            pt_agr = Dot(axes_r.c2p(id_val, ood_val_agr), radius=0.04, color=PAPER_PURPLE, fill_opacity=0.6)
            dots_acc.add(pt_acc)
            dots_agr.add(pt_agr)

        self.play(
            Create(line_acc), Create(line_agr), Create(dots_acc), Create(dots_agr),
            run_time=2.5
        ) # Reach 410.6s

        connect_arrow = DoubleArrow(fit_line_l.get_center(), line_agr.get_center(), color=PAPER_YELLOW, stroke_width=1.5)
        self.play(Create(connect_arrow), run_time=1.5) # Reach 412.1s

        keyword_text = Text("Đo Đồng Thuận \u2192 Ước Lượng OOD Accuracy", font_size=15, color=HIGHLIGHT).shift(UP * 1.5)
        self.play(Write(keyword_text), run_time=1.5) # Reach 413.6s

        # Micro-oscillations loop to keep screen dynamic until 439s (25.4s total)
        # 6 iterations of 4.2s loop = 25.2s
        for _ in range(6):
            self.play(
                *[p.animate.shift(np.random.normal(0, 0.03, 3)) for p in dots_l],
                *[p.animate.shift(np.random.normal(0, 0.03, 3)) for p in dots_acc],
                run_time=2.0,
                rate_func=there_and_back
            )
            self.play(Indicate(keyword_text, color=HIGHLIGHT), run_time=2.2) # Reach 438.8s
            
        self.wait(3.2) # Reach 442.0s

        # Cleanup Scene 4
        self.play(
            FadeOut(title), FadeOut(axes_l), FadeOut(lbl_xl), FadeOut(lbl_yl), FadeOut(diag_l),
            FadeOut(fit_line_l), FadeOut(fit_lbl_l), FadeOut(dots_l),
            FadeOut(axes_r), FadeOut(lbl_xr), FadeOut(lbl_yr), FadeOut(diag_r),
            FadeOut(line_acc), FadeOut(line_agr), FadeOut(dots_acc), FadeOut(dots_agr),
            FadeOut(connect_arrow), FadeOut(keyword_text),
            run_time=1.0
        ) # Reach 443.0s

        # Bridge transition segment: 443.0s to 445.0s (2.0s)
        bridge_title = Text("3 Phát hiện thực nghiệm quan trọng", font_size=28, color=TITLE_COLOR)
        self.play(Write(bridge_title), run_time=1.2) # Reach 444.2s
        self.play(FadeOut(bridge_title), run_time=0.8) # Reach 445.0s
        self.wait(2.0) # Reach 447.0s

    # ═══════════════════════════════════════════════════════════════════
    # SCENE 5 — Summary of empirical DL (≈1m)
    # ═══════════════════════════════════════════════════════════════════
    def scene5_summary(self):
        # 447.0s: Summary Title
        title = Text(
            "Tổng kết: Khoa học thực nghiệm DL",
            font_size=32,
            color=TITLE_COLOR,
        ).to_edge(UP, buff=0.6)
        self.play(Write(title), run_time=1.0) # Reach 448.0s

        # Card 1: Edge of Stability (starts at 447.0s)
        card1 = RoundedRectangle(width=8.0, height=0.9, corner_radius=0.1, fill_color=CARD_BG, fill_opacity=0.9, stroke_color=PAPER_ORANGE, stroke_width=1.5).shift(UP * 0.8)
        c1_head = Text("1. Edge of Stability", font_size=14, color=PAPER_ORANGE).move_to(card1.get_center() + LEFT * 2.5)
        c1_desc = Text("Sharpness sát ngưỡng 2/\u03b7, loss giảm nhảy vọt", font_size=14, color=TEXT_COLOR).move_to(card1.get_center() + RIGHT * 1.0)
        
        self.play(Create(card1), FadeIn(c1_head), FadeIn(c1_desc), run_time=1.0) # Reach 449.0s
        self.play(Indicate(card1), run_time=1.5) # Reach 450.5s
        
        # Add application text for Card 1
        app1 = Text("Ứng dụng: Tăng tốc huấn luyện bằng cách dùng tốc độ học lớn hơn", font_size=14, color=PAPER_ORANGE).shift(DOWN * 2.3)
        self.play(FadeIn(app1), run_time=1.5) # Reach 452.0s
        self.play(Circumscribe(card1, color=PAPER_ORANGE), run_time=2.0) # Reach 454.0s
        self.wait(8.0) # Reach 462.0s

        # 462.0s: Card 2 - Disagreement ≈ Error
        card2 = RoundedRectangle(width=8.0, height=0.9, corner_radius=0.1, fill_color=CARD_BG, fill_opacity=0.9, stroke_color=PAPER_GREEN, stroke_width=1.5).shift(DOWN * 0.3)
        c2_head = Text("2. Disagreement \u2248 Error", font_size=14, color=PAPER_GREEN).move_to(card2.get_center() + LEFT * 2.2)
        c2_desc = Text("Tỷ lệ bất đồng dự đoán phản ánh chính xác sai số", font_size=14, color=TEXT_COLOR).move_to(card2.get_center() + RIGHT * 1.2)
        
        self.play(Create(card2), FadeIn(c2_head), FadeIn(c2_desc), FadeOut(app1), run_time=1.0) # Reach 463.0s
        self.play(Indicate(card2), run_time=1.5) # Reach 464.5s
        
        # Add application text for Card 2
        app2 = Text("Ứng dụng: Ước lượng độ bất định (uncertainty estimation) không cần nhãn đúng", font_size=14, color=PAPER_GREEN).shift(DOWN * 2.3)
        self.play(FadeIn(app2), run_time=1.5) # Reach 466.0s
        self.play(Circumscribe(card2, color=PAPER_GREEN), run_time=2.0) # Reach 468.0s
        self.wait(7.5) # Reach 475.5s

        # 475.5s: Card 3 - Agreement on the Line
        card3 = RoundedRectangle(width=8.0, height=0.9, corner_radius=0.1, fill_color=CARD_BG, fill_opacity=0.9, stroke_color=PAPER_BLUE, stroke_width=1.5).shift(DOWN * 1.4)
        c3_head = Text("3. Agreement on the Line", font_size=14, color=PAPER_BLUE).move_to(card3.get_center() + LEFT * 2.0)
        c3_desc = Text("Ước lượng OOD accuracy bằng đo sự đồng thuận", font_size=14, color=TEXT_COLOR).move_to(card3.get_center() + RIGHT * 1.4)
        
        self.play(Create(card3), FadeIn(c3_head), FadeIn(c3_desc), FadeOut(app2), run_time=1.0) # Reach 476.5s
        self.play(Indicate(card3), run_time=1.5) # Reach 478.0s
        
        # Add application text for Card 3
        app3 = Text("Ứng dụng: Đánh giá độ an toàn của xe tự lái trên môi trường thực tế mới", font_size=14, color=PAPER_BLUE).shift(DOWN * 2.3)
        self.play(FadeIn(app3), run_time=1.5) # Reach 479.5s
        self.play(Circumscribe(card3, color=PAPER_BLUE), run_time=2.0) # Reach 481.5s
        self.wait(8.0) # Reach 489.5s

        # 489.5s: Core conclusion paradigm
        self.play(Indicate(card1), Indicate(card2), Indicate(card3), FadeOut(app3), run_time=1.5) # Reach 491.0s
        
        summary_kw = Text("Thực nghiệm \u2192 Quy luật \u2192 Lý thuyết", font_size=18, color=HIGHLIGHT).shift(UP * 1.8)
        self.play(Write(summary_kw), run_time=1.5) # Reach 492.5s

        self.play(Indicate(summary_kw, color=HIGHLIGHT), run_time=2.0) # Reach 494.5s
        self.play(*[Indicate(card) for card in [card1, card2, card3]], run_time=2.0) # Reach 496.5s
        self.play(Circumscribe(card1, color=PAPER_ORANGE), run_time=2.0) # Reach 498.5s
        self.play(Circumscribe(card2, color=PAPER_GREEN), run_time=2.0) # Reach 500.5s
        self.play(Circumscribe(card3, color=PAPER_BLUE), run_time=2.0) # Reach 502.5s
        self.wait(1.5) # Reach 504.0s

        # Cleanup Scene 5
        self.play(
            FadeOut(title), FadeOut(card1), FadeOut(card2), FadeOut(card3),
            FadeOut(c1_head), FadeOut(c1_desc), FadeOut(c2_head), FadeOut(c2_desc),
            FadeOut(c3_head), FadeOut(c3_desc), FadeOut(summary_kw),
            run_time=1.0
        ) # Reach 505.0s

    # ═══════════════════════════════════════════════════════════════════
    # SCENE 6 — Transition to AI Safety (≈30s)
    # ═══════════════════════════════════════════════════════════════════
    def scene6_transition(self):
        # 505.0s: AI Safety shield
        shield_pts = [
            UP * 1.2,
            UP * 1.0 + RIGHT * 0.9,
            DOWN * 0.4 + RIGHT * 0.9,
            DOWN * 1.2,
            DOWN * 0.4 + LEFT * 0.9,
            UP * 1.0 + LEFT * 0.9,
        ]
        shield = Polygon(
            *[ORIGIN + pt for pt in shield_pts],
            color=PAPER_GREEN, fill_color=PAPER_GREEN, fill_opacity=0.15, stroke_width=2.5
        ).move_to(ORIGIN + UP * 0.5)

        safety_text = Text(
            "AI Safety",
            font_size=40,
            color=PAPER_ORANGE,
        ).move_to(ORIGIN + UP * 0.5)

        sub_text = Text(
            "Hướng đi mới cho nghiên cứu học thuật",
            font_size=16,
            color=TEXT_COLOR,
        ).next_to(shield, DOWN, buff=0.5)

        self.play(Create(shield), Write(safety_text), run_time=1.5) # Reach 506.5s
        self.play(FadeIn(sub_text, shift=UP * 0.25), run_time=1.0) # Reach 507.5s

        self.play(Indicate(safety_text, color=PAPER_ORANGE), run_time=2.0) # Reach 509.5s
        self.wait(7.5) # Reach 517.0s

        # Fade out everything
        self.play(
            FadeOut(shield),
            FadeOut(safety_text),
            FadeOut(sub_text),
            run_time=1.0
        ) # Reach 518.0s
