import streamlit as st
import sys
import os

# Add the 'src' directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from llm_layer import ask_gemini

# --- Streamlit App UI ---

st.title("Path of Exile 2 LLM Augmentation System")
st.write(
    "Ask a question about Path of Exile 2. The system will search its local database "
    "for relevant information and use it to ask a better question of the Gemini LLM."
)
st.info(
    "Note: This system requires a `GEMINI_API_KEY` to be set in a `.env` file. "
    "Please see the `.env.example` for instructions.",
    icon="ℹ️"
)

# User input
user_query = st.text_input("Your Question:", placeholder="e.g., What are the changes to the Earthquake gem?")

if st.button("Ask the PoE2 Mentor"):
    if user_query:
        with st.spinner("Searching local knowledge base and consulting the LLM..."):
            # Call the backend function to get the answer
            answer = ask_gemini(user_query)

            # Display the answer
            st.markdown("### Answer from the Mentor:")
            st.write(answer)
    else:
        st.warning("Please enter a question before asking.")