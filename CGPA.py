"""
CGPA Calculator
Calculates semester GPA and class of degree, then saves the result to a file.
"""

from datetime import datetime

RESULT_FILE = "gpa_results.txt"


# ---------- Input helpers ----------

def get_text(prompt):
    """Ask for text and keep asking until it is not empty."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("  Error: This field cannot be empty.")


def get_int(prompt, minimum, maximum):
    """Ask for a whole number between minimum and maximum (inclusive)."""
    while True:
        try:
            value = int(input(prompt).strip())
        except ValueError:
            print("  Error: Please enter a whole number.")
            continue
        if minimum <= value <= maximum:
            return value
        print(f"  Error: Enter a number between {minimum} and {maximum}.")


def get_score(prompt):
    """Ask for a score between 0 and 100 until a valid one is entered."""
    while True:
        try:
            score = float(input(prompt).strip())
        except ValueError:
            print("  Error: Score must be a number.")
            continue
        if 0 <= score <= 100:
            return score
        print("  Error: Score must be between 0 and 100.")


# ---------- Core logic ----------

def score_to_grade(score):
    """Convert a score to (letter grade, grade point)."""
    if score >= 70:
        return "A", 5
    elif score >= 60:
        return "B", 4
    elif score >= 50:
        return "C", 3
    elif score >= 45:
        return "D", 2
    elif score >= 40:
        return "E", 1
    else:
        return "F", 0


def get_course_details(number):
    """Collect and return the details of one course as a dictionary."""
    print(f"\n--- Course {number} ---")
    code = get_text("Course code (e.g. CSC 101): ").upper()
    units = get_int("Credit unit (1 - 6): ", 1, 6)
    score = get_score("Score (0 - 100): ")
    grade, point = score_to_grade(score)
    return {
        "code": code,
        "units": units,
        "score": score,
        "grade": grade,
        "point": point,
        "weighted": units * point,   # credit unit x grade point
    }


def calculate_gpa(courses):
    """Return (total credit units, total grade points, GPA)."""
    total_units = sum(c["units"] for c in courses)
    total_points = sum(c["weighted"] for c in courses)
    gpa = total_points / total_units if total_units > 0 else 0.0
    return total_units, total_points, gpa


def get_class_of_degree(gpa):
    """Return the class of degree for a given GPA (5.0 scale)."""
    if gpa >= 4.50:
        return "First Class"
    elif gpa >= 3.50:
        return "Second Class Upper"
    elif gpa >= 2.40:
        return "Second Class Lower"
    elif gpa >= 1.50:
        return "Third Class"
    elif gpa >= 1.00:
        return "Pass"
    else:
        return "Fail"


# ---------- Output ----------

def build_report(name, department, courses, total_units, total_points, gpa, degree_class):
    """Build the result as a single string (used for display and saving)."""
    line = "=" * 62
    lines = [
        line,
        "SEMESTER RESULT",
        line,
        f"Name       : {name}",
        f"Department : {department}",
        f"Date       : {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "-" * 62,
        f"{'Course':<12}{'Units':>6}{'Score':>8}{'Grade':>8}{'GP':>5}{'Units x GP':>13}",
        "-" * 62,
    ]
    for c in courses:
        lines.append(
            f"{c['code']:<12}{c['units']:>6}{c['score']:>8.1f}"
            f"{c['grade']:>8}{c['point']:>5}{c['weighted']:>13}"
        )
    lines += [
        "-" * 62,
        f"Total Credit Units : {total_units}",
        f"Total Grade Points : {total_points}",
        f"GPA                : {gpa:.2f}",
        f"Class of Degree    : {degree_class}",
        line,
    ]
    return "\n".join(lines)


def save_to_file(report):
    """Append the report to the results file. Returns True if it worked."""
    try:
        with open(RESULT_FILE, "a", encoding="utf-8") as f:
            f.write(report + "\n\n")
        return True
    except OSError as error:
        print(f"Could not save the result: {error}")
        return False


# ---------- Main program ----------

def main():
    print("=== CGPA CALCULATOR ===\n")
    name = get_text("Enter your name: ")
    department = get_text("Enter your department: ")
    num_courses = get_int("How many courses are you offering? ", 1, 20)

    courses = [get_course_details(i) for i in range(1, num_courses + 1)]

    total_units, total_points, gpa = calculate_gpa(courses)
    degree_class = get_class_of_degree(gpa)

    report = build_report(name, department, courses,
                          total_units, total_points, gpa, degree_class)
    print("\n" + report)

    if save_to_file(report):
        print(f"\nResult saved to '{RESULT_FILE}'.")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n\nProgram stopped. Goodbye!")
