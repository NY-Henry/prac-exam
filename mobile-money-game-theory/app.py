"""Simple desktop UI for the MTN MoMo vs. Airtel Money game theory project."""

import tkinter as tk
from tkinter import ttk

from game import ACTIONS, PRESETS, Analysis, analyze, parse_payoff

BG = "#f7f7f5"
WHITE = "#ffffff"
TEXT = "#1f2937"
BEST_COLOR = "#dcfce7"
NASH_BORDER = "#f59e0b"
BORDER_IDLE = "#cbd5e1"
ERR_COLOR = "#fee2e2"


class MobileMoneyApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        root.title("MTN vs Airtel - Mobile Money Game Theory")
        root.geometry("740x680")
        root.minsize(640, 580)
        root.configure(bg=BG)

        self.actions = ACTIONS
        self.players = ("MTN", "Airtel")
        self.row_labels = []
        self.col_labels = []
        self.cells = {}
        self.entries = {}
        self.vars = {}
        self.loading = False

        main = tk.Frame(root, bg=BG, padx=18, pady=14)
        main.pack(fill="both", expand=True)

        tk.Label(main, text="MTN MoMo vs. Airtel Money (2x2 Game)", bg=BG, fg=TEXT,
                 font=("Segoe UI", 16, "bold")).pack(anchor="w")
        tk.Label(main, text="Enter payoffs for both companies, then click Analyze.",
                 bg=BG, fg="#4b5563", font=("Segoe UI", 10)).pack(anchor="w", pady=(2, 10))

        top_bar = tk.Frame(main, bg=BG)
        top_bar.pack(fill="x", pady=(0, 10))
        tk.Label(top_bar, text="Scenario:", bg=BG, fg=TEXT, font=("Segoe UI", 10, "bold")).pack(side="left")
        self.preset = ttk.Combobox(top_bar, values=tuple(PRESETS), state="readonly", width=34)
        self.preset.current(0)
        self.preset.pack(side="left", padx=8)
        self.preset.bind("<<ComboboxSelected>>", self.load_preset)

        tk.Button(top_bar, text="Reset", command=self.load_preset, padx=10, pady=4).pack(side="left")
        tk.Button(top_bar, text="Analyze", command=self.run_analysis, bg="#1d4ed8", fg=WHITE,
                  font=("Segoe UI", 10, "bold"), padx=14, pady=4, relief="flat").pack(side="right")

        matrix_box = tk.LabelFrame(main, text=" Payoff Matrix ", bg=WHITE, fg=TEXT,
                                   font=("Segoe UI", 10, "bold"), padx=14, pady=10)
        matrix_box.pack(fill="x", pady=(0, 10))

        grid = tk.Frame(matrix_box, bg=WHITE)
        grid.pack(fill="x")
        grid.columnconfigure(1, weight=1)
        grid.columnconfigure(2, weight=1)

        tk.Label(grid, text="MTN \\ Airtel", bg=WHITE, fg="#6b7280",
                 font=("Segoe UI", 9, "bold")).grid(row=0, column=0, padx=(0, 8), pady=(0, 6))

        for i in range(2):
            r_lbl = tk.Label(grid, bg=WHITE, fg="#92400e", font=("Segoe UI", 10, "bold"))
            c_lbl = tk.Label(grid, bg=WHITE, fg="#991b1b", font=("Segoe UI", 10, "bold"))
            r_lbl.grid(row=i + 1, column=0, sticky="w", padx=(0, 8))
            c_lbl.grid(row=0, column=i + 1, pady=(0, 6))
            self.row_labels.append(r_lbl)
            self.col_labels.append(c_lbl)

        for r in range(2):
            for c in range(2):
                frame = tk.Frame(grid, bg=BORDER_IDLE, padx=3, pady=3)
                frame.grid(row=r + 1, column=c + 1, sticky="ew", padx=4, pady=4)
                self.cells[r, c] = frame
                for p, color in enumerate(("#92400e", "#991b1b")):
                    frame.columnconfigure(p, weight=1)
                    lbl_txt = "MTN" if p == 0 else "Airtel"
                    tk.Label(frame, text=lbl_txt, bg=WHITE, fg=color,
                             font=("Segoe UI", 8, "bold")).grid(row=0, column=p, sticky="ew")
                    var = tk.StringVar(root)
                    box = tk.Entry(frame, textvariable=var, width=8, justify="center",
                                   font=("Segoe UI", 11), relief="flat", bg=WHITE)
                    box.grid(row=1, column=p, sticky="ew", padx=1, ipady=5)
                    self.entries[r, c, p] = box
                    self.vars[r, c, p] = var

        info_row = tk.Frame(matrix_box, bg=WHITE)
        info_row.pack(fill="x", pady=(8, 0))
        tk.Label(info_row, text="Green = Best response   |   Orange border = Pure Nash equilibrium",
                 bg=WHITE, fg="#4b5563", font=("Segoe UI", 9)).pack(side="left")
        self.status = tk.Label(info_row, text="", bg=WHITE, fg=TEXT, font=("Segoe UI", 9, "bold"))
        self.status.pack(side="right")

        result_box = tk.LabelFrame(main, text=" Analysis Results ", bg=WHITE, fg=TEXT,
                                   font=("Segoe UI", 10, "bold"), padx=12, pady=8)
        result_box.pack(fill="both", expand=True)

        scroll = tk.Scrollbar(result_box)
        scroll.pack(side="right", fill="y")
        self.output = tk.Text(result_box, wrap="word", relief="flat", bg=WHITE, fg=TEXT,
                              font=("Segoe UI", 10), yscrollcommand=scroll.set)
        self.output.pack(side="left", fill="both", expand=True)
        scroll.configure(command=self.output.yview)
        self.output.tag_configure("title", font=("Segoe UI", 10, "bold"), foreground="#1d4ed8")

        root.bind("<Return>", lambda _e: self.run_analysis())
        self.load_preset()
        for var in self.vars.values():
            var.trace_add("write", self.on_edit)

    def load_preset(self, _event=None):
        is_pennies = self.preset.current() == 2
        self.actions = ("Heads", "Tails") if is_pennies else ACTIONS
        self.players = ("Player A", "Player B") if is_pennies else ("MTN", "Airtel")
        for i, name in enumerate(self.actions):
            self.row_labels[i].configure(text=f"{self.players[0]}: {name}")
            self.col_labels[i].configure(text=f"{self.players[1]}: {name}")

        self.loading = True
        for i, pair in enumerate(PRESETS[self.preset.get()]):
            r, c = divmod(i, 2)
            self.vars[r, c, 0].set(str(pair[0]))
            self.vars[r, c, 1].set(str(pair[1]))
        self.loading = False
        self.run_analysis()

    def clear_marks(self):
        for cell in self.cells.values():
            cell.configure(bg=BORDER_IDLE)
        for entry in self.entries.values():
            entry.configure(bg=WHITE)

    def on_edit(self, *_args):
        if self.loading:
            return
        self.clear_marks()
        self.status.configure(text="Edited - click Analyze", fg="#6b7280")

    def write_output(self, sections):
        self.output.configure(state="normal")
        self.output.delete("1.0", "end")
        for heading, body in sections:
            self.output.insert("end", f"{heading}\n", "title")
            self.output.insert("end", f"{body}\n\n")
        self.output.configure(state="disabled")

    def run_analysis(self):
        self.clear_marks()
        vals = {}
        for (r, c, p), entry in self.entries.items():
            try:
                vals[r, c, p] = parse_payoff(entry.get())
            except ValueError as err:
                entry.configure(bg=ERR_COLOR)
                entry.focus_set()
                self.status.configure(text=f"Invalid value at ({r + 1}, {c + 1})", fg="#b91c1c")
                self.write_output([("Input Error", str(err))])
                return

        matrix = tuple(tuple((vals[r, c, 0], vals[r, c, 1]) for c in range(2)) for r in range(2))
        res = analyze(matrix)

        for r in range(2):
            for c in range(2):
                if r in res.a_best[c]:
                    self.entries[r, c, 0].configure(bg=BEST_COLOR)
                if c in res.b_best[r]:
                    self.entries[r, c, 1].configure(bg=BEST_COLOR)
        for prof in res.pure:
            self.cells[prof].configure(bg=NASH_BORDER)

        self.display_results(res, matrix)
        self.status.configure(text=f"Pure Nash: {len(res.pure)} | Mixed: {len(res.mixed)}", fg="#065f46")

    def display_results(self, res: Analysis, matrix):
        names = self.actions
        p1, p2 = self.players

        pure = [f"({names[r]}, {names[c]}) -> ({matrix[r][c][0]}, {matrix[r][c][1]})" for r, c in res.pure]
        mixed = [f"p = {p}, q = {q}" for p, q in res.mixed]
        if mixed:
            mixed.insert(0, f"p = prob({p1} plays {names[0]}), q = prob({p2} plays {names[0]})")

        dom = []
        for who, found in ((p1, res.a_dominance), (p2, res.b_dominance)):
            if found:
                act, kind = found[0]
                dom.append(f"{who}: {names[act]} is {kind}ly dominant ({names[1 - act]} is dominated).")
            else:
                dom.append(f"{who}: no dominant strategy.")

        br = []
        for i, opp in enumerate(names):
            a_br = " or ".join(names[x] for x in res.a_best[i])
            b_br = " or ".join(names[x] for x in res.b_best[i])
            br.append(f"If {p2} plays {opp} -> {p1} chooses {a_br}")
            br.append(f"If {p1} plays {opp} -> {p2} chooses {b_br}")

        self.write_output([
            ("Pure Nash Equilibrium", "\n".join(pure) or "None"),
            ("Mixed Nash Equilibrium", "\n".join(mixed) or "None"),
            ("Dominant Strategies", "\n".join(dom)),
            ("Best Responses", "\n".join(br)),
        ])


def main():
    root = tk.Tk()
    MobileMoneyApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
