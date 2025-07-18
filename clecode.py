from fpdf import FPDF
import csv

# Academic Marks for 4 Students
students_marks = {
    "Alice": {"Python": 88, "Java": 85, "C++": 89, "C": 87},
    "Bob": {"Python": 75, "Java": 70, "C++": 78, "C": 68},
    "Charlie": {"Python": 95, "Java": 92, "C++": 89, "C": 90},
    "David": {"Python": 55, "Java": 60, "C++": 58, "C": 57}
}

# Competition Result Positions
competition_positions = {
    "Debugging":     {"Charlie": "First", "Bob": "Third", "Daniela": "Second", "Satya": "Runner"},
    "Essay Writing": {"Charlie": "Second", "Bob": "First", "Daniela": "Runner", "Satya": "Third"},
    "Coding":        {"Charlie": "Second", "Bob": "Third", "Daniela": "First", "Satya": "Second"},
    "Drawing":       {"Charlie": "Runner", "Bob": "Second", "Daniela": "Third", "Satya": "First"}
}

#  Classification Rule
def classify(avg):
    if avg >= 90:
        return "First Class"
    elif avg >= 80:
        return "Second Class"
    elif avg >= 60:
        return "Third Class"
    else:
        return "Fail"

#  PDF Report Class
class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 14)
        title = (
            "Programming Language Mark Report"
            if self.page_no() in [1, 2]
            else "Competition Result Positions"
        )
        self.cell(0, 10, title, ln=True, align="C")
        self.ln(4)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 10)
        self.cell(0, 10, f"Page {self.page_no()}", 0, 0, "C")

    def add_student_table(self, name, subjects):
        total = sum(subjects.values())
        average = round(total / len(subjects), 2)
        out_of = len(subjects) * 100
        classi = classify(average)

        self.set_font("Arial", "B", 12)
        self.cell(0, 10, f"Student: {name}", ln=True)

        # Total and Average at the Top
        self.set_font("Arial", "", 11)
        self.cell(0, 8, f"Total Marks: {total}     Out of: {out_of}     Average: {average}", ln=True)
        self.ln(1)

        # Table Header
        self.set_font("Arial", "B", 11)
        self.cell(80, 10, "Subject", 1)
        self.cell(40, 10, "Mark", 1)
        self.ln()

        # Subject rows
        self.set_font("Arial", "", 11)
        for subject, mark in subjects.items():
            self.cell(80, 10, subject, 1)
            self.cell(40, 10, str(mark), 1)
            self.ln()

        # Classification below
        self.set_font("Arial", "B", 11)
        self.cell(0, 10, f"Classification: {classi}", ln=True)
        self.ln(5)

    def add_competition_table(self, positions):
        self.set_font("Arial", "B", 12)
        self.cell(45, 10, "Competition", 1)
        names = list(next(iter(positions.values())).keys())
        for name in names:
            self.cell(35, 10, name, 1)
        self.ln()

        self.set_font("Arial", "", 11)
        for event, results in positions.items():
            self.cell(45, 10, event, 1)
            for name in names:
                self.cell(35, 10, results.get(name, "-"), 1)
            self.ln()

# Generate PDF
pdf = PDF()

# Page 1: Alice & Bob
pdf.add_page()
pdf.add_student_table("Alice", students_marks["Alice"])
pdf.add_student_table("Bob", students_marks["Bob"])

# Page 2: Charlie & David
pdf.add_page()
pdf.add_student_table("Charlie", students_marks["Charlie"])
pdf.add_student_table("David", students_marks["David"])

# Page 3: Competition
pdf.add_page()
pdf.add_competition_table(competition_positions)

#  Save PDF
pdf.output("/storage/emulated/0/Download/student_report.pdf")

# Save CSV with Comments
with open("/storage/emulated/0/Download/student_report.csv", "w", encoding="utf-8", newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Student", "Subject", "Mark", "Comment"])
    for student, subjects in students_marks.items():
        for subject, mark in subjects.items():
            comment = " Very Good" if mark >= 85 else "Need Improvement"
            writer.writerow([student, subject, mark, comment])

print(" PDF & CSV reports generated successfully in Download folder!")
