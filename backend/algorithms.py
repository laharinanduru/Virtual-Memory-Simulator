
def simulate_fifo(pages, frame_count):
    frames = []
    history = []
    hits = 0
    faults = 0
    next_to_replace = 0

    for page in pages:
        if page in frames:
            hits += 1
            hit = True
        else:
            faults += 1
            hit = False

            if len(frames) < frame_count:
                frames.append(page)
            else:
                frames[next_to_replace] = page
                next_to_replace = (next_to_replace + 1) % frame_count

        history.append({
            "page": page,
            "frames": frames.copy(),
            "hit": hit,
            "fault": not hit
        })

    return build_result(history, hits, faults, len(pages))


def simulate_lru(pages, frame_count):
    frames = []
    history = []
    hits = 0
    faults = 0
    last_used = {}

    for index, page in enumerate(pages):
        if page in frames:
            hits += 1
            hit = True
        else:
            faults += 1
            hit = False

            if len(frames) < frame_count:
                frames.append(page)
            else:
                least_recent = min(frames, key=lambda p: last_used[p])
                frames[frames.index(least_recent)] = page

        last_used[page] = index

        history.append({
            "page": page,
            "frames": frames.copy(),
            "hit": hit,
            "fault": not hit
        })

    return build_result(history, hits, faults, len(pages))


def simulate_optimal(pages, frame_count):
    frames = []
    history = []
    hits = 0
    faults = 0

    for index, page in enumerate(pages):
        if page in frames:
            hits += 1
            hit = True
        else:
            faults += 1
            hit = False

            if len(frames) < frame_count:
                frames.append(page)
            else:
                future = pages[index + 1:]
                next_use = {}

                for frame_page in frames:
                    next_use[frame_page] = (
                        future.index(frame_page)
                        if frame_page in future
                        else float("inf")
                    )

                victim = max(frames, key=lambda p: next_use[p])
                frames[frames.index(victim)] = page

        history.append({
            "page": page,
            "frames": frames.copy(),
            "hit": hit,
            "fault": not hit
        })

    return build_result(history, hits, faults, len(pages))


def build_result(history, hits, faults, total):
    return {
        "history": history,
        "total_references": total,
        "page_hits": hits,
        "page_faults": faults,
        "hit_rate": round(hits / total, 4),
        "fault_rate": round(faults / total, 4)
    }
