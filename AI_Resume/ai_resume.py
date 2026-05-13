import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import PyPDF2
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class ResumeAnalyzer:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Resume Matcher & Skill Extractor")
        self.root.geometry("800x700")
        self.root.configure(bg="#f0f2f5")

        self.resume_text = ""
        self.setup_ui()

    def setup_ui(self):
        # Header
        tk.Label(self.root, text="📄 AI Resume Analyzer", font=("Arial", 20, "bold"), bg="#f0f2f5", fg="#1a73e8").pack(pady=20)

        # Job Description Area
        tk.Label(self.root, text="Paste Job Description:", bg="#f0f2f5", font=("Arial", 10, "bold")).pack(anchor="w", padx=50)
        self.jd_area = scrolledtext.ScrolledText(self.root, height=8, width=80, font=("Arial", 10))
        self.jd_area.pack(pady=5)

        # Action Buttons
        btn_frame = tk.Frame(self.root, bg="#f0f2f5")
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Upload Resume (PDF)", command=self.upload_resume, bg="#34a853", fg="white", padx=20).pack(side="left", padx=10)
        tk.Button(btn_frame, text="Analyze Match", command=self.analyze_match, bg="#1a73e8", fg="white", padx=20).pack(side="left", padx=10)

        # Results Display
        self.result_area = scrolledtext.ScrolledText(self.root, height=12, width=80, bg="#ffffff", font=("Consolas", 10))
        self.result_area.pack(pady=20)

    def upload_resume(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if file_path:
            try:
                with open(file_path, 'rb') as pdf_file:
                    reader = PyPDF2.PdfReader(pdf_file)
                    self.resume_text = ""
                    for page in reader.pages:
                        self.resume_text += page.extract_text()
                messagebox.showinfo("Success", "Resume uploaded and parsed successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Could not read PDF: {e}")

    def extract_skills(self, text):
        # A simple list of skills to look for. In a pro version, use a larger dataset or Spacy.
        skill_db = ["Python", "Java", "SQL", "Machine Learning", "Data Analysis", "Project Management", "React", "AWS", "Docker", "Excel"]
        found_skills = [skill for skill in skill_db if re.search(r'\b' + re.escape(skill) + r'\b', text, re.IGNORECASE)]
        return found_skills

    def analyze_match(self):
        jd_text = self.jd_area.get("1.0", tk.END).strip()
        if not jd_text or not self.resume_text:
            messagebox.showwarning("Input Missing", "Please paste a Job Description and upload a Resume.")
            return

        # 1. Match Score Calculation (Cosine Similarity)
        text_list = [self.resume_text, jd_text]
        cv = CountVectorizer()
        count_matrix = cv.fit_transform(text_list)
        match_percentage = cosine_similarity(count_matrix)[0][1] * 100

        # 2. Skill Extraction
        resume_skills = self.extract_skills(self.resume_text)
        jd_skills = self.extract_skills(jd_text)
        missing_skills = list(set(jd_skills) - set(resume_skills))

        # 3. Display Results
        self.result_area.delete("1.0", tk.END)
        self.result_area.insert(tk.END, f"MATCH SCORE: {match_percentage:.2f}%\n")
        self.result_area.insert(tk.END, "-"*40 + "\n")
        self.result_area.insert(tk.END, f"Detected Skills: {', '.join(resume_skills)}\n\n")
        
        if missing_skills:
            self.result_area.insert(tk.END, "SUGGESTED IMPROVEMENTS:\n")
            self.result_area.insert(tk.END, f"Your resume is missing these key skills found in the JD:\n")
            for skill in missing_skills:
                self.result_area.insert(tk.END, f"- {skill}\n")
        else:
            self.result_area.insert(tk.END, "Excellent! You have all the key skills mentioned.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ResumeAnalyzer(root)
    root.mainloop()