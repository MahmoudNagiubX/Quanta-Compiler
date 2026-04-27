from __future__ import annotations


def format_error(
    source: str,
    error_type: str,
    message: str,
    line: int | None = None,
    column: int | None = None,
    hint: str | None = None,
) -> str:
    """Format a compiler error with source context and a caret pointer."""
    lines = source.splitlines()
    output_lines: list[str] = []

    location = ""
    if line is not None and column is not None:
        location = f" at line {line}, column {column}"
    output_lines.append(f"{error_type}{location}")

    if line is not None and 1 <= line <= len(lines):
        source_line = lines[line - 1]
        output_lines.append(f"{line} | {source_line}")

        if column is not None and column >= 1:
            prefix = " " * (len(str(line)) + 3 + column - 1)
            output_lines.append(f"{prefix}^")

    if hint:
        output_lines.append(f"Hint: {hint}")
    else:
        output_lines.append(f"Hint: {message}")

    return "\n".join(output_lines)
