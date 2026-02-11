import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions, call_function


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError("API key not found")

    client = genai.Client(api_key=api_key)

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages = [types.Content(role="user", parts=[types.Part(text=args.prompt)])]

    for _ in range(20):
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions],
                system_instruction=system_prompt
                )
        )

        if response.candidates:
            for candidate in response.candidates:
                messages.append(candidate.content)

        if args.verbose: 
            print(f"User prompt: {args.prompt}")
            if response.usage_metadata is not None:
                print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
                print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
            else:
                raise RuntimeError("usage_metadata property is not found")

        function_results = []

        if response.function_calls:
            for fc in response.function_calls:
                function_call_result = call_function(fc, verbose=args.verbose)

                if not function_call_result.parts:
                    raise RuntimeError("Tool response had no parts")

                fr = function_call_result.parts[0].function_response
                if fr is None:
                    raise RuntimeError("First part missing function_response")

                if fr.response is None:
                    raise RuntimeError("FunctionResponse missing response")

                function_results.append(function_call_result.parts[0])

                if args.verbose:
                    print(f"-> {fr.response}")
            
            messages.append(types.Content(role="user", parts=function_results))

        else:
            print("Response:")
            print(response.text)
            break
    else:
        print("Maximum iterations reached; the model did not produce a final response.")
        exit(1)

if __name__ == "__main__":
    main()
