import pyperclip #type: ignore
import pyautogui #type: ignore
import requests #type: ignore
import threading
import time
import tkinter as tk
import queue
from pynput import mouse #type: ignore
from pynput.keyboard import Key, Controller as KeyboardController #type: ignore

OLLAMA_MODEL = "qwen2.5-coder:7b"
OLLAMA_URL = "http://localhost:11434/api/generate"

response_queue = queue.Queue()

start_pos = None
last_clipboard = pyperclip.paste()
keyboard = KeyboardController()

def ask_ollama(text):
    prompt = f"""
    You got a text in any language -> answers ARE in ENGLISH only.
    If input question ->  answer it in SHORT form (only the correct answer, no explanation).
    If input is simple text -> expain it in SHORT form (at least 2 sentence and maximum 4 sentences).
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
        response_queue.put(answer)
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
                    time.sleep(0.3)
                    
                    with keyboard.pressed(Key.cmd):
                        keyboard.press('c')
                        keyboard.release('c')
                    
                    time.sleep(0.2)
                    
                    new_clipboard = pyperclip.paste()
                    
                    if new_clipboard != last_clipboard and new_clipboard.strip():
                        last_clipboard = new_clipboard
                        print(f"Selection noticed: {new_clipboard[:30]}...")
                        threading.Thread(target=ask_ollama, args=(new_clipboard,), daemon=True).start()

def create_popup(text):
    popup = tk.Toplevel(root)
    popup.wm_overrideredirect(True)
    popup.attributes('-topmost', True)
    
    frame = tk.Frame(popup, bg="#FFFFFF", highlightbackground="#FFFFFF", highlightthickness=1)
    frame.pack(fill="both", expand=True)
    
    lbl = tk.Label(frame, text=text, bg="#000000", fg="#FFFFFF", 
                   font=("Helvetica", 16), justify="left", wraplength=350,
                   padx=30, pady=30)
    lbl.pack()
    
    lbl.bind("<Button-1>", lambda e: popup.destroy())
    
    popup.update_idletasks()
    popup_height = popup.winfo_reqheight()
    
    screen_height = root.winfo_screenheight()
    
    x_pos = 20
    y_pos = screen_height - popup_height - 60
    
    popup.geometry(f"+{x_pos}+{y_pos}")
    
    popup.after(10000, popup.destroy)

def check_queue():
    try:
        answer = response_queue.get_nowait()
        create_popup(answer)
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