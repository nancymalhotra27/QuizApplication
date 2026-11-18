import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector
from pathlib import Path

''' DATABASE '''

def connect_db():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="simran@2121",
            database="quiz_app"
        )
    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", f"Connection failed: {e}")
        return None

def setup_database():
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS results (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(50),
            score INT,
            language VARCHAR(20)
        )
        """)
        cursor.execute("SHOW COLUMNS FROM results LIKE 'language'")
        if cursor.fetchone() is None:
            cursor.execute("ALTER TABLE results ADD COLUMN language VARCHAR(20)")
        conn.commit()
        conn.close()

''' QUESTIONS '''
quiz_questions = {
    "Python": [
        ("1. What is a function in Python?", ["Keyword", "Type of variable", "Imported library", "A block of code that performs a specific task"], "A block of code that performs a specific task"),
        ("2. Which keyword defines a function?", ["func", "def", "class", "void"], "def"),
        ("3. What is true about lists?", ["Dynamic arrays", "Stores references contiguously", "Can contain different types", "All of the above"], "All of the above"),
        ("4. What can Python do?", ["Web Development", "Machine Learning", "Game Development", "All"], "All"),
        ("5. Which of the following Web frameworks is used in python?", ["Django/Flask", "TensorFlow/PyTorch", "Tkinter/PyQt", "Pandas/NumPy"], "Django/Flask"),
        ("6. Properties of Variables are?", ["Must be declared", "Only letters", "Case sensitive", "Cannot be reassigned"], "Case sensitive"),
        ("7. How to take User input?", ["input()", "get_input()", "user_input()", "read_input()"], "input()"),
        ("8. Which of the following are Data structures?", ["list", "tuple", "dictionary", "All"], "All"),
        ("9. NumPy is imported as?", ["np", "nUmpy", "numPY", "numpy"], "np"),
        ("10. which of the following is a database used in python?", ["MySQL", "DSA", "GUI", "class"], "MySQL")
    ],
    "C++": [
        ("1. What is C++?", ["Scripting language", "Compiled language", "Markup language", "Database"], "Compiled language"),
        ("2. Header for input/output?", ["<iostream>", "<stdio.h>", "<math.h>", "<file>"], "<iostream>"),
        ("3. What is Output stream?", ["cin", "cout", "print", "echo"], "cout"),
        ("4. What is Input stream?", ["cin", "scan", "input", "read"], "cin"),
        ("5. Does it have OOP support?", ["Yes", "No", "Partial", "None"], "Yes"),
        ("6. How the Loop keyword is defined?", ["for", "loop", "repeat", "iterate"], "for"),
        ("7. How to add a Comment?", ["//", "#", "/*", "--"], "//"),
        ("8. Which of these is a Data type?", ["int", "integer", "number", "num"], "int"),
        ("9. How to declare Main function?", ["main()", "start()", "run()", "init()"], "main()"),
        ("10. Which one is Pointer symbol?", ["&", "*", "#", "@"], "*")
    ],
    "Java": [
        ("1. What is Java?", ["Compiled", "Interpreted", "Both", "None"], "Both"),
        ("2. JVM stands for?", ["Java Virtual Machine", "Java Variable Manager", "Just Virtual Memory", "None"], "Java Virtual Machine"),
        ("3. Which one is Correct Print statement?", ["System.out.println", "print", "echo", "write"], "System.out.println"),
        ("4. Does it support OOP?", ["Yes", "No", "Partial", "None"], "Yes"),
        ("5. How the Loop is defined in java?", ["for", "loop", "repeat", "iterate"], "for"),
        ("6. how comments are added in java?", ["//", "#", "--", "/*"], "//"),
        ("7. which of the following is a valid Data type?", ["int", "integer", "number", "num"], "int"),
        ("8. which one is valid Class keyword?", ["class", "define", "object", "struct"], "class"),
        ("9. How to use Main method?", ["main()", "start()", "run()", "init()"], "main()"),
        ("10. Which of these is a Package for GUI?", ["java.awt", "java.io", "java.util", "java.net"], "java.awt")
    ]
}

questions = []
q_index = 0
score = 0
selected_lang = ""
time_left = 10
timer_id = None
quiz_started = False
quiz_win = None
timeout_label = None

def select_language(lang):
    global questions, selected_lang
    selected_lang = lang
    questions = quiz_questions.get(lang, [])
    messagebox.showinfo("Selected", f"{lang} selected. Click Start Quiz.")

def start_quiz():
    global q_index, score, quiz_started
    name = name_entry.get()
    if name.strip() == "" or name == "Enter your name":
        messagebox.showerror("Error", "Enter your name")
        return
    if not questions:
        messagebox.showwarning("Select Language", "Please select a language first!")
        return
    q_index = 0
    score = 0
    quiz_started = True
    main_frame.pack_forget()
    open_quiz_window()
    root.after(100, load_question)

def open_quiz_window():
    global quiz_win, selected_option, timer_label, score_label, frame, question_label, option_buttons, next_btn, timeout_label
    quiz_win = tk.Toplevel(root)
    quiz_win.title(f"{selected_lang} Quiz")
    quiz_win.configure(bg="#1e1e2f")
    quiz_win.geometry(f"{width}x{height}+0+0")
    quiz_win.protocol("WM_DELETE_WINDOW", lambda: None)

    selected_option = tk.StringVar(value="")

    timer_label = tk.Label(quiz_win, text="Time: 10", font=("Arial", 12, "bold"), bg="#1e1e2f", fg="#ff4d4d")
    timer_label.pack(pady=5)
    score_label = tk.Label(quiz_win, text="Score: 0", font=("Arial", 12), bg="#1e1e2f", fg="#00ffcc")
    score_label.pack(pady=5)

    timeout_label = tk.Label(quiz_win, text="", font=("Arial", 14, "bold"), bg="#1e1e2f", fg="#ffaa00")
    timeout_label.pack(pady=5)

    frame = tk.Frame(quiz_win, bg="#2b2b3c", bd=2, relief="ridge")
    frame.pack(pady=scale(15), padx=scale(50), fill="both", expand=True)
    frame.config(width=scale(700), height=scale(350))
    frame.pack_propagate(False)

    question_label = tk.Label(frame, text="", wraplength=scale(400), font=("Arial", scale(13)), bg="#2b2b3c", fg="white", justify="left")
    question_label.pack(pady=scale(20), anchor="w", padx=10)

    option_buttons = []
    for _ in range(4):
        btn = tk.Radiobutton(
            frame,
            text="",
            variable=selected_option,
            value="",
            font=("Arial", scale(11)),
            bg="#2b2b3c",
            fg="white",
            anchor="w",
            justify="left",
            selectcolor="#444",
            activebackground="#2b2b3c"
        )
        btn.pack(fill="x", pady=scale(5), padx=scale(20))
        option_buttons.append(btn)

    next_btn = tk.Button(quiz_win, text="Next", font=("Arial", 12, "bold"), bg="#00cc99", fg="black", command=next_question)
    next_btn.pack(pady=10)

def start_timer():
    global time_left, timer_id
    timer_label.config(text=f"Time: {time_left}")
    if time_left > 0:
        time_left -= 1
        timer_id = root.after(1500, start_timer)
    else:
        next_question()

def load_question():
    global q_index, time_left, timer_id
    if timer_id:
        root.after_cancel(timer_id)
        timer_id = None
    if q_index < len(questions):
        time_left = 10
        selected_option.set("")
        q, options, _ = questions[q_index]
        question_label.config(text=q)
        for i, option in enumerate(options):
            option_buttons[i].config(text=option, value=option)
        quiz_win.update_idletasks()
        start_timer()
    else:
        finish_quiz()

def next_question():
    global q_index, score
    if not quiz_started:
        messagebox.showwarning("Start Quiz", "Please click Start Quiz first!")
        return
    if q_index < len(questions):
        selected = selected_option.get()
        if selected == questions[q_index][2]:
            score += 1
        score_label.config(text=f"Score: {score}")
        q_index += 1
    load_question()

def finish_quiz():
    global quiz_started, timer_id
    if timer_id:
        root.after_cancel(timer_id)
        timer_id = None
    name = name_entry.get()
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO results (name, language, score) VALUES (%s, %s, %s)",
                (name, selected_lang, score)
            )
            conn.commit()
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", str(e))
        finally:
            conn.close()
    messagebox.showinfo("Result", f"{name}, Your Score: {score}/{len(questions)}")
    quiz_win.destroy()
    quiz_started = False
    main_frame.pack(expand=True)
    show_results()

def show_results():
    result_window = tk.Toplevel(root)
    result_window.title("Results Dashboard")
    result_window.geometry("600x400")
    result_window.configure(bg="#1e1e2f")

    title = tk.Label(result_window, text="🏆 Quiz Results", font=("Arial", 16, "bold"), bg="#1e1e2f", fg="white")
    title.pack(pady=10)

    frame = tk.Frame(result_window, bg="#2b2b3c")
    frame.pack(pady=20, padx=20, fill="both", expand=True)

    scrollbar = tk.Scrollbar(frame)
    scrollbar.pack(side="right", fill="y")

    style = ttk.Style()
    style.theme_use("default")
    style.configure("Treeview", background="#2b2b3c", foreground="white", rowheight=25, fieldbackground="#2b2b3c")
    style.map("Treeview", background=[("selected", "#00cc99")])

    tree = ttk.Treeview(frame, columns=("ID", "Name", "Language", "Score"), show="headings", yscrollcommand=scrollbar.set)
    tree.heading("ID", text="ID")
    tree.heading("Name", text="Name")
    tree.heading("Language", text="Language")
    tree.heading("Score", text="Score")
    tree.column("ID", width=50, anchor="center")
    tree.column("Name", width=150, anchor="center")
    tree.column("Language", width=120, anchor="center")
    tree.column("Score", width=100, anchor="center")
    tree.pack(fill="both", expand=True)
    scrollbar.config(command=tree.yview)

    try:
        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, language, score FROM results ORDER BY Id ASC")
            rows = cursor.fetchall()
            for row in rows:
                tree.insert("", tk.END, values=row)
            conn.close()
    except mysql.connector.Error as e:
        messagebox.showerror("Error", str(e))

    btn_frame = tk.Frame(result_window, bg="#1e1e2f")
    btn_frame.pack(pady=10)

    def clear_results():
        if messagebox.askyesno("Confirm", "Delete all results?"):
            conn = connect_db()
            if conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM results")
                conn.commit()
                conn.close()
                tree.delete(*tree.get_children())
                messagebox.showinfo("Done", "Results cleared!")

    clear_btn = tk.Button(btn_frame, text="Clear Results", bg="#ff4d4d", fg="white", font=("Arial", 10, "bold"), command=clear_results)
    clear_btn.grid(row=0, column=0, padx=10)
    close_btn = tk.Button(btn_frame, text="Close", bg="#00cc99", fg="black", font=("Arial", 10, "bold"), command=result_window.destroy)
    close_btn.grid(row=0, column=1, padx=10)

''' GUI '''
root = tk.Tk()
root.title("Quiz App")
root.configure(bg="#1e1e2f")
width = root.winfo_screenwidth() - 10
height = root.winfo_screenheight() - 90
root.geometry(f"{width}x{height}+0+0")
# Quiz icon source: https://img.icons8.com/ios/100/quiz.png
icon_image = tk.PhotoImage(file=str(Path(__file__).with_name("quiz_icon.png")))
root.iconphoto(True, icon_image)

scale_w = width / 1366
scale_h = height / 768

def scale(value):
    return int(value * min(scale_w, scale_h))

main_frame = tk.Frame(root, bg="#1e1e2f")
main_frame.pack(expand=True)

title = tk.Label(main_frame, text="Quiz Application", font=("Arial", 26, "bold"), bg="#1e1e2f", fg="#ffffff")
title.pack(pady=scale(20))

name_entry = tk.Entry(main_frame, font=("Arial", 14), width=25, justify="center")
name_entry.insert(0, "Enter your name")
name_entry.pack(pady=scale(10))

def on_focus_in(event):
    if name_entry.get() == "Enter your name":
        name_entry.delete(0, tk.END)
        name_entry.config(fg="black")

def on_focus_out(event):
    if name_entry.get() == "":
        name_entry.insert(0, "Enter your name")
        name_entry.config(fg="grey")

name_entry.bind("<FocusIn>", on_focus_in)
name_entry.bind("<FocusOut>", on_focus_out)
name_entry.config(fg="grey")

lang_frame = tk.Frame(main_frame, bg="#1e1e2f")
lang_frame.pack(pady=scale(20))

tk.Label(lang_frame, text="Select Language:", bg="#1e1e2f", fg="white", font=("Arial", 12, "bold")).pack(side="left", padx=scale(5))
tk.Button(lang_frame, text="Python", command=lambda: select_language("Python"), bg="#306998", fg="white").pack(side="left", padx=scale(5))
tk.Button(lang_frame, text="C++", command=lambda: select_language("C++"), bg="#00599C", fg="white").pack(side="left", padx=scale(5))
tk.Button(lang_frame, text="Java", command=lambda: select_language("Java"), bg="#b07219", fg="white").pack(side="left", padx=scale(5))

start_btn = tk.Button(main_frame, text="Start Quiz", font=("Arial", 14, "bold"), bg="#ffaa00", fg="black", width=scale(15), command=start_quiz)
start_btn.pack(pady=25)

view_btn = tk.Button(main_frame, text="View Results", font=("Arial", 10), bg="#cccccc", command=show_results)
view_btn.pack()

setup_database()
root.mainloop()