
import os
import time
from google import genai


# Gemini model configuration
MODEL_NAME = "gemini-3.6-flash"


def get_gemini_client():
    """Create a Gemini client using the secure API key."""
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return None

    return genai.Client(api_key=api_key)


def generate_with_retry(client, prompt, max_attempts=3):
    """
    Generate Gemini content with retries for temporary service errors.
    Waits 2 seconds, then 4 seconds before retrying.
    """
    for attempt in range(max_attempts):
        try:
            return client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt
            )

        except Exception as error:
            error_message = str(error).upper()

            temporary_error = any(
                message in error_message
                for message in [
                    "503",
                    "UNAVAILABLE",
                    "429",
                    "RESOURCE_EXHAUSTED"
                ]
            )

            # Do not retry permanent errors or the final attempt.
            if not temporary_error or attempt == max_attempts - 1:
                raise

            wait_time = 2 ** (attempt + 1)

            print(
                f"Gemini is temporarily unavailable. "
                f"Retrying in {wait_time} seconds..."
            )

            time.sleep(wait_time)


def basic_tutor_answer(question):
    """Provide a simple predefined answer if Gemini is unavailable."""

    question = question.lower()

    answers = {
        "frame": (
            "A frame is a fixed-size block of physical RAM. "
            "When a program needs memory, its pages can be placed "
            "into available frames."
        ),

        "virtual memory": (
            "Virtual memory is a memory management technique that "
            "allows a computer to use secondary storage as an extension "
            "of RAM. It gives programs the impression that they have "
            "a large, continuous memory space."
        ),

        "page fault": (
            "A page fault occurs when a program requests a page that "
            "is not currently present in physical RAM. The operating "
            "system must load that page from secondary storage."
        ),

        "page hit": (
            "A page hit occurs when the requested page is already "
            "available in physical memory. No page replacement is needed."
        ),

        "page replacement": (
            "Page replacement is the process of removing a page from "
            "RAM to make space for another page when memory is full."
        ),

        "fifo": (
            "FIFO stands for First-In, First-Out. It replaces the page "
            "that entered memory earliest."
        ),

        "lru": (
            "LRU stands for Least Recently Used. It replaces the page "
            "that has not been used for the longest time."
        ),

        "optimal": (
            "The Optimal page replacement algorithm replaces the page "
            "that will not be used for the longest time in the future. "
            "It is mainly used as a theoretical benchmark."
        ),

        "ram": (
            "RAM stands for Random Access Memory. It is the computer's "
            "main working memory and temporarily stores data used by "
            "running programs."
        ),

        "page": (
            "A page is a fixed-size block of virtual memory. The operating "
            "system maps virtual memory pages to physical memory frames."
        )
    }

    for keyword, answer in answers.items():
        if keyword in question:
            return answer

    return (
        "I can help explain virtual memory, RAM, pages, frames, page "
        "faults, page hits, and page replacement algorithms such as "
        "FIFO, LRU, and Optimal. Please ask me about one of these topics."
    )


def virtual_memory_tutor(question):
    """Generate a beginner-friendly answer about virtual memory."""

    if not isinstance(question, str) or not question.strip():
        return "Please enter a valid question."

    question = question.strip()

    if len(question) > 12000:
        return "Your question is too long. Please keep it under 12,000 characters."

    client = get_gemini_client()

    if client is None:
        return basic_tutor_answer(question)

    
    prompt = f"""
You are a friendly and patient Virtual Memory Tutor Bot.

The student asks:

{question}

YOUR TASK:
Answer the exact question asked by the student.

INSTRUCTIONS:
1. Understand what the student wants to know.
2. Explain only the requested concept.
3. Do not generate a complete lesson unless explicitly requested.
4. Use simple, beginner-friendly English.
5. Break difficult explanations into small steps.
6. Give a relevant real-life example when useful.
7. Explain technical terms only when necessary.
8. For comparison questions, compare only the requested topics.
9. Do not include unrelated algorithms or concepts.
10. If the question is unclear, politely ask the student
    to clarify it.

ANSWER LENGTH:
- Short question: 2-5 sentences.
- Explanation request: a few clear paragraphs.
- Detailed explanation request: provide more detail.
- Comparison request: use a small table when useful.

Keep your answer focused, accurate, and easy to understand.
"""


    try:
        response = generate_with_retry(client, prompt)

        if response and response.text:
            return response.text.strip()

        return basic_tutor_answer(question)

    except Exception as error:
        print("Gemini Tutor Error:", error)
        return basic_tutor_answer(question)


def generate_virtual_memory_report(topic, requirements=""):
    """Generate a structured educational report about virtual memory."""

    if not isinstance(topic, str) or not topic.strip():
        return "Please enter a valid report topic."

    if not isinstance(requirements, str):
        requirements = ""

    topic = topic.strip()
    requirements = requirements.strip()

    if len(topic) > 1000:
        return "The report topic is too long. Please keep it under 1,000 characters."

    if len(requirements) > 5000:
        return "The report requirements are too long. Please keep them under 5,000 characters."

    client = get_gemini_client()

    if client is None:
        return (
            "Report generation is unavailable because the Gemini API key "
            "could not be found. Please check the GEMINI_API_KEY setting."
        )

    prompt = f"""
You are an educational report-writing assistant specializing
in virtual memory and operating systems.

Write a clear, well-organized academic report on:

TOPIC: {topic}

ADDITIONAL REQUIREMENTS:
{requirements if requirements else "No additional requirements provided."}

Write the report using the following structure where relevant:

1. Title
2. Abstract
3. Introduction
4. Background and basic concepts
5. Detailed explanation of the topic
6. Working process
7. Algorithms or techniques involved
8. Practical examples
9. Advantages
10. Limitations and challenges
11. Applications and importance
12. Conclusion
13. References or suggested learning resources

Writing guidelines:

- Use clear, student-friendly academic English.
- Explain technical terms.
- Use headings and subheadings.
- Include examples where useful.
- Keep the information relevant to virtual memory.
- Avoid repeating the same points.
- Do not invent research papers, authors, or citations.
- Make the report detailed enough to be useful for a student.
- Follow the additional requirements provided by the student.
"""

    try:
        response = generate_with_retry(client, prompt)

        if response and response.text:
            return response.text.strip()

        return (
            "The report could not be generated. "
            "Please try again with a different topic."
        )

    except Exception as error:
        print("Gemini Report Error:", error)

        return (
            "Report generation is temporarily unavailable. "
            "Please try again later."
        )


def basic_performance_analysis(question, results=None, comparison=None, pages=None, frames=None):
    """Provide a rule-based analysis of simulation or comparison results."""
    if comparison and isinstance(comparison, list) and len(comparison) > 0:
        best = min(comparison, key=lambda x: x.get("page_faults", float("inf")))
        worst = max(comparison, key=lambda x: x.get("page_faults", -1))

        summary_lines = ["Comparison Analysis:"]
        for item in comparison:
            algo = item.get("algorithm", "Unknown")
            faults = item.get("page_faults", 0)
            hits = item.get("page_hits", 0)
            fault_rate = item.get("fault_rate", 0)
            summary_lines.append(f"- {algo}: {faults} faults, {hits} hits ({fault_rate}% fault rate)")

        summary_lines.append(
            f"\nBest Performing: {best.get('algorithm')} with the lowest number of faults ({best.get('page_faults')})."
        )
        if best.get("algorithm") != worst.get("algorithm"):
            summary_lines.append(
                "Optimal generally produces the theoretical minimum faults, while LRU and FIFO depend on reference locality."
            )
        return "\n".join(summary_lines)

    if results and isinstance(results, dict):
        algo = results.get("algorithm", "Selected Algorithm")
        faults = results.get("page_faults", 0)
        hits = results.get("page_hits", 0)
        total = results.get("total_references", faults + hits)
        fault_rate = results.get("fault_rate", 0)
        hit_rate = results.get("hit_rate", 0)

        assessment = (
            "High fault rate observed. Consider increasing frames or testing LRU/Optimal."
            if fault_rate > 50
            else "Good hit rate observed for this reference pattern."
        )

        return (
            f"Simulation Analysis for {algo}:\n"
            f"- Total references: {total}\n"
            f"- Page hits: {hits} ({hit_rate}%)\n"
            f"- Page faults: {faults} ({fault_rate}%)\n\n"
            f"{assessment}"
        )

    return (
        "No simulation results are available yet. Please enter a page-reference sequence, "
        "specify RAM frames, and click 'Run simulation' or 'Compare selected algorithms' "
        "first so I can analyze the results."
    )


def analyze_performance(question, results=None, comparison=None, pages=None, frames=None):
    """Analyze virtual memory simulation performance using Gemini or rule-based logic."""
    if not isinstance(question, str) or not question.strip():
        question = "Which algorithm performs best?"

    client = get_gemini_client()
    if client is None:
        return basic_performance_analysis(question, results, comparison, pages, frames)

    context_parts = [f"Student question: {question}"]
    if comparison:
        context_parts.append(f"Comparison data: {comparison}")
    if results:
        context_parts.append(f"Simulation result: {results}")
    if pages:
        context_parts.append(f"Page references: {pages}")
    if frames:
        context_parts.append(f"RAM frames: {frames}")

    context = "\n".join(context_parts)

    prompt = f"""
You are an operating systems performance analysis assistant for a Virtual Memory Simulator.

Simulation Context:
{context}

Analyze the performance, compare page faults and hits, explain which algorithm was most efficient and why, in beginner-friendly language.
"""

    try:
        response = generate_with_retry(client, prompt)
        if response and response.text:
            return response.text.strip()
        return basic_performance_analysis(question, results, comparison, pages, frames)
    except Exception as error:
        print("Gemini Analysis Error:", error)
        return basic_performance_analysis(question, results, comparison, pages, frames)


def generate_virtual_memory_report(topic, requirements=""):
    """Generate a structured educational report about virtual memory."""
    if not isinstance(topic, str) or not topic.strip():
        return "Please enter a valid report topic."

    if not isinstance(requirements, str):
        requirements = ""

    topic = topic.strip()
    requirements = requirements.strip()

    client = get_gemini_client()
    if client is None:
        return (
            f"Report on {topic}:\n"
            "Virtual memory enables modern operating systems to allocate memory safely and efficiently "
            "using paging, page tables, and page replacement strategies such as FIFO, LRU, and Optimal."
        )

    prompt = f"""
Write an academic report on the virtual memory topic:
Topic: {topic}
Requirements: {requirements}
"""
    try:
        response = generate_with_retry(client, prompt)
        if response and response.text:
            return response.text.strip()
        return f"Report on {topic} generated."
    except Exception as error:
        print("Gemini Report Error:", error)
        return "Report generation is temporarily unavailable."


# Run the tutor bot directly for testing
# Command-line interface for testing the tutor and report generator
if __name__ == "__main__":

    print("\n===== VIRTUAL MEMORY TUTOR BOT =====")

    while True:
        print("\nChoose an option:")
        print("1. Ask the Virtual Memory Tutor")
        print("2. Generate a Virtual Memory Report")
        print("3. Exit")

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            question = input("\nEnter your question: ")

            answer = virtual_memory_tutor(question)

            print("\n===== TUTOR ANSWER =====")
            print(answer)

        elif choice == "2":
            topic = input("\nEnter the report topic: ")
            requirements = input(
                "Enter additional requirements (or press Enter to skip): "
            )

            report = generate_virtual_memory_report(
                topic,
                requirements
            )

            print("\n===== GENERATED REPORT =====")
            print(report)

        elif choice == "3":
            print("\nThank you for using the Virtual Memory Tutor Bot!")
            break

        else:
            print("\nInvalid choice. Please enter 1, 2, or 3.")
