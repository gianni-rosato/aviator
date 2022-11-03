<div align="center">
<h1>Aviator</h1>

A lightweight, Flatpak-first, easy-to-use GUI utility for encoding with SVT-AV1 & Opus.

<img src="assets/aviator_splash2.avif" alt="Splash" width=450/>
<br>
<br>

[![Installs](https://img.shields.io/flathub/downloads/net.natesales.Aviator?style=for-the-badge)](https://flathub.org/apps/details/net.natesales.Aviator)
![Code Size](https://img.shields.io/github/languages/code-size/natesales/aviator?style=for-the-badge)
[![License](https://img.shields.io/github/license/natesales/q?style=for-the-badge)](https://raw.githubusercontent.com/natesales/q/main/LICENSE)

[![Please do not theme this app](https://stopthemingmy.app/badge.svg)](https://stopthemingmy.app)
[![Liberapay](https://img.shields.io/liberapay/receives/computerbuster.svg?logo=liberapay)](https://liberapay.com/computerbuster/donate)
</div>

### About

Aviator enables simple, easy-to-use video encoding for the word's most advanced open video codec, AV1. Encode your favorite media into super efficient files with incredible quality per bit, powered by the SVT-AV1 production encoder with Opus for audio encoding. The sky's the limit for your old home video collection &amp; large 4k smartphone videos, and you can fly in style with a beautiful libadwaita interface. Take off with Aviator!

Aviator is designed to be a no frills, easy to use AV1 encoder that any beginner can pick up and immediately understand how to use. 

### Installation

Aviator is available on Flathub. You can learn how to set up Flatpak on your distro of choice [here](https://flatpak.org/setup/).

<a href="https://flathub.org/apps/details/net.natesales.Aviator"><img width="200" alt="Download on Flathub" src="https://flathub.org/assets/badges/flathub-badge-en.png"/></a>

### Why AV1?

AV1 aims to be more efficient than HEVC & VP9 by around 30%, and more efficient than h.264 by 50%. Traditionally, a lot of AV1 encoder implementations have been pretty slow compared to competing codecs, but the production encoder SVT-AV1 is decently speedy. We decided to use SVT-AV1 in order to give users a scalable and fast AV1 encoder implementation that "just works," for the most part.

Aviator comes bundled with its own version of ffmpeg that is capable of encoding AV1 video using SVT-AV1.

### Aviator's Defaults

<img src="assets/aviator_vid.avif" alt="Aviator Video Settings" width=480/>

By default, when you load a video file some parameters will be set to match the source as closely as possible. These parameters include the resolution, framerate, and audio bitrate. Aviator's SVT-AV1 speed preset is set to 6 by default, with a CQ (Constant Quality) level of 32. You can set a CQ level from 0 to 63 using the slider, with larger numerical values indicating smaller filesize at the expense of visual quality. You can look at the detailed specifications behind each speed preset [here](https://gitlab.com/AOMediaCodec/SVT-AV1/-/blob/master/Docs/CommonQuestions.md#what-presets-do). Speed 6 offers a good balance between speed & compression efficiency at any CQ level. 

<img src="assets/aviator_audio.avif" alt="Aviator Audio Settings" width=480/>

Audio is reencoded even if the bitrate is set to be the same as the source audio. Audio is encoded to Opus, which is a highly efficient free audio codec that is often more efficient than competitors like AAC & MP3 audio. Because of Opus's incredible efficiency, audio tracks will be encoded at 48kbps if no source bitrate is detected. Opus reaches audio transparency at around 128kbps.

### Roadmap & Limitations

Currently, Aviator cannot handle:
- Video streams with multiple audio streams
- Video streams with subtitles

These are considered bugs, and we are working on fixing them ASAP.

In the future, we would like to:
- Add a progress bar
- Add maximize & minimize buttons in the header bar
- Add a "Stop Encode," button
- Add a queue, potentially
- Revamp outputting a file
- Revamp the About page

Let us know if you have any issues in our Issues section. Thank you for using Aviator!

<img src="assets/aviator_output.avif" alt="Aviator Output UI" width=480/>

### Credits

Actively developed by [Nate Sales](https://github.com/natesales/) & [Gianni Rosato](https://github.com/Amateurintheflesh/)
