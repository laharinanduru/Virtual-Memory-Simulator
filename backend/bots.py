
def virtual_memory_tutor(question):
    """
    Virtual Memory Tutor Bot
    Provides beginner-friendly explanations
    about virtual memory concepts.
    """

    # Check whether the question is valid
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
