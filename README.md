# 🐍 Snake Game

A classic snake game implemented with both a GUI (Tkinter) and a web interface (Flask + JavaScript), backed by MongoDB for storing game scores. The project includes testing, Docker support, and JSON data export capabilities.

---

## 🚀 Features

- 🎮 **GUI Snake Game** using Python's Tkinter library.
- 🌐 **Web-based Snake Game** built with Flask and JavaScript.
- 🗃️ **MongoDB Integration** for storing and retrieving game results.
- 🧪 **Unit Testing** using `unittest` and `pytest`.
- 📦 **Docker Support** for containerized deployment.
- 📁 **JSON Import/Export** for game data.

---

## ⚙️ Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/gannimatt/snake_game.git
   cd snake-game
   ```

2. **Create a virtual environment and activate it:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

---

## 🧑‍💻 Usage

### 🖥️ Run GUI Version
```bash
python src/snake_game.py
```

### 🌐 Run Web Version
```bash
python app.py
```
Then open `http://127.0.0.1:5000` in your browser.

---

## 🐳 Docker

To run the GUI version inside Docker:

```bash
docker build -t snake-game .
docker run -it --rm snake-game
```

---

## ✅ Testing

Run unit tests using:

```bash
pytest
```

---

## 📂 Data Management

- Game scores are stored in MongoDB (`snake_game_db.game_sessions`).
- Data is also exported to and imported from JSON files in the `db/` directory.

---

## 🔒 Contribution

This is currently a personal project and not open for contributions.

---

## 📄 License

MIT License (or specify your own if different)
