# 🧠 Build Your Own Redis CLI

This project is a part of the [Coding Challenges](https://codingchallenges.fyi/challenges/challenge-redis-cli/) series — a hands-on exercise to build a custom Redis CLI client from scratch using Python.

Much like the official `redis-cli`, this project lets you interact with a Redis server over the RESP protocol, with built-in support for command autocompletion and syntax hints.

Redis is a popular in-memory key-value store used extensively for caching, real-time analytics, pub/sub, and more. This challenge deepens your understanding of socket programming, CLI design, and parsing Redis protocol.

---

## 📦 Project Structure

```
.
├── ccredis_cli.py           # Main CLI client implementation
├── commands.json            # Redis command metadata (syntax, summary, etc.)
├── resp.py                  # RESP protocol serializer/deserializer
├── test_rediscli.py         # Unit tests for the CLI
```

---

## 🚀 Features

- 🔌 Connects to Redis over TCP
- 🎯 Supports full RESP serialization and deserialization
- 💡 Provides command hints with arguments as you type
- ⌨️ Autocompletion using `prompt_toolkit`
- 📖 Built-in `help` command for command groups or individual commands
- 🧪 Includes test coverage for key functionality

---

## 🛠️ Usage

Make sure you have Redis running locally on `127.0.0.1:6379`:

```bash
redis-server
```

Then, activate your Python environment and run the CLI:

```bash
python ccredis_cli.py
```

Example:

```bash
127.0.0.1:6379> set mykey hello
Hint: SET key value [condition] [get] [expiration]
OK
127.0.0.1:6379> get mykey
hello
```

You can use `help set`, `help @string`, or `quit` to exit.

---

## 🧪 Running Tests

To run the test suite:

```bash
python -m unittest test_rediscli.py
```

---



## 📚 Reference

- [RESP Protocol Specification](https://redis.io/docs/reference/protocol-spec/)
- [Redis CLI Docs](https://redis.io/docs/ui/cli/)
- [prompt_toolkit](https://github.com/prompt-toolkit/python-prompt-toolkit)

---
