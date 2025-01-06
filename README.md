![img](/img.jpg)

# TaskListBot

![TaskListBot](https://example.com/path/to/your/image.png)

TaskListBot is a Telegram bot for managing tasks. It allows users to add, delete, and view tasks, and also notifies administrators about new tasks.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Dependencies](#dependencies)
- [Contributing](#contributing)
- [License](#license)

## Features

- Add new tasks
- View task list
- Delete tasks
- Notify administrators about new tasks

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/TaskListBot.git
```

2. Navigate to the project directory:

```bash
cd TaskListBot
```

3. Install the necessary dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the bot:

```bash
python bot.py
```

## Configuration

1. Create a `.env` file and add your Telegram bot token:

```
TOKEN=YOUR_BOT_TOKEN
```

2. Add the authorized user IDs:

```python
ALLOWED_USERS = {123456789, 987654321}  # Replace with the actual user IDs
```

## Dependencies

- [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI)

## Contributing

We welcome contributions! If you have suggestions for improvement or have found a bug, please create an issue or submit a pull request.

## License

This project is licensed under the terms of the MIT License. See the LICENSE file for more information.
