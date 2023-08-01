
```markdown
# ChatGPT Bot

ChatGPT Bot is an advanced Telegram bot that uses the power of OpenAI's GPT-3 to generate AI responses for user queries. It provides a seamless conversational experience and can answer various types of questions.

## Features

- Generate AI responses for user queries.
- Issue API keys for accessing the `/gpt` command.
- Allow users to redeem API keys to access the `/gpt` command.
- View API key details for specific users.
- Revoke API keys from users.
- Mute and unmute users.
- Ban and unban users.
- Collect feedback from users.
- Allow admins to report users or specific messages.

## Getting Started

### Prerequisites

- Python 3.8 or higher
- OpenAI API key (Sign up at https://beta.openai.com/ to get an API key)

### Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/<your_username>/chatgpt-bot.git
   cd chatgpt-bot
   ```

2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file and add your OpenAI API key:

   ```plaintext
   OPENAI_API_KEY=sk-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
   BOT_TOKEN=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
   ```

   Replace `sk-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX` with your actual OpenAI API key and `BOT_TOKEN=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX` with your Telegram Bot token.

### Usage

1. Run the bot:

   ```bash
   python main.py
   ```

2. Use the `/gpt` command followed by your question to get AI responses.

3. Admins can use commands like `/mute`, `/unmute`, `/ban`, `/unban`, `/key`, `/redeem`, `/view`, `/revoke`, `/feedback`, and `/report` to manage the bot and users.

## Bot Commands

- `/gpt <question>`: Generate AI responses.
- `/key [number_of_keys] [validity_days]`: Generate API keys for accessing the `/gpt` command.
- `/redeem <key>`: Redeem an API key to access the `/gpt` command.
- `/view [username]`: View API key details for a specific user.
- `/revoke [user_id]`: Revoke a user's API key.
- `/mute`: (Admin only) Mute a user. Reply to a user's message with `/mute` to mute them.
- `/unmute`: (Admin only) Unmute a user. Reply to a user's message with `/unmute` to unmute them.
- `/ban`: (Admin only) Ban a user. Reply to a user's message with `/ban` to ban them.
- `/unban`: (Admin only) Unban a user. Reply to a user's message with `/unban` to unban them.
- `/feedback <message>`: Provide feedback about the bot.
- `/report`: (Admin only) Report a user or specific message to the bot.
- `/donate <openai_api_key>`: Provide your OpenAI API key to donate to the bot.

## Feedback and Support

If you have any feedback, suggestions, or need support, you can contact the bot developer [@NewAyan](https://telegram.me/NewAyan).

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgments

- [@NewAyan](https://telegram.me/NewAyan) - For creating this awesome ChatGPT Bot.
- [OpenAI](https://beta.openai.com/) - For providing the GPT-3 API.

---

_Replace `<your_username>` with your GitHub username and `<repository_url>` with the actual URL of your GitHub repository._
```

Please replace `<your_username>` with your actual GitHub username and make any other necessary modifications based on your specific project details. Remember to update the OpenAI API key and Telegram Bot token in the `.env` file to make the bot functional.
