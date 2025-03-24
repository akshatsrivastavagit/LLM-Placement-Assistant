import gradio as gr
import os
import tempfile
import base64
from PIL import Image
import pytesseract
import fitz
import time
import json
from openai import OpenAI

API_KEY = "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"
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=API_KEY,
)

def extract_text_from_image(image_path):
    """Extract text from an image using Tesseract OCR"""
    try:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img)
        return text
    except Exception as e:
        return f"Error extracting text: {str(e)}"

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file"""
    try:
        text = ""
        doc = fitz.open(pdf_path)
        for page in doc:
            text += page.get_text()
        return text
    except Exception as e:
        return f"Error extracting text from PDF: {str(e)}"

def process_document(file):
    """Process uploaded document and extract text"""
    if file is None:
        return "No file uploaded"
    
    file_path = file.name
    file_ext = os.path.splitext(file_path)[1].lower()
    
    if file_ext in ['.jpg', '.jpeg', '.png', '.bmp']:
        return extract_text_from_image(file_path)
    elif file_ext == '.pdf':
        return extract_text_from_pdf(file_path)
    else:
        return "Unsupported file format. Please upload an image or PDF."

def generate_llm_response(prompt, max_tokens=5000):
    """Generate response from LLM API"""
    try:
        completion = client.chat.completions.create(
            extra_headers={
                "HTTP-Referer": "https://placement-assistant.com",
                "X-Title": "Placement Preparation Assistant",
            },
            model="google/gemini-2.0-pro-exp-02-05:free",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=max_tokens
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Error generating response: {str(e)}"

def summarize_document(file, focus_area):
    """Extract and summarize content from uploaded document"""
    extracted_text = process_document(file)
    if extracted_text.startswith("Error"):
        return extracted_text
    
    prompt = f"""
    I've extracted the following text from a document related to placement preparation:
    
    {extracted_text[:4000]}  # Limiting text length to avoid token limits
    
    Please provide the following based on this content, focusing on {focus_area}:
    1. Key points and concepts
    2. Important topics to understand
    3. Concise explanations of complex ideas
    4. Suggested additional study materials
    
    Format your response in markdown for better readability.
    """
    
    return generate_llm_response(prompt)

def explain_code(code, language):
    """Explain code and suggest optimizations"""
    prompt = f"""
    Please explain the following {language} code step by step:
    
    ```{language}
    {code}
    ```
    
    Include:
    1. A clear explanation of what the code does
    2. Time and space complexity analysis
    3. Potential optimizations or improvements
    4. Any edge cases or bugs to be aware of
    
    Format your response in markdown.
    """
    
    return generate_llm_response(prompt)

def generate_dsa_problems(topic, difficulty, count=5):
    """Generate DSA problems based on topic and difficulty"""
    prompt = f"""
    Generate {count} {difficulty} level Data Structures and Algorithms problems on the topic of {topic}.
    
    For each problem:
    1. Provide a clear problem statement
    2. Include example inputs and outputs
    3. Mention constraints
    4. Give a hint (without revealing the full solution)
    5. Explain the approach to solve it
    
    Format your response in markdown.
    """
    
    return generate_llm_response(prompt)

def create_mock_test(topics, difficulty, duration):
    """Create a mock coding test"""
    prompt = f"""
    Create a mock coding test with the following parameters:
    - Topics: {topics}
    - Difficulty: {difficulty}
    - Duration: {duration} minutes
    
    Include:
    1. 3 coding problems of varying difficulty
    2. Clear problem statements with examples
    3. Constraints and input/output formats
    4. Evaluation criteria
    
    Format your response in markdown.
    """
    
    return generate_llm_response(prompt)

def generate_networking_cheatsheet(topic):
    """Generate networking cheatsheet"""
    prompt = f"""
    Create a comprehensive cheatsheet on the networking topic: {topic}
    
    Include:
    1. Key concepts and definitions
    2. Important protocols and their functions
    3. Common issues and troubleshooting steps
    4. Diagrams or visual explanations (described in text)
    5. Interview questions and answers related to this topic
    
    Format your response in markdown.
    """
    
    return generate_llm_response(prompt)

def system_design_guide(system):
    """Generate system design guide"""
    prompt = f"""
    Create a comprehensive system design guide for building {system}.
    
    Include:
    1. Requirements clarification
    2. System interface definition
    3. Back-of-the-envelope calculations
    4. System API design
    5. Database schema
    6. High-level component design
    7. Detailed component design
    8. Scaling the system
    9. Handling edge cases
    10. Common interview questions about this system
    
    Format your response in markdown with clear sections.
    """
    
    return generate_llm_response(prompt, max_tokens=2000)

def generate_star_response(experience):
    """Generate STAR-based response for behavioral questions"""
    prompt = f"""
    Based on the following experience:
    
    "{experience}"
    
    Generate a structured STAR (Situation, Task, Action, Result) response that could be used in a job interview.
    
    Make sure to:
    1. Clearly define the Situation
    2. Explain the Task that needed to be accomplished
    3. Detail the Actions taken
    4. Highlight the Results achieved
    5. Include metrics or specific achievements where possible
    
    Format your response in markdown.
    """
    
    return generate_llm_response(prompt)

def mock_hr_interview(job_role, experience_level):
    """Generate mock HR interview questions"""
    prompt = f"""
    Create a mock HR interview for a {job_role} position at {experience_level} level.
    
    Include:
    1. 10 common HR questions for this role
    2. 5 behavioral questions specific to this role
    3. 3 situational questions
    4. Tips for answering each type of question
    5. Common mistakes to avoid
    
    Format your response in markdown.
    """
    
    return generate_llm_response(prompt)

def analyze_resume(file, job_description):
    resume_text = process_document(file)
    if resume_text.startswith("Error"):
        return resume_text
    """Analyze resume and suggest improvements"""
    prompt = f"""
    I'll provide a resume and a job description. Please:
    
    1. Analyze how well the resume matches the job requirements
    2. Suggest specific improvements to better align with the job
    3. Identify missing keywords or skills
    4. Recommend formatting or content changes
    5. Generate a tailored cover letter for this job
    
    Resume:
    {resume_text[:2000]}
    
    Job Description:
    {job_description[:1000]}
    
    Format your response in markdown with clear sections.
    """
    
    return generate_llm_response(prompt, max_tokens=1500)

def company_specific_prep(company_name, job_role):
    """Generate company-specific preparation guide"""
    prompt = f"""
    Create a comprehensive interview preparation guide for {job_role} position at {company_name}.
    
    Include:
    1. Company background and culture
    2. Common interview process for this role
    3. Frequently asked technical questions
    4. Typical behavioral questions
    5. Required skills and how to demonstrate them
    6. Tips from successful candidates
    7. Resources for further preparation
    
    Format your response in markdown with clear sections.
    """
    
    return generate_llm_response(prompt)

def generate_study_plan(job_role, available_time, current_skills):
    """Generate personalized study plan"""
    prompt = f"""
    Create a detailed study plan for preparing for a {job_role} role with the following parameters:
    
    - Available time per day: {available_time} hours
    - Current skills: {current_skills}
    
    The study plan should include:
    1. Week-by-week breakdown of topics to cover
    2. Daily schedule with specific tasks
    3. Resource recommendations for each topic
    4. Practice exercises and mock tests
    5. Revision strategy
    6. Milestones and progress tracking
    
    Format your response in markdown with clear sections and tables.
    """
    
    return generate_llm_response(prompt, max_tokens=2000)

with gr.Blocks(title="LLM-Powered Placement Preparation Assistant") as app:
    gr.Markdown("# 🚀 LLM-Powered Placement Preparation Assistant")
    gr.Markdown("Prepare for placements with AI-powered assistance for all aspects of your interview preparation.")
    
    with gr.Tab("📄 Document Processing & Summarization"):
        gr.Markdown("### Upload your study materials and get key insights")
        
        with gr.Row():
            with gr.Column():
                doc_file = gr.File(label="Upload Document (PDF/Image)")
                focus_area = gr.Dropdown(
                    choices=["Data Structures", "Algorithms", "System Design", "Networking", "Operating Systems", "Database Management", "General Concepts"],
                    label="Focus Area",
                    value="General Concepts"
                )
                summarize_btn = gr.Button("Extract & Summarize")
            
            with gr.Column():
                summary_output = gr.Markdown(label="Summary & Key Points")
        
        summarize_btn.click(
            fn=summarize_document,
            inputs=[doc_file, focus_area],
            outputs=summary_output
        )
    
    with gr.Tab("💻 DSA & Competitive Programming"):
        gr.Markdown("### Improve your coding skills with personalized assistance")
        
        with gr.Tabs():
            with gr.Tab("Code Explainer"):
                with gr.Row():
                    with gr.Column():
                        code_input = gr.Textbox(
                            label="Paste your code here",
                            placeholder="Paste your code here...",
                            lines=10
                        )
                        code_lang = gr.Dropdown(
                            choices=["Python", "Java", "C++", "JavaScript", "Go", "C#"],
                            label="Language",
                            value="Python"
                        )
                        explain_btn = gr.Button("Explain Code")
                    
                    with gr.Column():
                        code_explanation = gr.Markdown(label="Code Explanation")
                
                explain_btn.click(
                    fn=explain_code,
                    inputs=[code_input, code_lang],
                    outputs=code_explanation
                )
            
            with gr.Tab("DSA Problems"):
                with gr.Row():
                    with gr.Column():
                        dsa_topic = gr.Dropdown(
                            choices=["Arrays", "Strings", "Linked Lists", "Stacks & Queues", "Trees", "Graphs", "Dynamic Programming", "Greedy Algorithms", "Sorting & Searching", "Hashing"],
                            label="Topic",
                            value="Arrays"
                        )
                        dsa_difficulty = gr.Radio(
                            choices=["Easy", "Medium", "Hard"],
                            label="Difficulty",
                            value="Medium"
                        )
                        dsa_count = gr.Slider(
                            minimum=1,
                            maximum=10,
                            value=5,
                            step=1,
                            label="Number of Problems"
                        )
                        dsa_btn = gr.Button("Generate Problems")
                    
                    with gr.Column():
                        dsa_problems = gr.Markdown(label="Generated Problems")
                
                dsa_btn.click(
                    fn=generate_dsa_problems,
                    inputs=[dsa_topic, dsa_difficulty, dsa_count],
                    outputs=dsa_problems
                )
            
            with gr.Tab("Mock Coding Test"):
                with gr.Row():
                    with gr.Column():
                        test_topics = gr.Textbox(
                            label="Topics (comma-separated)",
                            placeholder="Arrays, Strings, Dynamic Programming",
                            value="Arrays, Strings, Dynamic Programming"
                        )
                        test_difficulty = gr.Radio(
                            choices=["Easy", "Medium", "Hard", "Mixed"],
                            label="Difficulty",
                            value="Mixed"
                        )
                        test_duration = gr.Slider(
                            minimum=30,
                            maximum=180,
                            value=60,
                            step=15,
                            label="Duration (minutes)"
                        )
                        test_btn = gr.Button("Create Mock Test")
                    
                    with gr.Column():
                        mock_test = gr.Markdown(label="Mock Test")
                
                test_btn.click(
                    fn=create_mock_test,
                    inputs=[test_topics, test_difficulty, test_duration],
                    outputs=mock_test
                )
    
    with gr.Tab("🌐 Networking & System Design"):
        gr.Markdown("### Master networking concepts and system design principles")
        
        with gr.Tabs():
            with gr.Tab("Networking Cheatsheet"):
                with gr.Row():
                    with gr.Column():
                        network_topic = gr.Dropdown(
                            choices=["OSI Model", "TCP/IP", "HTTP/HTTPS", "DNS", "Load Balancing", "Firewalls", "VPN", "Subnetting", "Routing Protocols", "Wireless Networks"],
                            label="Networking Topic",
                            value="OSI Model"
                        )
                        network_btn = gr.Button("Generate Cheatsheet")
                    
                    with gr.Column():
                        network_cheatsheet = gr.Markdown(label="Networking Cheatsheet")
                
                network_btn.click(
                    fn=generate_networking_cheatsheet,
                    inputs=network_topic,
                    outputs=network_cheatsheet
                )
            
            with gr.Tab("System Design Guide"):
                with gr.Row():
                    with gr.Column():
                        system_name = gr.Textbox(
                            label="System to Design",
                            placeholder="URL Shortener, Twitter Clone, Netflix, etc.",
                            value="URL Shortener"
                        )
                        system_btn = gr.Button("Generate System Design Guide")
                    
                    with gr.Column():
                        system_guide = gr.Markdown(label="System Design Guide")
                
                system_btn.click(
                    fn=system_design_guide,
                    inputs=system_name,
                    outputs=system_guide
                )
    
    with gr.Tab("🎤 HR & Soft Skills Preparation"):
        gr.Markdown("### Prepare for behavioral and HR interviews")
        
        with gr.Tabs():
            with gr.Tab("STAR Response Generator"):
                with gr.Row():
                    with gr.Column():
                        experience_input = gr.Textbox(
                            label="Describe your experience",
                            placeholder="Describe a situation where you had to solve a complex problem...",
                            lines=5
                        )
                        star_btn = gr.Button("Generate STAR Response")
                    
                    with gr.Column():
                        star_response = gr.Markdown(label="STAR Response")
                
                star_btn.click(
                    fn=generate_star_response,
                    inputs=experience_input,
                    outputs=star_response
                )
            
            with gr.Tab("Mock HR Interview"):
                with gr.Row():
                    with gr.Column():
                        hr_job_role = gr.Textbox(
                            label="Job Role",
                            placeholder="Software Engineer, Data Scientist, etc.",
                            value="Software Engineer"
                        )
                        hr_experience = gr.Radio(
                            choices=["Entry Level", "Mid Level", "Senior Level"],
                            label="Experience Level",
                            value="Entry Level"
                        )
                        hr_btn = gr.Button("Generate Mock Interview")
                    
                    with gr.Column():
                        hr_interview = gr.Markdown(label="Mock HR Interview")
                
                hr_btn.click(
                    fn=mock_hr_interview,
                    inputs=[hr_job_role, hr_experience],
                    outputs=hr_interview
                )
    
    with gr.Tab("📄 Resume & Job Matching"):
        gr.Markdown("### Optimize your resume and prepare for specific companies")
        
        with gr.Tabs():
            # with gr.Tab("Resume Analyzer"):
            #     with gr.Row():
            #         with gr.Column():
            #             resume_text = gr.Textbox(
            #                 label="Paste your resume",
            #                 placeholder="Paste your resume text here...",
            #                 lines=10
            #             )
            #             job_desc = gr.Textbox(
            #                 label="Paste job description",
            #                 placeholder="Paste the job description here...",
            #                 lines=5
            #             )
            #             resume_btn = gr.Button("Analyze Resume")
                    
            #         with gr.Column():
            #             resume_analysis = gr.Markdown(label="Resume Analysis & Cover Letter")
                
            #     resume_btn.click(
            #         fn=analyze_resume,
            #         inputs=[resume_text, job_desc],
            #         outputs=resume_analysis
            #     )
            with gr.Tab("Resume Analyzer"):
                with gr.Row():
                    with gr.Column():
                        resume_file = gr.File(label="Upload Resume (PDF/Image/Text)")
                        job_desc = gr.Textbox(
                            label="Paste job description",
                            placeholder="Paste the job description here...",
                            lines=5
                        )
                        resume_btn = gr.Button("Analyze Resume")
                    
                    with gr.Column():
                        resume_analysis = gr.Markdown(label="Resume Analysis & Cover Letter")
                
                resume_btn.click(
                    fn=analyze_resume,
                    inputs=[resume_file, job_desc],
                    outputs=resume_analysis
                )
            
            with gr.Tab("Company-Specific Preparation"):
                with gr.Row():
                    with gr.Column():
                        company_name = gr.Textbox(
                            label="Company Name",
                            placeholder="Google, Amazon, Microsoft, etc.",
                            value="Google"
                        )
                        company_role = gr.Textbox(
                            label="Job Role",
                            placeholder="Software Engineer, Data Scientist, etc.",
                            value="Software Engineer"
                        )
                        company_btn = gr.Button("Generate Preparation Guide")
                    
                    with gr.Column():
                        company_guide = gr.Markdown(label="Company-Specific Preparation Guide")
                
                company_btn.click(
                    fn=company_specific_prep,
                    inputs=[company_name, company_role],
                    outputs=company_guide
                )
    
    with gr.Tab("📅 AI-Powered Study Planner"):
        gr.Markdown("### Get a personalized study plan based on your goals and available time")
        
        with gr.Row():
            with gr.Column():
                plan_role = gr.Textbox(
                    label="Target Job Role",
                    placeholder="Software Engineer, Data Scientist, etc.",
                    value="Software Engineer"
                )
                plan_time = gr.Slider(
                    minimum=1,
                    maximum=12,
                    value=4,
                    step=0.5,
                    label="Available Hours Per Day"
                )
                plan_skills = gr.Textbox(
                    label="Current Skills (comma-separated)",
                    placeholder="Python, Java, Basic DSA, etc.",
                    value="Python, Basic DSA, HTML/CSS"
                )
                # plan_date = gr.Textbox(
                #     label="Target Interview Date",
                #     placeholder="MM/DD/YYYY",
                #     value="06/26/2025"
                # )
                # plan_date = "06/26/2025"

                plan_btn = gr.Button("Generate Study Plan")
            
            with gr.Column():
                study_plan = gr.Markdown(label="Personalized Study Plan")
        
        plan_btn.click(
            fn=generate_study_plan,
            inputs=[plan_role, plan_time, plan_skills],
            outputs=study_plan
        )

if __name__ == "__main__":
    app.launch()