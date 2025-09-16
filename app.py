import streamlit as st
from components.waveform_player.waveform_player import waveform_player
# import datetime
# import io
# import numpy as np

# --- Helper Functions ---
def is_valid_timestamp_format(timestamp):
    """Check if timestamp is in mm:ss or mm:ss.fff format"""
    # Pattern for mm:ss or mm:ss.fff
    pattern = r'^\d{1,2}:\d{2}(\.\d{1,3})?'

# --- App Config ---
st.set_page_config(
    page_title="Synced Lyrics Generator",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Title and Description ---
st.title("🎵 Synced Lyrics Generator")
st.markdown("""
Upload an audio file and paste your lyrics.
Sync each lyric line to the audio and export as an LRC file!
""")

# --- Session State Initialization ---
if "audio_file" not in st.session_state:
    st.session_state.audio_file = None
if "lyrics" not in st.session_state:
    st.session_state.lyrics = []
if "sync_times" not in st.session_state:
    st.session_state.sync_times = []
if "waveform_img" not in st.session_state:
    st.session_state.waveform_img = None

# --- 1. Audio Upload Section ---
st.header("1. Upload Audio File")
audio_file = st.file_uploader(
    "Choose an audio file (mp3, wav, etc.)",
    type=["mp3", "wav", "ogg", "flac"],
    key="audio_file_uploader"
)
if audio_file:
    st.session_state.audio_file = audio_file
    st.audio(audio_file, format="audio/mp3")

# --- 2. Upload Lyrics File Section ---
st.header("2. Upload Lyrics File")
lyrics_file = st.file_uploader(
    "Upload a .txt file with your lyrics (one line per lyric):",
    type=["txt"],
    key="lyrics_file_uploader"
)
if lyrics_file:
    lyrics_content = lyrics_file.read().decode("utf-8")
    st.session_state.lyrics = [line.strip() for line in lyrics_content.splitlines() if line.strip()]
    col1, col2, col3 = st.columns(3)

    with col1:
        st.header("Text")

    with col2:
        st.header("Time Stamp")

    with col3:
        st.header("Reset")

    for i, lyric in enumerate(st.session_state.lyrics):
        with col1:
            st.text_input(f"Lyric{i}", value=lyric, key=f"lyric_{i}", label_visibility="collapsed")
        # You can also add a text input field to enter the timestamp for each line
        with col2:
            st.time_input(
                "Time",
                key=f"time_{i}",
                label_visibility="collapsed",
                value=None,
                step=1
            )
        with col3:
            st.button("Set", key=f"set_{i}")

    st.session_state.sync_times = [None] * len(st.session_state.lyrics)

# --- 3. Audio Visualization Section (Waveform/Spectrogram) ---
st.header("3. Audio Visualization")

audio_uploaded = st.session_state.audio_file is not None

if audio_uploaded:
    # Reset file pointer if needed
    st.session_state.audio_file.seek(0)
    audio_bytes = st.session_state.audio_file.read()
    st.session_state.audio_file.seek(0)
    st.subheader("Interactive Waveform Player")
    # waveform_player(
    #     audio_bytes=audio_bytes,
    #     key="waveform_player",
    #     height=80,
    #     show_controls=True,
    # )
else:
    st.info("Waveform will appear here after audio upload.")


# --- 4. Sync Lyrics Section ---
st.header("4. Sync Lyrics")
if st.session_state.audio_file and st.session_state.lyrics:
    st.write("Assign timestamps to each lyric line as you play the audio.")
    
    # Display the audio player for reference
    st.audio(st.session_state.audio_file, format="audio/mp3")
    
    # Initialize session state for current line index if not exists
    if "current_line_index" not in st.session_state:
        st.session_state.current_line_index = 0
    
    # Display current line highlight
    if st.session_state.lyrics:
        st.markdown(f"**Current Line ({st.session_state.current_line_index + 1}/{len(st.session_state.lyrics)}):**")
        if st.session_state.current_line_index < len(st.session_state.lyrics):
            st.markdown(f"### {st.session_state.lyrics[st.session_state.current_line_index]}")
    
    # Create a form for timestamp input
    with st.form("sync_form"):
        st.write("Enter timestamps for each lyric line:")
        
        # Create input fields for each lyric line
        timestamp_inputs = []
        for i, lyric in enumerate(st.session_state.lyrics):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"Line {i+1}: {lyric}")
            with col2:
                # Format timestamp as mm:ss.fff or mm:ss
                default_time = st.session_state.sync_times[i] if st.session_state.sync_times[i] else ""
                timestamp = st.text_input(f"Timestamp", value=default_time, key=f"timestamp_{i}", label_visibility="collapsed")
                timestamp_inputs.append(timestamp)
        
        # Form submission
        submitted = st.form_submit_button("Save Timestamps")
        if submitted:
            # Validate timestamps
            valid_timestamps = True
            for i, timestamp in enumerate(timestamp_inputs):
                if timestamp:  # Only validate non-empty timestamps
                    # Check if timestamp is in mm:ss or mm:ss.fff format
                    if not is_valid_timestamp_format(timestamp):
                        st.error(f"Invalid timestamp format for Line {i+1}: '{timestamp}'. Use mm:ss or mm:ss.fff format.")
                        valid_timestamps = False

            if valid_timestamps:
                # Update sync times in session state
                st.session_state.sync_times = timestamp_inputs
                st.success("Timestamps saved!")
            else:
                st.error("Please correct the timestamp format errors above.")
    
    # Navigation buttons
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("⏮️ Previous Line") and st.session_state.current_line_index > 0:
            st.session_state.current_line_index -= 1
    with col2:
        if st.button("⏭️ Next Line") and st.session_state.current_line_index < len(st.session_state.lyrics) - 1:
            st.session_state.current_line_index += 1
    with col3:
        if st.button("🔄 Reset Current Line"):
            st.session_state.current_line_index = 0
            
else:
    st.info("Upload audio and paste lyrics to enable syncing.")

# --- 5. Export Synced Lyrics Section ---
st.header("5. Export Synced Lyrics")
if st.session_state.sync_times and any(t is not None for t in st.session_state.sync_times):
    # Placeholder for export functionality
    st.success("Export functionality coming soon: Download your synced lyrics as an LRC file.")
else:
    st.info("Sync at least one lyric line to enable export.")

# --- Sidebar: About/Help ---
with st.sidebar:
    st.markdown("## About")
    st.markdown("""
    This app helps you manually sync lyrics to music for karaoke or lyric videos.
    - Built with [Streamlit](https://streamlit.io/)
    - Audio processing: librosa, pydub, ffmpeg
    - Visualization: matplotlib
    """)
    st.markdown("**MVP Version** – core features only.")
