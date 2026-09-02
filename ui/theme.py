import streamlit as st

def apply_custom_theme():
    """Applies Neon Glow effects with Soft Contrast for readability."""
    accent_green = "#4ADE80"
    accent_blue = "#00E5FF"   
    bg_card = "#0A0A0A"
    border_color = "#334155"  # Slightly brighter default border
    text_heading = "#FFFFFF"  # Bright white for titles
    text_body = "#D1D5DB"     # Soft gray for paragraphs (No eye strain)

    st.markdown(f"""
        <style>
        /* 1. NUKE THE BOTTOM WHITE BAR */
        div[data-testid="stBottomBlock"], 
        div[data-testid="stBottomBlock"] > div {{
            background-color: #000000 !important;
        }}
        section[data-testid="stSidebar"] {{
            border-right: 1px solid {border_color} !important;
        }}

        /* 2. TEXT CONTRAST FIX (Anti-Halation) */
        h1, h2, h3, h4, h5, h6 {{
            color: {text_heading} !important;
            font-weight: 600 !important;
        }}
        p, span, div, label {{
            color: {text_body} !important;
        }}

        /* 3. NEON GREEN GLOW FOR BUTTONS */
        div[data-testid="stButton"] > button {{
            background-color: #000000 !important;
            border: 1px solid {border_color} !important;
            border-radius: 8px !important;
            transition: all 0.3s ease !important;
        }}
        div[data-testid="stButton"] > button:hover {{
            border: 1px solid {accent_green} !important;
            box-shadow: 0 0 10px {accent_green}, 0 0 20px {accent_green}, inset 0 0 5px {accent_green} !important;
        }}
        div[data-testid="stButton"] > button:hover * {{
            color: {accent_green} !important;
        }}

        /* 4. NEON BLUE GLOW FOR CHAT BOX (With Default Discoverability) */
        div[data-testid="stChatInput"] {{
            padding-bottom: 20px !important; 
        }}
        div[data-testid="stChatInput"] > div {{
            background-color: {bg_card} !important;
            border: 1px solid {border_color} !important; /* Visible by default */
            border-radius: 12px !important;
            transition: all 0.3s ease !important;
        }}
        div[data-testid="stChatInput"] > div:hover,
        div[data-testid="stChatInput"] > div:focus-within {{
            border: 1px solid {accent_blue} !important;
            box-shadow: 0 0 15px {accent_blue}, 0 0 30px {accent_blue}, inset 0 0 8px {accent_blue} !important;
        }}
        div[data-testid="stChatInput"] textarea {{
            color: {text_heading} !important; 
        }}

        /* 5. Custom Cards */
        .custom-card {{
            background-color: {bg_card} !important;
            border: 1px solid {border_color} !important;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 16px;
        }}
        </style>
    """, unsafe_allow_html=True)