from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from langchain_community.chat_models import ChatCohere
from langchain_groq import ChatGroq
import subprocess
import os
from agentops.agent import track_agent
import agentops
from agentops.langchain_callback_handler import LangchainCallbackHandler
# Initialize agentops
agentops.init(tags=["resume-tailor-demo"])


@CrewBase
class AiResumeTailorCrew:
    """AiResumeTailor crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    def __init__(self) -> None:
        # Groq LLM
        self.groq_llm = ChatGroq(
            temperature=0.3,
            groq_api_key=os.environ.get("GROQ_API_KEY"),
            model_name="llama3-70b-8192",
            callbacks=[LangchainCallbackHandler()],
        )
        # Cohere LLM
        self.cohere_llm = ChatCohere(
            cohere_api_key=os.environ["COHERE_API_KEY"],
            model="command-r-plus",
            temperature=0.5,
        )

    @track_agent(name="job_analyzer")
    @agent
    def job_analyzer(self) -> Agent:
        """Agent responsible for analyzing job descrption and generating insights."""
        return Agent(
            config=self.agents_config["job_analyzer"],
            llm=self.groq_llm,
            allow_delegation=False,
            verbose=True,
        )

    @track_agent(name="resume_modifier")
    @agent
    def resume_modifier(self) -> Agent:
        """Agent responsible for generating modified resume latex"""
        return Agent(
            config=self.agents_config["resume_modifier"],
            llm=self.groq_llm,
            allow_delegation=False,
            verbose=True,
        )

    @task
    def skill_extraction_task(self) -> Task:
        return Task(
            config=self.tasks_config["skill_extraction_task"],
            agent=self.job_analyzer(),
            output_file="./outputs/analysis.md",
        )

    @task
    def resume_modify_task(self) -> Task:
        return Task(
            config=self.tasks_config["resume_modify_task"],
            agent=self.resume_modifier(),
            output_file="./outputs/tailored_resume_partial.tex",
            callback=self.convert_to_pdf,
        )

    @crew
    def crew(self) -> Crew:
        """Creates the AiResumeTailor crew"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=2,
        )

    @agentops.record_function("convert_to_pdf")
    def convert_to_pdf(self, output: str) -> None:

        with open("./outputs/packages.tex", "r") as file:
            packages_chunk = file.read()

        with open("./outputs/tailored_resume_partial.tex", "r") as file:
            resume_chunk = file.read()

        complete_content = (
            packages_chunk
            + "\\begin{document}"
            + "\n"
            + resume_chunk
            + "\n"
            + "\\end{document}"
        )

        final_destination = "./outputs/Tailored_Resume.tex"
        with open(final_destination, "w") as file:
            file.write(complete_content)

        try:
            subprocess.run(["pdflatex", "-output-directory=outputs", final_destination])
            for filename in (
                "Tailored_Resume.aux",
                "Tailored_Resume.log",
                "Tailored_Resume.out",
                "tailored_resume_partial.tex",
                "packages.out",
            ):
                filepath = './outputs/' + filename
                if os.path.exists(filepath):
                    os.remove(filepath)
        except subprocess.CalledProcessError as e:
            print(f"An error occurred during LaTeX compilation: {e}")
