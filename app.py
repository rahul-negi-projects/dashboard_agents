import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from backend import importing_data,workflow
st.secrets['GROQ_API_KEY']

# ---- Streamlit Page ----
st.set_page_config(page_title="Dashboard Generator", layout="wide")

st.sidebar.title("📊 Dashboard Generator")

# Text input box
user_prompt = st.sidebar.text_area("✍️ Enter your custom instruction or question:")

# File uploader
uploaded_file = st.sidebar.file_uploader("📂 Upload your CSV file", type=["csv"])

# Sidebar Submit button
submit_button = st.sidebar.button('🚀 Submit')


######################  Once user clicks submit button
if submit_button:
    messages = []

    # Check for missing file
    if not uploaded_file:
        messages.append(("error", "⚠️ Please upload a CSV file before submitting."))

    # Check for missing prompt
    if not user_prompt:
        messages.append(("warning", "⚠️ You didn’t provide any custom instruction. Default behavior will be used."))

    # Save messages to session state
    st.session_state['status_msgs'] = messages

    if uploaded_file:
      st.session_state['status_msgs'] = []
      # If file exists → process CSV
      st.success("✅ Inputs received, processing your request...")
      st.write("Your Prompt:", user_prompt if user_prompt else "🔄 Using default instructions")
      st.write("Uploaded File:", uploaded_file.name)
    #   csv_file = pd.read_csv(uploaded_file)
      df,df_json_first,df_json = importing_data(uploaded_file)
    #   st.dataframe(df.loc[:0,:], width='stretch')

      output = workflow.invoke({"json_data":df_json_first})
      html_code = output['dahsbaord_code'].content

      # st.write(html_code)

      # Render inside Streamlit
      components.html(html_code, height=1000, width="100%", scrolling=True)


# Show all messages
if 'status_msgs' in st.session_state:
    for msg_type, msg_text in st.session_state['status_msgs']:
        getattr(st, msg_type)(msg_text)

st.write("---") # Optional: Add a horizontal line for separation
st.write("Created by: Rahul Negi")
st.write("Version: 1.0") # Optional: Add version information