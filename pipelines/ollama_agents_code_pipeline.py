from typing import List, Union, Generator, Iterator
from schemas import OpenAIChatMessage
from pydantic import BaseModel
import requests


class Pipeline:
    class Valves(BaseModel):
        OLLAMA_BASE_URL: str
        MODEL: str

    def __init__(self):
        self.name = "Code Review Plugin"
        self.valves = self.Valves(**{
            "OLLAMA_BASE_URL": "http://host.docker.internal:11434",
            "MODEL": "codestral:latest"
        })
        pass

    async def on_startup(self):
        print(f"on_startup:{__name__}")
        pass

    async def on_shutdown(self):
        print(f"on_shutdown:{__name__}")
        pass

    async def on_valves_updated(self):
        print(f"on_valves_updated:{__name__}")
        pass

    def analyze_code(self, code: str) -> str:
        prompt = f"Analyze the submitted code for potential issues, such as syntax errors, code smells, security vulnerabilities, and performance bottlenecks. Provide a report of the findings in markdown format:\n--\nCode: {code}"
        
        try:
            r = requests.post(
                url=f"{self.valves.OLLAMA_BASE_URL}/v1/chat/completions",
                json={"model": self.valves.MODEL, "messages": [{"role": "user", "content": prompt}]},
                stream=False,
            )

            r.raise_for_status()

            response = r.json()
            analysis_report = response["choices"][0]["message"]["content"]

            formatted_output = f"## Agent 0: Code Analysis Report\n\n{analysis_report}"
            return formatted_output, analysis_report
        except Exception as e:
            error_message = f"Error occurred during code analysis: {e}"
            print(error_message)
            return f"## Agent 0: An error occurred. Please try again later.", None

    def refactor_code(self, code: str, analysis: str) -> str:
        prompt = f"Provide suggestions for refactoring the submitted code to improve its structure, readability, and maintainability. Identify opportunities for applying design patterns, removing duplication, and enhancing code organization. Provide the suggestions in markdown format:\n--\nCode: {code}\n--\nCode Analysis: {analysis}"
        
        try:
            r = requests.post(
                url=f"{self.valves.OLLAMA_BASE_URL}/v1/chat/completions",
                json={"model": self.valves.MODEL, "messages": [{"role": "user", "content": prompt}]},
                stream=False,
            )

            r.raise_for_status()

            response = r.json()
            refactoring_suggestions = response["choices"][0]["message"]["content"]

            formatted_output = f"## Agent 1: Code Refactoring Suggestions\n\n{refactoring_suggestions}"
            return formatted_output, refactoring_suggestions
        except Exception as e:
            error_message = f"Error occurred during code refactoring: {e}"
            print(error_message)
            return f"## Agent 1: An error occurred. Please try again later.", None

    def moderate_review(self, code: str, analysis: str, refactoring_suggestions: str) -> str:
        prompt = f"Summarize the key findings and recommendations from the code review process. Provide an overall assessment of the code quality and suggest next steps for the developer. Include insights from the code analysis and give a complete code block applying the refactoring suggestions in markdown format:\n--\nCode: {code}\n--\nCode Analysis: {analysis}\nRefactoring Suggestions: {refactoring_suggestions}"
        
        try:
            r = requests.post(
                url=f"{self.valves.OLLAMA_BASE_URL}/v1/chat/completions",
                json={"model": self.valves.MODEL, "messages": [{"role": "user", "content": prompt}]},
                stream=False,
            )

            r.raise_for_status()

            response = r.json()
            moderated_review = response["choices"][0]["message"]["content"]

            formatted_output = f"## Agent 2: Moderated Code Review\n\n{moderated_review}"
            return formatted_output, moderated_review
        except Exception as e:
            error_message = f"Error occurred during code review moderation: {e}"
            print(error_message)
            return f"## Agent 2: An error occurred. Please try again later.", None

    def prioritize_issues(self, code: str, analysis: str, refactoring_suggestions: str, review: str) -> str:
        prompt = f"Prioritize the identified issues based on their severity and impact on the codebase. Categorize them as high, medium, or low priority in markdown format:\n--\nCode: {code}\n--\nCode Analysis: {analysis}\nRefactoring Suggestions: {refactoring_suggestions}\nReview: {review}"
        
        try:
            r = requests.post(
                url=f"{self.valves.OLLAMA_BASE_URL}/v1/chat/completions",
                json={"model": self.valves.MODEL, "messages": [{"role": "user", "content": prompt}]},
                stream=False,
            )

            r.raise_for_status()

            response = r.json()
            prioritized_issues = response["choices"][0]["message"]["content"]

            formatted_output = f"## Agent 3: Prioritized Issues\n\n{prioritized_issues}"
            return formatted_output
        except Exception as e:
            error_message = f"Error occurred during issue prioritization: {e}"
            print(error_message)
            return f"## Agent 3: An error occurred. Please try again later."

    def generate_test_cases(self, code: str, analysis: str, refactoring_suggestions: str, review: str) -> str:
        prompt = f"Generate test cases to cover the identified issues and ensure the correctness of the refactored code. Provide examples of test inputs and expected outputs in markdown format:\n--\nCode: {code}\n--\nCode Analysis: {analysis}\nRefactoring Suggestions: {refactoring_suggestions}\nReview: {review}"
        
        try:
            r = requests.post(
                url=f"{self.valves.OLLAMA_BASE_URL}/v1/chat/completions",
                json={"model": self.valves.MODEL, "messages": [{"role": "user", "content": prompt}]},
                stream=False,
            )

            r.raise_for_status()

            response = r.json()
            test_cases = response["choices"][0]["message"]["content"]

            formatted_output = f"## Agent 4: Generated Test Cases\n\n{test_cases}"
            return formatted_output
        except Exception as e:
            error_message = f"Error occurred during test case generation: {e}"
            print(error_message)
            return f"## Agent 4: An error occurred. Please try again later."

    def pipe(
        self, user_message: str, model_id: str, messages: List[dict], body: dict
    ) -> Union[str, Generator, Iterator]:
        print(f"pipe:{__name__}")

        if "user" in body:
            print("######################################")
            print(f'# User: {body["user"]["name"]} ({body["user"]["id"]})')
            print(f"# Message: {user_message}")
            print("######################################")

        # Call the analyze_code function with the user's code
        code_analysis_report, analysis = self.analyze_code(user_message)

        # Call the refactor_code function with the user's code and the code analysis report
        code_refactoring_suggestions, refactoring_suggestions = self.refactor_code(user_message, analysis)

        # Call the moderate_review function with the user's code, code analysis report, and refactoring suggestions
        moderated_review, review = self.moderate_review(user_message, analysis, refactoring_suggestions)

        # Call the prioritize_issues function with the user's code, code analysis report, refactoring suggestions, and moderated review
        prioritized_issues = self.prioritize_issues(user_message, analysis, refactoring_suggestions, review)

        # Call the generate_test_cases function with the user's code, code analysis report, refactoring suggestions, and moderated review
        generated_test_cases = self.generate_test_cases(user_message, analysis, refactoring_suggestions, review)

        # Combine the outputs of Agent 0, Agent 1, Agent 2, Agent 3, and Agent 4
        final_output = f"{code_analysis_report}\n\n{code_refactoring_suggestions}\n\n{moderated_review}\n\n{prioritized_issues}\n\n{generated_test_cases}"

        return final_output
