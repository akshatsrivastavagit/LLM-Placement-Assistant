# LLM-Powered Placement Preparation Assistant

## Overview
The **LLM-Powered Placement Preparation Assistant** is a web-based application that helps users prepare for job placements using AI-powered assistance. It provides personalized coding practice, system design guidance, mock interviews, resume analysis, and much more.

## Features
- **Document Processing & Summarization:** Extracts and summarizes text from PDFs and images using Tesseract OCR and PyMuPDF.
- **Code Explanation:** Provides step-by-step explanations and optimizations for code in various languages.
- **DSA Problem Generation:** Generates custom data structures and algorithm problems.
- **Mock Tests:** Creates coding mock tests based on selected topics and difficulty levels.
- **Networking & System Design:** Offers networking cheatsheets and detailed system design guides.
- **STAR Response Generator:** Generates behavioral interview responses using the STAR method.
- **Mock HR Interviews:** Prepares users with tailored HR interview questions.
- **Resume Analysis:** Compares resumes with job descriptions and suggests improvements.
- **Company-Specific Preparation:** Provides interview tips and commonly asked questions for specific companies.
- **Study Plan Generation:** Creates personalized study plans based on user goals and current skills.

## Tech Stack
- **Frontend:** Gradio
- **Backend:** Python
- **AI Model:** OpenAI API (via OpenRouter)
- **OCR:** Tesseract
- **PDF Processing:** PyMuPDF (fitz)

## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/placement-preparation-assistant.git
    cd placement-preparation-assistant
    ```
2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3. Set up environment variables:
    ```bash
    export API_KEY=your_openai_api_key
    ```
4. Run the application:
    ```bash
    python app.py
    ```

## Usage
1. Access the app at `http://localhost:7860`
2. Choose from the available features using the tabbed interface.
3. Upload documents, generate problems, analyze resumes, or get interview preparation tips.

## API Configuration
The project uses OpenAI API via OpenRouter. Ensure your API key is set correctly in `API_KEY`.

## Contribution
Feel free to contribute by submitting issues or making pull requests. Ensure proper documentation for any new features.

## License
This project is licensed under the MIT License. See `LICENSE` for more information.

