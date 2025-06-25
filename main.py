import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

from prompts import system_prompt
from call_functions import available_functions, call_function

def main():
    load_dotenv()

    verbose = "--verbose" in sys.argv
    args = [arg for arg in sys.argv[1:] if not arg.startswith("--")]

    if not args:
        print("A prompt was not submitted")
        sys.exit(1)
    
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    prompt = " ".join(args)

    if verbose:
        print("User prompt:", prompt)

    messages = [
        types.Content(role="user", parts=[types.Part(text=prompt)]),
    ]

    max_iter = 20
    iter = 0
    while True:
        iter += 1
        if iter > max_iter:
            print("Reached max iterations")
            sys.exit(1)

        try:
            final_resp = generate_content(client, messages, verbose)
            if final_resp:
                print("Final response:")
                print(final_resp)
                break
        except Exception as e:
            print(f'Exception raised: {e}')

def generate_content(client, messages, verbose):
    response = client.models.generate_content(
        model="gemini-2.0-flash-001", 
        contents=messages, 
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt))

    if verbose:
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)

    if response.candidates:
        for candidate in response.candidates:
            messages.append(candidate.content)

    if not response.function_calls:
        return response.text

    function_responses = []
    for func in response.function_calls:
        func_call_result = call_function(func, verbose)

        if (not func_call_result.parts[0].function_response.response or not func_call_result.parts):
            raise Exception("No function response!")
        
        if verbose:
            print(f'-> {func_call_result.parts[0].function_response.response}')
        function_responses.append(func_call_result.parts[0])
    
    if not function_responses:
        raise Exception("There were no function responses")
    
    messages.append(types.Content(role="tool", parts=function_responses))

if __name__ == "__main__":
    main()
