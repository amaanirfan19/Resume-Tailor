#!/usr/bin/env python
from ai_resume_tailor.crew import AiResumeTailorCrew
from dotenv import load_dotenv
import agentops
import os
import requests
from bs4 import BeautifulSoup
import re

load_dotenv()
# Initialize agentops
agentops.init(tags=["resume-tailor-demo"])


@agentops.record_function("Scrape web")
def crawl_web(url: str) -> str:
    # Request url endpoint
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")

        # Remove headers and footers
        for header in soup.find_all("header"):
            header.decompose()
        for footer in soup.find_all("footer"):
            footer.decompose()

        # Retrieve all text
        text = soup.get_text()

        # Removes any extra newline characters and whitespace
        clean_text = re.sub(r"\n\s*\n", "\n", text)
        return clean_text

    else:
        raise ValueError("Failed to retrieve the webpage")


def remove_previous_output_files():
    for filename in (
        "packages.tex",
        "analysis.md",
        "tailored_resume_partial.tex",
        "Tailored_Resume.tex",
        "Tailored_Resume.pdf",
    ):
        filepath = "./outputs/" + filename
        if os.path.exists(filepath):
            os.remove(filepath)


def main():
    remove_previous_output_files()

    # Request input url from user input
    url = input("🚀 Enter Job Posting URL: ")
    # Scrapes that url and returns the text
    scraped_text = crawl_web(url)

    # Read in original resume latex file
    with open("original_resume.tex", "r") as file:
        tex_content = file.read()

    # 1. Split the resume latex file into packages and document chunks
    # 2. Remove \begin{document} and \end{document} tags to get the main resume content
    if "\\begin{document}" in tex_content:
        packages_chunk, document_chunk = tex_content.split("\\begin{document}", 1)
        document_chunk = document_chunk.replace("\\end{document}", "").strip()

        # Store the packages chunk in a latex file for later use
        with open("./outputs/packages.tex", "w") as file:
            file.write(packages_chunk)

    # Pass in these inputs to our agents
    inputs = {"job_description": scraped_text, "latex_resume": document_chunk}

    # Initialize the crew and kickoff!
    crew = AiResumeTailorCrew()
    crew.crew().kickoff(inputs=inputs)

    agentops.end_session("Success")


if __name__ == "__main__":
    main()
