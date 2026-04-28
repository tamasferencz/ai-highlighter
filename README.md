# Smart Select AI 🪄

A lightweight, Python-based background application for macOS that automatically sends the text you highlight with your mouse to a local Ollama model, and displays the response in a stylish pop-up window right next to your cursor.

## Features
* **Instant AI Response:** Just highlight any text, and the background AI answers immediately.
* **100% Local & Free (0 €):** Uses Ollama, so your data never leaves your machine.
* **Seamless Operation:** Only triggers when you actually highlight new text.

## Installation

1. Make sure [Ollama](https://ollama.com/) is installed and running in the background (the code uses the `llama3` model by default).
2. Clone this repository:
   ```bash
   git clone [https://github.com/tamasferencz/ai-highlighter.git](https://github.com/tamasferencz/ai-highlighter.git)
   cd ai-highlighter
   ```
3. Install the required Python packages:
   ```bash
   pip install pynput pyautogui pyperclip requests
   ```
4. Run the application:
   ```bash
   python smart_popup.py
   ```
   (On the first run, macOS may ask for permission to monitor your mouse/keyboard. You can grant this in System Settings > Privacy & Security > Accessibility)

## Usage
Once started, the program runs in the background. If you highlight text in any application (browser, PDF reader, code editor), the answer will pop up in a small window. The window will close upon clicking it, or automatically disappear after 10 seconds.
