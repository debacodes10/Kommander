# Kommander ⌘

<p align="center">
  <img src="https://placehold.co/600x300/1a1b26/7aa2f7?text=Kommander&font=raleway" alt="Kommander Banner"/>
</p>

<p align="center">
  <strong>Stop searching for shell commands. Start asking for them.</strong>
  <br />
  <br />
  <a href="#">
    <img alt="PyPI Version" src="https://img.shields.io/pypi/v/kommander-cli?color=7aa2f7&label=pypi%20package&style=for-the-badge">
  </a>
  <a href="https://github.com/debacodes10/Kommander/blob/main/LICENSE">
    <img alt="License" src="https://img.shields.io/github/license/debacodes10/Kommander?color=7dcfff&style=for-the-badge">
  </a>
  <a href="#">
    <img alt="Build Status" src="https://img.shields.io/github/actions/workflow/status/debacodes10/Kommander/ci.yml?branch=main&style=for-the-badge&logo=github">
  </a>
</p>

---

Kommander is a command-line companion that translates your natural language requests into safe, executable shell scripts for Windows, macOS, and Linux.

## How it Works

Stop wasting time on Stack Overflow or digging through man pages. Describe the task you want to accomplish in plain English, and let Kommander generate the script for you. Review the script, and then execute it, copy it, or abort—you are always in control.

<p align="center">
  <br/>
  <img src="https://github.com/debacodes10/Kommander/blob/main/.assets/kommander-demo.gif?raw=true" alt="Kommander Demo"/>
</p>

## ✨ Core Features

* **Natural Language Interface**: Just `kom ask "your request"` and get a ready-to-run script.
* **Cross-Platform**: Generates PowerShell for Windows and bash/zsh for Linux & macOS.
* **Safety First**: Scripts are never executed automatically. You always see a preview and must approve execution.
* **Provider Agnostic**: Configure your preferred AI provider (starting with Google's Gemini).
* **Works With Your Terminal**: Not a terminal replacement. A universal tool that works in the environment you already love.

## 🚀 Installation

Kommander requires Python 3.8+ and `pip`.

```sh
pip install kommander-cli
```

## ⚙️ Configuration
Before your first use, you need to configure Kommander with your AI provider's API key.

1. Get your API key from Google AI Studio.
2. Run the configure command:

```bash
kom configure
```

3. Paste your API key when prompted. That's it! Your key will be saved securely in your user directory

## 💡 Usage

The primary command is ask. Just pass your request as a string.

Windows Example
```bash
kom ask "using winget, install the latest versions of 7zip and vlc"
```

Linux Example
```bash
kom ask "find all files larger than 100MB in my home directory and list the top 10"
```

macOs Example
```bash
kom ask "using brew, install neovim and update all existing formulas"
```

After running the command, you will be presented with the generated script and the choice to execute, copy, or abort.

## 🤝 Contributing
Contributions are welcome! Whether it's reporting a bug, suggesting a feature, or submitting a pull request, your help is appreciated. Please read our CONTRIBUTING.md to get started.

## 📄 License
This project is licensed under the MIT License. See the LICENSE file for details.