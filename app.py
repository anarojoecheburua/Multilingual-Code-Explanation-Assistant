import streamlit as st
import requests

# Replace with your Hugging Face API key
HUGGINGFACE_API_KEY = ""
API_URL = "https://api-inference.huggingface.co/models/meta-llama/Llama-3.3-70B-Instruct"

# Headers for Hugging Face API
HEADERS = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}


# Function to query the Hugging Face API
def query_llama3(input_text, language):
    # Create the prompt
    prompt = (
        f"Provide a simple explanation of this code in {language}:\n\n{input_text}\n"
        f"Only output the explanation and nothing else. Make sure that the output is written in {language} and only in {language}"
    )

    # Payload for the API
    payload = {
        "inputs": prompt,
        "parameters": {"max_new_tokens": 500, "temperature": 0.3},
    }
    
    # Make the API request
    response = requests.post(API_URL, headers=HEADERS, json=payload)

    if response.status_code == 200:
        result = response.json()
        
        # Extract the response text
        full_response = result[0]["generated_text"] if isinstance(result, list) else result.get("generated_text", "")
        
        # Clean up: Remove the prompt itself from the response
        clean_response = full_response.replace(prompt, "").strip()

        # Further clean any leading colons or formatting
        if ":" in clean_response:
            clean_response = clean_response.split(":", 1)[-1].strip()
        
        return clean_response or "No explanation available."
    else:
        return f"Error: {response.status_code} - {response.text}"

# Streamlit App
st.set_page_config(page_title="Multilingual Code Explanation Assistant", layout="wide")

# Sidebar Instructions
st.sidebar.title("How to Use the App")
st.sidebar.markdown("""
1. Paste your code snippet into the input box.
2. Enter the language you want the explanation in (e.g., English, Spanish, French).
3. Click 'Generate Explanation' to see the results.
""")
st.sidebar.divider()
st.sidebar.markdown(
    """
    <div style="text-align: center; font-size: 12px; color: grey;">
        Made with ♡ by Ana
    </div>
    """,
    unsafe_allow_html=True
)

# App Title
st.title("Multilingual Code Explanation Assistant")
st.markdown("### Powered by Llama 3.3 from Hugging Face 🦙")

# Input Fields
code_snippet = st.text_area("Paste your code snippet here:", height=200)
preferred_language = st.text_input("Enter your preferred language for explanation (e.g., English, Spanish):")

# Button to Generate Explanation
if st.button("Generate Explanation"):
    if code_snippet and preferred_language:
        with st.spinner("Generating explanation... ⏳"):
            explanation = query_llama3(code_snippet, preferred_language)
        st.subheader("Generated Explanation:")
        st.write(explanation)
    else:
        st.warning("⚠️ Please provide both the code snippet and preferred language.")

# Footer
st.markdown("---")
st.markdown("🧠 **Note**: This app uses Llama 3.3 from Hugging Face for multilingual code explanations.")