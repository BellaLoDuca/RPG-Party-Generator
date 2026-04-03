import random
import tkinter as tk

try:
    import winsound
except ImportError:
    winsound = None

from engine import generate_candidates, score_party, get_party_rank


PARTY_SLOTS = [
    ("Leader", "Leader"),
    ("Fighter", "Fighter 1"),
    ("Fighter", "Fighter 2"),
    ("Support", "Support 1"),
    ("Support", "Support 2"),
]

ROLE_ICONS = {
    "Leader": "👑",
    "Fighter": "⚔",
    "Support": "✦",
}

SLOT_ICON_COLORS = {
    "Leader": "#f4d35e",
    "Fighter": "#e76f51",
    "Support": "#7bdff2",
}

STAT_LABELS = {
    "strength": "STR",
    "dexterity": "DEX",
    "constitution": "CON",
    "intelligence": "INT",
    "wisdom": "WIS",
    "charisma": "CHA",
}


class PartyGeneratorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Fantasy RPG Party Generator")
        self.root.geometry("1360x820")
        self.root.minsize(1200, 760)
        self.root.configure(bg="#120f1f")

        self.party = []
        self.current_index = 0
        self.current_candidates = []
        self.sparkles = []
        self.card_frames = []

        self.bg_canvas = tk.Canvas(
            self.root,
            bg="#120f1f",
            highlightthickness=0,
            bd=0
        )
        self.bg_canvas.place(relwidth=1, relheight=1)

        self.main_container = tk.Frame(self.root, bg="#120f1f")
        self.main_container.place(relwidth=1, relheight=1)

        self.sidebar = tk.Frame(
            self.main_container,
            bg="#181428",
            width=260,
            highlightthickness=1,
            highlightbackground="#3b3158"
        )
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        self.content_wrapper = tk.Frame(self.main_container, bg="#120f1f")
        self.content_wrapper.pack(side="left", fill="both", expand=True)

        self.header_frame = tk.Frame(self.content_wrapper, bg="#120f1f")
        self.header_frame.pack(fill="x", pady=(20, 10))

        self.title_label = tk.Label(
            self.header_frame,
            text="RPG Party Generator",
            font=("Georgia", 30, "bold"),
            bg="#120f1f",
            fg="#f8f3e7"
        )
        self.title_label.pack()

        self.subtitle_label = tk.Label(
            self.header_frame,
            text="Forge a party worthy of legend",
            font=("Georgia", 13, "italic"),
            bg="#120f1f",
            fg="#b8add7"
        )
        self.subtitle_label.pack(pady=(4, 0))

        self.progress_label = tk.Label(
            self.content_wrapper,
            text="",
            font=("Segoe UI", 15),
            bg="#120f1f",
            fg="#d7cffa"
        )
        self.progress_label.pack(pady=(4, 22))

        self.content_frame = tk.Frame(self.content_wrapper, bg="#120f1f")
        self.content_frame.pack(fill="both", expand=True, padx=26, pady=(0, 24))

        self.root.bind("<Configure>", self.on_resize)

        self.build_sidebar()
        self.create_magic_background()
        self.start_screen()

    def play_hover_sound(self):
        if winsound:
            try:
                winsound.MessageBeep()
            except Exception:
                pass

    def play_select_sound(self):
        if winsound:
            try:
                winsound.Beep(740, 80)
                winsound.Beep(880, 90)
            except Exception:
                pass

    def play_finish_sound(self):
        if winsound:
            try:
                winsound.Beep(523, 90)
                winsound.Beep(659, 90)
                winsound.Beep(784, 140)
            except Exception:
                pass

    def create_magic_background(self):
        self.bg_canvas.delete("all")
        self.sparkles = []

        width = max(self.root.winfo_width(), 1200)
        height = max(self.root.winfo_height(), 760)

        self.bg_canvas.create_rectangle(
            0, 0, width, height,
            fill="#120f1f",
            outline=""
        )

        for _ in range(65):
            x = random.randint(0, width)
            y = random.randint(0, height)
            r = random.randint(1, 3)
            color = random.choice(["#f4d35e", "#7bdff2", "#d0bfff", "#ffffff", "#ffd6ff"])

            star = self.bg_canvas.create_oval(
                x - r, y - r, x + r, y + r,
                fill=color, outline=""
            )

            drift_x = random.choice([-1, 1]) * random.uniform(0.15, 0.5)
            drift_y = random.choice([-1, 1]) * random.uniform(0.15, 0.5)

            self.sparkles.append({
                "id": star,
                "dx": drift_x,
                "dy": drift_y,
                "r": r
            })

        self.bg_canvas.create_oval(
            width - 360, -80, width + 120, 350,
            fill="#2a1f47", outline=""
        )
        self.bg_canvas.create_oval(
            width - 310, -40, width + 70, 310,
            fill="#3b2d63", outline=""
        )

        self.animate_background()

    def animate_background(self):
        width = max(self.root.winfo_width(), 1200)
        height = max(self.root.winfo_height(), 760)

        for sparkle in self.sparkles:
            star_id = sparkle["id"]
            self.bg_canvas.move(star_id, sparkle["dx"], sparkle["dy"])
            x1, y1, x2, y2 = self.bg_canvas.coords(star_id)

            if x2 < 0:
                self.bg_canvas.move(star_id, width + 10, 0)
            elif x1 > width:
                self.bg_canvas.move(star_id, -width - 10, 0)

            if y2 < 0:
                self.bg_canvas.move(star_id, 0, height + 10)
            elif y1 > height:
                self.bg_canvas.move(star_id, 0, -height - 10)

        self.root.after(80, self.animate_background)

    def on_resize(self, event):
        if event.widget == self.root:
            self.create_magic_background()

    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        self.card_frames = []

    def build_sidebar(self):
        for widget in self.sidebar.winfo_children():
            widget.destroy()

        sidebar_title = tk.Label(
            self.sidebar,
            text="Current Party",
            font=("Georgia", 20, "bold"),
            bg="#181428",
            fg="#f8f3e7"
        )
        sidebar_title.pack(pady=(22, 6))

        sidebar_subtitle = tk.Label(
            self.sidebar,
            text="Chosen heroes",
            font=("Segoe UI", 11),
            bg="#181428",
            fg="#aa9ccf"
        )
        sidebar_subtitle.pack(pady=(0, 20))

        self.sidebar_slots_frame = tk.Frame(self.sidebar, bg="#181428")
        self.sidebar_slots_frame.pack(fill="x", padx=16)

        for role_name, slot_name in PARTY_SLOTS:
            self.create_sidebar_slot(role_name, slot_name)

        spacer = tk.Frame(self.sidebar, bg="#181428")
        spacer.pack(expand=True, fill="both")

        tip_frame = tk.Frame(
            self.sidebar,
            bg="#201936",
            highlightthickness=1,
            highlightbackground="#3b3158",
            padx=12,
            pady=12
        )
        tip_frame.pack(fill="x", padx=16, pady=(0, 20))

        tip_label = tk.Label(
            tip_frame,
            text="Tip: hover over cards and choose carefully — duplicate races and classes can hurt your final score.",
            font=("Segoe UI", 10),
            bg="#201936",
            fg="#d9d1f0",
            wraplength=200,
            justify="left"
        )
        tip_label.pack()

    def create_sidebar_slot(self, role_name, slot_name):
        container = tk.Frame(
            self.sidebar_slots_frame,
            bg="#211b35",
            highlightthickness=1,
            highlightbackground="#342b4b",
            padx=10,
            pady=10
        )
        container.pack(fill="x", pady=7)

        top_row = tk.Frame(container, bg="#211b35")
        top_row.pack(fill="x")

        icon_label = tk.Label(
            top_row,
            text=ROLE_ICONS[role_name],
            font=("Segoe UI Emoji", 20),
            bg="#211b35",
            fg=SLOT_ICON_COLORS[role_name],
            width=2
        )
        icon_label.pack(side="left")

        text_frame = tk.Frame(top_row, bg="#211b35")
        text_frame.pack(side="left", fill="x", expand=True)

        slot_label = tk.Label(
            text_frame,
            text=slot_name,
            font=("Segoe UI", 11, "bold"),
            bg="#211b35",
            fg="#f4efff",
            anchor="w"
        )
        slot_label.pack(fill="x")

        role_label = tk.Label(
            text_frame,
            text=role_name,
            font=("Segoe UI", 9),
            bg="#211b35",
            fg="#ab9ccc",
            anchor="w"
        )
        role_label.pack(fill="x")

        chosen_label = tk.Label(
            container,
            text="Not selected yet",
            font=("Segoe UI", 10),
            bg="#211b35",
            fg="#7e749d",
            anchor="w",
            justify="left",
            wraplength=180
        )
        chosen_label.pack(fill="x", pady=(8, 0))

        container.slot_name = slot_name
        container.chosen_label = chosen_label

    def refresh_sidebar(self):
        slot_to_member = {member["slot"]: member for member in self.party}

        for container in self.sidebar_slots_frame.winfo_children():
            slot_name = container.slot_name
            if slot_name in slot_to_member:
                member = slot_to_member[slot_name]
                role_name = member["role"]
                container.chosen_label.config(
                    text=f"{ROLE_ICONS[role_name]} {member['race'].title()} {member['class']}",
                    fg="#f8f3e7"
                )
            else:
                container.chosen_label.config(
                    text="Not selected yet",
                    fg="#7e749d"
                )

    def bind_hover_effect(self, widget, enter_fn, leave_fn):
        widget.bind("<Enter>", enter_fn)
        widget.bind("<Leave>", leave_fn)

    def start_screen(self):
        self.clear_content()
        self.refresh_sidebar()

        intro_outer = tk.Frame(self.content_frame, bg="#120f1f")
        intro_outer.pack(expand=True)

        intro_card = tk.Frame(
            intro_outer,
            bg="#1d1730",
            highlightthickness=2,
            highlightbackground="#4f3b79",
            padx=36,
            pady=36
        )
        intro_card.pack()

        crest = tk.Label(
            intro_card,
            text="✦  ⚔  👑  ✦",
            font=("Segoe UI Emoji", 26),
            bg="#1d1730",
            fg="#f4d35e"
        )
        crest.pack(pady=(0, 16))

        intro_label = tk.Label(
            intro_card,
            text="Build your party one role at a time.\nChoose from three contenders for each slot,\nand uncover your final party rank at the end.",
            font=("Georgia", 15),
            bg="#1d1730",
            fg="#f8f3e7",
            justify="center"
        )
        intro_label.pack(pady=(0, 24))

        start_button = tk.Button(
            intro_card,
            text="Begin the Summoning",
            font=("Segoe UI", 14, "bold"),
            bg="#6d4aff",
            fg="white",
            activebackground="#8566ff",
            activeforeground="white",
            relief="flat",
            padx=24,
            pady=12,
            cursor="hand2",
            command=self.begin_selection
        )
        start_button.pack()

        self.bind_button_glow(start_button, "#6d4aff", "#8566ff")

        self.progress_label.config(text="")

    def begin_selection(self):
        self.party = []
        self.current_index = 0
        self.refresh_sidebar()
        self.load_next_role()

    def load_next_role(self):
        if self.current_index >= len(PARTY_SLOTS):
            self.show_final_results()
            return

        role_name, slot_name = PARTY_SLOTS[self.current_index]
        self.current_candidates = generate_candidates(role_name, 3)

        self.progress_label.config(
            text=f"Step {self.current_index + 1} of {len(PARTY_SLOTS)} — Choose your {slot_name}"
        )

        self.show_candidates(role_name, slot_name, self.current_candidates)

    def show_candidates(self, role_name, slot_name, candidates):
        self.clear_content()
        self.refresh_sidebar()

        heading = tk.Label(
            self.content_frame,
            text=f"{ROLE_ICONS[role_name]}  {slot_name} Candidates",
            font=("Georgia", 24, "bold"),
            bg="#120f1f",
            fg="#f8f3e7"
        )
        heading.pack(pady=(0, 20))

        top_controls = tk.Frame(self.content_frame, bg="#120f1f")
        top_controls.pack(fill="x", pady=(0, 18))

        reroll_button = tk.Button(
            top_controls,
            text="Reroll Candidates",
            font=("Segoe UI", 11, "bold"),
            bg="#2c2344",
            fg="#f4efff",
            activebackground="#433160",
            activeforeground="white",
            relief="flat",
            padx=16,
            pady=8,
            cursor="hand2",
            command=self.load_next_role
        )
        reroll_button.pack()
        self.bind_button_glow(reroll_button, "#2c2344", "#433160")

        cards_frame = tk.Frame(self.content_frame, bg="#120f1f")
        cards_frame.pack(expand=True, fill="both")

        for i in range(3):
            cards_frame.grid_columnconfigure(i, weight=1)

        cards_frame.grid_rowconfigure(0, weight=1)

        for i, candidate in enumerate(candidates):
            self.create_candidate_card(cards_frame, i, candidate, slot_name)

    def create_candidate_card(self, parent, column_index, candidate, slot_name):
        outer = tk.Frame(
            parent,
            bg="#120f1f",
            padx=12,
            pady=12
        )
        outer.grid(row=0, column=column_index, sticky="nsew", padx=12, pady=10)

        card = tk.Frame(
            outer,
            bg="#221a34",
            width=305,
            height=470,
            highlightthickness=2,
            highlightbackground="#4b3d67",
            padx=18,
            pady=18
        )
        card.pack(expand=True)
        card.pack_propagate(False)

        self.card_frames.append(card)

        role_name = candidate["role"]

        icon_label = tk.Label(
            card,
            text=ROLE_ICONS[role_name],
            font=("Segoe UI Emoji", 28),
            bg="#221a34",
            fg=SLOT_ICON_COLORS[role_name]
        )
        icon_label.pack(pady=(0, 8))

        name_label = tk.Label(
            card,
            text=f"{candidate['race'].title()} {candidate['class']}",
            font=("Georgia", 18, "bold"),
            bg="#221a34",
            fg="#f8f3e7",
            wraplength=240,
            justify="center"
        )
        name_label.pack(pady=(0, 8))

        role_label = tk.Label(
            card,
            text=f"Role: {candidate['role']}",
            font=("Segoe UI", 11),
            bg="#221a34",
            fg="#c2b7e6"
        )
        role_label.pack(pady=(0, 12))

        divider = tk.Frame(card, bg="#4f3b79", height=2)
        divider.pack(fill="x", pady=(0, 14))

        stats_title = tk.Label(
            card,
            text="Stats",
            font=("Georgia", 15, "bold"),
            bg="#221a34",
            fg="#f4d35e"
        )
        stats_title.pack(pady=(0, 10))

        stats_box = tk.Frame(card, bg="#1a1428")
        stats_box.pack(fill="x", pady=(0, 10))

        for stat, value in candidate["stats"].items():
            row = tk.Frame(stats_box, bg="#1a1428")
            row.pack(fill="x", padx=10, pady=4)

            stat_name = tk.Label(
                row,
                text=STAT_LABELS.get(stat, stat.upper()),
                font=("Consolas", 11, "bold"),
                bg="#1a1428",
                fg="#bbaedf",
                anchor="w",
                width=5
            )
            stat_name.pack(side="left")

            stat_value = tk.Label(
                row,
                text=str(value),
                font=("Consolas", 11),
                bg="#1a1428",
                fg="#f8f3e7",
                anchor="e"
            )
            stat_value.pack(side="right")

        spacer = tk.Frame(card, bg="#221a34")
        spacer.pack(expand=True, fill="both")

        select_button = tk.Button(
            card,
            text="Select Hero",
            font=("Segoe UI", 12, "bold"),
            bg="#6d4aff",
            fg="white",
            activebackground="#8566ff",
            activeforeground="white",
            relief="flat",
            padx=18,
            pady=10,
            cursor="hand2",
            command=lambda c=candidate, s=slot_name: self.select_candidate(c, s)
        )
        select_button.pack(fill="x", pady=(8, 0))

        self.bind_button_glow(select_button, "#6d4aff", "#8566ff")
        self.bind_card_glow(card)

    def select_candidate(self, candidate, slot_name):
        self.play_select_sound()
        selected = candidate.copy()
        selected["slot"] = slot_name
        self.party.append(selected)
        self.refresh_sidebar()
        self.current_index += 1
        self.load_next_role()

    def show_final_results(self):
        self.clear_content()
        self.refresh_sidebar()
        self.play_finish_sound()

        total_party_score = score_party(self.party)
        party_rank = get_party_rank(total_party_score)

        self.progress_label.config(text="Your party has been forged")

        heading = tk.Label(
            self.content_frame,
            text="✦ Final Party ✦",
            font=("Georgia", 28, "bold"),
            bg="#120f1f",
            fg="#f8f3e7"
        )
        heading.pack(pady=(0, 22))

        results_card = tk.Frame(
            self.content_frame,
            bg="#1d1730",
            highlightthickness=2,
            highlightbackground="#4f3b79",
            padx=24,
            pady=24
        )
        results_card.pack(pady=8)

        for member in self.party:
            row = tk.Frame(results_card, bg="#1d1730")
            row.pack(fill="x", pady=8)

            slot_color = SLOT_ICON_COLORS.get(member["role"], "#f8f3e7")

            icon = tk.Label(
                row,
                text=ROLE_ICONS[member["role"]],
                font=("Segoe UI Emoji", 18),
                bg="#1d1730",
                fg=slot_color,
                width=3
            )
            icon.pack(side="left")

            slot_label = tk.Label(
                row,
                text=member["slot"],
                font=("Segoe UI", 12, "bold"),
                bg="#1d1730",
                fg="#f4d35e",
                width=12,
                anchor="w"
            )
            slot_label.pack(side="left")

            info_label = tk.Label(
                row,
                text=f"{member['race'].title()} {member['class']}",
                font=("Georgia", 14),
                bg="#1d1730",
                fg="#f8f3e7",
                anchor="w"
            )
            info_label.pack(side="left")

        summary_frame = tk.Frame(self.content_frame, bg="#120f1f")
        summary_frame.pack(pady=26)

        score_label = tk.Label(
            summary_frame,
            text=f"Total Party Score: {total_party_score}",
            font=("Georgia", 18, "bold"),
            bg="#120f1f",
            fg="#f8f3e7"
        )
        score_label.pack(pady=4)

        rank_color = self.get_rank_color(party_rank)

        rank_label = tk.Label(
            summary_frame,
            text=f"Party Rank: {party_rank}",
            font=("Georgia", 24, "bold"),
            bg="#120f1f",
            fg=rank_color
        )
        rank_label.pack(pady=4)

        rank_flavor = tk.Label(
            summary_frame,
            text=self.get_rank_flavor_text(party_rank),
            font=("Segoe UI", 11, "italic"),
            bg="#120f1f",
            fg="#c8bde8"
        )
        rank_flavor.pack(pady=(4, 0))

        button_frame = tk.Frame(self.content_frame, bg="#120f1f")
        button_frame.pack(pady=18)

        restart_button = tk.Button(
            button_frame,
            text="Build Another Party",
            font=("Segoe UI", 12, "bold"),
            bg="#6d4aff",
            fg="white",
            activebackground="#8566ff",
            activeforeground="white",
            relief="flat",
            padx=18,
            pady=10,
            cursor="hand2",
            command=self.begin_selection
        )
        restart_button.grid(row=0, column=0, padx=10)

        quit_button = tk.Button(
            button_frame,
            text="Quit",
            font=("Segoe UI", 12, "bold"),
            bg="#8b2f4a",
            fg="white",
            activebackground="#a73f5c",
            activeforeground="white",
            relief="flat",
            padx=18,
            pady=10,
            cursor="hand2",
            command=self.root.quit
        )
        quit_button.grid(row=0, column=1, padx=10)

        self.bind_button_glow(restart_button, "#6d4aff", "#8566ff")
        self.bind_button_glow(quit_button, "#8b2f4a", "#a73f5c")

    def bind_button_glow(self, button, normal_bg, hover_bg):
        def on_enter(event):
            button.config(bg=hover_bg)
            self.play_hover_sound()

        def on_leave(event):
            button.config(bg=normal_bg)

        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)

    def bind_card_glow(self, card):
        def on_enter(event):
            card.config(bg="#2b2142", highlightbackground="#8c6cff")
            for child in card.winfo_children():
                self.set_child_bg(child, "#2b2142")
            self.play_hover_sound()

        def on_leave(event):
            card.config(bg="#221a34", highlightbackground="#4b3d67")
            for child in card.winfo_children():
                self.restore_card_colors(child)

        card.bind("<Enter>", on_enter)
        card.bind("<Leave>", on_leave)

        for child in card.winfo_children():
            child.bind("<Enter>", on_enter)
            child.bind("<Leave>", on_leave)

    def set_child_bg(self, widget, bg):
        widget_class = widget.winfo_class()

        if widget_class not in ("Button", "Canvas"):
            try:
                current_bg = widget.cget("bg")
                if current_bg != "#1a1428":
                    widget.config(bg=bg)
            except Exception:
                pass

        for child in widget.winfo_children():
            self.set_child_bg(child, bg)

    def restore_card_colors(self, widget):
        try:
            current_bg = widget.cget("bg")
        except Exception:
            current_bg = None

        if current_bg == "#2b2142":
            try:
                widget.config(bg="#221a34")
            except Exception:
                pass

        if current_bg == "#1a1428":
            return

        for child in widget.winfo_children():
            self.restore_card_colors(child)

    def get_rank_color(self, rank):
        if rank == "S Tier":
            return "#ffd166"
        if rank == "A Tier":
            return "#7bdff2"
        if rank == "B Tier":
            return "#8be28b"
        if rank == "C Tier":
            return "#f4a261"
        return "#d17a95"

    def get_rank_flavor_text(self, rank):
        if rank == "S Tier":
            return "A legendary band of heroes. Taverns will sing of this one."
        if rank == "A Tier":
            return "A powerful and balanced party with strong promise."
        if rank == "B Tier":
            return "Solid adventurers. Not flawless, but definitely capable."
        if rank == "C Tier":
            return "They may survive... assuming fate is feeling generous."
        return "A questionable fellowship. Brave, chaotic, and mildly doomed."


def main():
    root = tk.Tk()
    app = PartyGeneratorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()