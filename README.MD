# AI Resume Tailor Crew

Welcome to the AiResumeTailor Crew project, powered by [crewAI](https://crewai.com). This template is designed to help you set up a multi-agent AI system with ease, leveraging the powerful and flexible framework provided by crewAI.

## Installation

Ensure you have Python >=3.10 <=3.13 installed on your system. This project uses [Poetry](https://python-poetry.org/) for dependency management and package handling, offering a seamless setup and execution experience.

First, if you haven't already, install Poetry:

```bash
pip install poetry
```

Next, navigate to your project directory and install the dependencies:

1. First lock the dependencies and then install them:
```bash
poetry lock
```
```bash
poetry install
```
### Customizing

**Add your `COHERE_API_KEY`, `AGENTOPS_API_KEY`, and `GROQ_API_KEYinto` in the `.env` file**

- Modify `src/ai_resume_tailor/config/agents.yaml` to customize your agents
- Modify `src/ai_resume_tailor/config/tasks.yaml` to customize your tasks
- Modify `src/ai_resume_tailor/crew.py` to add your own logic, tools and specific args
- Modify `src/ai_resume_tailor/main.py` to add custom inputs for your agents and tasks

## Running the Project

To kickstart your crew of AI agents and begin task execution, run this from the root folder of your project:

**Make sure to delete files from outputs folder first.**

```bash
poetry run ai_resume_tailor
```

This command initializes the ai-resume-tailor Crew, assembling the agents and assigning them tasks as defined in your configuration.

## Understanding Your Crew

The ai-resume-tailor Crew is composed of multiple AI agents, each with unique roles, goals, and tools. These agents collaborate on a series of tasks, defined in `config/tasks.yaml`, leveraging their collective skills to achieve complex objectives. The `config/agents.yaml` file outlines the capabilities and configurations of each agent in your crew.

## Challenges Faced:
- Extracting just the job description from URL as there is usually a lot of random text from other elements which is not needed.

- Figuring out logic of data flow for each of the steps in: ```User Input -> Agents -> LLM output -> PDF```.

- Figuring out the right amount and type of data to provide to LLM (e.g extracting latex code for packages and only passig in main resume content to LLM).

- Prompt engineering for agents and tasks to get the output required.
    1. Not adding additional latex code of its own which can cause compilation errors when converting to PDF.

    2. Modifying all parts of the resume to match job description while still maintaining context of the initial experience and position.

## What I enjoyed:
- Solving a problem that almost every student / job applicant is facing which is crafting a customized resume for a job or just learning from what an ideal candidate resume would look like and try to incorporate it as much as possible.

- Its very visually appealing when you see the Tailored Resume.pdf creted and you can compare your old resume side by side to see what changed.


- Tracking my agents and custom functions I defined through AgentOps interactive dashboard.

## What value I found from it:
- Learning how to break down a big problem into smaller parts (e.g through the use of agents)

- Debugging and tracking your application is crucial when you have multiple agents and functions and important to incorporate error handling, logging through tools like AgentOps. 

## Future additions: 
- Use custom tools to create an additional markdown file which tells the candidate specific projects they should make based on the job description, including links to resources to create those projects.

- Enabling human input when updating resume so the user can add specific changes if needed.

- Have a user just upload a PDF instead of latex file to make it more robust.

- Accept a list of job description to tailor resumes for and name those tailored resumes.

- Output a ```difference.pdf``` file which highlights the difference between the original and new resume to make it clear to the user where the changes occurred.

- Generate a cover letter by combining information from user's resume and job description.

- Host it on a web application and deploy it for others to use.
