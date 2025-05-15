import streamlit as st
from ai_handler import generate_script

# Make the app wider
st.set_page_config(layout="wide")

# Define default settings for each video type
VIDEO_TYPE_DEFAULTS = {
    "Broadcast News": {
        "tone": "Professional",
        "length": 2.0,
        "density": 0.7,
        "ai_model": "Claude 3.7",
        "language": "English (US)",
        "geo_background": "U.S.",
        "similar_to": "News Anchor",
        "knowledge_level": "Advanced",
        "enable_opinions": False,
        "political": "Centrist",
        "economic": "Balanced",
        "social": "Balanced",
        "custom_dataset": False,
        "additional_instructions": "Use formal transitions between segments. Include clear attribution for sources and statistics. Start with a concise headline and end with a brief summary."
    },
    "Tiktok": {
        "tone": "Casual",
        "length": 0.3,
        "density": 0.3,
        "ai_model": "Gemini Pro",
        "language": "English (US)",
        "geo_background": "U.S.",
        "similar_to": "Social Media Influencer",
        "knowledge_level": "Beginner",
        "enable_opinions": True,
        "political": "Centrist",
        "economic": "Balanced",
        "social": "Balanced",
        "custom_dataset": False,
        "additional_instructions": "Use attention-grabbing first 3 seconds. Keep sentences under 10 words."
    },
    "Opinion": {
        "tone": "Conversational",
        "length": 3.0,
        "density": 0.5,
        "ai_model": "Claude 3.7",
        "language": "English (US)",
        "geo_background": "U.S.",
        "similar_to": "Podcaster",
        "knowledge_level": "Advanced",
        "enable_opinions": True,
        "political": "Centrist",
        "economic": "Balanced",
        "social": "Balanced",
        "custom_dataset": False,
        "additional_instructions": "Start with personal anecdote or question. Present balanced counterarguments before addressing them. Use first-person perspective. Incorporate rhetorical questions. End with thought-provoking takeaway."
    },
    "Kids News": {
        "tone": "Casual",
        "length": 1.5,
        "density": 0.2,
        "ai_model": "GPT 4o",
        "language": "English (US)",
        "geo_background": "U.S.",
        "similar_to": "Neutral/Generic",
        "knowledge_level": "Beginner",
        "enable_opinions": False,
        "political": "Centrist",
        "economic": "Balanced",
        "social": "Balanced",
        "custom_dataset": False,
        "additional_instructions": "Use simple vocabulary (grades 3-5 reading level). Explain any complex terms. Ask engaging questions throughout. Use analogies related to school, family, or popular kids' culture. End with a fun fact. Avoid frightening content or tone. Include suggestions for adults to discuss topic further."
    }
}

st.title("ARTICLE TO VIDEO SCRIPT WRITING TOOL")

# Function to create larger labels
def make_label(text):
    st.markdown(f"### {text}")

# Initialize session state for settings if not exists
if 'current_settings' not in st.session_state:
    st.session_state.current_settings = VIDEO_TYPE_DEFAULTS["Broadcast News"]

# Top menu options
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    make_label("Video Type")
    video_type = st.selectbox(
        "",
        list(VIDEO_TYPE_DEFAULTS.keys()),
        key="video_type",
        on_change=lambda: st.session_state.update({"current_settings": VIDEO_TYPE_DEFAULTS[st.session_state.video_type]})
    )
    
with col2:
    make_label("AI Model")
    ai_model = st.selectbox(
        "",
        ["Claude 3.7", "GPT 4o", "Gemini Pro"],
        index=["Claude 3.7", "GPT 4o", "Gemini Pro"].index(st.session_state.current_settings["ai_model"]),
        key="ai_model"
    )

with col3:
    make_label("Language / Region")
    language = st.selectbox(
        "",
        ["English (US)", "English (UK)", "Spanish", "French", "German", 
         "Portuguese", "Italian", "Dutch", "Russian", "Chinese", 
         "Japanese", "Korean", "Arabic", "Hindi", "Bengali", 
         "Turkish", "Thai", "Vietnamese", "Swedish", "Polish"],
        index=["English (US)", "English (UK)", "Spanish", "French", "German", 
               "Portuguese", "Italian", "Dutch", "Russian", "Chinese", 
               "Japanese", "Korean", "Arabic", "Hindi", "Bengali", 
               "Turkish", "Thai", "Vietnamese", "Swedish", "Polish"].index(st.session_state.current_settings["language"]),
        key="language"
    )

# Horizontal line before Presenter Selection
st.markdown("---")

# Presenter selection
st.markdown("## Presenter Selection")
col1, col2 = st.columns(2)

with col1:
    make_label("Geographic Background")
    geo_background = st.selectbox(
        "",
        ["U.S.", "U.K.", "Latin America", "East Asia", "South Asia", 
         "Continental Europe", "Middle East", "Africa", "Australia/Oceania"],
        index=["U.S.", "U.K.", "Latin America", "East Asia", "South Asia", 
               "Continental Europe", "Middle East", "Africa", "Australia/Oceania"].index(st.session_state.current_settings["geo_background"]),
        key="geo_background"
    )

with col2:
    make_label("Similar To")
    similar_to = st.selectbox(
        "",
        ["Neutral/Generic", "News Anchor", "Podcaster", "Social Media Influencer", 
         "Professor/Academic", "Talk Show Host", "Documentary Narrator"],
        index=["Neutral/Generic", "News Anchor", "Podcaster", "Social Media Influencer", 
               "Professor/Academic", "Talk Show Host", "Documentary Narrator"].index(st.session_state.current_settings["similar_to"]),
        key="similar_to"
    )

# Opinions/Stance section with checkbox
enable_opinions = st.checkbox("Enable Inject Opinions/Stance", 
                            value=st.session_state.current_settings["enable_opinions"],
                            key="enable_opinions")

if enable_opinions:
    political = st.select_slider(
        "Political",
        options=["Progressive", "Moderate Left", "Centrist", "Moderate Right", "Conservative"],
        value=st.session_state.current_settings["political"],
        key="political"
    )
    
    economic = st.select_slider(
        "Economic",
        options=["Pro-labor", "Balanced", "Pro-business"],
        value=st.session_state.current_settings["economic"],
        key="economic"
    )
    
    social = st.select_slider(
        "Social",
        options=["Progressive", "Balanced", "Traditional"],
        value=st.session_state.current_settings["social"],
        key="social"
    )

# Horizontal line before Script Style Settings
st.markdown("---")

# Script style settings
st.markdown("## Script Style Settings")

make_label("Knowledgeability Level")
knowledge_level = st.select_slider(
    "",
    options=["Beginner", "Intermediate", "Advanced"],
    value=st.session_state.current_settings["knowledge_level"],
    key="knowledge_level"
)

make_label("Tone")
tone = st.select_slider(
    "",
    options=["Casual", "Conversational", "Professional"],
    value=st.session_state.current_settings["tone"],
    key="tone"
)

make_label("Information Density")
info_density = st.slider(
    "",
    min_value=0.0,
    max_value=1.0,
    value=st.session_state.current_settings["density"],
    step=0.1,
    format="%.1f",
    help="0 = Low, 0.5 = Medium, 1 = High",
    key="info_density"
)

make_label("Length Target (minutes)")
length_target = st.slider(
    "",
    min_value=0.5,
    max_value=10.0,
    value=st.session_state.current_settings["length"],
    step=0.5,
    format="%.1f",
    key="length_target"
)

# Custom dataset and additional instruction options
st.markdown("### Use Custom Dataset")
custom_dataset = st.checkbox("", 
                           value=st.session_state.current_settings["custom_dataset"],
                           key="custom_dataset")
if custom_dataset:
    custom_dataset_text = st.text_area("Paste Youtube Channel URL", height=100, key="custom_dataset_text")

guardrails = st.checkbox("Enable Guardrails (Brand Safety & Content Compliance)", value=True, disabled=True, key="guardrails")

make_label("Additional Instructions")
additional_instructions = st.text_area("", 
                                     value=st.session_state.current_settings["additional_instructions"],
                                     height=100,
                                     key="additional_instructions")

# Horizontal line
st.markdown("---")

# Article input
make_label("Input Article")
article_text = st.text_area("", height=200, key="article_text")

# Submit button with custom styling
st.markdown("""
<style>
.stButton>button {
    font-size: 24px;
    padding: 15px 30px;
    height: auto;
}
</style>
""", unsafe_allow_html=True)

# Submit button
submit_button = st.button("Generate Script", key="submit")

# When submit is clicked, process the article and generate a script
if submit_button and article_text:
    with st.spinner('Generating script...'):
        # Collect all settings into a dictionary
        current_settings = {
            "video_type": video_type,
            "ai_model": ai_model,
            "language": language,
            "geo_background": geo_background,
            "similar_to": similar_to,
            "enable_opinions": enable_opinions,
            "political": political if enable_opinions else "Centrist",
            "economic": economic if enable_opinions else "Balanced",
            "social": social if enable_opinions else "Balanced",
            "knowledge_level": knowledge_level,
            "tone": tone,
            "density": info_density,
            "length": length_target,
            "custom_dataset": custom_dataset,
            "additional_instructions": additional_instructions
        }
        
        # Generate the script
        generated_script = generate_script(current_settings, article_text)
        
        # Display any error messages in red
        if generated_script.startswith("Error"):
            st.error(generated_script)
        else:
            st.success("Script generated successfully!")
            # Update the script output text area with the generated script
            st.session_state.script_output = generated_script

# Output script section
st.markdown("### Output Script")

# Display the script as a markdown table
if 'script_output' in st.session_state:
    st.markdown(st.session_state.script_output)
    
    # Add download button for the script
    st.download_button(
        label="Download Script",
        data=st.session_state.script_output,
        file_name="video_script.md",
        mime="text/markdown"
    )