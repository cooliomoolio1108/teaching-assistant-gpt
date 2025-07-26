import streamlit as st

def inject_custom_css():
    css = """
    <style>
    h2 {
        margin-left:10px;
        color: white;
        font-size: 1.5rem;
        font-weight: 600;
    }
    div[data-testid="stSidebarHeader"] > img, div[data-testid="collapsedControl"] > img {
        height: 10rem;
        width: auto;
        padding-top: 2rem;
    }
    div[data-testid="stSidebarContent"] {
        padding-top: 2rem;
    }
    div[data-testid="stSidebarHeader"], div[data-testid="stSidebarHeader"] > *,
    div[data-testid="collapsedControl"], div[data-testid="collapsedControl"] > * {
        display: flex;
        align-items: center;
    }
    [data-testid="stSidebarNavItems"] {
        padding-top: 2rem;
    }
    [data-testid="stSidebar"] {
        display: flex;
        
    }
    [data-testid="stVerticalBlock"] {
        gap: 1rem;
    }
    [data-testid="stHeader"] {
        background: rgb(0, 0, 0, 0);
    }

    [data-testid="stBaseButton-primary"] {
        background: rgb(0, 0, 0, 0);
        border: 1px solid rgba(255, 255, 255, 1);
        transition: all 0.4s ease; /* slower and smooth */
        
    }
    [data-testid="stBaseButton-primary"]:hover {
        background: rgb(24 29 155);
        border: 1px solid rgb(24 29 155);
    }
    data-testid="stBaseButton-primary"]:active {
        color: white !important;
        background: rgb(24 29 155);
        border: 1px solid rgb(24 29 155);
    }
    data-testid="stBaseButton-primary"]:click {
        color: white !important;
        background: rgb(24 29 155);
        border: 1px solid rgb(24 29 155);
    }
    data-testid="stBaseButton-primary"]:focus {
        color: white !important;
        background: rgb(24 29 155);
        border: 1px solid rgb(24 29 155);
    }
    section[data-testid="stSidebar"] [data-testid="stBaseButton-secondary"] {
        text-align: left;
        transition: all 0.4s ease;  /* slower and smooth */
        background: rgb(0, 0, 0, 0);
        border: 0;
        padding: 0.2rem !important;  /* override inline style */
        justify-content: flex-start;  /* align text left */
        width: 100% !important;       /* make full-width */
        box-sizing: border-box;       /* include padding in width */
        display: flex;                /* required to align text with justify-content */
    }
    section[data-testid="stSidebar"] [data-testid="stBaseButton-secondary"]:hover {
        color: white !important;
        background: rgba(24, 29, 155, 0.6);
        border: 1px solid rgb(24 29 155);
        
    }
    section[data-testid="stSidebar"] [data-testid="stBaseButton-secondary"]:active {
        color: white !important;
        background: rgba(24, 29, 155, 0.6);
        border: 1px solid rgb(24 29 155);
    }
    section[data-testid="stSidebar"] [data-testid="stBaseButton-secondary"]:focus {
        color: white !important;
        background: rgba(24, 29, 155, 0.8);
        border: 1px solid rgb(24 29 155);
    }
    section[data-testid="stSidebar"] [data-testid="stBaseButton-secondary"] button:hover {
        color: white !important;
        background: rgba(24, 29, 155, 0.8);
        border: 1px solid rgb(24 29 155);
    }
    [data-testid="stFileUploaderDropzone"] {
        display: flex;
    }
    [data-testid="stFileUploaderDropzoneInstructions"] {
        display: flex;
    }
    iframe {
        border: none;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        width: 100%;
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)
    st.logo("assets/chatbot.png", size="large")
