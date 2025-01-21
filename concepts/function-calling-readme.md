# Function Calling - Make AI orchestrator & LLM model great
LLM models like OpenAI, Gemini, etc are capable of iteratively calling functions to solve a user's need. This is accomplished by creating a feedback loop where the AI can call a function, check the result, and then decide what to do next. 

[How auto function calling works](https://learn.microsoft.com/en-us/semantic-kernel/concepts/ai-services/chat-completion/function-calling/?pivots=programming-language-csharp#how-auto-function-calling-works)

![alt txt](/images/functioncalling.png)

For example, a user may ask the AI to "toggle" a light bulb. The AI would first need to check the state of the light bulb before deciding whether to turn it on or off.

See below the example of parallel function calling

![alt txt](/images/functioncalling-eg.png)

[Concept in action & code](/src/lights-hello-semantic-kernel/)