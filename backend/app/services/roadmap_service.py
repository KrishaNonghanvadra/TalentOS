from sqlalchemy.orm import Session

from app.models.job import Job
from app.models.student_profile import StudentProfile

from app.services.job_matching_service import calculate_job_match


ROADMAP_TOPICS = {
    "python": [
        ("Python Fundamentals", "Revise variables, data types, conditions, loops and functions."),
        ("Object-Oriented Programming", "Learn classes, objects, inheritance, encapsulation and polymorphism."),
        ("Python Data Structures", "Practice lists, tuples, sets, dictionaries and common operations."),
        ("Exception Handling", "Learn try, except, finally and custom exceptions."),
        ("Python Projects", "Build a practical Python project using the concepts you learned.")
    ],

    "sql": [
        ("SQL Fundamentals", "Learn SELECT, INSERT, UPDATE, DELETE and basic database concepts."),
        ("Filtering Data", "Practice WHERE, ORDER BY, LIMIT and filtering conditions."),
        ("SQL JOINs", "Learn INNER JOIN, LEFT JOIN, RIGHT JOIN and relationships between tables."),
        ("Aggregation", "Practice COUNT, SUM, AVG, MIN, MAX and GROUP BY."),
        ("Subqueries", "Learn nested queries and correlated subqueries."),
        ("SQL Practice", "Solve SQL problems using realistic datasets.")
    ],

    "java": [
        ("Java Fundamentals", "Revise variables, conditions, loops, arrays and methods."),
        ("Object-Oriented Programming", "Learn classes, objects, inheritance, abstraction and interfaces."),
        ("Collections Framework", "Learn List, Set, Map and their common implementations."),
        ("Exception Handling", "Practice checked and unchecked exceptions."),
        ("Java DSA Practice", "Solve data structure and algorithm problems using Java.")
    ],

    "javascript": [
        ("JavaScript Fundamentals", "Learn variables, functions, conditions, loops and arrays."),
        ("DOM Manipulation", "Learn how JavaScript interacts with HTML elements."),
        ("ES6+", "Learn let, const, arrow functions, destructuring and modules."),
        ("Asynchronous JavaScript", "Learn promises, async/await and API requests."),
        ("JavaScript Projects", "Build practical projects using JavaScript.")
    ],

    "html": [
        ("HTML Fundamentals", "Learn semantic HTML elements and page structure."),
        ("Forms", "Learn form elements, validation and user input."),
        ("Accessibility", "Learn semantic structure and accessible HTML practices.")
    ],

    "css": [
        ("CSS Fundamentals", "Learn selectors, properties, box model and positioning."),
        ("Flexbox", "Learn flexible layouts using Flexbox."),
        ("CSS Grid", "Build responsive layouts using CSS Grid."),
        ("Responsive Design", "Make websites work across different screen sizes.")
    ]
}


def get_roadmap_for_skill(skill_name: str):
    skill_key = skill_name.lower()

    if skill_key in ROADMAP_TOPICS:
        return ROADMAP_TOPICS[skill_key]

    return [
        (
            f"{skill_name} Fundamentals",
            f"Learn the fundamental concepts of {skill_name}."
        ),
        (
            f"{skill_name} Intermediate Concepts",
            f"Practice intermediate concepts and common problems in {skill_name}."
        ),
        (
            f"{skill_name} Practical Project",
            f"Build a practical project using {skill_name}."
        )
    ]


def generate_learning_roadmap(
    db: Session,
    student_profile: StudentProfile,
    job: Job
):
    match_result = calculate_job_match(
        db,
        student_profile,
        job
    )

    tasks = []

    for gap in match_result["skill_gaps"]:

        skill_name = gap["skill"]
        priority = gap["priority"]

        topics = get_roadmap_for_skill(skill_name)

        for topic, description in topics:

            tasks.append({
                "skill": skill_name,
                "priority": priority,
                "topic": topic,
                "description": description
            })

    priority_order = {
        "High": 1,
        "Medium": 2,
        "Low": 3
    }

    tasks.sort(
        key=lambda task: priority_order.get(
            task["priority"],
            4
        )
    )

    return {
        "job_id": job.id,
        "job_title": job.title,
        "company": job.company,
        "tasks": tasks
    }