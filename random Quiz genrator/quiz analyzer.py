import tkinter as tk
from tkinter import ttk, messagebox
import random

# Quiz Data: Question and multiple-choice answers (A, B, C, D), and the correct one
quiz_data = [
    ("What does CIA triad stand for in cybersecurity?",
     ["Confidentiality, Integrity, Availability", "Central Intelligence Agency", "Control, Integrity, Access", "Confidentiality, Internet, Access"],
     "A"),

    ("Which of the following is a strong password?",
     ["password123", "qwerty", "P@55w0rd!", "12345678"],
     "C"),

    ("Which tool is commonly used for network penetration testing?",
     ["Wireshark", "Metasploit", "Nmap", "Notepad"],
     "B"),

    ("What is phishing?",
     ["A way to encrypt data", "A social engineering attack to steal credentials", "A type of firewall", "A network protocol"],
     "B"),

    ("Which one is an antivirus software?",
     ["BitLocker", "Norton", "Tor", "VirtualBox"],
     "B"),

    ("Which layer does a firewall typically operate on?",
     ["Physical", "Data Link", "Network", "Application"],
     "C"),

    ("What does 2FA stand for?",
     ["Two-Factor Authentication", "Two-Firewall Access", "Two-File Authority", "None of the above"],
     "A"),

    ("What port does HTTPS use by default?",
     ["80", "443", "21", "22"],
     "B"),

    ("What is the main purpose of encryption?",
     ["Compress files", "Speed up download", "Protect data confidentiality", "Improve performance"], "C"),

    ("What is a VPN used for?", ["Faster browsing", "Game enhancement", "Secure remote connection", "Backup files"], "C"),

    ("Which is a common attack type?", ["SQL Injection", "Java Loop", "CSS Break", "HTML Hack"],
    "A"),

    ("What is malware?",
     ["A type of software license", "Malicious software", "Safe application", "Security protocol"],
     "B"),

    ("What is brute force attack?",
     ["Trying many passwords to gain access", "Email scam", "DDoS attack", "None"],
     "A"),

    ("Which of these is a security protocol?",
     ["HTTP", "FTP", "SSH", "PNG"],
     "C"),

    ("What is a digital certificate used for?",
     ["To improve WiFi", "To validate identity online", "To speed up downloads", "To access admin panel"],
     "B"),

    ("Which is a secure way to connect remotely?",
     ["Telnet", "FTP", "RDP over VPN", "Unsecured Wi-Fi"],
     "C"),

    ("What does DDoS stand for?",
     ["Dedicated Data Operating System", "Distributed Denial of Service", "Domain Defender of System", "None"],
     "B"),

    ("Which OS is most used for hacking?",
     ["Ubuntu", "Windows", "Kali Linux", "macOS"],
     "C"),

    ("Which device filters traffic in and out of a network?",
     ["Monitor", "Router", "Firewall", "Switch"],
     "C"),

    ("Which file extension is used for Python scripts?",
     [".txt", ".py", ".exe", ".bin"],
     "B"),
]

random.shuffle(quiz_data)

class CyberQuizApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Cybersecurity Quiz")
        self.geometry("900x600")
        self.configure(bg='#1e1e2f')
        self.current_q = 0
        self.score = 0
        self.user_answers = []
        self.name = tk.StringVar()
        self.date = tk.StringVar()
        self.period = tk.StringVar()
        self.build_intro_screen()

    def build_intro_screen(self):
        for widget in self.winfo_children(): widget.destroy()

        title = tk.Label(self, text="Cybersecurity Quiz", font=("Arial", 28, "bold"), fg="white", bg="#1e1e2f")
        title.pack(pady=30)

        form_frame = tk.Frame(self, bg="#1e1e2f")
        form_frame.pack(pady=20)

        tk.Label(form_frame, text="Name:", font=("Arial", 16), fg="white", bg="#1e1e2f").grid(row=0, column=0, padx=10, pady=10, sticky='e')
        tk.Entry(form_frame, textvariable=self.name, font=("Arial", 16), width=25).grid(row=0, column=1)

        tk.Label(form_frame, text="Date:", font=("Arial", 16), fg="white", bg="#1e1e2f").grid(row=1, column=0, padx=10, pady=10, sticky='e')
        tk.Entry(form_frame, textvariable=self.date, font=("Arial", 16), width=25).grid(row=1, column=1)

        tk.Label(form_frame, text="Period:", font=("Arial", 16), fg="white", bg="#1e1e2f").grid(row=2, column=0, padx=10, pady=10, sticky='e')
        tk.Entry(form_frame, textvariable=self.period, font=("Arial", 16), width=25).grid(row=2, column=1)

        tk.Button(self, text="Start Quiz", font=("Arial", 18, "bold"), bg="#00bcd4", fg="white",
                  command=self.start_quiz).pack(pady=40)

    def start_quiz(self):
        self.current_q = 0
        self.score = 0
        self.user_answers = []
        self.build_quiz_screen()

    def build_quiz_screen(self):
        for widget in self.winfo_children(): widget.destroy()

        if self.current_q >= len(quiz_data):
            self.show_result()
            return

        question, options, _ = quiz_data[self.current_q]

        tk.Label(self, text=f"Q{self.current_q+1}: {question}", font=("Arial", 18, "bold"), wraplength=800,
                 fg="white", bg="#1e1e2f").pack(pady=40)

        self.selected_option = tk.StringVar()

        for i, option in enumerate(options):
            tk.Radiobutton(self, text=option, variable=self.selected_option, value='ABCD'[i],
                           font=("Arial", 16), bg="#2e2e3f", fg="white", selectcolor="#00bcd4", wraplength=750,
                           indicatoron=1, width=70, anchor='w', padx=20).pack(pady=8)

        tk.Button(self, text="Next", font=("Arial", 16, "bold"), bg="#4caf50", fg="white",
                  command=self.check_answer).pack(pady=30)

    def check_answer(self):
        if not self.selected_option.get():
            messagebox.showwarning("No Selection", "Please select an answer before continuing.")
            return

        _, _, correct = quiz_data[self.current_q]
        if self.selected_option.get() == correct:
            self.score += 1
        self.user_answers.append(self.selected_option.get())
        self.current_q += 1
        self.build_quiz_screen()

    def show_result(self):
        for widget in self.winfo_children(): widget.destroy()

        result = f"Thanks, {self.name.get()}!\nYou scored {self.score} out of {len(quiz_data)}."
        tk.Label(self, text=result, font=("Arial", 22, "bold"), fg="white", bg="#1e1e2f").pack(pady=100)

        tk.Button(self, text="Exit", font=("Arial", 16, "bold"), bg="red", fg="white", command=self.quit).pack()


if __name__ == '__main__':
    app = CyberQuizApp()
    app.mainloop()
