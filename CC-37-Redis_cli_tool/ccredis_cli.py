import argparse
import json
import os
import socket

from prompt_toolkit import PromptSession
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.history import FileHistory

from resp import serialize, deserialize, RESPError

COMMANDS_JSON = "commands.json"

def load_redis_commands(path=COMMANDS_JSON):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Cannot find {path}")
    with open(path, "r") as f:
        data = json.load(f)

    commands = {}
    for name, info in data.items():
        cmd_name = name.upper()
        syntax = [cmd_name]

        for arg in info.get("arguments", []):
            text = arg.get("display_text") or arg.get("name", "")
            if arg.get("optional", False):
                syntax.append(f"[{text}]")
            else:
                syntax.append(text)

        info["syntax_hint"] = " ".join(syntax)
        commands[cmd_name] = {"name": cmd_name, **info}

    return commands

redis_commands = load_redis_commands()
redis_command_names = sorted(redis_commands.keys())

class RedisCompleter(Completer):
    def get_completions(self, document, complete_event):
        text = document.text_before_cursor.strip()
        words = text.split()
        if len(words) <= 1:
            for cmd in redis_command_names:
                if cmd.lower().startswith(document.get_word_before_cursor().lower()):
                    yield Completion(cmd.lower(), start_position=-len(document.get_word_before_cursor()))

def get_hint(text):
    parts = text.strip().split()
    if not parts:
        return ""
    cmd = parts[0].upper()
    if cmd in redis_commands:
        return redis_commands[cmd]["syntax_hint"]
    return ""

def print_help(parts):
    if len(parts) == 1:
        print("To get help about Redis commands type:")
        print('  "help @<group>" to get a list of commands in <group>')
        print('  "help <command>" for help on <command>')
        print('  "quit" to exit')
    else:
        keyword = " ".join(parts[1:]).upper()

        if keyword.startswith("@"):
            group = keyword[1:]
            entries = [cmd for cmd in redis_commands.values() if cmd.get("group", "").lower() == group.lower()]
            if not entries:
                print(f"No commands found in group '{group}'")
            else:
                for c in sorted(entries, key=lambda x: x["name"]):
                    print(c["name"])
        else:
            cmd = redis_commands.get(keyword)
            if not cmd:
                print(f"No documentation found for command '{keyword}'")
            else:
                print()
                if "arguments" in cmd:
                    syntax = [cmd["name"]]
                    for arg in cmd["arguments"]:
                        name = arg.get("display_text") or arg.get("name", "")
                        if arg.get("optional", False):
                            syntax.append(f"[{name}]")
                        else:
                            syntax.append(name)
                    print("  " + " ".join(syntax))
                print(f"  summary: {cmd.get('summary', '')}")
                print(f"  since: {cmd.get('since', '')}")
                print(f"  group: {cmd.get('group', '')}")
                print()

def read_full_response(sock):
    data = b""
    while True:
        chunk = sock.recv(4096)
        if not chunk:
            break
        data += chunk
        try:
            deserialize(data.decode())
            break
        except RESPError:
            continue
    return data

def main():
    parser = argparse.ArgumentParser(description="A basic Redis CLI client")
    parser.add_argument('--host', default='127.0.0.1', help='Redis server host')
    parser.add_argument('--port', type=int, default=6379, help='Redis server port')

    args = parser.parse_args()

    session = PromptSession(
        history=FileHistory(os.path.expanduser("~/.ccredis_history")),
        completer=RedisCompleter(),
        bottom_toolbar=lambda: HTML("<b>Hint:</b> " + get_hint(session.default_buffer.document.text)),
    )

    try:
        with socket.create_connection((args.host, args.port)) as sock:
            while True:
                try:
                    cmd_input = session.prompt(f"{args.host}:{args.port}> ").strip()
                    if not cmd_input:
                        continue

                    parts = cmd_input.split()

                    if parts[0].lower() == "quit":
                        break

                    if parts[0].lower() == "help":
                        print_help(parts)
                        continue

                    serialized = serialize(parts)
                    sock.sendall(serialized.encode())

                    raw_response = read_full_response(sock)
                    response = deserialize(raw_response.decode())

                    if isinstance(response, list):
                        for i, item in enumerate(response, 1):
                            print(f"{i}) {item}")
                    elif isinstance(response, dict) and "error" in response:
                        print(f"(error) {response['error']}")
                    else:
                        print(response)

                except RESPError as e:
                    print(f"Protocol error: {e}")
                except Exception as e:
                    print(f"Unexpected error: {e}")
                    break

    except ConnectionRefusedError:
        print(f"Could not connect to Redis server at {args.host}:{args.port}")
    except KeyboardInterrupt:
        print("\nGoodbye!")

if __name__ == "__main__":
    main()
