import asyncio

from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.connectors.ai.function_choice_behavior import FunctionChoiceBehavior
from semantic_kernel.connectors.ai.chat_completion_client_base import ChatCompletionClientBase
from semantic_kernel.contents.chat_history import ChatHistory
from semantic_kernel.functions.kernel_arguments import KernelArguments

from semantic_kernel.connectors.ai.open_ai.prompt_execution_settings.azure_chat_prompt_execution_settings import (
    AzureChatPromptExecutionSettings,
)

from lights_plugin import LightsPlugin

import logging
import os

async def main():
    # Initialize the kernel
    kernel = Kernel()

    # Add Azure OpenAI chat completion service to the kernel
    chat_completion = AzureChatCompletion(
        deployment_name="gpt-4o",
        api_key=os.getenv("AX_AZURE_OPENAI_API_KEY"),
        endpoint=os.getenv("AX_AI_ENDPOINT"),
        api_version="2024-05-01-preview"
    )
    kernel.add_service(chat_completion)

    # Add Enterprise Services like logging to the kernel
    # Set the logging level for  semantic_kernel.kernel to DEBUG.
    logging.basicConfig(
        format="[%(asctime)s - %(name)s:%(lineno)d - %(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    logging.getLogger("kernel").setLevel(logging.DEBUG)

    # Get the chat completion service from the kernel (No need to build the kernel in Python)
    chat_completion : AzureChatCompletion = kernel.get_service(type=ChatCompletionClientBase)

    # Add the plugin to the kernel
    kernel.add_plugin(
        LightsPlugin(),
        plugin_name="Lights",
    )

    # Enable (planning) automatic function calling
    execution_settings = AzureChatPromptExecutionSettings()
    execution_settings.function_choice_behavior = FunctionChoiceBehavior.Auto()

    # Create a history of the conversation
    history = ChatHistory()

    # Initiate a back-and-forth chat
    userInput = None
    while True:
        # Collect user input
        userInput = input("User > ")

        # Terminate the loop if the user says "exit"
        if userInput == "exit":
            break

        # Add user input to the history
        history.add_user_message(userInput)

        # Get the response from the AI with automatic function calling
        result = await chat_completion.get_chat_message_content(
            chat_history=history,
            settings=execution_settings,
            kernel=kernel,
        )

        # Print the results
        print("Assistant > " + str(result))

        # Add the message from the agent to the chat history
        history.add_message(result) 

# Run the main function
if __name__ == "__main__":
    asyncio.run(main())