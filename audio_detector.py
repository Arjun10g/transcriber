import streamlit as st
import whisper
import tempfile
from pydub import AudioSegment

# Function to convert the audio file to .wav if it's not in .wav format
def convert_to_wav(audio_file):
    audio = AudioSegment.from_file(audio_file)
    temp_wav = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    audio.export(temp_wav.name, format="wav")
    return temp_wav.name

# Function to transcribe audio using Whisper
def transcribe_audio(file_path, model_size="base"):
    model = whisper.load_model(model_size)
    result = model.transcribe(file_path)
    return result["text"]

# Streamlit App
st.title("Audio Transcription App with Whisper")

# File upload
uploaded_file = st.file_uploader("Upload an audio file (e.g., .m4a, .mp3, .wav)", type=["m4a", "mp3", "wav"])
progress_bar = st.progress(0)

if uploaded_file:
    st.success("File uploaded successfully!")
    
    # Convert to .wav if necessary
    if uploaded_file.type != "audio/wav":
        st.write("Converting audio file to .wav format...")
        audio_path = convert_to_wav(uploaded_file)
    else:
        audio_path = tempfile.NamedTemporaryFile(delete=False, suffix=".wav").name
        with open(audio_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
            
    # Model size selection
    model_size = st.selectbox("Select Whisper model size:", ["tiny", "base", "small", "medium", "large"])
    
    # Transcription process
    if st.button("Transcribe Text"):
        try:
            st.write("Starting transcription...")
            progress_bar.progress(20)  # Set initial progress
            
            # Transcription with progress update
            transcription_text = transcribe_audio(audio_path, model_size=model_size)
            progress_bar.progress(80)  # Update progress
            
            # Display transcription
            st.text_area("Transcription:", transcription_text, height=200)
            
            # Save transcription to a file
            with open("transcription.txt", "w") as f:
                f.write(transcription_text)
            st.success("Transcription completed. Saved to transcription.txt")
            progress_bar.progress(100)
        
        except Exception as e:
            st.error(f"An error occurred: {e}")
            progress_bar.empty()
else:
    st.warning("Please upload an audio file to start.")


# Streamlit runs continuously until manually stopped.
    
# cd "/Users/arjunghumman/Downloads/VS Code Stuff/Python/streamlitApp"

# streamlit run audio_detector.py
