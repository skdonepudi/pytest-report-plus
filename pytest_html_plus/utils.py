def extract_trace_block(trace: str) -> str:
    if not trace:
        return ""
    lines = trace.splitlines()
    trace_lines = []

    for line in lines:
        if line.lstrip().startswith("E "):
            break
        trace_lines.append(line)

    return "\n".join(trace_lines).strip()


def extract_error_block(error: str) -> str:
    if not error:
        return ""
    error_lines = [line for line in error.splitlines() if line.strip().startswith("E ")]
    return "\n".join(error_lines).strip() or error.strip()  # fallback to full error if E-block is absent
