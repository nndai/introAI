from manim import *
import numpy as np

# Color Palette
BG_COLOR = "#0D0D11"       # Deep dark space blue
TEXT_COLOR = "#E2E8F0"     # Warm white
HIGHLIGHT = "#F59E0B"      # Golden Amber
PAPER_ORANGE = "#FF7F50"   # Coral
PAPER_BLUE = "#3B82F6"     # Deep Blue
PAPER_GREEN = "#10B981"    # Emerald
PAPER_RED = "#EF4444"      # Red
TITLE_COLOR = "#F1F5F9"    # Bright slate
CARD_BG = "#1E1E24"        # Dark slate card

class Part12Scene(ThreeDScene):
    def construct(self):
        # Set default font for Vietnamese text support
        Text.set_default(font="sans-serif")
        
        # Configure background color
        self.camera.background_color = BG_COLOR

        # Execute Scenes sequentially
        self.scene1_recap()
        self.scene2_academia()
        self.scene3_message()
        self.scene4_quote()

    # ═══════════════════════════════════════════════════════════════════
    # SCENE 1 — recap flow (0.0s to 121.5s)
    # ═══════════════════════════════════════════════════════════════════
    def scene1_recap(self):
        title = Text("Nhìn lại hành trình: Từ Tối ưu hóa đến An toàn", font_size=32, color=TITLE_COLOR).to_edge(UP, buff=0.6)
        self.add_fixed_in_frame_mobjects(title)
        self.play(Write(title), run_time=1.5) # Reach 1.5s
        self.wait(13.0) # Reach 14.5s

        # Tilting the camera to reveal 3D Optimization Space
        self.move_camera(phi=60 * DEGREES, theta=-45 * DEGREES, zoom=0.85, run_time=2.0) # Reach 16.5s

        # 3D surface representing optimization bowl / landscape
        surface = Surface(
            lambda u, v: np.array([u, v, 0.25 * (u**2 + v**2) - 1.0]),
            u_range=[-1.8, 1.8],
            v_range=[-1.8, 1.8],
            resolution=(15, 15),
            color=PAPER_ORANGE
        ).shift(LEFT * 2.5 + DOWN * 0.5)
        surface.set_style(fill_opacity=0.35, stroke_color=PAPER_ORANGE, stroke_width=0.5)
        
        # Optimization trajectory down the surface (spiral curve)
        opt_path = ParametricFunction(
            lambda t: np.array([
                1.5 * np.cos(t) * (1 - t/12) - 2.5,
                1.5 * np.sin(t) * (1 - t/12) - 0.5,
                0.25 * (1.5 * (1 - t/12))**2 - 1.5
            ]),
            t_range=[0, 10],
            color=HIGHLIGHT,
            stroke_width=2.5
        )
        dot = Dot(color=HIGHLIGHT, radius=0.08).move_to(opt_path.points[0])
        
        # Optimization card on the right (fixed in frame to prevent skewing)
        opt_card = RoundedRectangle(width=4.4, height=3.0, corner_radius=0.1, fill_color=CARD_BG, fill_opacity=0.9, stroke_color=PAPER_ORANGE, stroke_width=2.0).shift(RIGHT * 3.5 + DOWN * 0.5)
        opt_lbl = Text("Tối ưu hóa (Optimization)", font_size=16, color=PAPER_ORANGE).move_to(opt_card.get_top() + DOWN * 0.4)
        opt_sub = Text("ICNN, OptNet, DEQ\nRàng buộc lồi nghiêm ngặt\nTốc độ hội tụ và độ an toàn", font_size=14, color=TEXT_COLOR, line_spacing=0.8).next_to(opt_lbl, DOWN, buff=0.25)
        
        self.add_fixed_in_frame_mobjects(opt_card, opt_lbl, opt_sub)
        
        self.play(Create(surface), Create(opt_path), FadeIn(dot), run_time=2.0) # Reach 18.5s
        self.play(MoveAlongPath(dot, opt_path), run_time=3.5) # Reach 22.0s
        self.wait(9.0) # Reach 31.0s
 
        opt_detail = Text("Ràng buộc cứng\nNhưng scale chậm", font_size=14, color=PAPER_ORANGE, line_spacing=0.8).next_to(opt_sub, DOWN, buff=0.25)
        self.add_fixed_in_frame_mobjects(opt_detail)
        
        self.play(Write(opt_detail), run_time=1.5) # Reach 32.5s
        self.wait(13.5) # Reach 46.0s

        # Fade out optimization surface and restore camera back to flat 2D
        self.play(
            FadeOut(surface), FadeOut(opt_path), FadeOut(dot),
            FadeOut(opt_card), FadeOut(opt_lbl), FadeOut(opt_sub), FadeOut(opt_detail),
            run_time=1.5
        ) # Reach 47.5s
        
        self.move_camera(phi=0, theta=-90 * DEGREES, zoom=1.0, run_time=1.0) # Reach 48.5s
        self.wait(0.5) # Reach 49.0s

        # Create block 2: Robustness
        rob_rect = RoundedRectangle(width=2.5, height=1.5, corner_radius=0.1, fill_color=CARD_BG, fill_opacity=0.9, stroke_color=PAPER_BLUE, stroke_width=2.0).shift(LEFT * 1.5 + DOWN * 0.5)
        rob_label = Text("Độ bền vững", font_size=18, color=PAPER_BLUE).move_to(rob_rect.get_center() + UP * 0.45)
        rob_sub = Text("Convex, Smoothing", font_size=14, color=TEXT_COLOR).move_to(rob_rect.get_center() + UP * 0.15)
        
        # Epsilon-ball visual inside Robustness
        center_dot = Dot(color=PAPER_BLUE, radius=0.06).move_to(rob_rect.get_center() + DOWN * 0.3)
        eps_ball = Circle(radius=0.3, color=PAPER_BLUE, stroke_width=1.0).set_opacity(0.4).move_to(center_dot.get_center())
        # Adversarial perturbations (red dots)
        adv_dots = VGroup(*[
            Dot(point=center_dot.get_center() + np.array([np.cos(a)*r, np.sin(a)*r, 0]), color=PAPER_RED, radius=0.035)
            for a, r in zip([0.5, 1.8, 3.2, 4.5], [0.15, 0.2, 0.4, 0.25])
        ])
        
        # Draw arrow from where the 3D surface was (LEFT * 2.5) to rob_rect (LEFT * 1.5)
        arrow1 = Arrow(LEFT * 2.5 + DOWN * 0.5, rob_rect.get_left(), color=TEXT_COLOR, stroke_width=2.0)
        
        self.play(
            GrowArrow(arrow1), Create(rob_rect), FadeIn(rob_label), FadeIn(rob_sub),
            FadeIn(center_dot), Create(eps_ball),
            run_time=2.0
        ) # Reach 51.0s
        self.play(FadeIn(adv_dots, lag_ratio=0.2), run_time=1.5) # Reach 52.5s
        self.play(*[Indicate(d, color=PAPER_RED, scale_factor=1.3) for d in adv_dots], run_time=1.5) # Reach 54.0s
        self.wait(12.0) # Reach 66.0s

        rob_detail = Text("Chứng minh an toàn\nNhưng giảm accuracy", font_size=14, color=TEXT_COLOR, line_spacing=0.8).next_to(rob_rect, DOWN, buff=0.4)
        
        # Create block 3: Empirical
        emp_rect = RoundedRectangle(width=2.5, height=1.5, corner_radius=0.1, fill_color=CARD_BG, fill_opacity=0.9, stroke_color=PAPER_GREEN, stroke_width=2.0).shift(RIGHT * 1.5 + DOWN * 0.5)
        emp_label = Text("Thực nghiệm", font_size=18, color=PAPER_GREEN).move_to(emp_rect.get_center() + UP * 0.45)
        emp_sub = Text("Edge, Disagreement", font_size=14, color=TEXT_COLOR).move_to(emp_rect.get_center() + UP * 0.15)
        
        # Scatter & Line fit inside Empirical
        scat_pts = [
            np.array([-0.4, -0.2, 0]),
            np.array([-0.2, -0.05, 0]),
            np.array([0.0, 0.0, 0]),
            np.array([0.15, 0.2, 0]),
            np.array([0.35, 0.1, 0]),
            np.array([0.5, 0.25, 0])
        ]
        scat_dots = VGroup(*[Dot(point=emp_rect.get_center() + pt + DOWN * 0.35, color=TEXT_COLOR, radius=0.035) for pt in scat_pts])
        fit_line = Line(
            emp_rect.get_center() + np.array([-0.55, -0.27, 0]) + DOWN * 0.35,
            emp_rect.get_center() + np.array([0.65, 0.32, 0]) + DOWN * 0.35,
            color=PAPER_GREEN, stroke_width=1.5
        )
        
        arrow2 = Arrow(rob_rect.get_right(), emp_rect.get_left(), color=TEXT_COLOR, stroke_width=2.0)
        
        self.play(
            Write(rob_detail), GrowArrow(arrow2), Create(emp_rect), FadeIn(emp_label), FadeIn(emp_sub),
            FadeIn(scat_dots),
            run_time=2.5
        ) # Reach 68.5s
        self.play(Create(fit_line), run_time=1.5) # Reach 70.0s
        self.wait(15.5) # Reach 85.5s

        emp_detail = Text("Đo đạc quy luật\nGiải thích lý thuyết", font_size=14, color=TEXT_COLOR, line_spacing=0.8).next_to(emp_rect, DOWN, buff=0.4)
        self.play(Write(emp_detail), run_time=1.5) # Reach 87.0s
        self.wait(13.0) # Reach 100.0s

        # Create block 4: Safety
        saf_rect = RoundedRectangle(width=2.5, height=1.5, corner_radius=0.1, fill_color=CARD_BG, fill_opacity=0.9, stroke_color=HIGHLIGHT, stroke_width=2.0).shift(RIGHT * 4.5 + DOWN * 0.5)
        saf_label = Text("An toàn AI", font_size=18, color=HIGHLIGHT).move_to(saf_rect.get_center() + UP * 0.45)
        saf_sub = Text("Jailbreak, Unlearning", font_size=14, color=TEXT_COLOR).move_to(saf_rect.get_center() + UP * 0.15)
        
        # Small Neural Net and Shield visual inside Safety
        net_dots = VGroup()
        for col, num in enumerate([3, 2, 1]):
            for row in range(num):
                pt = saf_rect.get_center() + np.array([col * 0.25 - 0.25, row * 0.2 - (num - 1) * 0.1 - 0.35, 0])
                net_dots.add(Dot(point=pt, color=TEXT_COLOR, radius=0.03))
        shield = Circle(radius=0.38, color=HIGHLIGHT, stroke_width=1.5).move_to(saf_rect.get_center() + DOWN * 0.35).set_opacity(0.8)
        
        arrow3 = Arrow(emp_rect.get_right(), saf_rect.get_left(), color=TEXT_COLOR, stroke_width=2.0)
        saf_detail = Text("Kiểm soát hành vi\nPretraining an toàn", font_size=14, color=TEXT_COLOR, line_spacing=0.8).next_to(saf_rect, DOWN, buff=0.4)
        
        self.play(
            GrowArrow(arrow3), Create(saf_rect), FadeIn(saf_label), FadeIn(saf_sub), Write(saf_detail),
            FadeIn(net_dots),
            run_time=2.5
        ) # Reach 102.5s
        self.play(Create(shield), run_time=1.5) # Reach 104.0s
        self.wait(16.0) # Reach 120.0s
        
        # Fade out Scene 1
        self.play(
            FadeOut(title),
            FadeOut(rob_rect), FadeOut(rob_label), FadeOut(rob_sub), FadeOut(rob_detail),
            FadeOut(emp_rect), FadeOut(emp_label), FadeOut(emp_sub), FadeOut(emp_detail),
            FadeOut(saf_rect), FadeOut(saf_label), FadeOut(saf_sub), FadeOut(saf_detail),
            FadeOut(arrow1), FadeOut(arrow2), FadeOut(arrow3),
            FadeOut(center_dot), FadeOut(eps_ball), FadeOut(adv_dots),
            FadeOut(scat_dots), FadeOut(fit_line), FadeOut(net_dots), FadeOut(shield),
            run_time=1.0
        ) # Reach 121.0s
        self.remove_fixed_in_frame_mobjects(title)
        self.wait(0.5) # Reach 121.5s

    # ═══════════════════════════════════════════════════════════════════
    # SCENE 2 — Academia Opportunity (121.5s to 195.5s)
    # ═══════════════════════════════════════════════════════════════════
    def scene2_academia(self):
        title = Text("AI Safety: Cơ hội lớn nhất cho Academia", font_size=32, color=TITLE_COLOR).to_edge(UP, buff=0.6)
        self.play(Write(title), run_time=1.5) # Reach 123.0s

        # Industry Card
        ind_card = RoundedRectangle(width=4.5, height=2.0, corner_radius=0.1, fill_color=CARD_BG, fill_opacity=0.9, stroke_color=PAPER_RED, stroke_width=2.0).shift(LEFT * 3.5 + UP * 0.5)
        ind_lbl = Text("Công nghiệp (Industry)", font_size=18, color=PAPER_RED).move_to(ind_card.get_center() + UP * 0.6)
        ind_desc = Text(
            "Hàng ngàn GPU\nTriệu đô-la\nHuấn luyện\nmô hình lớn", 
            font_size=14, 
            color=TEXT_COLOR,
            line_spacing=0.8
        ).move_to(ind_card.get_center() + RIGHT * 0.9 + DOWN * 0.2)
        
        # Industry Visuals: A 3x3 grid of red GPUs/servers on the left side of the card
        gpu_grid = VGroup()
        grid_center = ind_card.get_center() + LEFT * 1.0 + DOWN * 0.2
        for r in range(3):
            for c in range(3):
                gpu_grid.add(Square(side_length=0.15, fill_color=PAPER_RED, fill_opacity=0.8, stroke_color=BG_COLOR, stroke_width=0.5).move_to(grid_center + np.array([c * 0.25 - 0.25, r * 0.25 - 0.25, 0])))
        
        # Academia Card
        acad_card = RoundedRectangle(width=4.5, height=2.0, corner_radius=0.1, fill_color=CARD_BG, fill_opacity=0.9, stroke_color=PAPER_BLUE, stroke_width=2.0).shift(RIGHT * 3.5 + UP * 0.5)
        acad_lbl = Text("Học thuật (Academia)", font_size=18, color=PAPER_BLUE).move_to(acad_card.get_center() + UP * 0.6)
        acad_desc = Text(
            "Tài nguyên hạn chế\nÍt GPU\nLo ngại\ncạnh tranh?", 
            font_size=14, 
            color=TEXT_COLOR,
            line_spacing=0.8
        ).move_to(acad_card.get_center() + RIGHT * 0.9 + DOWN * 0.2)
        
        # Academia Visuals: A glowing sphere/brain representing creative idea on the left side of the card
        brain_node = Circle(radius=0.35, color=PAPER_BLUE, fill_color=CARD_BG, fill_opacity=1.0, stroke_width=1.5).move_to(acad_card.get_center() + LEFT * 1.0 + DOWN * 0.2)
        brain_text = Text("Ý tưởng", font_size=14, color=PAPER_BLUE).move_to(brain_node.get_center())
        
        self.play(
            Create(ind_card), FadeIn(ind_lbl), FadeIn(ind_desc), FadeIn(gpu_grid),
            Create(acad_card), FadeIn(acad_lbl), FadeIn(acad_desc), FadeIn(brain_node), FadeIn(brain_text),
            run_time=2.0
        ) # Reach 125.0s
        
        # Pulse industry GPUs to represent computing force
        self.play(*[Indicate(g, color=HIGHLIGHT, scale_factor=1.2) for g in gpu_grid], run_time=1.5) # Reach 126.5s
        self.wait(13.0) # Reach 139.5s

        opportunity_txt = Text("AI Safety: Cơ hội định hình lại cuộc chơi", font_size=24, color=HIGHLIGHT).shift(DOWN * 1.5)
        self.play(Write(opportunity_txt), run_time=1.5) # Reach 141.0s
        self.wait(7.5) # Reach 148.5s

        # Fade out Industry and Academia cards to make space
        self.play(
            FadeOut(ind_card), FadeOut(ind_lbl), FadeOut(ind_desc), FadeOut(gpu_grid),
            FadeOut(acad_card), FadeOut(acad_lbl), FadeOut(acad_desc), FadeOut(brain_node), FadeOut(brain_text),
            opportunity_txt.animate.shift(UP * 2.5),
            run_time=1.5
        ) # Reach 150.0s
        
        # Draw 3 pillars of conceptual research
        p1 = RoundedRectangle(width=3.6, height=1.3, corner_radius=0.1, fill_color=CARD_BG, fill_opacity=0.9, stroke_color=PAPER_GREEN, stroke_width=1.5).shift(LEFT * 4.0 + DOWN * 0.5)
        p1_lbl = Text("Automated Jailbreaks\n(Tối ưu hóa suffix)", font_size=14, color=PAPER_GREEN, line_spacing=0.8).move_to(p1.get_center() + UP * 0.25)
        p1_visual = Text("[Prompt] + [Suffix!#$]", font_size=14, color=TEXT_COLOR).move_to(p1.get_center() + DOWN * 0.3)
        
        p2 = RoundedRectangle(width=3.6, height=1.3, corner_radius=0.1, fill_color=CARD_BG, fill_opacity=0.9, stroke_color=PAPER_GREEN, stroke_width=1.5).shift(DOWN * 0.5)
        p2_lbl = Text("Machine Unlearning\n(Quên chọn lọc)", font_size=14, color=PAPER_GREEN, line_spacing=0.8).move_to(p2.get_center() + UP * 0.25)
        
        # Unlearning node representation
        unlearn_dots = VGroup(*[Dot(point=p2.get_center() + np.array([np.cos(a)*0.25, np.sin(a)*0.25, 0]) + DOWN*0.35, color=PAPER_GREEN, radius=0.035) for a in np.linspace(0, 2*np.pi, 5, endpoint=False)])
        target_dot = Dot(point=p2.get_center() + DOWN*0.35, color=PAPER_RED, radius=0.045)
        
        p3 = RoundedRectangle(width=3.6, height=1.3, corner_radius=0.1, fill_color=CARD_BG, fill_opacity=0.9, stroke_color=PAPER_GREEN, stroke_width=1.5).shift(RIGHT * 4.0 + DOWN * 0.5)
        p3_lbl = Text("Anti-distillation\n(Ngăn sao chép)", font_size=14, color=PAPER_GREEN, line_spacing=0.8).move_to(p3.get_center() + UP * 0.25)
        
        # Distillation model copy representation
        teacher_box = RoundedRectangle(width=0.5, height=0.3, corner_radius=0.05, stroke_color=PAPER_BLUE, stroke_width=1.0).move_to(p3.get_center() + LEFT * 0.7 + DOWN * 0.3)
        student_box = RoundedRectangle(width=0.5, height=0.3, corner_radius=0.05, stroke_color=PAPER_ORANGE, stroke_width=1.0).move_to(p3.get_center() + RIGHT * 0.7 + DOWN * 0.3)
        copy_arrow = DoubleArrow(teacher_box.get_right(), student_box.get_left(), color=PAPER_RED, stroke_width=1.0)
        
        self.play(
            Create(p1), FadeIn(p1_lbl), FadeIn(p1_visual),
            Create(p2), FadeIn(p2_lbl), FadeIn(unlearn_dots), FadeIn(target_dot),
            Create(p3), FadeIn(p3_lbl), Create(teacher_box), Create(student_box), GrowArrow(copy_arrow),
            run_time=2.0
        ) # Reach 152.0s
        
        # Animate machine unlearning weight fading away
        self.play(target_dot.animate.set_color(CARD_BG).set_opacity(0.0), run_time=1.5) # Reach 153.5s
        self.wait(17.5) # Reach 171.0s

        concept_box = RoundedRectangle(width=7.0, height=1.0, corner_radius=0.1, fill_color=CARD_BG, fill_opacity=0.9, stroke_color=PAPER_ORANGE, stroke_width=2.0).shift(DOWN * 2.2)
        concept_txt = Text("Tư duy Khái niệm > Sức mạnh GPU", font_size=18, color=PAPER_ORANGE).move_to(concept_box.get_center())
        
        self.play(Create(concept_box), Write(concept_txt), run_time=1.5) # Reach 172.5s
        self.wait(11.0) # Reach 183.5s

        potential_txt = Text("Tiềm năng định hình tương lai công nghệ!", font_size=20, color=HIGHLIGHT).shift(DOWN * 2.2)
        self.play(ReplacementTransform(concept_txt, potential_txt), run_time=1.5) # Reach 185.0s
        self.wait(9.0) # Reach 194.0s
        
        # Fade out Scene 2
        self.play(
            FadeOut(title), FadeOut(opportunity_txt), FadeOut(p1), FadeOut(p1_lbl), FadeOut(p1_visual),
            FadeOut(p2), FadeOut(p2_lbl), FadeOut(unlearn_dots), FadeOut(target_dot),
            FadeOut(p3), FadeOut(p3_lbl), FadeOut(teacher_box), FadeOut(student_box), FadeOut(copy_arrow),
            FadeOut(concept_box), FadeOut(potential_txt),
            run_time=1.0
        ) # Reach 195.0s
        self.wait(0.5) # Reach 195.5s

    # ═══════════════════════════════════════════════════════════════════
    # SCENE 3 — Call to Action: Next ICLR 2015 (195.5s to 264.5s)
    # ═══════════════════════════════════════════════════════════════════
    def scene3_message(self):
        title = Text("Thông điệp gửi tới thế hệ tương lai", font_size=32, color=TITLE_COLOR).to_edge(UP, buff=0.6)
        self.play(Write(title), run_time=1.5) # Reach 197.0s
        self.wait(5.5) # Reach 202.5s

        junior_box = RoundedRectangle(width=5.5, height=3.0, corner_radius=0.1, fill_color=CARD_BG, fill_opacity=0.9, stroke_color=PAPER_ORANGE, stroke_width=2.0).shift(LEFT * 3.5 + UP * 0.2)
        junior_lbl = Text("Nghiên cứu sinh trẻ\n(Junior Researchers)", font_size=18, color=PAPER_ORANGE, line_spacing=0.8).move_to(junior_box.get_top() + DOWN * 0.5)
        junior_desc = Text("Đừng lo lắng nếu đề tài kỳ lạ\nTìm kiếm hướng đi mới\nDám đi lệch khỏi số đông", font_size=14, color=TEXT_COLOR, line_spacing=0.8).next_to(junior_lbl, DOWN, buff=0.25)
        
        self.play(Create(junior_box), FadeIn(junior_lbl), FadeIn(junior_desc), run_time=2.0) # Reach 204.5s
        self.wait(11.5) # Reach 216.0s

        iclr_label = Text("Hội nghị ICLR 2015: Chỉ 31 bài báo", font_size=20, color=PAPER_GREEN).shift(RIGHT * 3.5 + UP * 1.5)
        self.play(Write(iclr_label), run_time=1.5) # Reach 217.5s
        
        # Draw 31 dots in a grid
        dots = VGroup()
        for r in range(5):
            for c in range(6):
                dots.add(Dot(point=RIGHT * 2.0 + RIGHT * (c * 0.6) + DOWN * (r * 0.5), color=TEXT_COLOR, radius=0.08))
        dots.add(Dot(point=RIGHT * 2.0 + DOWN * 2.5, color=TEXT_COLOR, radius=0.08))
        dots.shift(UP * 0.5)
        
        self.play(FadeIn(dots), run_time=1.5) # Reach 219.0s
        
        landmark_highlights = [
            Circumscribe(dots[3], color=HIGHLIGHT),
            Circumscribe(dots[11], color=HIGHLIGHT),
            Circumscribe(dots[20], color=HIGHLIGHT),
        ]
        landmark_label = Text("Adam, GANs, Neural Turing Machines...", font_size=14, color=HIGHLIGHT).next_to(dots, DOWN, buff=0.4)
        
        self.play(*landmark_highlights, Write(landmark_label), run_time=2.0) # Reach 221.0s
        
        # Morph 31 dots grid into a massive cloud of 150 dots representing ICLR 2025's growth
        np.random.seed(42) # Set seed for deterministic randomness in render
        dots_2025 = VGroup(*[
            Dot(point=RIGHT * 3.5 + np.array([np.random.uniform(-1.5, 1.5), np.random.uniform(-1.5, 1.2), 0]), color=PAPER_BLUE, radius=0.035).set_opacity(0.6)
            for _ in range(150)
        ])
        iclr_label_2025 = Text("Hội nghị ICLR 2025: ~3700 bài báo", font_size=20, color=PAPER_BLUE).shift(RIGHT * 3.5 + UP * 1.5)
        
        self.play(
            ReplacementTransform(dots, dots_2025),
            ReplacementTransform(iclr_label, iclr_label_2025),
            run_time=2.5
        ) # Reach 223.5s
        self.wait(15.0) # Reach 238.5s

        # Fade out junior and ICLR grid/cloud
        self.play(
            FadeOut(junior_box), FadeOut(junior_lbl), FadeOut(junior_desc),
            FadeOut(iclr_label_2025), FadeOut(dots_2025), FadeOut(landmark_label),
            run_time=1.5
        ) # Reach 240.0s
        
        senior_box = RoundedRectangle(width=8.0, height=3.0, corner_radius=0.1, fill_color=CARD_BG, fill_opacity=0.9, stroke_color=PAPER_BLUE, stroke_width=2.0).shift(DOWN * 0.2)
        senior_lbl = Text("Giáo sư & Nhà nghiên cứu đi trước (Senior Faculty)", font_size=18, color=PAPER_BLUE).move_to(senior_box.get_top() + DOWN * 0.5)
        senior_desc = Text("Hãy rộng lượng và cởi mở với ứng viên mới\nHỗ trợ những hướng đi phi truyền thống\nĐón nhận sự thay đổi của khoa học trước mắt", font_size=14, color=TEXT_COLOR, line_spacing=0.8).next_to(senior_lbl, DOWN, buff=0.25)
        
        self.play(Create(senior_box), FadeIn(senior_lbl), FadeIn(senior_desc), run_time=2.0) # Reach 242.0s
        self.wait(12.5) # Reach 254.5s

        creative_txt = Text("Khuyến khích sự Khác biệt & Sáng tạo", font_size=20, color=HIGHLIGHT).shift(DOWN * 2.0)
        self.play(Write(creative_txt), run_time=1.5) # Reach 256.0s
        self.wait(7.0) # Reach 263.0s
        
        # Fade out Scene 3
        self.play(
            FadeOut(title), FadeOut(senior_box), FadeOut(senior_lbl), FadeOut(senior_desc), FadeOut(creative_txt),
            run_time=1.0
        ) # Reach 264.0s
        self.wait(0.5) # Reach 264.5s

    # ═══════════════════════════════════════════════════════════════════
    # SCENE 4 — Herb Simon & Final message (264.5s to 350.0s)
    # ═══════════════════════════════════════════════════════════════════
    def scene4_quote(self):
        simon_lbl = Text("Herbert Simon", font_size=32, color=HIGHLIGHT).to_edge(UP, buff=0.8)
        simon_desc = Text("Giải Nobel Kinh tế (1978) - Tiên phong Trí tuệ Nhân tạo", font_size=16, color=TEXT_COLOR).next_to(simon_lbl, DOWN, buff=0.2)
        
        self.play(Write(simon_lbl), FadeIn(simon_desc), run_time=2.0) # Reach 266.5s
        
        # Timeline visual representation
        timeline_line = Line(LEFT * 5 + DOWN * 2.0, RIGHT * 5 + DOWN * 2.0, color=TEXT_COLOR, stroke_width=2.0).set_opacity(0.3)
        t_1965 = Dot(point=LEFT * 4 + DOWN * 2.0, color=PAPER_BLUE, radius=0.08)
        lbl_1965 = Text("1965", font_size=14, color=PAPER_BLUE).next_to(t_1965, DOWN, buff=0.1)
        
        t_1985 = Dot(point=LEFT * 1 + DOWN * 2.0, color=PAPER_RED, radius=0.08)
        lbl_1985 = Text("1985", font_size=14, color=PAPER_RED).next_to(t_1985, DOWN, buff=0.1)
        
        t_2025 = Dot(point=RIGHT * 3 + DOWN * 2.0, color=PAPER_GREEN, radius=0.08)
        lbl_2025 = Text("2025", font_size=14, color=PAPER_GREEN).next_to(t_2025, DOWN, buff=0.1)
        
        timeline_cursor = Dot(point=LEFT * 4 + DOWN * 2.0, color=HIGHLIGHT, radius=0.12)
        
        self.play(
            Create(timeline_line), FadeIn(t_1965), FadeIn(lbl_1965),
            FadeIn(t_1985), FadeIn(lbl_1985), FadeIn(t_2025), FadeIn(lbl_2025),
            FadeIn(timeline_cursor),
            run_time=2.0
        ) # Reach 268.5s
        self.wait(12.0) # Reach 280.5s

        quote_box = RoundedRectangle(width=10.0, height=2.0, corner_radius=0.1, fill_color=CARD_BG, fill_opacity=0.9, stroke_color=PAPER_BLUE, stroke_width=1.5).shift(UP * 0.2)
        quote_text1 = Text('"Machines will be capable, within twenty years,', font_size=20, color=TITLE_COLOR).move_to(quote_box.get_center() + UP * 0.4)
        quote_text2 = Text('of doing any work a man can do."', font_size=20, color=TITLE_COLOR).move_to(quote_box.get_center() + DOWN * 0.2)
        quote_author = Text("— Herbert Simon, 1965", font_size=16, color=PAPER_BLUE).move_to(quote_box.get_center() + DOWN * 0.7)
        
        self.play(Create(quote_box), Write(quote_text1), Write(quote_text2), FadeIn(quote_author), run_time=2.0) # Reach 282.5s
        
        # Slide timeline cursor to 1985 (Simon's AGI estimate)
        self.play(timeline_cursor.animate.move_to(t_1985.get_center()), run_time=2.5) # Reach 285.0s
        self.wait(4.0) # Reach 289.0s

        wrong_label = Text("Ông ấy đã sai về mốc thời gian!", font_size=22, color=PAPER_RED).shift(DOWN * 1.0)
        self.play(Write(wrong_label), run_time=1.5) # Reach 290.5s
        
        # Add a red Cross indicating Simon was wrong on timeline, then slide to present (2025)
        cross_x = Cross(lbl_1985, stroke_color=PAPER_RED, stroke_width=3.0, scale_factor=0.8)
        self.play(Create(cross_x), run_time=1.5) # Reach 292.0s
        self.play(timeline_cursor.animate.move_to(t_2025.get_center()), run_time=3.0) # Reach 295.0s
        self.wait(12.5) # Reach 307.5s

        optimism_txt = Text("Thành quả bền vững từ sự Lạc quan khoa học!", font_size=22, color=PAPER_GREEN).shift(DOWN * 1.0)
        self.play(ReplacementTransform(wrong_label, optimism_txt), run_time=1.5) # Reach 309.0s
        self.wait(10.0) # Reach 319.0s

        # Fade out Simon details & Timeline elements
        self.play(
            FadeOut(simon_lbl), FadeOut(simon_desc),
            FadeOut(quote_box), FadeOut(quote_text1), FadeOut(quote_text2), FadeOut(quote_author),
            FadeOut(optimism_txt),
            FadeOut(timeline_line), FadeOut(t_1965), FadeOut(lbl_1965),
            FadeOut(t_1985), FadeOut(lbl_1985), FadeOut(t_2025), FadeOut(lbl_2025),
            FadeOut(timeline_cursor), FadeOut(cross_x),
            run_time=2.0
        ) # Reach 321.0s
        
        # Spark Network in 3D (shifted to the right to leave space for the legend on the left)
        spark_pts = [
            np.array([0.0, 1.3, 0.6]),
            np.array([1.5, 0.4, -0.5]),
            np.array([2.3, 1.5, 0.4]),
            np.array([3.8, 0.2, -0.6]),
            np.array([0.5, -0.7, -0.4]),
            np.array([1.4, -1.3, 0.5]),
            np.array([2.3, -0.5, -0.3]),
            np.array([3.8, -1.5, 0.5]),
        ]
        spark_labels = [
            "ICNN", "OptNet", "Robustness", "Smoothing",
            "Stability", "Disagreement", "Agreement", "Safety"
        ]
        
        dots_sp = VGroup()
        for pt in spark_pts:
            dots_sp.add(Dot(point=pt, color=HIGHLIGHT, radius=0.15))
            
        lines_sp = VGroup()
        for i in range(len(spark_pts) - 1):
            lines_sp.add(Line(spark_pts[i], spark_pts[i+1], color=PAPER_BLUE, stroke_width=1.5).set_opacity(0.4))
            
        # 2D Legend Card on the left (added as fixed_in_frame to prevent tilting)
        legend_box = RoundedRectangle(width=3.8, height=4.8, corner_radius=0.1, fill_color=CARD_BG, fill_opacity=0.9, stroke_color=PAPER_BLUE, stroke_width=1.5).shift(LEFT * 4.0 + DOWN * 0.2)
        legend_title = Text("Các Trụ cột Tri thức", font_size=16, color=PAPER_BLUE).move_to(legend_box.get_top() + DOWN * 0.4)
        
        legend_items = VGroup()
        for i, lbl in enumerate(spark_labels):
            item = Text(f"• {lbl}", font_size=14, color=TEXT_COLOR)
            item.next_to(legend_title, DOWN, buff=0.3 + i * 0.42).align_to(legend_title, LEFT)
            legend_items.add(item)
            
        # Tilting the camera to reveal 3D space while creating the lines
        self.move_camera(phi=60 * DEGREES, theta=-60 * DEGREES, zoom=0.9, added_anims=[Create(lines_sp)], run_time=3.0) # Reach 324.0s
        
        # Start ambient camera rotation for dynamic depth
        self.begin_ambient_camera_rotation(rate=0.06)
        
        # Add legend to fixed_in_frame to prevent it from tilting or skewing, then fade it in along with 3D dots
        self.add_fixed_in_frame_mobjects(legend_box, legend_title, *legend_items)
        
        animations = [
            FadeIn(legend_box), Write(legend_title), FadeIn(legend_items, lag_ratio=0.1),
            *[FadeIn(d) for d in dots_sp]
        ]
        self.play(*animations, run_time=3.0) # Reach 327.0s
        
        # Spark Neural Net flash effect
        self.play(
            *[Indicate(d, color=HIGHLIGHT) for d in dots_sp],
            *[Flash(d, color=HIGHLIGHT, line_length=0.15) for d in dots_sp],
            run_time=2.0
        ) # Reach 329.0s
        self.wait(13.0) # Reach 342.0s

        # Stop ambient camera rotation and smoothly sweep camera back to 2D XY plane while collapsing network to center
        self.stop_ambient_camera_rotation()
        self.move_camera(
            phi=0, theta=-90 * DEGREES, zoom=1.0,
            added_anims=[
                FadeOut(legend_box), FadeOut(legend_title), FadeOut(legend_items), FadeOut(lines_sp),
                *[d.animate.move_to(ORIGIN) for d in dots_sp]
            ],
            run_time=2.0
        ) # Reach 344.0s
        
        final_dot = Dot(point=ORIGIN, color=HIGHLIGHT, radius=0.25)
        self.add(final_dot)
        self.remove(dots_sp)
        
        final_msg1 = Text("Giữ vững sự Lạc quan Khoa học", font_size=24, color=HIGHLIGHT).shift(UP * 1.2)
        final_msg2 = Text("và tiếp tục Khám phá!", font_size=24, color=HIGHLIGHT).shift(UP * 0.4)
        thank_you = Text("Cảm ơn các bạn đã đồng hành!", font_size=20, color=TEXT_COLOR).shift(DOWN * 1.0)
        
        self.play(
            Flash(final_dot, color=HIGHLIGHT, line_length=0.3), # Spark explosion on merge
            Indicate(final_dot, color=HIGHLIGHT),
            Write(final_msg1), Write(final_msg2),
            FadeIn(thank_you, shift=UP * 0.2),
            run_time=2.5
        ) # Reach 346.5s
        self.wait(2.5) # Reach 349.0s
        
        self.play(
            FadeOut(final_dot), FadeOut(final_msg1), FadeOut(final_msg2), FadeOut(thank_you),
            run_time=1.0
        ) # Reach 350.0s
