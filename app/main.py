import argparse
import os
import json
from typing import Any, cast
from openai import OpenAI

from .utils import bash, get_tools, read_file, write_file

API_KEY = os.getenv("OPENROUTER_API_KEY")
BASE_URL = os.getenv("OPENROUTER_BASE_URL", default="https://openrouter.ai/api/v1")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("-p", required=True)
    args = p.parse_args()

    if not API_KEY:
        raise RuntimeError("OPENROUTER_API_KEY is not set")

    client = OpenAI(api_key=API_KEY, base_url=BASE_URL)
    messages = [{"role": "user", "content": args.p}]
    tools = get_tools()


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
            messages=messages,
            tools=tools
        )

        if not chat.choices or len(chat.choices) == 0:
            raise RuntimeError("no choices in response")

        response = chat.choices[0].message
        response_message = chat.choices[0].message
        message_dict = {
            "role": response_message.role,
            "content": response_message.content,
        }
        if hasattr(response_message, "tool_calls") and response_message.tool_calls:
            message_dict["tool_calls"] = [
                {
                    "id": tc.id,
                    "type": tc.type,
                    "function": {
                        "name": tc.function.name,
                        "arguments": tc.function.arguments,
                    },
                }
                for tc in response_message.tool_calls
            ]
        messages.append(message_dict)
        if not message_dict.get("tool_calls"):
            print(response.content)
            break

                # Check if the LLM decided to call any tools
        # if message.tool_calls and len(message.tool_calls) > 0:
            # Extract the first tool call
            # tool_call = message.tool_calls[0]
            
        #     for tool_call in message.tool_calls:

        #         if tool_call.function.name == "Read":
        #             arguments = json.loads(tool_call.function.arguments)
        #             file_path = arguments.get("file_path")

        #             try:
        #                 with open(file_path, 'r') as file:
        #                     # print(file.read(), end="")
        #                     tool_result = file.read()
        #             # except FileNotFoundError:
        #             #     print(f"Error: File '{file_path}' not found.", file=sys.stderr)
        #             # except Exception as e:
        #             #     print(f"Error reading file: {e}", file=sys.stderr)

        #             except FileNotFoundError:
        #                 tool_result = f"Error: File '{file_path}' not found."
        #                 print(tool_result, file=sys.stderr)
        #             except Exception as e:
        #                 tool_result = f"Error reading file: {e}"
        #                 print(tool_result, file=sys.stderr)

        #             messages.append({
        #                 "role": "tool",
        #                 "tool_call_id": tool_call.id,
        #                 "content": tool_result
        #             })
            
        # else:
        #     if message.content:
        #         print(message.content)
        #     break


        for tc in response.tool_calls:
            tool_name = getattr(tc.function, "name", None) or getattr(
                tc, "name", None
            )
            # args_dict = json.loads(tc.function.arguments)

            if tool_name == "Read":
                tool = read_file
            elif tool_name == "Write":
                tool = write_file
            elif tool_name == "Bash":
                tool = bash
            else:
                raise RuntimeError(f"Unknown tool: {tool_name}")

            # FIX 3: Catch file errors and feed them back to the LLM so it doesn't get stuck
            # if tc.function.name == "Read":
            #     with open(args_dict["file_path"], "r") as f:
            #         result = f.read()
            #         messages.append(
            #             {
            #                 "role": "tool",
            #                 "tool_call_id": tc.id,
            #                 "content": result,
            #             }
            #         )

            tool_args = getattr(tc.function, "arguments", None) or getattr(
                tc, "arguments", None
            )
            if tool_args is None:
                tool_kwargs = {}
            else:
                # Some runtimes may provide arguments as bytes; decode if needed
                if isinstance(tool_args, (bytes, bytearray)):
                    tool_args = tool_args.decode()
                tool_kwargs = json.loads(tool_args)
            result = tool(**tool_kwargs)
            messages.append(
                {"role": "tool", "tool_call_id": tc.id, "content": result}
            )


    # # You can use print statements as follows for debugging, they'll be visible when running tests.
    # print("Logs from your program will appear here!", file=sys.stderr)

    # # TODO: Uncomment the following line to pass the first stage
    # print(chat.choices[0].message.content)

if __name__ == "__main__":
    main()