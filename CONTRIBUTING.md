# Contributing to `flaskcwg.github.io`

## Setup Instructions

### 1. **Fork the Repository**
- Navigate to the [repository's fork page](https://github.com/flaskcwg/flaskcwg.github.io/fork).
- Click the "Fork" button to create a copy of the repository under your GitHub account.

### 2. **Clone Your Forked Repository**
- Clone your fork to your local machine:

    ```bash
    git clone https://github.com/{username}/flaskcwg.github.io.git
    cd flaskcwg.github.io
    ```

### 3. **Set Up the Upstream Remote**
- Add the original repository as an upstream remote to keep your fork synchronized:

    ```bash
    git remote add upstream https://github.com/flaskcwg/flaskcwg.github.io.git
    ```

### 4. **Create and Activate a Virtual Environment**
- **For Linux/Mac**:

    ```bash
    python -m venv env
    source env/bin/activate
    ```

- **For Windows**:

    ```bash
    py -m venv env
    source env\Scripts\activate
    ```

### 5. **Install Dependencies**
- Install the required Python dependencies:

    ```bash
    pip install -r requirements.txt
    ```

### 6. **Build the Static HTML Content**
- Run the `static.py` script to generate the HTML content in the `docs/` directory:

    ```bash
    python static.py
    ```

### 7. **Serve the Generated Site**
- Serve the generated content locally by running the `serve.py` script:

    ```bash
    cd docs
    python serve.py
    ```

- Access the site using the IP address displayed in the console output.

### 8. **Push Your Changes to Your Fork**
- Add your fork as a remote to push your contributions. Replace `{username}` with your GitHub username. This step names your forked repository remote as `fork` while retaining `origin` for the original repository:

    ```bash
    git remote add fork https://github.com/{username}/flaskcwg.github.io.git
    ```

---

### Notes:
- Ensure your fork is updated with the upstream repository before starting new work by running:
    ```bash
    git fetch upstream
    git merge upstream/main
    ```
- Submit your contributions via a pull request after committing your changes to your forked repository.

By following these instructions, you'll be able to set up your environment and contribute effectively. Happy coding! 🎉
