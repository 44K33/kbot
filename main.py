import tkinter as tk
import threading
import time
from input_handler import InputHandler
from fsm import BotFSM


class BotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("kbot - Kostadin Kostadinov")
        self.root.geometry("400x500")
        self.root.resizable(False, False)

        self.bot_thread = None
        self.bot_running = False
        self.region = None
        self.bot = None

        self._build_ui()

    def _build_ui(self):
        # Region selection
        region_frame = tk.LabelFrame(self.root, text="Game Region", padx=10, pady=10)
        region_frame.pack(fill="x", padx=15, pady=10)

        self.region_label = tk.Label(region_frame, text="No region selected", fg="red")
        self.region_label.pack()

        select_btn = tk.Button(region_frame, text="Select Region", command=self._select_region)
        select_btn.pack(pady=5)

        # Bot controls
        control_frame = tk.LabelFrame(self.root, text="Controls", padx=10, pady=10)
        control_frame.pack(fill="x", padx=15, pady=10)

        self.start_btn = tk.Button(control_frame, text="Start", bg="green", fg="white",
                                   width=15, command=self._start_bot, state="disabled")
        self.start_btn.pack(side="left", padx=5)

        self.stop_btn = tk.Button(control_frame, text="Stop", bg="red", fg="white",
                                  width=15, command=self._stop_bot, state="disabled")
        self.stop_btn.pack(side="left", padx=5)

        # Current state
        state_frame = tk.LabelFrame(self.root, text="Current State", padx=10, pady=10)
        state_frame.pack(fill="x", padx=15, pady=10)

        self.state_label = tk.Label(state_frame, text="IDLE", font=("Arial", 12, "bold"), fg="gray")
        self.state_label.pack()

        # Log window
        log_frame = tk.LabelFrame(self.root, text="Log", padx=10, pady=10)
        log_frame.pack(fill="both", expand=True, padx=15, pady=10)

        self.log_box = tk.Text(log_frame, height=10, state="disabled", bg="#1e1e1e", fg="#00ff00",
                               font=("Courier", 9))
        self.log_box.pack(fill="both", expand=True)

        scrollbar = tk.Scrollbar(log_frame, command=self.log_box.yview)
        self.log_box.configure(yscrollcommand=scrollbar.set)

    def _log(self, message):
        timestamp = time.strftime("%H:%M:%S")
        self.log_box.configure(state="normal")
        self.log_box.insert("end", f"[{timestamp}] {message}\n")
        self.log_box.see("end")
        self.log_box.configure(state="disabled")

    def _update_state(self, state):
        self.state_label.config(text=state)

    def _select_region(self):
        self._log("Selecting region — draw a rectangle over the game window...")
        self.root.withdraw()
        time.sleep(0.5)

        overlay = tk.Toplevel()
        overlay.attributes("-fullscreen", True)
        overlay.attributes("-alpha", 0.3)
        overlay.attributes("-topmost", True)
        overlay.configure(bg="black")

        canvas = tk.Canvas(overlay, cursor="cross", bg="black")
        canvas.pack(fill="both", expand=True)

        start_x = start_y = 0
        rect = None

        def on_press(event):
            nonlocal start_x, start_y, rect
            start_x, start_y = event.x, event.y
            rect = canvas.create_rectangle(start_x, start_y, start_x, start_y,
                                           outline="red", width=2)

        def on_drag(event):
            canvas.coords(rect, start_x, start_y, event.x, event.y)

        def on_release(event):
            x1, y1 = min(start_x, event.x), min(start_y, event.y)
            x2, y2 = max(start_x, event.x), max(start_y, event.y)
            self.region = (x1, y1, x2 - x1, y2 - y1)
            overlay.destroy()
            self.root.deiconify()
            self.region_label.config(
                text=f"x={x1} y={y1} w={x2 - x1} h={y2 - y1}", fg="green"
            )
            self.start_btn.config(state="normal")
            self._log(f"Region set: x={x1}, y={y1}, width={x2-x1}, height={y2-y1}")

        canvas.bind("<ButtonPress-1>", on_press)
        canvas.bind("<B1-Motion>", on_drag)
        canvas.bind("<ButtonRelease-1>", on_release)

    def _start_bot(self):
        if not self.region:
            self._log("No region selected!")
            return

        self.bot_running = True
        self.start_btn.config(state="disabled")
        self.stop_btn.config(state="normal")
        self._log("Bot started.")

        input_handler = InputHandler()
        self.bot = BotFSM(input_handler, region=self.region,
                          state_callback=self._update_state,
                          log_callback=self._log)

        self.bot_thread = threading.Thread(target=self.bot.run, daemon=True)
        self.bot_thread.start()

    def _stop_bot(self):
        self.bot_running = False
        if self.bot:
            self.bot.stop()
        self.start_btn.config(state="normal")
        self.stop_btn.config(state="disabled")
        self._update_state("IDLE")
        self._log("Bot stopped.")


if __name__ == "__main__":
    root = tk.Tk()
    app = BotGUI(root)
    root.mainloop()