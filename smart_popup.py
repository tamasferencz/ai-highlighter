import pyperclip #type: ignore
import pyautogui #type: ignore
import requests #type: ignore
import threading
import time
import tkinter as tk
import queue
from pynput import mouse #type: ignore

OLLAMA_MODEL = "qwen2.5-coder:7b"
OLLAMA_URL = "http://localhost:11434/api/generate"

response_queue = queue.Queue()

start_pos = None
last_clipboard = pyperclip.paste()

def ask_ollama(text, x, y):
    prompt = f"""
    You got a text in any language -> answers ARE in that SAME language.
    If input question ->  answer it in SHORT form (only the correct answer, no explanation).
    If input is simple text -> expain it in SHORT form (maximum 1 or 2 sentences).
    Text input: "{text}"
    """
    
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False
    }
    
    try:
        response = requests.post(OLLAMA_URL, json=payload)
        response.raise_for_status()
        answer = response.json().get("response", "Did not recieved any response!")
        response_queue.put((x, y, answer))
    except Exception as e:
        print(f"Error: {e}")

def on_click(x, y, button, pressed):
    global start_pos, last_clipboard
    
    if button == mouse.Button.left:
        if pressed:
            start_pos = (x, y)
        else:
            if start_pos:
                dx = abs(x - start_pos[0])
                dy = abs(y - start_pos[1])
                
                if dx > 15 or dy > 15:
                    time.sleep(0.1)
                    
                    pyautogui.hotkey('command', 'c')
                    time.sleep(0.1)
                    
                    new_clipboard = pyperclip.paste()
                    
                    if new_clipboard != last_clipboard and new_clipboard.strip():
                        last_clipboard = new_clipboard
                        print(f"Selection noticed: {new_clipboard[:30]}... Sending to Ollama!")
                        threading.Thread(target=ask_ollama, args=(new_clipboard, x, y), daemon=True).start()

def create_popup(x, y, text):
    popup = tk.Toplevel(root)
    popup.wm_overrideredirect(True)
    popup.attributes('-topmost', True)
    
    popup.geometry(f"+{int(x) + 15}+{int(y) + 15}")
    
    frame = tk.Frame(popup, bg="#FFFFFF", highlightbackground="#FFFFFF", highlightthickness=1)
    frame.pack(fill="both", expand=True)
    
    lbl = tk.Label(frame, text=text, bg="#000000", fg="#FFFFFF", 
                   font=("Helvetica", 16), justify="left", wraplength=350,
                   padx=15, pady=15)
    lbl.pack()
    
    lbl.bind("<Button-1>", lambda e: popup.destroy())
    
    popup.after(10000, popup.destroy)

def check_queue():
    try:
        x, y, answer = response_queue.get_nowait()
        create_popup(x, y, answer)
    except queue.Empty:
        pass
    root.after(200, check_queue)

root = tk.Tk()
root.withdraw() 

listener = mouse.Listener(on_click=on_click)
listener.start()

print("The system is working! Highlight a text!!!")

root.after(200, check_queue)
root.mainloop()