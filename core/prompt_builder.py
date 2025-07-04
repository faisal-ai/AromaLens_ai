def build_prompt(chemicals: dict, heuristics: dict) -> str:
    prompt = (
        "You are an expert perfumer and fragrance chemist.\n\n"
        "Your task is to analyze the following list of fragrance ingredients, each with a given percentage concentration, "
        "and classify each chemical into one of the following olfactive note categories:\n"
        "- Top Note: Volatile, light molecules perceived immediately.\n"
        "- Middle Note (Heart Note): The central body of the fragrance, often floral, fruity, or spicy.\n"
        "- Base Note: Heavy, long-lasting components that anchor and fix the scent.\n\n"
        "For each chemical:\n"
        "1. Assign it to a note category (top/middle/base).\n"
        "2. Briefly explain your reasoning based on its volatility, olfactive family, or typical perfumery role.\n"
        "3. Mention any functional role (e.g., fixative, modifier), blending behavior, or common usage notes.\n"
        "4. If a compound is hard to classify or rarely used, mark it as “Uncertain” and explain.\n\n"
        "Here are the input chemicals and their concentrations:\n"
    )

    for name, pct in chemicals.items():
        prompt += f"- {name}: {pct}%\n"

    prompt += "\nHeuristic suggestions based on olfactive families:\n"
    for note in ["top", "middle", "base"]:
        names = heuristics.get(note, [])
        if names:
            prompt += f"{note.capitalize()} Notes (heuristic): {', '.join(names)}\n"

    prompt += (
        "\nReturn your answer in a structured format like this:\n"
        '{\n'
        '  "top_notes": [\n    {"name": "...", "reason": "..."},\n    ...\n  ],\n'
        '  "middle_notes": [\n    {"name": "...", "reason": "..."},\n    ...\n  ],\n'
        '  "base_notes": [\n    {"name": "...", "reason": "..."},\n    ...\n  ],\n'
        '  "uncertain": [\n    {"name": "...", "reason": "..."}\n  ]\n'
        '}\n'
    )

    return prompt
