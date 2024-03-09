"""
This module contains the AnthropicService class which
is used for generating LinkedIn posts using the Anthropic API.

The AnthropicService class initializes with an API key obtained from the environment variables.
It uses this key to interact with the Anthropic API.

The main functionality of the AnthropicService class is provided by the `generate_response` method.
This method takes a prompt as input and generates a LinkedIn post
based on this prompt using the Anthropic API.

Example:
    service = AnthropicService()
    post = service.generate_response("Prompt for the post")

This module requires the 'anthropic' and 'python-dotenv' packages to be installed.
"""

import os
import json
import anthropic
from dotenv import load_dotenv


class AnthropicService:
    """
    A service class for generating LinkedIn posts using the Anthropic API.
    """

    def __init__(self):
        """
        Initializes the AnthropicService class.
        """
        load_dotenv()
        self.llm = anthropic.Anthropic(
            api_key=os.getenv("ANTHROPIC_API_KEY"),
        )

    def generate_reponse(self, prompt: str):
        """
        Generates a LinkedIn post based on the given prompt.

        Args:
            prompt (str): The prompt for generating the LinkedIn post.

        Returns:
            dict: A dictionary containing the generated LinkedIn post"
            "with keys 'content', 'keywords', and 'title'.
        """
        system_prompt = (
            "You are a marketing expert, specialized in writing LinkedIn"
            "posts to build a personal brand on the platform."
            "Always start with a strong hook on the first line and"
            "limit posts to 800 characters or less."
            "Use emoijs where appropriate, but never more than 3 in one post"
            "The user will provide the topics and extra details to include in the post."
            "Output in JSON format, with the following keys: content, keywords, title"
            "content: the full linkedin post, with the content properly escaped"
            "and formatted with every paragraph separated by a newline character."
            "keywords: list of relevant keywords for the post,"
            "title: a title for the post for internal reference in CMS"
        )

        message = self.llm.messages.create(
            model="claude-3-sonnet-20240229",  # Most balanced model
            max_tokens=1000,
            temperature=0.0,
            system=system_prompt,
            messages=[
                {"role": "user", "content": prompt},
                {
                    "role": "assistant",
                    "content": "{",
                },  # Prefill Claude's response to force JSON output
            ],
        )

        # Attempt to correctly escape and format the JSON string
        try:
            # Create a valid JSON string with the escaped content
            json_string = "{" + message.content[0].text
            parsed_result = json.loads(json_string)
            return parsed_result
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {e}")
            return None


anthropic_service = AnthropicService()


result = anthropic_service.generate_reponse(
    prompt="Write a linkedin post about the often overlooked importance data plays in AI strategy."
)

print(result["content"])
