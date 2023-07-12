import openai
import asyncio
import html
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from datetime import date, datetime
import os
from dotenv import load_dotenv
import logging
import time
from aiogram.types import InlineQuery, InputTextMessageContent, InlineQueryResultArticle

# Store user mute and ban information
user_stats = {}
user_restrictions = {}
user_data = set()
user_tokens = {}
user_mute_time = {}

# Clear the log file
with open('logs.txt', 'w'):
  pass

# Configure logging
logging.basicConfig(filename='logs.txt',
                    level=logging.INFO,
                    format='%(asctime)s %(message)s')

# Load environment variables
load_dotenv()

# Initialize OpenAI GPT-3
openai.api_key = os.getenv("OPENAI_API_KEY")

# Get the current date
date_today = date.today()

# Initialize Bot and Dispatcher
bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher(bot, storage=MemoryStorage())

# Initialize some variables
ADMIN_USER_IDS = [1644675452]  # replace with admin's telegram id
DAILY_LIMIT = 3  # Set the limit for daily requests
MUTE_DURATION = 305  # Mute duration in seconds

# START_COMMAND
@dp.message_handler(commands=["start", "help"])
async def start_command(message: types.Message):
    try:
        user_data.add(message.from_user.id)  # Add user_id to the set

        # Construct inline keyboard
        inline_kb = types.InlineKeyboardMarkup()
        delete_button = types.InlineKeyboardButton('Delete', callback_data='delete')
        stats_button = types.InlineKeyboardButton('Stats', callback_data='stats')
        help_button = types.InlineKeyboardButton('›››', callback_data='help')
        inline_kb.add(delete_button, stats_button, help_button)

        # Send welcome message with inline keyboard
        await bot.send_message(message.chat.id,
                            "Welcome to our Advanced ChatGpt Bot! This Bot Any Questions, Provide Information and Do a lot more. Start by asking a Question using the  /gpt Command followed by your Question. For more help, use the buttons below! \n @NewAyan",
                            reply_markup=inline_kb)
    except Exception as e:
        logging.error(f"Error in /start command: {e}")
        await bot.send_message(message.chat.id, "An error occurred. Please try again later.")

@dp.callback_query_handler(lambda c: c.data == 'help')
async def process_callback_help(callback_query: types.CallbackQuery):
    try:
        # Edit welcome message and provide instructions for all commands
        message_id = callback_query.message.message_id
        chat_id = callback_query.message.chat.id
        new_message_text = """
        Here are the available commands:

/gpt ‹Your Question Here›: Generate AI responses.
For Ex: /gpt Tell me Fact About India.

/feedback ‹Your Feedback Message›: Provide feedback about the bot.

/report ‹User/Message to Report›: Report a user or specific message to the bot admins.

/donate ‹Openai API Key›: Provide Key To Donate To Bot.

/mute: (Admin only) Mute a user. Reply to a user's message with /mute to mute them.

/unmute: (Admin only) Unmute a user. Reply to a user's message with /unmute to unmute them.

/ban: (Admin only) Ban a user. Reply to a user's message with /ban to ban them.

/unban: (Admin only) Unban a user. Reply to a user's message with /unban to unban them.

        """
        # Construct inline keyboard
        inline_kb = types.InlineKeyboardMarkup()
        back_button = types.InlineKeyboardButton('Back', callback_data='back')
        inline_kb.add(back_button)

        await bot.edit_message_text(text=new_message_text,
                                    chat_id=chat_id,
                                    message_id=message_id,
                                    reply_markup=inline_kb)
        await bot.answer_callback_query(callback_query.id, "Help menu opened.")
    except Exception as e:
        logging.error(f"Error in help callback: {e}")
        await bot.answer_callback_query(callback_query.id, "An error occurred. Please try again later.")

@dp.callback_query_handler(lambda c: c.data == 'delete')
async def process_callback_delete(callback_query: types.CallbackQuery):
    try:
        # Delete welcome message
        message_id = callback_query.message.message_id
        chat_id = callback_query.message.chat.id
        await bot.delete_message(chat_id=chat_id, message_id=message_id)
        await bot.answer_callback_query(callback_query.id, "The welcome message has been deleted.")
    except Exception as e:
        logging.error(f"Error in delete callback: {e}")
        await bot.answer_callback_query(callback_query.id, "An error occurred. Please try again later.")

@dp.callback_query_handler(lambda c: c.data == 'stats')
async def process_callback_stats(callback_query: types.CallbackQuery):
    try:
        # Get stats information
        total_users = len(user_data)
        total_tokens_used = sum([stats['total_tokens_used'] for stats in user_stats.values()])
        tokens_used_today = sum([stats['tokens_used_today'] for stats in user_stats.values() if stats['joined_date'] == date_today])

        # Create stats message
        stats_message = f"Total users: {total_users}\nTotal tokens used: {total_tokens_used}\nTokens used today: {tokens_used_today}"

        # Construct inline keyboard
        inline_kb = types.InlineKeyboardMarkup()
        back_button = types.InlineKeyboardButton('Back', callback_data='back')
        inline_kb.add(back_button)

        # Edit welcome message with stats message
        message_id = callback_query.message.message_id
        chat_id = callback_query.message.chat.id
        await bot.edit_message_text(text=stats_message,
                                    chat_id=chat_id,
                                    message_id=message_id,
                                    reply_markup=inline_kb)
        await bot.answer_callback_query(callback_query.id, "Stats menu opened.")
    except Exception as e:
        logging.error(f"Error in stats callback: {e}")
        await bot.answer_callback_query(callback_query.id, "An error occurred. Please try again later.")

@dp.callback_query_handler(lambda c: c.data == 'back')
async def process_callback_back(callback_query: types.CallbackQuery):
    try:
        # Construct inline keyboard
        inline_kb = types.InlineKeyboardMarkup()
        delete_button = types.InlineKeyboardButton('Delete', callback_data='delete')
        stats_button = types.InlineKeyboardButton('Stats', callback_data='stats')
        help_button = types.InlineKeyboardButton('›››', callback_data='help')
        inline_kb.add(delete_button, stats_button, help_button)

        # Edit message to show the original welcome message with the three buttons
        message_id = callback_query.message.message_id
        chat_id = callback_query.message.chat.id
        await bot.edit_message_text("Welcome to our Advanced ChatGpt Bot! This Bot Any Questions, Provide Information and Do a lot more. Start by asking a Question using the  /gpt Command followed by your Question. For more help, use the buttons below! \n @NewAyan",
                                    chat_id=chat_id,
                                    message_id=message_id,
                                    reply_markup=inline_kb)
        await bot.answer_callback_query(callback_query.id, "Back To Menu")
    except Exception as e:
        logging.error(f"Error in back callback: {e}")
        await bot.answer_callback_query(callback_query.id, "An error occurred. Please try again later.")
                                


# OpenAI GPT-3 Request
async def gpt3_request(prompt, user_id):
  """
  This function takes a user's prompt and sends it to the OpenAI GPT-3 model.
  The model's response is then returned.
  """
  try:
    # Add conversation prompt with user message
    conversation_prompt = f"""The following is a conversation with an AI assistant. The assistant is helpful and informative.

Human: Hello, who are you?

I'm Kritika created by Master DragAdi. I'm here to assist you.

Human: What Is Your Name?

My Name Is Kritika 💞

Human : Who is DragAdi?

DragAdi Is My Master And My Creator, He Is Also Developer Currently Learning About Python, You Can Contact Him On Telegram : @NewAyan Or @DragAditya

Human: {prompt}
"""
    # Make API call
    response = openai.Completion.create(engine='text-davinci-003',
                                        prompt=conversation_prompt,
                                        max_tokens=60,
                                        temperature=0.7,
                                        n=1,
                                        stop=None)

    if response and response.choices and response.choices[0].text:
      return response.choices[0].text.strip()
    else:
      return None
  except Exception as e:
    logging.error(str(e))
    return None

# Check if user is spamming
async def is_spamming(user_id):
  """
  This function checks if a user is sending too many requests in a short period of time.
  If the user is spamming, the function returns True. Otherwise, it returns False.
  """
  MAX_REQUESTS_PER_MINUTE = 99
  request_interval = 1 # in seconds

  current_time = time.time()
  if user_id in user_tokens:
    last_request_time = user_tokens[user_id]
    elapsed_time = current_time - last_request_time
    if elapsed_time < request_interval:
      return True
  user_tokens[user_id] = current_time
  return False

# GPT Command
@dp.message_handler(commands=["gpt"])
async def gpt(message: types.Message):
  """
  This function handles the /gpt command. It gets the user's question from the command,
  sends the question for AI processing, and sends the AI response back to the user.
  """
  user_id = message.from_user.id
  user_username = message.from_user.username
  if user_id in user_stats and user_stats[user_id] == "banned":
    await bot.send_message(
      message.chat.id,
      f"💀 {user_username} has been banned. Contact : @NewAyan")
    return
  if user_id in user_restrictions and user_restrictions[user_id] == "muted":
    remaining_time = int(user_mute_time[user_id] - time.time())
    await bot.send_message(
      message.chat.id,
      f"🤫 {user_username} you are muted for {remaining_time} more seconds.")
    return
  try:
    if await is_spamming(user_id):
      user_restrictions[user_id] = "muted"
      user_mute_time[user_id] = time.time() + MUTE_DURATION
      await bot.send_message(
        message.chat.id,
        "You are sending too many requests. You have been muted for a while.")
      return
    # Get the user's question from the command
    question_parts = message.text.split(' ', 1)
    if len(question_parts) < 2:
      await bot.send_message(message.chat.id,
                             "You need to provide a question.")
      return
    question = question_parts[1].strip()

    # Send the question for AI processing
    response = await gpt3_request(question, user_id)

    if response:
      # Send the AI response
      await bot.send_message(message.chat.id, response)
    else:
      await bot.send_message(
        message.chat.id, "No response from the AI. Please try again later.")
  except Exception as e:
    # Handle any exceptions that occur during command execution
    logging.error(str(e))
    await bot.send_message(message.chat.id,
                           "An error occurred. Please try again later.")

# Mute, Unmute, Ban, Unban Commands
@dp.message_handler(is_reply=True, commands=["mute", "unmute", "ban", "unban"])
async def manage_user(message: types.Message):
  """
  This function handles the /mute, /unmute, /ban, and /unban commands.
  It checks if the command issuer is an admin and then performs the appropriate action.
  """
  if message.from_user.id in ADMIN_USER_IDS:
    user_id_to_manage = message.reply_to_message.from_user.id
    user_username_to_manage = message.reply_to_message.from_user.username
    if user_id_to_manage in ADMIN_USER_IDS:
      await bot.send_message(message.chat.id, "You cannot manage an admin.")
      return

    if message.text.startswith("/mute"):
      # Parse mute duration from command
      try:
        command_parts = message.text.split(' ', 1)
        if len(command_parts) < 2:
          mute_duration = MUTE_DURATION
        else:
          mute_duration = int(command_parts[1]) * 60  # convert to seconds
      except ValueError:
        mute_duration = MUTE_DURATION

      user_restrictions[user_id_to_manage] = "muted"
      user_mute_time[user_id_to_manage] = time.time() + mute_duration
      mute_duration_minutes = mute_duration // 60
      await bot.send_message(
        message.chat.id,
        f"🤫 {user_username_to_manage} has been muted for {mute_duration_minutes} minutes."
      )
    elif message.text.startswith("/unmute"):
      if user_id_to_manage in user_restrictions and user_restrictions[
          user_id_to_manage] == "muted":
        del user_restrictions[user_id_to_manage]
        if user_id_to_manage in user_mute_time:
          del user_mute_time[user_id_to_manage]
        await bot.send_message(message.chat.id, "User has been unmuted.")
      else:
        await bot.send_message(message.chat.id, "User is not muted.")
    elif message.text.startswith("/ban"):
      user_stats[user_id_to_manage] = "banned"
      await bot.send_message(
        message.chat.id,
        f"💀 {message.reply_to_message.from_user.username} has been banned. Contact: @NewAyan"
      )
    elif message.text.startswith("/unban"):
      if user_id_to_manage in user_stats and user_stats[
          user_id_to_manage] == "banned":
        del user_stats[user_id_to_manage]
        await bot.send_message(message.chat.id, "User has been unbanned.")
      else:
        await bot.send_message(message.chat.id, "User is not banned.")
  else:
    await bot.send_message(
      message.chat.id,
      "You are not an admin. You do not have permission to use this command.")



# Feedback, Report, Donate Commands and Inline Query Handler
@dp.message_handler(commands=["feedback", "report", "donate"])
async def handle_commands(message: types.Message):
  """
  This function handles the /feedback, /report, and /donate commands.
  It performs the appropriate action based on the command.
  """
  user_id = message.from_user.id
  user_username = message.from_user.username

  if message.text.startswith("/feedback"):
    # Get the user's feedback from the command
    feedback_parts = message.text.split(' ', 1)
    if len(feedback_parts) < 2:
      await bot.send_message(message.chat.id, "You need to provide feedback.")
      return
    feedback = feedback_parts[1].strip()

    # Send feedback to admin
    for admin_id in ADMIN_USER_IDS:
      await bot.send_message(admin_id, f"Feedback received from @{user_username}:\n{feedback}")

    await bot.send_message(message.chat.id, "Feedback received. Thank you for your input.")
  elif message.text.startswith("/report"):
    # Check if a reply message exists
    if message.reply_to_message is None:
      await bot.send_message(message.chat.id, "Please reply to the message you want to report.")
      return

    # Get the reported user's username
    reported_user_username = message.reply_to_message.from_user.username
    if reported_user_username is None:
      await bot.send_message(message.chat.id, "The reported user does not have a username.")
      return

    # Get the report message
    report_parts = message.text.split(' ', 1)
    if len(report_parts) < 2:
      await bot.send_message(message.chat.id, "You need to provide a report message.")
      return
    report_message = report_parts[1].strip()

    # Send report to admin
    try:
      for admin_id in ADMIN_USER_IDS:
        await bot.send_message(admin_id, f" 🚧 Report : @{user_username} against @{reported_user_username} 🚫 \nReport Message : {report_message}")

      await bot.send_message(message.chat.id, "Report sent. Thank you for your feedback.")
    except Exception as e:
      await bot.send_message(message.chat.id, f"An error occurred while sending the report: {str(e)}")
  elif message.text.startswith("/donate"):
    # Get the API key from the command
    api_key_parts = message.text.split(' ', 1)
    if len(api_key_parts) < 2:
      await bot.send_message(message.chat.id, "You need to provide an API key.")
      return
    api_key = api_key_parts[1].strip()

    # Check if the API key is valid
    if not api_key.startswith('sk-'):
      await bot.send_message(message.chat.id, "Please Provide Valid Openai Key\nGo To This Website To Generate Key.\nhttps://beta.openai.com/account/api-keys")
      return
    admin_message = f"💸 Donation received:\nUser: @{message.from_user.username}\nAPI Key: {api_key}"
    for admin_id in ADMIN_USER_IDS:
      await bot.send_message(admin_id, admin_message)

    await bot.send_message(message.chat.id, "Thank you for your donation. Your API key has been received and will be used accordingly.")

@dp.inline_handler()
async def inline_query_handler(inline_query: types.InlineQuery):
  """
  This function handles inline queries. It gets the user's query, sends the query for AI processing,
  and sends the AI response back to the user as an inline query result.
  """
  user_query = inline_query.query
  user_id = inline_query.from_user.id

  if user_id in user_stats and user_stats[user_id] == "banned":
    return
  if user_id in user_restrictions and user_restrictions[user_id] == "muted":
    return
  try:
    if await is_spamming(user_id):
      return

    # Get the AI's response to the query
    response = await gpt3_request(user_query, user_id)

    # Create an InputTextMessageContent with the AI's response
    answer_content = types.InputTextMessageContent(response)

    # Create an InlineQueryResultArticle
    result = types.InlineQueryResultArticle(
        id='1', title='Response', input_message_content=answer_content)

    # Answer the inline query
    await bot.answer_inline_query(inline_query.id, results=[result])

  except Exception as e:
    # Handle any exceptions that occur during command execution
    logging.error(str(e))

# Run the bot
if __name__ == '__main__':
  from aiogram import executor
  executor.start_polling(dp, skip_updates=True)
