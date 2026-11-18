
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

    # Convert question to lowercase
    question = question.lower().strip()

    # RAM
    if "ram" in question:
        return (
            "RAM stands for Random Access Memory. "
            "It is the computer's temporary working memory "
            "used to store data that is currently needed."
        )

    # Virtual Memory
    elif "virtual memory" in question:
        return (
            "Virtual memory is a memory management technique "
            "that allows programs to use an address space "
            "larger than the available physical RAM. "
            "The operating system moves pages between RAM "
            "and secondary storage when needed."
        )

    # Page Fault
    elif "page fault" in question:
        return (
            "A page fault occurs when a requested page "
            "is not currently present in physical RAM. "
            "The operating system must bring that page "
            "into RAM before the program can continue."
        )

    # Page Hit
    elif "page hit" in question:
        return (
            "A page hit occurs when the requested page "
            "is already available in RAM. "
            "Therefore, no page replacement is needed."
        )

    # Page
    elif "page" in question:
        return (
            "A page is a fixed-size block of virtual memory. "
            "Pages are loaded into physical memory when needed."
        )

    # Frame
    elif "frame" in question:
        return (
            "A frame is a fixed-size block of physical RAM "
            "that stores one page of a process."
        )

    # FIFO
    elif "fifo" in question or "first in first out" in question:
        return (
            "FIFO stands for First In, First Out. "
            "When memory is full, it removes the page "
            "that entered memory first."
        )

    # LRU
    elif "lru" in question or "least recently used" in question:
        return (
            "LRU stands for Least Recently Used. "
            "It replaces the page that has not been used "
            "for the longest time."
        )

    # Optimal
    elif "optimal" in question:
        return (
            "Optimal Page Replacement removes the page "
            "whose next use is farthest in the future. "
            "It produces the minimum possible page faults "
            "for a given reference string and frame count."
        )

    # Page Replacement
    elif "page replacement" in question:
        return (
            "Page replacement is the process of selecting "
            "a page to remove from RAM when memory is full "
            "and a new page needs to be loaded."
        )

    # Unknown question
    else:
        return (
            "Sorry, I don't know the answer to that question yet. "
            "You can ask me about RAM, virtual memory, pages, "
            "frames, page hits, page faults, FIFO, LRU, "
            "or Optimal Page Replacement."
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
if __name__ == "__main__":

    print("===== Virtual Memory Tutor Bot =====")
    print("Ask me about virtual memory concepts.")
    print("Type 'exit' to stop.\n")

    while True:
        user_question = input("You: ")

        if user_question.lower().strip() == "exit":
            print("Tutor: Thank you! Keep learning.")
            break

        answer = virtual_memory_tutor(user_question)
        print("Tutor:", answer)
        print()
