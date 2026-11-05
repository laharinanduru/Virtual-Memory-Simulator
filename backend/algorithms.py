def fifo(pages, capacity):
    frames = []
    states = []
    hits = 0
    faults = 0
    pointer = 0

    for page in pages:
        if page in frames:
            hits += 1
        else:
            faults += 1

            if len(frames) < capacity:
                frames.append(page)
            else:
                frames[pointer] = page
                pointer = (pointer + 1) % capacity

        states.append(frames.copy())

    return {
        "page_hits": hits,
        "page_faults": faults,
        "frame_states": states
    }


def lru(pages, capacity):
    frames = []
    states = []
    recent = {}
    hits = 0
    faults = 0

    for i, page in enumerate(pages):
        if page in frames:
            hits += 1
        else:
            faults += 1

            if len(frames) < capacity:
                frames.append(page)
            else:
                oldest = min(frames, key=lambda x: recent[x])
                frames[frames.index(oldest)] = page

        recent[page] = i
        states.append(frames.copy())

    return {
        "page_hits": hits,
        "page_faults": faults,
        "frame_states": states
    }


def optimal(pages, capacity):
    frames = []
    states = []
    hits = 0
    faults = 0

    for i, page in enumerate(pages):
        if page in frames:
            hits += 1
        else:
            faults += 1

            if len(frames) < capacity:
                frames.append(page)
            else:
                future = pages[i + 1:]

                distances = [
                    future.index(f) if f in future else float('inf')
                    for f in frames
                ]

                replace_index = distances.index(max(distances))
                frames[replace_index] = page

        states.append(frames.copy())

    return {
        "page_hits": hits,
        "page_faults": faults,
        "frame_states": states
    }
