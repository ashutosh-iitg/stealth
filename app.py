import streamlit as st
import requests
import json

def initialize_chat_history():
    if "messages" not in st.session_state:
        st.session_state.messages = []

def display_chat_history():
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

def main():
    st.title("PDF Chat Assistant")
    
    initialize_chat_history()
    display_chat_history()

    # File upload section
    uploaded_file = st.file_uploader("Upload a PDF to start chatting", type=['pdf'])
    
    if uploaded_file is not None:
        files = {"file": uploaded_file}
        
        try:
            # Upload file
            response = requests.post("http://localhost:8000/upload", files=files)
            
            if response.status_code == 200:
                filename = response.json()["filename"]
                results = requests.get(f"http://localhost:8000/get-results/{filename}")
                
                if results.status_code == 200:
                    results_data = results.json()
                    
                    # Add system message about successful upload
                    system_msg = f"📄 PDF uploaded successfully! I've analyzed a {results_data['page_count']} page document titled: {results_data['content']['title']}"
                    if not any(msg["content"] == system_msg for msg in st.session_state.messages):
                        st.session_state.messages.append({"role": "assistant", "content": system_msg})
                    
                    # Chat input
                    if prompt := st.chat_input("Ask me about the PDF..."):
                        # Add user message to chat
                        st.session_state.messages.append({"role": "user", "content": prompt})
                        
                        # Here you would typically send the prompt to your backend for processing
                        # For now, we'll just acknowledge the question
                        response = f"I received your question about the PDF: {prompt}"
                        st.session_state.messages.append({"role": "assistant", "content": response})
                        
                        st.rerun()
                else:
                    st.error("Error processing PDF")
            else:
                st.error("Error uploading file")
                
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
