import streamlit as st
import requests
from PIL import Image

def initialize_session_state():
    if 'api_key' not in st.session_state:
        st.session_state.api_key = None

def create_openai_client(api_key):
    try:
        # Store API key in session state
        st.session_state.api_key = api_key
        # Test the API key with a small request
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "gpt-4",
                "messages": [{"role": "user", "content": "test"}],
                "max_tokens": 5
            }
        )
        if response.status_code == 200:
            return True
        else:
            st.error("Invalid API key. Please check your API key and try again.")
            return False
    except Exception as e:
        st.error("An error occurred. Please check your network connection.")
        return False

def get_openai_response(prompt):
    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {st.session_state.api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "gpt-4",
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 1000,
                "temperature": 0.5
            }
        )
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            st.error("Error generating response. Please try again.")
            return None
    except Exception as e:
        st.error("An error occurred. Please check your network connection.")
        return None

def main():
    initialize_session_state()
    
    # Page configuration
    st.set_page_config(
        page_title="Legal Document Assistant",
        page_icon="⚖️",
        layout="wide"
    )

    # Try to load logo if it exists
    try:
        logo = Image.open("logo.png")
        col1, col2, col3 = st.columns(3)
        with col2:
            st.image(logo, use_column_width="auto")
    except FileNotFoundError:
        st.title("⚖️ AI-Powered Legal Document Assistant")

    st.write("Welcome! This assistant can help you with legal questions, document templates, and contract drafting.")

    # API Key input
    api_key = st.text_input(
        "Enter your OpenAI API Key:",
        type="password",
        help="Need an API key? Message the developer for assistance."
    )

    if api_key:
        if st.session_state.api_key is None:
            if create_openai_client(api_key):
                st.success("API key validated successfully!")
            else:
                st.stop()

        # Sidebar navigation
        st.sidebar.title("Navigation")
        option = st.sidebar.radio(
            "Choose a service:",
            ["Ask a Legal Question", "Request a Document Template", "Generate Legal Contract Draft"]
        )

        if option == "Ask a Legal Question":
            st.subheader("Ask a Legal Question")
            question = st.text_area(
                "Enter your legal question:",
                height=100,
                help="Be as specific as possible for better results"
            )
            
            if st.button("Get Answer", type="primary"):
                if question:
                    with st.spinner("Generating response..."):
                        prompt = f"""As a legal assistant, please provide a clear and detailed answer to this question. 
                        Include any relevant legal considerations and disclaimers: {question}"""
                        answer = get_openai_response(prompt)
                        if answer:
                            st.info("Legal Guidance:")
                            st.write(answer)
                            st.caption("Note: This is AI-generated guidance and should not be considered as formal legal advice.")
                else:
                    st.warning("Please enter a question.")

        elif option == "Request a Document Template":
            st.subheader("Document Template Generator")
            doc_type = st.selectbox(
                "Select document type:",
                ["Non-Disclosure Agreement", "Employment Contract", "Service Agreement", 
                 "Terms of Service", "Privacy Policy", "Other"]
            )
            
            if doc_type == "Other":
                doc_type = st.text_input("Specify the document type:")
            
            if st.button("Generate Template", type="primary"):
                if doc_type:
                    with st.spinner("Generating template..."):
                        prompt = f"Create a detailed template for a {doc_type} with standard legal clauses and sections."
                        template = get_openai_response(prompt)
                        if template:
                            st.info("Document Template:")
                            st.text_area("Generated Template:", template, height=400)
                            if st.button("Download Template"):
                                st.download_button(
                                    "Download as Text",
                                    template,
                                    file_name=f"{doc_type.lower().replace(' ', '_')}_template.txt"
                                )
                else:
                    st.warning("Please select or specify a document type.")

        elif option == "Generate Legal Contract Draft":
            st.subheader("Contract Draft Generator")
            col1, col2 = st.columns(2)
            
            with col1:
                party_a = st.text_input("Party A (First Party):")
                party_b = st.text_input("Party B (Second Party):")
            
            with col2:
                contract_type = st.selectbox(
                    "Contract Type:",
                    ["Service Agreement", "Sales Contract", "Partnership Agreement", "Custom"]
                )
                if contract_type == "Custom":
                    contract_type = st.text_input("Specify contract type:")

            key_terms = st.text_area("Key Terms and Conditions:", height=150)
            
            if st.button("Generate Contract Draft", type="primary"):
                if party_a and party_b and contract_type and key_terms:
                    with st.spinner("Generating contract draft..."):
                        prompt = f"""Generate a detailed {contract_type} between {party_a} and {party_b} 
                        with the following terms and conditions: {key_terms}"""
                        contract_draft = get_openai_response(prompt)
                        if contract_draft:
                            st.info("Contract Draft:")
                            st.text_area("Generated Contract:", contract_draft, height=400)
                            if st.button("Download Contract"):
                                st.download_button(
                                    "Download as Text",
                                    contract_draft,
                                    file_name=f"{contract_type.lower().replace(' ', '_')}_draft.txt"
                                )
                else:
                    st.warning("Please fill in all required fields.")

    else:
        st.info("Please enter your OpenAI API key to proceed.")
        st.caption("If you need an API key, please message the developer for assistance.")

if __name__ == "__main__":
    main()
