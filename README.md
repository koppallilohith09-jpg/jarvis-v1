# JARVIS V1

Windows desktop voice assistant with hand gestures, local speech recognition, local memory, file tools, and an interactive 3D globe. This repository publishes the **compact friend edition of JARVIS 1.8**. V1 is the distribution name; it does not change the underlying application version.

[Download JARVIS V1 for Windows x64](https://github.com/koppallilohith09-jpg/jarvis-v1/releases/latest/download/jarvis-v1.zip)

## Install

1. Extract the downloaded `jarvis-v1.zip` to a writable folder.
2. Run `JARVIS-1.8-Friend-Compact-Extract.exe` and choose an extraction folder.
3. Open the resulting `JARVIS-1.8-Friend` folder and run `JARVIS-Local-Gestures.exe`. Keep its support folders beside the EXE.
4. Open Settings and connect **your own Gemini or OpenAI API key**. Chat and document analysis require an internet connection and available provider quota. OpenAI API billing is separate from a ChatGPT subscription.

Windows native voice is included. For the optional Kokoro British voice, download the [voice pack](https://github.com/koppallilohith09-jpg/jarvis-v1/releases/latest/download/jarvis-v1-kokoro-voice-pack.zip), close JARVIS, and extract it into the same parent folder containing `JARVIS-1.8-Friend`. Restart, then select Kokoro in Settings > Offline speech. Keep Windows native voice selected until the pack is installed.

The compact download is about 482 MB and expands to about 1.48 GB. The optional voice pack adds about 142 MB after extraction. No separate extraction software is needed. See [README-COMPACT.txt](README-COMPACT.txt) and [README-FIRST.txt](README-FIRST.txt).

## Features and limits

- Type commands or hold Hold to talk while speaking, then release to send.
- Use local Whisper recognition, Windows speech, hand detection, and SQLite memory. There is **no offline language model or Ollama runtime**.
- Use Modes > Hand gestures to start the camera and enable Windows pointer control. Index finger moves; pinch clicks; two raised fingers and vertical motion scroll; open palm pauses. Ctrl+Alt+G stops input.
- Rotate and zoom the original JARVIS globe. iPad access requires separate private HTTPS pairing.
- Webcam eye tracking is experimental; head-assisted pointer control is available. Physical camera accuracy depends on the device and environment.

This is the selected 1.8 build. The newer [JARVIS V2](https://github.com/koppallilohith09-jpg/jarvis-v2) contains the 1.8.2 launch confirmation, network, and camera fixes, with Kokoro included.

## Privacy

The friend package excludes the creator's keys, settings, chats, uploads, and memory. A new local profile is created on your computer. When cloud AI is connected, your requests and relevant file or memory content are sent to the selected provider. Camera and local speech processing run on your computer. Review the provider's data terms before connecting.

## Source and attribution

The `source/` directory contains the integration source shipped with the release, including its dependency lists and build scripts. Large application libraries, models, and runtime assets are distributed through Releases, not Git. A source checkout alone is not the complete portable application; use the release for the ready-to-run build.

This is a modified integration based on [FatihMakes/Mark-LVI](https://github.com/FatihMakes/Mark-LVI), licensed **CC BY-NC 4.0**. Attribution is required and commercial use is not permitted under that license. [Holo Gestures](https://github.com/zubair-trabzada/holo-gestures) components retain their MIT license. The friend edition uses original JARVIS globe scene code with the three.js runtime; private Brahma reference scene assets are excluded. Other included components retain their own licenses.

See [LICENSE](LICENSE), [UPSTREAM.json](UPSTREAM.json), [THIRD-PARTY-NOTICES.txt](THIRD-PARTY-NOTICES.txt), the retained component notices, and [7ZIP-LICENSE.txt](7ZIP-LICENSE.txt). The compact extractor uses the unmodified 7-Zip extraction module; its source distribution is linked in the compact instructions.
