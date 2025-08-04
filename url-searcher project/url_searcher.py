import re
import requests
import pyperclip
from fpdf import FPDF
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from urllib.parse import urlparse
import webbrowser
import time
from datetime import datetime

# --- URL Extraction and Analysis Logic ---
def extract_urls(text):
    urlRegex = re.compile(r'''(
        (https?|ftp|file|mailto)://
        [a-zA-Z0-9.-]+
        (\.[a-zA-Z]{2,})
        (:[0-9]+)?
        (/[^\s]*)?
    )''', re.VERBOSE)

    raw_matches = urlRegex.findall(text)
    urls = list(set([match[0].rstrip('/') for match in raw_matches]))
    return urls


def analyze_urls(urls):
    secure_count = 0
    insecure_count = 0
    analysis_results = []

    for url in urls:
        parsed = urlparse(url)
        if parsed.scheme == "https":
            security = "🔒 Secure (HTTPS)"
            port = "443"
            secure_count += 1
        elif parsed.scheme == "http":
            security = "⚠ Insecure (HTTP)"
            port = "80"
            insecure_count += 1
        elif parsed.scheme == "ftp":
            security = "📤 FTP (not secure)"
            port = parsed.port or "21"
        elif parsed.scheme == "mailto":
            security = "📧 Email Link"
            port = "N/A"
        else:
            security = "❓ Unknown Protocol"
            port = parsed.port or "N/A"

        try:
            if parsed.scheme in ["http", "https"]:
                start_time = time.time()
                response = requests.get(url, timeout=5)
                elapsed = int((time.time() - start_time) * 1000)
                code = response.status_code
                if code == 200:
                    status = f"✅ Status Code: {code} (OK)"
                elif code in [301, 302, 403]:
                    status = f"⚠ Status Code: {code} (Redirect/Forbidden)"
                else:
                    status = f"❌ Status Code: {code}"
                status += f" | ⚡ {elapsed} ms"
            else:
                status = "ℹ️ Not checked"
        except Exception as e:
            status = f"❌ Error: {str(e)}"

        analysis_results.append(
            f"{url}\n   → Security: {security}\n   → Port: {port}\n   → {status}\n"
        )

    return analysis_results, secure_count, insecure_count


def export_to_pdf(results, secure_count, insecure_count):
    def remove_emojis(text):
        return (text
                .replace("🔍", "URL Analysis")
                .replace("✅", "OK")
                .replace("❌", "Error")
                .replace("⚠", "Warning")
                .replace("🔒", "Secure")
                .replace("📊", "Summary")
                .replace("📧", "Email")
                .replace("📤", "FTP")
                .replace("ℹ️", "Info")
                .replace("❓", "Unknown"))

    try:
        cleaned_results = [remove_emojis(line) for line in results]

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        pdf.cell(200, 10, txt="URL Analysis Report", ln=True, align="C")
        pdf.cell(200, 10, txt="============================", ln=True, align="C")
        pdf.ln()

        for line in cleaned_results:
            for subline in line.split('\n'):
                safe_line = subline.encode('latin-1', errors='ignore').decode('latin-1')
                pdf.cell(200, 10, txt=safe_line[:90], ln=True)

        pdf.ln()
        pdf.cell(200, 10, txt=f"Total URLs: {len(results)}", ln=True)
        pdf.cell(200, 10, txt=f"Secure: {secure_count}", ln=True)
        pdf.cell(200, 10, txt=f"Insecure: {insecure_count}", ln=True)

        pdf.output("url_analysis_report.pdf")
        messagebox.showinfo("Exported", "PDF saved as 'url_analysis_report.pdf'")

    except Exception as e:
        messagebox.showerror("PDF Error", f"❌ Failed to export PDF:\n{str(e)}")
        print("PDF export error:", e)


def export_as_pdf():
    export_to_pdf(output_box.analysis_results, output_box.secure_count, output_box.insecure_count)


def analyze_clipboard():
    text = pyperclip.paste()
    run_analysis(text)


def load_txt_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
            run_analysis(text)


def run_analysis(text):
    urls = extract_urls(text)
    if urls:
        results, secure_count, insecure_count = analyze_urls(urls)
        output_box.delete(1.0, tk.END)
        for line in results:
            output_box.insert(tk.END, line + "\n")

        output_box.analysis_results = results
        output_box.secure_count = secure_count
        output_box.insecure_count = insecure_count
    else:
        messagebox.showwarning("No URLs", "🚫 No URLs found. Please paste valid text or upload a .txt file.")


def export_as_txt():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text File", "*.txt")])
    if file_path:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("🔍 URL Analysis Report\n=======================\n\n")
            for line in output_box.analysis_results:
                f.write(line + "\n")
            f.write("\n📊 Summary:\n")
            f.write(f"🔒 Secure: {output_box.secure_count}\n")
            f.write(f"⚠ Insecure: {output_box.insecure_count}\n")
            f.write(f"🕒 Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        messagebox.showinfo("Exported", "Text file saved successfully.")


def toggle_theme():
    global dark_mode
    dark_mode = not dark_mode
    bg = "#1e1e1e" if dark_mode else "#f0f0f0"
    fg = "white" if dark_mode else "black"
    root.config(bg=bg)
    for widget in root.winfo_children():
        if isinstance(widget, (tk.Button, tk.Label)):
            widget.config(bg=bg, fg=fg)
    output_box.config(bg=bg, fg=fg, insertbackground=fg)


# GUI Setup
root = tk.Tk()
root.title("🔗 Advanced URL Analyzer")
root.geometry("950x650")

frame = tk.Frame(root)
frame.pack(pady=10)

button_style = {"padx": 6, "pady": 4, "font": ("Segoe UI", 10, "bold")}

btn1 = tk.Button(frame, text="📋 Analyze Clipboard", command=analyze_clipboard, **button_style)
btn1.grid(row=0, column=0, padx=6)

btn2 = tk.Button(frame, text="📁 Upload .txt", command=load_txt_file, **button_style)
btn2.grid(row=0, column=1, padx=6)

btn3 = tk.Button(frame, text="💾 Export TXT", command=export_as_txt, **button_style)
btn3.grid(row=0, column=2, padx=6)

btn4 = tk.Button(frame, text="📄 Export PDF", command=export_as_pdf, **button_style)
btn4.grid(row=0, column=3, padx=6)

btn5 = tk.Button(frame, text="🌓 Toggle Theme", command=toggle_theme, **button_style)
btn5.grid(row=0, column=4, padx=6)

output_box = scrolledtext.ScrolledText(root, height=25, wrap=tk.WORD, font=("Consolas", 10))
output_box.pack(fill="both", expand=True, padx=10, pady=10)
output_box.analysis_results = []
output_box.secure_count = 0
output_box.insecure_count = 0

output_box.tag_config("link", foreground="blue", underline=1)

def on_click(event):
    index = output_box.index("@%s,%s" % (event.x, event.y))
    for tag in output_box.tag_names(index):
        if tag.startswith("url:"):
            url = tag.split(":", 1)[1]
            webbrowser.open(url)
            return

def add_clickable_links():
    output_box.tag_remove("link", "1.0", tk.END)
    text = output_box.get("1.0", tk.END)
    urls = extract_urls(text)
    for url in urls:
        start = "1.0"
        while True:
            pos = output_box.search(url, start, stopindex=tk.END)
            if not pos:
                break
            end = f"{pos}+{len(url)}c"
            output_box.tag_add(f"url:{url}", pos, end)
            output_box.tag_config(f"url:{url}", foreground="blue", underline=1)
            start = end

output_box.bind("<Button-1>", on_click)
output_box.bind("<KeyRelease>", lambda e: add_clickable_links())

dark_mode = False

root.mainloop()
