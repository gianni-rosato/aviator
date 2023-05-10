<div align="center">
<h1>Aviator</h1>

A Flatpak-first easy-to-use GUI for encoding with SVT-AV1 & libopus.

<img src="assets/aviator_splash2.avif" alt="Splash" width=450/>
<br>
<br>

[![Installs](https://img.shields.io/flathub/downloads/net.natesales.Aviator?style=for-the-badge)](https://flathub.org/apps/details/net.natesales.Aviator)
![Code Size](https://img.shields.io/github/languages/code-size/natesales/aviator?style=for-the-badge)
[![License](https://img.shields.io/github/license/natesales/q?style=for-the-badge)](https://raw.githubusercontent.com/natesales/q/main/LICENSE)

[![Please do not theme this app](https://stopthemingmy.app/badge.svg)](https://stopthemingmy.app)
</div>

## About

Aviator enables simple & easy video encoding for the world's most advanced open video codec, AV1. Encode your favorite media into super efficient files with incredible quality per bit, powered by the fast SVT-AV1 encoder with libopus for audio encoding. The sky's the limit for your old home video collection, large 4k smartphone videos, screen recordings, Blu-ray rips, you name it - take off with Aviator!

Aviator is designed to be a no frills, easy to use AV1 encoding GUI that any beginner can pick up and immediately understand how to use. 

## Installation

### Flathub

Aviator is available on Flathub. You can learn how to set up Flatpak on your distro of choice [here](https://flatpak.org/setup/).

<a href="https://flathub.org/apps/details/net.natesales.Aviator"><img width="200" alt="Download on Flathub" src="https://flathub.org/assets/badges/flathub-badge-en.png"/></a>

### Building from Source

Make sure you have all required dependencies before building from source. This includes `flatpak-builder`, `python3` & `gcc`

```bash
git clone https://github.com/natesales/aviator
cd aviator
make
```

Third party packaging formats are not officially supported by Aviator, and if you encounter bugs while using them please do not submit them as issues; we do not officially support third party packaged versions of Aviator.

## Why AV1?

AV1 aims to be more efficient than HEVC & VP9 by around 30%, and more efficient than h.264 by 50%. Traditionally, a lot of AV1 encoder implementations have been pretty slow compared to competing codecs' encoders, but the [SVT-AV1](https://gitlab.com/AOMediaCodec/SVT-AV1/) production encoder is scalable, fast, and feature rich. We decided to use SVT-AV1 in order to give users a fast AV1 encoder implementation will scale well no matter what system you're using, and take advantage of your system resources to the fullest.

Aviator comes bundled with its own version of ffmpeg that is capable decoding videos to detect source information, upscaling & downscaling videos with a sharp scaling algorithm called lanczos, & encoding audio using the Opus audio codec via libopus.

## Aviator's Defaults

Hovering over most user configurable options in Aviator will produce a helpful tooltip that you can look at to make things more clear.

### Video

<img src="assets/aviator_video.webp" alt="Aviator Video Settings" width=480/>

By default, when you load a video file some parameters will be set to match the source as closely as possible. These parameters include the resolution and audio bitrate. Aviator's SVT-AV1 speed preset is set to 6 by default, with a CRF (Constant Rate Factor) level of 32. You can set a CRF from 0 to 63 using the slider, with larger numerical values indicating smaller filesize at the expense of visual quality. You can look at the detailed specifications behind each speed preset [here](https://gitlab.com/AOMediaCodec/SVT-AV1/-/blob/master/Docs/CommonQuestions.md#what-presets-do). Speed 6 offers a good balance between speed & compression efficiency at any CRF level.

The Grain Synth slider allows you to add artificial grain to your video to mimic its natural grain, which applies the artificial grain at decode time as a filter which makes it easier to encode grainy videos at high fidelity.

### Audio

<img src="assets/aviator_audio.webp" alt="Aviator Audio Settings" width=480/>

Audio is reencoded even if the bitrate is set to be the same as the source audio. Audio is encoded to Opus, which is a highly efficient free audio codec that is often more efficient than competitors like AAC & MP3 audio. Because of Opus's incredible efficiency, audio tracks will be encoded at 48kbps if no source bitrate is detected. Opus reaches audio transparency at around 128kbps.

### Output

<img src="assets/aviator_output.webp" alt="Aviator Output UI" width=480/>

The container your video is stored in is associated with the file extension. Aviator offers two options for video output: the Matroska video container & the WebM container. The open-source Matroska container (.MKV) is Aviator's default container, a universal multimedia container with widespread video &amp; audio support. WebM is designed for web compatibility &amp; may break subtitles. Both work out of the box with Aviator's AV1 video & Opus audio formats.

## Roadmap & Limitations

Currently, Aviator cannot handle:
- Video streams with subtitles encoding to .webm

These are considered bugs, and we are working on fixing them ASAP. In the meantime, we'd prefer you choose the .mkv container if you are having trouble with subtitles.

In the future, we would like to:
- Add a queue, potentially
- Add an option to copy your audio without reencoding (that disables WebM output)
- Revamp outputting a file

Let us know if you have any issues in our Issues section. Thank you for using Aviator!

## Credits

Actively developed by [Nate Sales](https://github.com/natesales/) & [Gianni Rosato](https://github.com/gianni-rosato/)
