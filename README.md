# Sync Lyrics — Streamlit Web App for Synced Lyrics Generation

A small Streamlit-based web application for creating time-synced lyrics (LRC files) from an audio file and a set of lyric lines. The app shows an interactive waveform, provides playback and scrubbing controls, and lets users assign timestamps to each lyric line to export a synchronized `.lrc` file.

## Features

- Upload audio files (MP3, WAV, etc.) and display an interactive waveform.
- Add, edit, or upload lyrics as a plain text file.
- Play, pause, scrub, change playback speed, and control volume from the waveform player.
- Assign timestamps to individual lyric lines using a "Set" button that captures the current playback time.
- Store in-progress projects in session state and load/save partially-synced `.lrc` files.
- Export fully-synced lyrics as a standard `.lrc` file.

## Tech Stack

- App framework: Streamlit (Python)
- Frontend: A custom Streamlit component using React and WaveSurfer.js for waveform visualization and interactive audio playback
- Data storage: Streamlit session state for in-memory project state

## Status

Core functionality implemented: audio upload/handling, waveform display via a custom component, lyrics editing, timestamp assignment and export. Active lyric-line highlighting during playback is not yet implemented.

## Usage

1. Run the Streamlit app (e.g., `streamlit run app.py`).
2. Upload an audio file and either upload or paste/edit lyric lines.
3. Use the waveform player to play and scrub the audio. Click the "Set" button next to a lyric line to capture the current timestamp.
4. When finished, export the synced lyrics as an `.lrc` file.

## Project Notes & Future Work

- Consider adding automatic sync suggestions using speech-to-text or beat detection.
- Add user accounts and project persistence for long-term storage.
- Support additional export formats such as SRT.

## References

See `project_plan.md` in the repository for more details on the original plan and design notes.
