import streamlit as st
import json
st.set_page_config(layout="wide")
st.markdown(
    """
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&display=swap" rel="stylesheet">
    """,
    unsafe_allow_html=True
)

def local_css():
    st.markdown(
        """
        <style>
        /* Set background image for app */
        .stApp {
            background-image: url("https://media.istockphoto.com/id/1713008927/de/foto/workshop-für-aromatische-kerzen-reine-kerzenessenzen.jpg?s=612x612&w=0&k=20&c=ukOiYpFqLcDdyEilCyvmXh3u7UIu8AMHXU6t6TC5gMY=");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }

        /* Light transparent overlay for better readability */
        .stApp::before {
            content: "";
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(255, 255, 255, 0.55); /* slightly darker for contrast */
            z-index: -1;
        }

        /* Style the label of selectbox */
        div[data-testid="stSelectbox"] > label > div {
            color: black !important;
            font-size: 1.5rem !important;
            font-weight: 600;
            padding: 0.5rem 0.75rem;
            background-color: rgba(255, 255, 255, 0.85);
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
            display: inline-block;
        }

        /* Style the selectbox input */
        div[data-testid="stSelectbox"] > div {
            background-color: white !important;
            border: 2px solid #C49E5A !important;
            border-radius: 12px !important;
            padding: 0.5rem !important;
            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        }

        /* Style the placeholder text in select dropdown */
        .css-1wa3eu0-placeholder {
            color: #555 !important;
            font-size: 1rem !important;
        }

        /* Rounded input boxes */
        .stTextInput>div>div>input {
            border-radius: 12px !important;
            border: 1.5px solid #C49E5A !important;
            padding: 0.5rem 1rem !important;
            font-size: 1rem !important;
        }

        /* Buttons with smooth hover */
        button[kind="primary"] {
            background-color: #C49E5A !important;
            border-radius: 12px !important;
            padding: 0.6rem 1.5rem !important;
            font-weight: 600 !important;
            transition: background-color 0.3s ease;
        }
        button[kind="primary"]:hover {
            background-color: #A57F32 !important;
            cursor: pointer;
        }

        /* Card style for output */
        .styled-output {
            background-color: rgba(167, 216, 216, 0.9);
            border-radius: 16px;
            padding: 1.5rem;
            box-shadow: 0 8px 16px rgba(196, 158, 90, 0.15);
            margin-top: 1.5rem;
            color: black;
            max-height: 80vh;
            overflow-y: auto;
            font-family: 'Playfair Display', cursive, serif;
        }

        .styled-output p {
            color: #222 !important;
            font-size: 1.1rem !important;
            margin: 0.2rem 0 0.4rem 1rem !important;
        }

        /* Header style */
        .css-1v3fvcr h1 {
            font-family: 'Playfair Display', cursive, serif;
            color: #8A5C9E;
            font-weight: 700;
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
        }

        </style>
        """,
        unsafe_allow_html=True
    )


local_css()

from core.rule_based import get_heuristic_notes
from core.prompt_builder import build_prompt
from core.llm_interface import query_llm
from core.data_loader import load_presets

# Loading presets JSON
PRESETS_FILE = "data/presets.json"
presets = load_presets(PRESETS_FILE)

# Two columns layout: left for inputs, right for output
col1, col2 = st.columns([1, 1.5])

with col1:
    st.markdown(
        '''
        <div style="background-color: rgba(255, 255, 255, 0.85); 
                    padding: 1rem 1.5rem; 
                    border-radius: 16px; 
                    box-shadow: 0 4px 12px rgba(0,0,0,0.1); 
                    display: inline-block; 
                    margin-bottom: 1rem;">
            <h1 style="color:black; 
                       font-weight:700; 
                       font-size:2rem; 
                       margin: 0;">
                <span style="font-family: cursive; color: #8A5C9E;">🌺 AromaLens</span> : Discover Your Perfume’s Story with AI
            </h1>
        </div>
        ''',
        unsafe_allow_html=True
    )

    # Dropdown for selecting a preset or manual entry
    compound_option = st.selectbox("Create a compound and check notes:", ["Add a new compound"] + list(presets.keys()))

    if compound_option != "Add a new compound":
        chemicals = presets[compound_option]
        heuristics = get_heuristic_notes(chemicals)
        prompt = build_prompt(chemicals, heuristics)
        st.session_state["prompt"] = prompt
        st.session_state["chemicals"] = chemicals
    else:
        st.info("Enter fragrance chemicals and percentages manually, one per line (e.g. BENZYL SALICYLATE: 7)")
        manual_input = st.text_area("Input chemical and percentages:")
        chemicals = {}
        if manual_input:
            try:
                for line in manual_input.strip().splitlines():
                    name, pct = line.split(":")
                    chemicals[name.strip()] = float(pct.strip())
            except Exception:
                st.error("Invalid format. Please use 'CHEMICAL NAME: %' per line.")

    # Show chemicals if any (both preset or manual)
    if chemicals:
        st.markdown(
            """
            <div class="styled-output">
                <h3 style="
                    color: #4B3F72;
                    font-size: 1.8rem;
                    margin-bottom: 1rem;
                    font-family: 'Playfair Display', cursive;
                ">
                    Current Compound Chemicals 🧪
                </h3>
            """,
            unsafe_allow_html=True
        )

        for name, pct in chemicals.items():
            st.markdown(
                f"""
                <p style="
                    font-size: 1.1rem;
                    color: #222;
                    margin: 0.2rem 0 0.4rem 1rem;
                ">
                    • <b>{name}</b>: {pct}%
                </p>
                """,
                unsafe_allow_html=True
            )

        st.markdown("</div>", unsafe_allow_html=True)

    # If adding a new compound, allow naming & saving it
    if compound_option == "Add a new compound":
        new_name = st.text_input("Name your compound to save:")
        if st.button("Save this compound"):
            if new_name.strip() == "":
                st.error("Please enter a valid name.")
            else:
                presets[new_name] = chemicals
                with open(PRESETS_FILE, "w") as f:
                    json.dump(presets, f, indent=2)
                st.success(f"Compound '{new_name}' saved successfully!")

    # Build prompt & heuristics for further processing if chemicals exist
    if chemicals:
        heuristics = get_heuristic_notes(chemicals)
        prompt = build_prompt(chemicals, heuristics)
        st.session_state["prompt"] = prompt
        st.session_state["chemicals"] = chemicals
    else:
        st.session_state["prompt"] = None

    # Generate notes button logic
    if st.session_state.get("prompt"):
        if st.button("Generate Notes"):
            st.session_state["generate_clicked"] = True
    else:
        st.session_state["generate_clicked"] = False

def build_notes_html(notes, title, emoji):
    if not notes:
        return f"<p><em>No {title.lower()} detected.</em></p>"

    html = f"<h3>{emoji} {title}</h3>"
    for item in notes:
        name = item.get("name", "Unknown")
        reason = item.get("reason", "")
        html += f"<p><strong>{name}</strong>: {reason}</p>"
    return html


with col2:
    if st.session_state.get("generate_clicked", False) and st.session_state.get("prompt"):
        with st.spinner("💐Thinking like a master perfumer..."):
            response = query_llm(st.session_state["prompt"])

        if "error" in response:
            st.error(f"Error from LLM: {response['error']}")
        else:
            st.success("Analyzing completed successfully!")

            top_html = build_notes_html(response.get("top_notes"), "Top Notes", "🌿")
            middle_html = build_notes_html(response.get("middle_notes"), "Middle Notes", "🌸")
            base_html = build_notes_html(response.get("base_notes"), "Base Notes", "🌲")

            uncertain = response.get("uncertain")
            uncertain_html = ""
            if uncertain:
                uncertain_html = "<h3>🤔 Uncertain Notes</h3>"
                for item in uncertain:
                    uncertain_html += f"<p><strong>{item.get('name', 'Unknown')}</strong></p>"

            full_html = f"""
            <div class="styled-output">
                {top_html}
                {middle_html}
                {base_html}
                {uncertain_html}
            </div>
            """
            st.markdown(full_html, unsafe_allow_html=True)