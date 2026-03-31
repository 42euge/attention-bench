"""AttentionBench Explainer Video — Manim Scene (standalone, no audio sync)."""
from manim import *
import numpy as np

# Color scheme
SELECTIVE_COLOR = BLUE
SUSTAINED_COLOR = GREEN
DIVIDED_COLOR = ORANGE
CHANGE_COLOR = PURPLE
BG_COLOR = "#1a1a2e"


def make_axes_with_text_labels(x_range, y_range, x_length, y_length,
                                x_labels=None, y_labels=None):
    """Create axes with Text labels instead of LaTeX to avoid dvisvgm issues."""
    axes = Axes(
        x_range=x_range, y_range=y_range,
        x_length=x_length, y_length=y_length,
        axis_config={"color": GREY_C, "include_numbers": False},
    )
    labels = VGroup()
    if x_labels:
        for val in x_labels:
            label = Text(str(val), font_size=14, color=GREY_C)
            label.next_to(axes.c2p(val, y_range[0]), DOWN, buff=0.15)
            labels.add(label)
    if y_labels:
        for val in y_labels:
            label = Text(str(val), font_size=14, color=GREY_C)
            label.next_to(axes.c2p(x_range[0], val), LEFT, buff=0.15)
            labels.add(label)
    return axes, labels


class AttentionBenchVideo(Scene):
    def setup(self):
        self.camera.background_color = BG_COLOR

    def construct(self):
        self.s01_hook()
        self.s02_question()
        self.s03_problem()
        self.s04_intro()
        self.s05_four_types()
        self.s06_selective()
        self.s07_selective_demo()
        self.s08_sustained()
        self.s09_sustained_demo()
        self.s10_divided()
        self.s11_divided_demo()
        self.s12_change()
        self.s13_change_demo()
        self.s14_key_insight()
        self.s15_conclusion()

    def s01_hook(self):
        icons = VGroup(
            Text("f(x) = ...", font_size=28, color=BLUE_C),
            Text("def solve():", font_size=28, color=GREEN_C),
            Text('"Therefore..."', font_size=28, color=YELLOW),
        ).arrange(RIGHT, buff=1.5).shift(DOWN * 0.5)

        labels = VGroup(
            Text("Reason", font_size=22, color=GREY),
            Text("Code", font_size=22, color=GREY),
            Text("Debate", font_size=22, color=GREY),
        )
        for label, icon in zip(labels, icons):
            label.next_to(icon, DOWN, buff=0.3)

        title = Text("LLMs can...", font_size=44, color=WHITE).shift(UP * 1.5)

        self.play(Write(title), run_time=1)
        for icon, label in zip(icons, labels):
            self.play(FadeIn(icon), FadeIn(label), run_time=0.5)
        self.wait(2)
        self.play(FadeOut(VGroup(title, icons, labels)), run_time=0.5)

    def s02_question(self):
        question = Text("But can they focus?", font_size=56, color=WHITE)
        underline = Line(LEFT * 2.5, RIGHT * 2.5, color=YELLOW).next_to(question, DOWN, buff=0.2)
        self.play(Write(question), run_time=1)
        self.play(Create(underline), run_time=0.5)
        self.wait(2)
        self.play(FadeOut(VGroup(question, underline)), run_time=0.5)

    def s03_problem(self):
        left_title = Text("Current Benchmarks", font_size=30, color=GREY).shift(LEFT * 3 + UP * 2)
        left_items = VGroup(
            Text("What models know", font_size=24, color=WHITE),
            Text("Reasoning ability", font_size=24, color=WHITE),
            Text("Knowledge recall", font_size=24, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(left_title, DOWN, buff=0.5)

        right_title = Text("AttentionBench", font_size=30, color=YELLOW).shift(RIGHT * 3 + UP * 2)
        right_items = VGroup(
            Text("How models attend", font_size=24, color=YELLOW),
            Text("Focus under load", font_size=24, color=YELLOW),
            Text("Sustained performance", font_size=24, color=YELLOW),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(right_title, DOWN, buff=0.5)

        divider = Line(UP * 2, DOWN * 1.5, color=GREY_D)

        self.play(FadeIn(left_title), FadeIn(divider), run_time=0.5)
        for item in left_items:
            self.play(FadeIn(item, shift=RIGHT * 0.3), run_time=0.3)
        self.wait(1)
        self.play(FadeIn(right_title), run_time=0.5)
        for item in right_items:
            self.play(FadeIn(item, shift=LEFT * 0.3), run_time=0.3)
        self.wait(2)
        self.play(FadeOut(VGroup(left_title, left_items, right_title, right_items, divider)), run_time=0.5)

    def s04_intro(self):
        logo = Text("AttentionBench", font_size=56, color=WHITE)
        subtitle = Text(
            "Measuring Attention in Frontier LLMs",
            font_size=28, color=GREY_B
        ).next_to(logo, DOWN, buff=0.4)
        badge = Text(
            "Google DeepMind x Kaggle AGI Hackathon",
            font_size=20, color=GREY
        ).next_to(subtitle, DOWN, buff=0.8)

        self.play(Write(logo), run_time=1)
        self.play(FadeIn(subtitle, shift=UP * 0.3), run_time=0.5)
        self.play(FadeIn(badge), run_time=0.5)
        self.wait(2)
        self.play(FadeOut(VGroup(logo, subtitle, badge)), run_time=0.5)

    def s05_four_types(self):
        title = Text("Four Types of Attention", font_size=40, color=WHITE).shift(UP * 2.5)

        types = [
            ("Selective", SELECTIVE_COLOR, "Filter signal from noise"),
            ("Sustained", SUSTAINED_COLOR, "Maintain focus over time"),
            ("Divided", DIVIDED_COLOR, "Handle concurrent demands"),
            ("Change Detection", CHANGE_COLOR, "Notice what changed"),
        ]

        cards = VGroup()
        for name, color, desc in types:
            card = VGroup(
                RoundedRectangle(
                    corner_radius=0.15, width=2.8, height=1.6,
                    stroke_color=color, fill_color=color, fill_opacity=0.1,
                    stroke_width=2,
                ),
                Text(name, font_size=24, color=color).shift(UP * 0.2),
                Text(desc, font_size=14, color=GREY_B).shift(DOWN * 0.3),
            )
            cards.add(card)
        cards.arrange(RIGHT, buff=0.3)

        self.play(Write(title), run_time=0.8)
        for card in cards:
            self.play(FadeIn(card, shift=UP * 0.3), run_time=0.5)
        self.wait(3)
        self.play(FadeOut(VGroup(title, cards)), run_time=0.5)

    def s06_selective(self):
        title = Text("Selective Attention", font_size=44, color=SELECTIVE_COLOR)
        subtitle = Text("Can the model filter signal from noise?", font_size=26, color=GREY_B)
        subtitle.next_to(title, DOWN, buff=0.4)
        self.play(Write(title), FadeIn(subtitle), run_time=1)
        self.wait(1.5)
        self.play(FadeOut(VGroup(title, subtitle)), run_time=0.5)

    def s07_selective_demo(self):
        signal_box = RoundedRectangle(
            width=1.5, height=0.8, corner_radius=0.1,
            fill_color=SELECTIVE_COLOR, fill_opacity=0.8, stroke_width=0,
        )
        signal_label = Text("Signal", font_size=18, color=WHITE).move_to(signal_box)
        signal = VGroup(signal_box, signal_label)

        ratios = ["1:1", "5:1", "10:1", "25:1", "50:1", "100:1"]
        title = Text("Noise Filtering", font_size=32, color=SELECTIVE_COLOR).shift(UP * 2.5)
        self.play(Write(title), run_time=0.5)

        prev_blocks = None
        prev_label = None
        for i, ratio in enumerate(ratios):
            noise_count = [1, 5, 10, 12, 15, 18][i]
            noise_blocks = VGroup()
            for _ in range(min(noise_count, 18)):
                block = RoundedRectangle(
                    width=0.4 + np.random.random() * 0.3,
                    height=0.3 + np.random.random() * 0.2,
                    corner_radius=0.05,
                    fill_color=GREY_D, fill_opacity=0.4, stroke_width=0,
                )
                noise_blocks.add(block)

            all_blocks = VGroup(*noise_blocks, signal.copy())
            all_blocks.arrange_in_grid(
                rows=max(2, noise_count // 4 + 1), buff=0.15
            ).scale(0.7).move_to(ORIGIN)

            ratio_label = Text(f"Noise ratio: {ratio}", font_size=24, color=WHITE).shift(DOWN * 2.5)

            if i == 0:
                self.play(FadeIn(all_blocks), FadeIn(ratio_label), run_time=0.8)
            else:
                self.play(
                    Transform(prev_blocks, all_blocks),
                    Transform(prev_label, ratio_label),
                    run_time=0.6,
                )
            prev_blocks = all_blocks
            prev_label = ratio_label
            self.wait(0.5)

        self.wait(1)
        self.play(FadeOut(VGroup(title, prev_blocks, prev_label)), run_time=0.5)

    def s08_sustained(self):
        title = Text("Sustained Attention", font_size=44, color=SUSTAINED_COLOR)
        subtitle = Text("Can the model maintain focus over time?", font_size=26, color=GREY_B)
        subtitle.next_to(title, DOWN, buff=0.4)
        self.play(Write(title), FadeIn(subtitle), run_time=1)
        self.wait(1.5)
        self.play(FadeOut(VGroup(title, subtitle)), run_time=0.5)

    def s09_sustained_demo(self):
        title = Text("Vigilance Decrement", font_size=32, color=SUSTAINED_COLOR).shift(UP * 2.5)

        axes, ax_labels = make_axes_with_text_labels(
            x_range=[0, 100, 20], y_range=[0.5, 1.05, 0.1],
            x_length=8, y_length=4,
            x_labels=[0, 20, 40, 60, 80, 100],
            y_labels=[0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
        )
        axes_group = VGroup(axes, ax_labels).shift(DOWN * 0.3)

        x_label = Text("Position in Sequence", font_size=18, color=GREY).next_to(axes_group, DOWN, buff=0.3)
        y_label = Text("Accuracy", font_size=18, color=GREY).next_to(axes_group, LEFT, buff=0.3).rotate(PI / 2)

        def decay_func(x):
            return 0.98 - 0.25 * (1 / (1 + np.exp(-0.05 * (x - 60))))

        curve = axes.plot(decay_func, x_range=[1, 100], color=SUSTAINED_COLOR, stroke_width=3)

        threshold_y = 0.95
        threshold_line = DashedLine(
            axes.c2p(0, threshold_y), axes.c2p(100, threshold_y),
            color=YELLOW, stroke_width=1.5
        )
        threshold_label = Text("95% threshold", font_size=16, color=YELLOW).next_to(
            axes.c2p(100, threshold_y), RIGHT, buff=0.2
        )

        self.play(Write(title), run_time=0.5)
        self.play(Create(axes), FadeIn(ax_labels), FadeIn(x_label), FadeIn(y_label), run_time=1)
        self.play(Create(curve), run_time=2)
        self.play(Create(threshold_line), FadeIn(threshold_label), run_time=0.5)
        self.wait(2)
        self.play(FadeOut(VGroup(title, axes_group, x_label, y_label, curve, threshold_line, threshold_label)), run_time=0.5)

    def s10_divided(self):
        title = Text("Divided Attention", font_size=44, color=DIVIDED_COLOR)
        subtitle = Text("Can the model handle concurrent demands?", font_size=26, color=GREY_B)
        subtitle.next_to(title, DOWN, buff=0.4)
        self.play(Write(title), FadeIn(subtitle), run_time=1)
        self.wait(1.5)
        self.play(FadeOut(VGroup(title, subtitle)), run_time=0.5)

    def s11_divided_demo(self):
        title = Text("Attentional Blink", font_size=32, color=DIVIDED_COLOR).shift(UP * 2.5)

        axes, ax_labels = make_axes_with_text_labels(
            x_range=[0, 9, 1], y_range=[0, 1.05, 0.2],
            x_length=8, y_length=4,
            x_labels=list(range(1, 9)),
            y_labels=[0.0, 0.2, 0.4, 0.6, 0.8, 1.0],
        )
        axes_group = VGroup(axes, ax_labels).shift(DOWN * 0.3)

        x_label = Text("Lag (items between T1 and T2)", font_size=18, color=GREY).next_to(axes_group, DOWN, buff=0.3)
        y_label = Text("T2 Accuracy", font_size=18, color=GREY).next_to(axes_group, LEFT, buff=0.3).rotate(PI / 2)

        lag_data = {1: 0.85, 2: 0.55, 3: 0.45, 4: 0.50, 5: 0.65, 6: 0.78, 7: 0.85, 8: 0.88}
        points = [axes.c2p(lag, acc) for lag, acc in lag_data.items()]
        dots = VGroup(*[Dot(p, color=DIVIDED_COLOR, radius=0.08) for p in points])
        line = VMobject(color=DIVIDED_COLOR, stroke_width=3)
        line.set_points_smoothly(points)

        # Blink region shading — simple rectangle instead of axes.get_area
        blink_rect = Rectangle(
            width=axes.c2p(5.5, 0)[0] - axes.c2p(1.5, 0)[0],
            height=axes.c2p(0, 1.0)[1] - axes.c2p(0, 0)[1],
            fill_color=RED, fill_opacity=0.1, stroke_width=0,
        ).move_to(axes.c2p(3.5, 0.5))
        blink_label = Text("Blink window", font_size=16, color=RED_C).move_to(axes.c2p(3.5, 0.15))

        self.play(Write(title), run_time=0.5)
        self.play(Create(axes), FadeIn(ax_labels), FadeIn(x_label), FadeIn(y_label), run_time=1)
        self.play(FadeIn(blink_rect), FadeIn(blink_label), run_time=0.5)
        self.play(Create(line), run_time=1.5)
        self.play(FadeIn(dots), run_time=0.5)
        self.wait(2)
        self.play(FadeOut(VGroup(title, axes_group, x_label, y_label, dots, line, blink_rect, blink_label)), run_time=0.5)

    def s12_change(self):
        title = Text("Change Detection", font_size=44, color=CHANGE_COLOR)
        subtitle = Text("Can the model notice what changed?", font_size=26, color=GREY_B)
        subtitle.next_to(title, DOWN, buff=0.4)
        self.play(Write(title), FadeIn(subtitle), run_time=1)
        self.wait(1.5)
        self.play(FadeOut(VGroup(title, subtitle)), run_time=0.5)

    def s13_change_demo(self):
        title = Text("Change Blindness", font_size=32, color=CHANGE_COLOR).shift(UP * 2.8)

        va = RoundedRectangle(
            width=2.5, height=1.5, corner_radius=0.1,
            stroke_color=CHANGE_COLOR, fill_color=CHANGE_COLOR, fill_opacity=0.1,
        ).shift(LEFT * 3.5)
        va_label = Text("Version A", font_size=20, color=CHANGE_COLOR).next_to(va, UP, buff=0.2)
        va_text = Text("...847 megawatts...", font_size=14, color=WHITE).move_to(va)

        disruptor = RoundedRectangle(
            width=2.5, height=1.5, corner_radius=0.1,
            stroke_color=GREY_D, fill_color=GREY_D, fill_opacity=0.2,
        )
        dis_label = Text("Disruptor", font_size=20, color=GREY).next_to(disruptor, UP, buff=0.2)
        dis_text = Text("(unrelated content)", font_size=14, color=GREY_C).move_to(disruptor)

        vb = RoundedRectangle(
            width=2.5, height=1.5, corner_radius=0.1,
            stroke_color=CHANGE_COLOR, fill_color=CHANGE_COLOR, fill_opacity=0.1,
        ).shift(RIGHT * 3.5)
        vb_label = Text("Version B", font_size=20, color=CHANGE_COLOR).next_to(vb, UP, buff=0.2)
        vb_text = Text("...634 megawatts...", font_size=14, color=RED_C).move_to(vb)

        arrows = VGroup(
            Arrow(va.get_right(), disruptor.get_left(), buff=0.2, color=GREY_C),
            Arrow(disruptor.get_right(), vb.get_left(), buff=0.2, color=GREY_C),
        )

        question = Text(
            "What changed?", font_size=24, color=YELLOW
        ).shift(DOWN * 2)

        self.play(Write(title), run_time=0.5)
        self.play(FadeIn(va), FadeIn(va_label), FadeIn(va_text), run_time=0.5)
        self.play(GrowArrow(arrows[0]), run_time=0.3)
        self.play(FadeIn(disruptor), FadeIn(dis_label), FadeIn(dis_text), run_time=0.5)
        self.play(GrowArrow(arrows[1]), run_time=0.3)
        self.play(FadeIn(vb), FadeIn(vb_label), FadeIn(vb_text), run_time=0.5)
        self.play(Write(question), run_time=0.5)
        self.wait(2)

        all_objs = VGroup(
            title, va, va_label, va_text, disruptor, dis_label, dis_text,
            vb, vb_label, vb_text, arrows, question
        )
        self.play(FadeOut(all_objs), run_time=0.5)

    def s14_key_insight(self):
        title = Text("The Key Insight", font_size=40, color=YELLOW).shift(UP * 2)

        left = VGroup(
            Text("Task Difficulty", font_size=24, color=WHITE),
            Text("CONSTANT", font_size=32, color=GREEN, weight=BOLD),
        ).arrange(DOWN, buff=0.3).shift(LEFT * 3)

        right = VGroup(
            Text("Attentional Load", font_size=24, color=WHITE),
            Text("VARIES", font_size=32, color=RED, weight=BOLD),
        ).arrange(DOWN, buff=0.3).shift(RIGHT * 3)

        arrow = Arrow(LEFT * 0.5, RIGHT * 0.5, color=YELLOW, buff=0)

        result = Text(
            "Any drop = attention failure, not reasoning failure",
            font_size=22, color=GREY_B,
        ).shift(DOWN * 1.5)

        self.play(Write(title), run_time=0.8)
        self.play(FadeIn(left), FadeIn(right), GrowArrow(arrow), run_time=1)
        self.wait(1)
        self.play(FadeIn(result, shift=UP * 0.3), run_time=0.8)
        self.wait(2)
        self.play(FadeOut(VGroup(title, left, right, arrow, result)), run_time=0.5)

    def s15_conclusion(self):
        stats = VGroup(
            Text("8 Tasks", font_size=36, color=WHITE),
            Text("4 Attention Types", font_size=36, color=WHITE),
        ).arrange(DOWN, buff=0.5).shift(UP * 0.5)

        question = Text(
            "Can your model focus on what matters?",
            font_size=30, color=YELLOW,
        ).shift(DOWN * 1.5)

        logo = Text("AttentionBench", font_size=52, color=WHITE).shift(UP * 2.5)

        self.play(Write(logo), run_time=1)
        for stat in stats:
            self.play(FadeIn(stat, shift=RIGHT * 0.3), run_time=0.5)
        self.wait(1)
        self.play(Write(question), run_time=1)
        self.wait(3)
        self.play(FadeOut(VGroup(logo, stats, question)), run_time=1)
