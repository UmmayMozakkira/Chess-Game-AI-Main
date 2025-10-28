import tkinter as tk
from tkinter import font as tkfont
from PIL import Image, ImageTk
import chess
import chess.engine
import os

STOCKFISH_PATH = r"E:\HEss projet\Project\stockfish-windows-x86-64-avx2"
"
AI_CHARACTERS = [
    {"name": "Jamil", "image": "Jamil.jpg", "elo": 2800, "dialogue": "This won't take long. I'll finish you quickly."},
    {"name": "Fardin", "image": "Fardin.jpg", "elo": 2000, "dialogue": "Let's see what you've got!"},
    {"name": "Karuna", "image": "Karuna.jpg", "elo": 1500, "dialogue": "Your king looks nervous already."},
    {"name": "Drish", "image": "Drish.jpg", "elo": 1000, "dialogue": "Go easy on me..."},
]

# UPDATED HUMAN NAMES
HUMAN_IMAGES = [
    {"name": "Jamil", "image": "human1.jpg"},
    {"name": "Likhon", "image": "human2.jpg"},
    {"name": "Satu", "image": "human3.jpg"},
    {"name": "Mozakkira", "image": "human4.jpg"},
]

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("GrandMaster Arena")
        self.state('zoomed')
        self.selected = {}
        self.container = tk.Frame(self, bg="#aee0fa")
        self.container.pack(fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        for F in (HomePage, AiVsHumanPage, HumanVsHumanPage):
            frame = F(self.container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(HomePage)

    def show_frame(self, page):
        frame = self.frames[page]
        frame.tkraise()
        if hasattr(frame, "refresh"):
            frame.refresh()

class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#aee0fa")
        self.controller = controller

        # Responsive fonts
        self.title_font = tkfont.Font(family="Arial", size=32, weight="bold")
        self.subtitle_font = tkfont.Font(family="Arial", size=16)
        self.section_title_font = tkfont.Font(family="Arial", size=22, weight="bold")
        self.label_font = tkfont.Font(family="Arial", size=16, weight="bold")
        self.vs_font = tkfont.Font(family="Arial", size=28, weight="bold")
        self.button_font = tkfont.Font(family="Arial", size=18, weight="bold")

        # Title
        title = tk.Label(self, text="Welcome to GrandMaster Arena", font=self.title_font, bg="#aee0fa")
        title.pack(pady=(30, 0))
        subtitle = tk.Label(self, text="Your Ultimate Destination for Chess Battles, Learning & Strategy!", font=self.subtitle_font, bg="#aee0fa")
        subtitle.pack()
        lets_play = tk.Label(self, text="Let's Play", font=self.section_title_font, bg="#aee0fa")
        lets_play.pack(pady=(0, 20))

        # Main section
        main_frame = tk.Frame(self, bg="#aee0fa")
        main_frame.pack(expand=True, fill="both", pady=10)
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)

        # AI vs Human Section
        self.ai_vs_human_frame = self.create_vs_section(
            main_frame,
            "AI vs Human",
            "AI", AI_CHARACTERS,
            "Human", HUMAN_IMAGES,
            self.start_ai_vs_human
        )
        self.ai_vs_human_frame.grid(row=0, column=0, sticky="nsew", padx=40, pady=10)

        # White vs Black Section
        self.white_vs_black_frame = self.create_vs_section(
            main_frame,
            "Human vs Human",
            "Player 1", HUMAN_IMAGES,
            "Player 2", HUMAN_IMAGES,
            self.start_human_vs_human
        )
        self.white_vs_black_frame.grid(row=0, column=1, sticky="nsew", padx=40, pady=10)

        # Default selections
        self.ai_var.set(AI_CHARACTERS[0]["name"])
        self.human_var.set(HUMAN_IMAGES[0]["name"])
        self.white_var.set(HUMAN_IMAGES[0]["name"])
        self.black_var.set(HUMAN_IMAGES[1]["name"])

    def create_vs_section(self, parent, section_title, left_label, left_list, right_label, right_list, start_command):
        frame = tk.Frame(parent, bg="#e6f7ff", bd=3, relief="ridge")
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        # Section Title
        tk.Label(frame, text=section_title, font=self.section_title_font, bg="#e6f7ff").pack(pady=(20, 10))

        # Left label
        tk.Label(frame, text=left_label, font=self.label_font, bg="#e6f7ff").pack()
        # Left images
        var = tk.StringVar()
        img_frame1 = tk.Frame(frame, bg="#e6f7ff")
        img_frame1.pack(pady=(5, 10))
        for item in left_list:
            img = Image.open(item["image"]).resize((90, 90))
            photo = ImageTk.PhotoImage(img)
            btn = tk.Radiobutton(img_frame1, image=photo, variable=var, value=item["name"], indicatoron=0, bg="#e6f7ff", selectcolor="#b3e0ff")
            btn.image = photo
            btn.pack(side=tk.LEFT, padx=8)
        if section_title == "AI vs Human":
            self.ai_var = var
        else:
            self.white_var = var

        # VS
        tk.Label(frame, text="VS", font=self.vs_font, bg="#e6f7ff", fg="#4caf50").pack(pady=10)

        # Right label
        tk.Label(frame, text=right_label, font=self.label_font, bg="#e6f7ff").pack()
        # Right images
        var2 = tk.StringVar()
        img_frame2 = tk.Frame(frame, bg="#e6f7ff")
        img_frame2.pack(pady=(5, 10))
        for item in right_list:
            img = Image.open(item["image"]).resize((90, 90))
            photo = ImageTk.PhotoImage(img)
            btn = tk.Radiobutton(img_frame2, image=photo, variable=var2, value=item["name"], indicatoron=0, bg="#e6f7ff", selectcolor="#b3e0ff")
            btn.image = photo
            btn.pack(side=tk.LEFT, padx=8)
        if section_title == "AI vs Human":
            self.human_var = var2
        else:
            self.black_var = var2

        # Start button
        tk.Button(frame, text="Start Playing", font=self.button_font, bg="#4caf50", fg="white", height=2,
                  command=start_command).pack(pady=(20, 30), fill=tk.X, padx=40)
        return frame

    def start_ai_vs_human(self):
        ai = next(a for a in AI_CHARACTERS if a["name"] == self.ai_var.get())
        human = next(h for h in HUMAN_IMAGES if h["name"] == self.human_var.get())
        self.controller.selected = {
            "ai": ai,
            "human": human
        }
        self.controller.show_frame(AiVsHumanPage)

    def start_human_vs_human(self):
        white = next(h for h in HUMAN_IMAGES if h["name"] == self.white_var.get())
        black = next(h for h in HUMAN_IMAGES if h["name"] == self.black_var.get())
        self.controller.selected = {
            "white": white,
            "black": black
        }
        self.controller.show_frame(HumanVsHumanPage)

class CenteredFrame(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.inner = tk.Frame(self, bg=self["bg"])
        self.inner.grid(row=0, column=0)
        self.inner.grid_rowconfigure(0, weight=1)
        self.inner.grid_columnconfigure(1, weight=1)

class AiVsHumanPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#e6f7ff")
        self.controller = controller
        self.board = chess.Board()
        self.selected_square = None
        self.human_color = chess.WHITE
        self.engine = chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH)
        self.square_size = 100
        self.create_widgets()

    def create_widgets(self):
        self.centered = CenteredFrame(self, bg="#e6f7ff")
        self.centered.pack(expand=True, fill="both")

        # Left panel
        self.left_side = tk.Frame(self.centered.inner, bg="#d6f0ff", width=200)
        self.left_side.grid(row=0, column=0, sticky="ns", padx=(0, 20), pady=0)
        self.left_side.grid_propagate(False)
        self.human_img_label = tk.Label(self.left_side, bg="#d6f0ff")
        self.human_img_label.pack(pady=(10, 10))
        self.human_name_label = tk.Label(self.left_side, font=("Arial", 16, "bold"), bg="#d6f0ff")
        self.human_name_label.pack(pady=(0, 20))
        tk.Button(self.left_side, text="Home Page", bg="#00e6e6", fg="black", font=("Arial", 13, "bold"),
                  command=lambda: self.controller.show_frame(HomePage)).pack(pady=10, ipadx=10, ipady=5)
        tk.Button(self.left_side, text="Human vs Human", bg="#00e6e6", fg="black", font=("Arial", 13, "bold"),
                  command=lambda: self.controller.show_frame(HumanVsHumanPage)).pack(pady=10, ipadx=10, ipady=5)

        # Center board
        self.board_frame = tk.Frame(self.centered.inner, bg="#e6f7ff")
        self.board_frame.grid(row=0, column=1, sticky="nsew")
        self.board_frame.grid_rowconfigure(0, weight=1)
        self.board_frame.grid_columnconfigure(0, weight=1)
        self.canvas = tk.Canvas(self.board_frame, width=self.square_size * 8, height=self.square_size * 8, bg="#e6f7ff", highlightthickness=0)
        self.canvas.grid(row=0, column=0, pady=0, padx=0, sticky="nsew")
        self.canvas.bind("<Button-1>", self.on_click)

        # Right panel
        self.right_side = tk.Frame(self.centered.inner, bg="#e6f7ff", width=260)
        self.right_side.grid(row=0, column=2, sticky="ns", padx=(20, 0), pady=0)
        self.right_side.grid_propagate(False)
        self.ai_img_label = tk.Label(self.right_side, bg="#e6f7ff")
        self.ai_img_label.pack(pady=(10, 0))
        self.ai_dialogue_label = tk.Label(self.right_side, fg="green", font=("Arial", 13), bg="#e6f7ff")
        self.ai_dialogue_label.pack(pady=10)
        self.ai_status_label = tk.Label(self.right_side, font=("Arial", 12, "italic"), fg="purple", bg="#e6f7ff")
        self.ai_status_label.pack(pady=5)
        button_frame = tk.Frame(self.right_side, bg="#e6f7ff")
        button_frame.pack(pady=10)
        tk.Button(button_frame, text="Suggest Move", command=self.suggest_move, bg="green", fg="white", font=("Arial", 12, "bold")).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Restart", command=self.restart_game, bg="red", fg="white", font=("Arial", 12, "bold")).pack(side=tk.LEFT, padx=5)
        self.side_var = tk.StringVar(value="White")
        tk.Label(self.right_side, text="Choose Your Side:", font=("Arial", 12, "bold"), bg="#e6f7ff").pack(pady=(20, 0))
        tk.Radiobutton(self.right_side, text="White", variable=self.side_var, value="White", command=self.update_side, bg="#e6f7ff", font=("Arial", 11)).pack()
        tk.Radiobutton(self.right_side, text="Black", variable=self.side_var, value="Black", command=self.update_side, bg="#e6f7ff", font=("Arial", 11)).pack()

    def refresh(self):
        ai = self.controller.selected.get("ai", AI_CHARACTERS[0])
        human = self.controller.selected.get("human", HUMAN_IMAGES[0])
        img = Image.open(human["image"]).resize((100, 100))
        self.human_photo = ImageTk.PhotoImage(img)
        self.human_img_label.config(image=self.human_photo)
        self.human_img_label.image = self.human_photo
        self.human_name_label.config(text=human["name"])
        img = Image.open(ai["image"]).resize((100, 100))
        self.ai_photo = ImageTk.PhotoImage(img)
        self.ai_img_label.config(image=self.ai_photo)
        self.ai_img_label.image = self.ai_photo
        self.ai_dialogue_label.config(text=f"{ai['name']}: {ai['dialogue']}")
        self.ai_status_label.config(text=f"AI: {ai['name']} (ELO {ai['elo']})")
        self.restart_game()

    def update_side(self):
        self.human_color = chess.WHITE if self.side_var.get() == "White" else chess.BLACK
        self.restart_game()

    def restart_game(self):
        self.board.reset()
        self.selected_square = None
        self.update_board()
        if self.human_color == chess.BLACK:
            self.after(500, self.ai_move)

    def draw_piece(self, square, piece):
        file = chess.square_file(square)
        rank = chess.square_rank(square)
        if self.human_color == chess.BLACK:
            file = 7 - file
            rank = 7 - rank
        x = file * self.square_size
        y = (7 - rank) * self.square_size
        if piece:
            piece_symbol = piece.symbol()
            color = "black" if piece_symbol.islower() else "white"
            piece_symbol = piece_symbol.upper()
            self.canvas.create_text(
                x + self.square_size // 2,
                y + self.square_size // 2,
                text=self.get_unicode_piece(piece_symbol, color),
                font=("Arial", int(self.square_size * 0.6)),
            )

    def get_unicode_piece(self, piece, color):
        pieces = {
            "K": "\u2654", "Q": "\u2655", "R": "\u2656",
            "B": "\u2657", "N": "\u2658", "P": "\u2659"
        }
        unicode_piece = pieces.get(piece, "")
        return unicode_piece if color == "white" else chr(ord(unicode_piece) + 6)

    def update_board(self):
        self.canvas.delete("all")
        for row in range(8):
            for col in range(8):
                x1 = col * self.square_size
                y1 = row * self.square_size
                x2 = x1 + self.square_size
                y2 = y1 + self.square_size
                color = "#f0d9b5" if (row + col) % 2 == 0 else "#b58863"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color)
        for square in chess.SQUARES:
            piece = self.board.piece_at(square)
            if piece:
                self.draw_piece(square, piece)

    def on_click(self, event):
        col = int(event.x // self.square_size)
        row = int(event.y // self.square_size)
        if self.human_color == chess.BLACK:
            col = 7 - col
            row = 7 - row
        square = chess.square(col, 7 - row)
        if self.selected_square is None:
            if self.board.piece_at(square) and self.board.piece_at(square).color == self.human_color:
                self.selected_square = square
        else:
            move = chess.Move(self.selected_square, square)
            if move in self.board.legal_moves:
                self.board.push(move)
                self.selected_square = None
                self.update_board()
                self.after(100, self.ai_move)
            else:
                self.selected_square = None

    def ai_move(self):
        if not self.board.is_game_over():
            result = self.engine.play(self.board, chess.engine.Limit(time=0.1))
            self.board.push(result.move)
            self.update_board()

    def suggest_move(self):
        if not self.board.is_game_over():
            result = self.engine.play(self.board, chess.engine.Limit(time=0.1))
            move = result.move
            from_square = move.from_square
            to_square = move.to_square
            fx = chess.square_file(from_square)
            fy = chess.square_rank(from_square)
            tx = chess.square_file(to_square)
            ty = chess.square_rank(to_square)
            if self.human_color == chess.BLACK:
                fx = 7 - fx
                fy = 7 - fy
                tx = 7 - tx
                ty = 7 - ty
            fx = fx * self.square_size + self.square_size // 2
            fy = (7 - fy) * self.square_size + self.square_size // 2
            tx = tx * self.square_size + self.square_size // 2
            ty = (7 - ty) * self.square_size + self.square_size // 2
            self.canvas.create_line(fx, fy, tx, ty, fill="blue", width=4, arrow=tk.LAST)

class HumanVsHumanPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#a084ee")
        self.controller = controller
        self.board = chess.Board()
        self.selected_square = None
        self.orientation = chess.WHITE
        self.square_size = 100
        self.create_widgets()

    def create_widgets(self):
        self.centered = CenteredFrame(self, bg="#a084ee")
        self.centered.pack(expand=True, fill="both")

        # Left panel
        self.left_side = tk.Frame(self.centered.inner, bg="#a084ee", width=200)
        self.left_side.grid(row=0, column=0, sticky="ns", padx=(0, 20), pady=0)
        self.left_side.grid_propagate(False)
        self.white_img_label = tk.Label(self.left_side, bg="#a084ee")
        self.white_img_label.pack(pady=(10, 10))
        tk.Label(self.left_side, text="Player 1", font=("Arial", 16, "bold"), bg="#a084ee").pack(pady=(0, 10))
        tk.Button(self.left_side, text="Move Undo", bg="#00e6e6", fg="black", font=("Arial", 13, "bold"),
                  command=self.undo_move).pack(pady=10, ipadx=10, ipady=5)
        tk.Button(self.left_side, text="AI vs Human", bg="#00e6e6", fg="black", font=("Arial", 13, "bold"),
                  command=lambda: self.controller.show_frame(AiVsHumanPage)).pack(pady=10, ipadx=10, ipady=5)

        # Center board
        self.board_frame = tk.Frame(self.centered.inner, bg="#a084ee")
        self.board_frame.grid(row=0, column=1, sticky="nsew")
        self.board_frame.grid_rowconfigure(0, weight=1)
        self.board_frame.grid_columnconfigure(0, weight=1)
        self.canvas = tk.Canvas(self.board_frame, width=self.square_size * 8, height=self.square_size * 8, bg="#a084ee", highlightthickness=0)
        self.canvas.grid(row=0, column=0, pady=0, padx=0, sticky="nsew")
        self.canvas.bind("<Button-1>", self.on_click)

        # Right panel
        self.right_side = tk.Frame(self.centered.inner, bg="#a084ee", width=260)
        self.right_side.grid(row=0, column=2, sticky="ns", padx=(20, 0), pady=0)
        self.right_side.grid_propagate(False)
        self.black_img_label = tk.Label(self.right_side, bg="#a084ee")
        self.black_img_label.pack(pady=(10, 10))
        tk.Label(self.right_side, text="Player 2", font=("Arial", 16, "bold"), bg="#a084ee").pack(pady=(0, 10))
        tk.Button(self.right_side, text="Move Undo", bg="#00e6e6", fg="black", font=("Arial", 13, "bold"),
                  command=self.undo_move).pack(pady=10, ipadx=10, ipady=5)
        tk.Button(self.right_side, text="Home Page", bg="#00e6e6", fg="black", font=("Arial", 13, "bold"),
                  command=lambda: self.controller.show_frame(HomePage)).pack(pady=10, ipadx=10, ipady=5)

    def refresh(self):
        white = self.controller.selected.get("white", HUMAN_IMAGES[0])
        black = self.controller.selected.get("black", HUMAN_IMAGES[1])
        img = Image.open(white["image"]).resize((100, 100))
        self.white_photo = ImageTk.PhotoImage(img)
        self.white_img_label.config(image=self.white_photo)
        self.white_img_label.image = self.white_photo
        img = Image.open(black["image"]).resize((100, 100))
        self.black_photo = ImageTk.PhotoImage(img)
        self.black_img_label.config(image=self.black_photo)
        self.black_img_label.image = self.black_photo
        self.restart_game()

    def undo_move(self):
        if len(self.board.move_stack) > 0:
            self.board.pop()
            self.orientation = not self.orientation
            self.update_board()

    def restart_game(self):
        self.board.reset()
        self.selected_square = None
        self.orientation = chess.WHITE
        self.update_board()

    def draw_piece(self, square, piece):
        file = chess.square_file(square)
        rank = chess.square_rank(square)
        if self.orientation == chess.BLACK:
            file = 7 - file
            rank = 7 - rank
        x = file * self.square_size
        y = (7 - rank) * self.square_size
        if piece:
            piece_symbol = piece.symbol()
            color = "black" if piece_symbol.islower() else "white"
            piece_symbol = piece_symbol.upper()
            self.canvas.create_text(
                x + self.square_size // 2,
                y + self.square_size // 2,
                text=self.get_unicode_piece(piece_symbol, color),
                font=("Arial", int(self.square_size * 0.6)),
            )

    def get_unicode_piece(self, piece, color):
        pieces = {
            "K": "\u2654", "Q": "\u2655", "R": "\u2656",
            "B": "\u2657", "N": "\u2658", "P": "\u2659"
        }
        unicode_piece = pieces.get(piece, "")
        return unicode_piece if color == "white" else chr(ord(unicode_piece) + 6)

    def update_board(self):
        self.canvas.delete("all")
        for row in range(8):
            for col in range(8):
                x1 = col * self.square_size
                y1 = row * self.square_size
                x2 = x1 + self.square_size
                y2 = y1 + self.square_size
                color = "#f0d9b5" if (row + col) % 2 == 0 else "#b58863"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color)
        for square in chess.SQUARES:
            piece = self.board.piece_at(square)
            if piece:
                self.draw_piece(square, piece)

    def on_click(self, event):
        col = int(event.x // self.square_size)
        row = int(event.y // self.square_size)
        if self.orientation == chess.BLACK:
            col = 7 - col
            row = 7 - row
        square = chess.square(col, 7 - row)
        if self.selected_square is None:
            if self.board.piece_at(square) and self.board.piece_at(square).color == self.orientation:
                self.selected_square = square
        else:
            move = chess.Move(self.selected_square, square)
            if move in self.board.legal_moves:
                self.board.push(move)
                self.selected_square = None
                self.orientation = not self.orientation
                self.update_board()
            else:
                self.selected_square = None

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()