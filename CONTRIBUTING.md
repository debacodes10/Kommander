# Contributing to Kommander

First off, thank you for considering contributing to Kommander! We're excited to build this project with the help of the community.

## How to Contribute

The best way to contribute right now is by reporting bugs or suggesting features.

* **Bug Reports:** If you find a bug, please open an issue and provide as much detail as possible, including your OS, the command you ran, and the unexpected output.
* **Feature Requests:** Have a great idea? Open an issue and describe how you see it working.

## Setting Up Your Development Environment

Ready to write some code? Here’s how to get started:

1.  **Fork & Clone:** Fork the repository to your own GitHub account and then clone it to your local machine.
    ```sh
    git clone [https://github.com/debacodes10/kommander.git](https://github.com/debacodes10/kommander.git)
    cd kommander
    ```

2.  **Create a Virtual Environment:** We strongly recommend using a Python virtual environment to manage dependencies.
    ```sh
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3.  **Install Dependencies:** Install the project in editable mode along with the development dependencies.
    ```sh
    pip install -e .[dev]
    ```

That's it! You should now be able to run the tool and execute the test suite.