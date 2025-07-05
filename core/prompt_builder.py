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
        "3. Mention its olfactory family (e.g., floral, woody, citrus, oriental, fresh, gourmand).\n"
        "4. Describe common fragrance accords or blends it typically appears in.\n"
        "5. Note any sensory characteristics (e.g., fresh, warm, sweet, balsamic).\n"
        "6. Mention any functional role (e.g., fixative, modifier), blending behavior, or common usage notes.\n"
        "7. If a compound is hard to classify or rarely used, mark it as “Uncertain” and explain.\n\n"
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
        "\nReturn your answer in a structured JSON format like this:\n"
        '{\n'
        '  "top_notes": [\n'
        '    {\n'
        '      "name": "...",\n'
        '      "reason": "...",\n'
        '      "olfactory_family": "...",\n'
        '      "common_accords": "...",\n'
        '      "sensory_characteristics": "...",\n'
        '      "functional_role": "..." \n'
        '    },\n'
        '    ...\n'
        '  ],\n'
        '  "middle_notes": [\n'
        '    {\n'
        '      "name": "...",\n'
        '      "reason": "...",\n'
        '      "olfactory_family": "...",\n'
        '      "common_accords": "...",\n'
        '      "sensory_characteristics": "...",\n'
        '      "functional_role": "..." \n'
        '    },\n'
        '    ...\n'
        '  ],\n'
        '  "base_notes": [\n'
        '    {\n'
        '      "name": "...",\n'
        '      "reason": "...",\n'
        '      "olfactory_family": "...",\n'
        '      "common_accords": "...",\n'
        '      "sensory_characteristics": "...",\n'
        '      "functional_role": "..." \n'
        '    },\n'
        '    ...\n'
        '  ],\n'
        '  "uncertain": [\n'
        '    {\n'
        '      "name": "...",\n'
        '      "reason": "..." \n'
        '    }\n'
        '  ]\n'
        '}\n'
    )

    return prompt
