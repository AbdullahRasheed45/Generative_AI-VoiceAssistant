from setuptools import find_packages, setup

setup(
    name="Multi Lingual assistant",
    version="0.0.1",
    author="Abdullah",
    author_email="abdullahrasheed45@gmail.com",
    packages=find_packages(),
    install_requires=["SpeechRecognition","pipwin","pyaudio","gTTS","google-generativeai","python-dotenv","streamlit"]
)