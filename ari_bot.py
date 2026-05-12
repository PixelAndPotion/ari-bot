import tkinter as tk
from tkinter import scrolledtext
from datetime import datetime
import requests
import random
import threading

#  Key 
OMDB_API_KEY = "5bee5fd5"

#  Palette 
BG_DEEP   = "#0A0A0F"
BG_PANEL  = "#111118"
BG_INPUT  = "#18181F"
ACCENT    = "#00FFB2"
ACCENT2   = "#7C3AED"
TEXT_MAIN = "#E8E8F0"
TEXT_DIM  = "#44445A"
TEXT_YOU  = "#00FFB2"
TEXT_ARI  = "#A78BFA"

#  Handlers 
def get_weather(text: str) -> str:
    try:
        lat, lon, label = -29.8587, 31.0218, "Durban"
        city_map = {
            "london":       (51.5074,  -0.1278,  "London"),
            "new york":     (40.7128,  -74.0060, "New York"),
            "johannesburg": (-26.2041,  28.0473, "Johannesburg"),
            "cape town":    (-33.9249,  18.4241, "Cape Town"),
            "durban":       (-29.8587,  31.0218, "Durban"),
            "tokyo":        (35.6895,  139.6917, "Tokyo"),
            "paris":        (48.8566,    2.3522, "Paris"),
            "sydney":       (-33.8688, 151.2093, "Sydney"),
            "dubai":        (25.2048,   55.2708, "Dubai"),
            "lagos":        (6.5244,     3.3792, "Lagos"),
        }
        if " in " in text:
            city = text.split(" in ")[-1].strip().rstrip("?. ")
            if city.lower() in city_map:
                lat, lon, label = city_map[city.lower()]
        url = (
            "https://api.open-meteo.com/v1/forecast"
            f"?latitude={lat}&longitude={lon}&current_weather=true"
        )
        d    = requests.get(url, timeout=6).json()
        cw   = d["current_weather"]
        temp = cw["temperature"]
        wind = cw["windspeed"]
        code = cw["weathercode"]
        icons = {
            0:"☀", 1:"🌤", 2:"⛅", 3:"☁",
            45:"🌫", 48:"🌫", 51:"🌦", 61:"🌧",
            71:"❄", 80:"🌧", 95:"⛈"
        }
        icon = icons.get(code, "🌡")
        return f"{icon}  {label}: {temp}°C  |  💨 Wind: {wind} km/h"
    except:
        return "Couldn't fetch weather — try again shortly."


def get_crypto(text: str) -> str:
    try:
        coin, symbol = "bitcoin", "BTC"
        if "ethereum" in text or " eth" in text:
            coin, symbol = "ethereum", "ETH"
        elif "solana" in text or " sol" in text:
            coin, symbol = "solana",   "SOL"
        elif "dogecoin" in text or "doge" in text:
            coin, symbol = "dogecoin", "DOGE"
        url  = (
            f"https://api.coingecko.com/api/v3/simple/price"
            f"?ids={coin}&vs_currencies=usd&include_24hr_change=true"
        )
        d      = requests.get(url, timeout=6).json()
        price  = d[coin]["usd"]
        change = d[coin].get("usd_24h_change", 0)
        arrow  = "▲" if change >= 0 else "▼"
        sign   = "+" if change >= 0 else ""
        return f"💰 {symbol}: ${price:,.2f}  {arrow} {sign}{change:.2f}% (24h)"
    except:
        return "Couldn't fetch crypto data right now."


def get_news() -> str:
    try:
        url  = "https://api.spaceflightnewsapi.net/v4/articles/?limit=3"
        d    = requests.get(url, timeout=6).json()
        lines = ["📡 Latest space headlines:\n"]
        for i, art in enumerate(d["results"], 1):
            lines.append(f"  {i}. {art['title']}")
        return "\n".join(lines)
    except:
        return "Couldn't fetch news right now."


def get_movie(text: str) -> str:
    try:
        title = (text.lower()
                 .replace("movie", "")
                 .replace("film", "")
                 .replace("tell me about", "")
                 .replace("search", "")
                 .replace("look up", "")
                 .strip().rstrip("?. "))
        if not title:
            return "Which movie? Try: 'movie Interstellar'"
        url  = f"http://www.omdbapi.com/?apikey={OMDB_API_KEY}&t={title}"
        d    = requests.get(url, timeout=6).json()
        if d.get("Response") == "True":
            return (
                f"🎬 {d['Title']} ({d['Year']})  ⭐ {d['imdbRating']}/10\n"
                f"Genre: {d.get('Genre', 'N/A')}\n"
                f"Cast:  {d.get('Actors', 'N/A')}\n\n"
                f"{d['Plot']}"
            )
        return "Movie not found — check the title and try again."
    except:
        return "Couldn't reach movie database right now."


def get_joke() -> str:
    return random.choice([
        "Why do programmers prefer dark mode? Because light attracts bugs. 🐛",
        "I told my AI to think outside the box. It returned None.",
        "A SQL query walks into a bar and asks two tables: 'Can I join you?'",
        "How many developers does it take to change a lightbulb? None — that's a hardware problem.",
        "There are only 10 kinds of people: those who understand binary, and those who don't.",
        "Why was the JavaScript developer sad? Because he didn't know how to 'null' his feelings.",
    ])


def wellness_response() -> str:
    return random.choice([
        "I hear you. You don't have to have it together all the time. 💙",
        "Take a slow breath. You're doing better than you think.",
        "Whatever you're carrying right now — it's okay to put it down for a moment.",
        "Tough moments don't last forever. You do. 🌱",
        "You're allowed to rest. That's not giving up.",
    ])


#  Router 
def generate_response(text: str) -> str:
    t = text.lower().strip()

    if any(w in t for w in ("hello","hi","hey","howdy","sup","yo","what's up","good morning","good evening")):
        return random.choice([
            "Hey. 👋 What do you need?",
            "Hello — I'm listening. What's on your mind?",
            "Hi there! Ask me anything.",
        ])

    if "your name" in t or "who are you" in t or "what are you" in t:
        return "I'm A.R.I — Artificial Response Intelligence. Built to assist, not impress. (Though hopefully both.)"

    if "time" in t and "weather" not in t:
        return f"🕐 {datetime.now().strftime('%H:%M:%S')}"

    if "date" in t and "weather" not in t:
        return f"📅 {datetime.now().strftime('%A, %d %B %Y')}"

    if "weather" in t:
        return get_weather(t)

    if any(w in t for w in ("bitcoin","ethereum","solana","dogecoin","crypto","btc","eth","sol","doge")):
        return get_crypto(t)

    if "news" in t or "headline" in t:
        return get_news()

    if "movie" in t or "film" in t:
        return get_movie(t)

    if any(w in t for w in ("joke","funny","laugh","make me laugh")):
        return get_joke()

    if any(w in t for w in ("sad","stressed","tired","angry","upset","anxious","overwhelmed","depressed","lonely")):
        return wellness_response()

    if "thank" in t:
        return random.choice(["Anytime. 🤝", "Happy to help.", "That's what I'm here for."])

    if "bye" in t or "goodbye" in t or "exit" in t:
        return "Take care. Come back anytime. 👋"

    return "I don't know that one yet — but I'm always learning. 🤖"


#  GUI 
class ARIBotGUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("A.R.I — Artificial Response Intelligence")
        self.root.geometry("860x700")
        self.root.minsize(640, 520)
        self.root.configure(bg=BG_DEEP)
        self._build()
        self._welcome()

    def _build(self):
        #  Top bar 
        bar = tk.Frame(self.root, bg=BG_PANEL, height=60)
        bar.pack(fill=tk.X)
        bar.pack_propagate(False)

        self.dot_canvas = tk.Canvas(bar, width=12, height=12,
                                    bg=BG_PANEL, highlightthickness=0)
        self.dot_canvas.place(x=22, rely=0.5, anchor="w")
        self._pulse(True)

        tk.Label(bar, text="A.R.I", font=("Courier New", 18, "bold"),
                 bg=BG_PANEL, fg=ACCENT).place(x=44, rely=0.5, anchor="w")

        tk.Label(bar, text="Artificial Response Intelligence",
                 font=("Courier New", 9), bg=BG_PANEL, fg=TEXT_DIM).place(
                 x=132, rely=0.5, anchor="w")

        tk.Label(bar, text="● ONLINE",
                 font=("Courier New", 8, "bold"),
                 bg=BG_PANEL, fg=ACCENT).place(relx=1.0, x=-20, rely=0.5, anchor="e")

        #  Accent line 
        tk.Frame(self.root, bg=ACCENT, height=2).pack(fill=tk.X)

        #  Chat area 
        self.chat_area = scrolledtext.ScrolledText(
            self.root,
            wrap=tk.WORD,
            font=("Courier New", 11),
            bg=BG_PANEL,
            fg=TEXT_MAIN,
            insertbackground=ACCENT,
            selectbackground=ACCENT2,
            relief=tk.FLAT,
            bd=0,
            padx=18,
            pady=14
        )
        self.chat_area.pack(fill=tk.BOTH, expand=True)
        self.chat_area.config(state=tk.DISABLED)

        self.chat_area.tag_config("ts",  foreground=TEXT_DIM,  font=("Courier New", 9))
        self.chat_area.tag_config("ari", foreground=TEXT_ARI,  font=("Courier New", 11, "bold"))
        self.chat_area.tag_config("you", foreground=TEXT_YOU,  font=("Courier New", 11, "bold"))
        self.chat_area.tag_config("msg", foreground=TEXT_MAIN, font=("Courier New", 11))

        #  Bottom line 
        tk.Frame(self.root, bg=ACCENT2, height=1).pack(fill=tk.X)

        #  Input row 
        row = tk.Frame(self.root, bg=BG_INPUT)
        row.pack(fill=tk.X)

        tk.Label(row, text=">", font=("Courier New", 13, "bold"),
                 bg=BG_INPUT, fg=ACCENT).pack(side=tk.LEFT, padx=(14, 4), pady=12)

        self.entry = tk.Entry(
            row,
            font=("Courier New", 12),
            bg=BG_INPUT,
            fg=TEXT_MAIN,
            insertbackground=ACCENT,
            relief=tk.FLAT,
            bd=0
        )
        self.entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, ipady=10, pady=10)
        self.entry.bind("<Return>", self.send)
        self.entry.focus()

        self.send_btn = tk.Button(
            row,
            text="SEND",
            font=("Courier New", 10, "bold"),
            bg=ACCENT2, fg=TEXT_MAIN,
            activebackground=ACCENT,
            activeforeground=BG_DEEP,
            relief=tk.FLAT, bd=0,
            cursor="hand2",
            padx=22, pady=12,
            command=self.send
        )
        self.send_btn.pack(side=tk.RIGHT)

        #  Footer 
        tk.Label(self.root,
                 text="A.R.I v2.0  ·  Weather · Crypto · Movies · News",
                 font=("Courier New", 8),
                 bg=BG_DEEP, fg=TEXT_DIM).pack(pady=5)

    def _pulse(self, state: bool):
        color = ACCENT if state else "#004433"
        self.dot_canvas.delete("all")
        self.dot_canvas.create_oval(1, 1, 11, 11, fill=color, outline="")
        self.root.after(900, lambda: self._pulse(not state))

    def _welcome(self):
        self.display("A.R.I",
                     "System online. I'm A.R.I — ask me about weather, crypto, "
                     "movies, news, jokes, or just say hi.",
                     typing=True)

    def display(self, sender: str, message: str, typing=False):
        self.chat_area.config(state=tk.NORMAL)
        ts  = datetime.now().strftime("%H:%M")
        tag = "ari" if sender == "A.R.I" else "you"

        self.chat_area.insert(tk.END, f"  {ts}  ", "ts")
        self.chat_area.insert(tk.END, f"{sender}:\n", tag)
        self.chat_area.insert(tk.END, "  ")

        if typing:
            for char in message:
                self.chat_area.insert(tk.END, char, "msg")
                self.chat_area.update()
                self.chat_area.after(7)
        else:
            self.chat_area.insert(tk.END, message, "msg")

        self.chat_area.insert(tk.END, "\n\n")
        self.chat_area.config(state=tk.DISABLED)
        self.chat_area.yview(tk.END)

    def send(self, event=None):
        text = self.entry.get().strip()
        if not text:
            return
        self.display("You", text)
        self.entry.delete(0, tk.END)
        self.send_btn.config(state=tk.DISABLED, text="···")
        threading.Thread(target=self._worker, args=(text,), daemon=True).start()

    def _worker(self, text: str):
        reply = generate_response(text)
        self.root.after(0, lambda: self._deliver(reply))

    def _deliver(self, reply: str):
        self.display("A.R.I", reply, typing=True)
        self.send_btn.config(state=tk.NORMAL, text="SEND")


#  Run 
if __name__ == "__main__":
    root = tk.Tk()
    ARIBotGUI(root)
    root.mainloop()