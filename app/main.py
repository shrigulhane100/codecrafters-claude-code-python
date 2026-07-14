import argparse
import os
import sys
import json

from openai import OpenAI

API_KEY = os.getenv("OPENROUTER_API_KEY")
BASE_URL = os.getenv("OPENROUTER_BASE_URL", default="https://openrouter.ai/api/v1")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("-p", required=True)
    args = p.parse_args()

    if not API_KEY:
        raise RuntimeError("OPENROUTER_API_KEY is not set")

    client = OpenAI(api_key=API_KEY, base_url=BASE_URL)
    messages = [{"role":"user", "content": args.p}]

    read_tool = {
                "type": "function",
                "function": {
                    "name": "Read",
                    "description": "Read and return the contents of a file",
                    "parameters": {
                    "type": "object",
                    "properties": {
                        "file_path": {
                        "type": "string",
                        "description": "The path to the file to read"
                        }
                    },
                    "required": ["file_path"]
                    }
                }
            }    

    tools = [read_tool]


    # chat = client.chat.completions.create(
    #     model="anthropic/claude-haiku-4.5",
    #     messages=[{"role": "user", "content": args.p}],
    #         tools=[read_tool]
    # )

    # if not chat.choices or len(chat.choices) == 0:
    #     raise RuntimeError("no choices in response")

    while True:
        chat = client.chat.completions.create(
        model="anthropic/claude-haiku-4.5",
        messages=[{"role": "user", "content": args.p}],
        tools=[read_tool])

        if not chat.choices or len(chat.choices) == 0:
            raise RuntimeError("no choices in response")

        choice = chat.choices[0]
        message = chat.choices[0].message

        assistant_message = {
            "role": "assistant",
            "content": message.content if message.content is not None else ""
        }

        if message.tool_calls:
            assistant_message["tool_calls"] = [
                {
                    "id": tc.id,
                    "type": tc.type,
                    "function": {
                        "name": tc.function.name,
                        "arguments": tc.function.arguments
                    }
                } for tc in message.tool_calls
            ]

        messages.append(assistant_message)

        if choice.finish_reason == "stop" or not message.tool_calls:
            if message.content:
                print(message.content)
            break

        
        # Check if the LLM decided to call any tools
        if message.tool_calls and len(message.tool_calls) > 0:
            # Extract the first tool call
            # tool_call = message.tool_calls[0]
            
            for tool_call in message.tool_calls:

                if tool_call.function.name == "Read":
                    arguments = json.loads(tool_call.function.arguments)
                    file_path = arguments.get("file_path")

                    try:
                        with open(file_path, 'r') as file:
                            # print(file.read(), end="")
                            tool_result = file.read()
                    # except FileNotFoundError:
                    #     print(f"Error: File '{file_path}' not found.", file=sys.stderr)
                    # except Exception as e:
                    #     print(f"Error reading file: {e}", file=sys.stderr)

                    except FileNotFoundError:
                        tool_result = f"Error: File '{file_path}' not found."
                        print(tool_result, file=sys.stderr)
                    except Exception as e:
                        tool_result = f"Error reading file: {e}"
                        print(tool_result, file=sys.stderr)

                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": tool_result
                    })
            
        else:
            if message.content:
                print(message.content)
            break

    # # You can use print statements as follows for debugging, they'll be visible when running tests.
    # print("Logs from your program will appear here!", file=sys.stderr)

    # # TODO: Uncomment the following line to pass the first stage
    # print(chat.choices[0].message.content)


if __name__ == "__main__":
    main()
