import streamlit as st
from src.helper import voice_input, llm_model_object, text_to_speech


def main():
    st.title("My Chotu AI Assistant 🤖")

    if st.button("Ask me anything"):
        with st.spinner("Listening..."):
            text = voice_input()

            if not text.strip():  # Check if text is empty
                st.warning("No voice input detected. Please try again.")
                return

            response = llm_model_object(text)
            text_to_speech(response)

            with open("speech.mp3", "rb") as audio_file:
                audio_bytes = audio_file.read()

            st.text_area(label="Response:", value=response, height=350)
            st.audio(audio_bytes)
            st.download_button(label="Download Speech",
                               data=audio_bytes,
                               file_name="speech.mp3",
                               mime="audio/mp3")

            
if __name__=='__main__':
    main()