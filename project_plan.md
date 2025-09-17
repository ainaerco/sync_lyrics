Python Web App for Synced Lyrics Generation – Project Plan (Streamlit Version)

---

### Status: Core functionality implemented. See handover.txt for next steps.

---

## 1. Project Overview

**Goal:**
Build a Python-based web app using Streamlit where users upload an audio file and lyrics. The app displays an interactive waveform of the audio, allows scrubbing and playback control, and lets users assign timestamps to each lyric line to generate a synced LRC file.

---

## 2. Tech Stack

- **App Framework:** Streamlit
- **Frontend:** 
    - Streamlit widgets for the main UI.
    - A custom Streamlit component using **React** and **WaveSurfer.js** for the interactive audio player.
- **Data Storage:** In-memory via Streamlit session state (`st.session_state`).

---

## 3. Core Features & Flow

### 3.1. User Flow

1.  **Upload Audio:** User uploads an audio file (mp3, wav, etc.). The editor appears.
2.  **Manage Lyrics:** User can either upload a .txt file or add/edit/delete lyric lines manually within the editor.
3.  **Audio Visualization & Playback:** The app displays an interactive waveform of the audio. The user can play/pause, change speed, and scrub through the track by dragging the waveform.
4.  **Tagging:** For each lyric line, the user plays the audio to the desired point and clicks a "Set" button to capture the current timestamp.
5.  **Export:** User downloads the synced lyrics as a standard .lrc file.

### 3.2. Streamlit App Tasks

- **[COMPLETED]** Audio File Handling: Upload and read audio files into memory.
- **[COMPLETED]** Waveform Display: A custom component renders and controls the waveform on the client-side.
- **[COMPLETED]** Lyrics Handling: Receive lyrics from a .txt file or allow full manual editing (add, delete, modify lines).
- **[COMPLETED]** Sync Data Storage: Store lyrics and their corresponding timestamps in session state.
- **[COMPLETED]** Export Functionality: Generate and download a .lrc file.

### 3.3. Streamlit UI Tasks

- **[COMPLETED]** Audio Player: A custom `waveform_player` component provides playback, pause, speed control, and scrubbing.
- **[COMPLETED]** Timestamp Display: The player shows the current playback time and total duration.
- **[COMPLETED]** Waveform/Spectrogram Display: An interactive waveform is shown.
- **[COMPLETED]** Lyrics Editor: Displays lyrics line-by-line with editable text and timestamp fields.
- **[COMPLETED]** Timestamp Assignment: A "Set" button assigns the current audio time to each line.
- **[NOT IMPLEMENTED]** Active Lyric Highlighting: The app does not yet highlight the lyric line that corresponds to the current audio playback time.
- **[COMPLETED]** Export Button: A download button is provided to get the final .lrc file.

---

## 4. Optional Enhancements (Future Work)

- **Auto-Sync Suggestion:** Use speech-to-text or beat detection to suggest initial sync points.
- **User Accounts:** Allow saving and editing projects.
- **Multiple Export Formats:** Support for SRT, etc.
- **Volume Control:** Add a volume slider to the audio player.

---

## NOTES:
- The application is built purely in Streamlit with a custom frontend component for the audio player.
- Audio visualization is handled client-side via WaveSurfer.js.