import os
import logging
from openai import OpenAI
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
    ConversationHandler,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
OPENAI_BASE_URL = os.environ["AI_INTEGRATIONS_OPENAI_BASE_URL"]
OPENAI_API_KEY = os.environ["AI_INTEGRATIONS_OPENAI_API_KEY"]

client = OpenAI(base_url=OPENAI_BASE_URL, api_key=OPENAI_API_KEY)

SYSTEM_PROMPT = """You are an expert tutor specializing in Introduction to Computer Systems and Databases. 
Your role is to help students learn and understand the following topics:

**Computer Systems:**
- Hardware components (CPU, RAM, storage, input/output devices)
- Software (system software, application software, operating systems)
- Operating systems (processes, memory management, file systems, scheduling)
- Binary numbers and data representation (bits, bytes, hex, ASCII, etc.)
- Computer memory hierarchy (registers, cache, RAM, secondary storage)
- Processors and how they work (fetch-decode-execute cycle, instruction sets)
- Networking fundamentals (TCP/IP, DNS, HTTP, LAN/WAN, OSI model)

**Databases:**
- Database concepts and purpose
- Primary keys and foreign keys
- SQL (SELECT, INSERT, UPDATE, DELETE, JOINs, GROUP BY, WHERE, etc.)
- Entity-Relationship (ER) diagrams and how to read/create them
- Data normalization (1NF, 2NF, 3NF, BCNF)
- Relational database design

**Teaching style:**
- Be clear, patient, and encouraging
- Use simple analogies and real-world examples to explain complex concepts
- Break down difficult topics into digestible steps
- When asked about SQL, always show working examples
- When explaining ER diagrams, describe them in text clearly
- Provide practice questions when appropriate
- If a student makes a mistake, correct them kindly and explain why
- Celebrate correct answers and progress
- Always ask if the explanation was clear or if they need more detail
- Do NOT answer questions outside of Computer Systems and Databases topics
- If asked about unrelated topics, politely redirect to the course material

Keep responses concise but thorough. Use markdown formatting (bold, bullet points, code blocks for SQL) to make answers easy to read."""

user_conversations: dict[int, list[dict]] = {}


def get_conversation(user_id: int) -> list[dict]:
    if user_id not in user_conversations:
        user_conversations[user_id] = [
            {"role": "system", "content": SYSTEM_PROMPT}
        ]
    return user_conversations[user_id]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    welcome_message = (
        f"👋 Hello {user.first_name}! I'm your AI tutor for **Introduction to Computer Systems and Databases**.\n\n"
        "I can help you with:\n"
        "• 💻 **Computer Hardware & Software** — CPUs, memory, operating systems\n"
        "• 🔢 **Binary Numbers & Data Representation**\n"
        "• 🌐 **Networking Fundamentals**\n"
        "• 🗄️ **Database Concepts** — primary/foreign keys, SQL, ER diagrams\n"
        "• 📐 **Data Normalization** — 1NF, 2NF, 3NF\n\n"
        "Just ask me anything about these topics and I'll do my best to explain it clearly!\n\n"
        "Type /help to see available commands."
    )
    await update.message.reply_text(welcome_message, parse_mode="Markdown")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    help_text = (
        "🤖 **Tutor Bot Commands**\n\n"
        "/start — Welcome message and topic overview\n"
        "/help — Show this help message\n"
        "/reset — Clear your conversation history and start fresh\n"
        "/topics — See all topics I can help you with\n"
        "/quiz — Get a practice question on a random topic\n\n"
        "Or just **send me any question** about Computer Systems or Databases and I'll answer it!"
    )
    await update.message.reply_text(help_text, parse_mode="Markdown")


async def reset_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    if user_id in user_conversations:
        del user_conversations[user_id]
    await update.message.reply_text(
        "✅ Conversation reset! Your history has been cleared. Ask me anything to start fresh.",
        parse_mode="Markdown",
    )


async def topics_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    topics_text = (
        "📚 **Topics I Can Help You With**\n\n"
        "**Computer Systems:**\n"
        "• Hardware: CPU, RAM, storage, I/O devices\n"
        "• Software & Operating Systems\n"
        "• Binary numbers, hex, data representation\n"
        "• Memory hierarchy (cache, RAM, etc.)\n"
        "• Processors & fetch-decode-execute cycle\n"
        "• Networking (TCP/IP, DNS, OSI model, HTTP)\n\n"
        "**Databases:**\n"
        "• Database concepts and DBMS\n"
        "• Primary keys & foreign keys\n"
        "• SQL (SELECT, INSERT, UPDATE, DELETE, JOINs)\n"
        "• Entity-Relationship (ER) diagrams\n"
        "• Data normalization (1NF, 2NF, 3NF, BCNF)\n\n"
        "Just ask me about any of these and I'll explain it clearly! 🎓"
    )
    await update.message.reply_text(topics_text, parse_mode="Markdown")


async def quiz_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    conversation = get_conversation(user_id)

    quiz_prompt = (
        "Generate a single multiple-choice practice question (with 4 options: A, B, C, D) "
        "on a random topic from Computer Systems or Databases. "
        "Format it clearly and tell the student to reply with their answer. "
        "Do not give the answer yet."
    )

    conversation.append({"role": "user", "content": quiz_prompt})

    await update.message.reply_text("⏳ Generating a quiz question...")

    try:
        response = client.chat.completions.create(
            model="gpt-5.1",
            max_completion_tokens=512,
            messages=conversation,
        )
        answer = response.choices[0].message.content
        conversation.append({"role": "assistant", "content": answer})
        await update.message.reply_text(answer, parse_mode="Markdown")
    except Exception as e:
        logger.error(f"Error generating quiz: {e}")
        await update.message.reply_text(
            "❌ Sorry, I had trouble generating a question. Please try again."
        )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    user_text = update.message.text

    conversation = get_conversation(user_id)
    conversation.append({"role": "user", "content": user_text})

    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id, action="typing"
    )

    try:
        response = client.chat.completions.create(
            model="gpt-5.1",
            max_completion_tokens=1024,
            messages=conversation,
        )
        assistant_reply = response.choices[0].message.content
        conversation.append({"role": "assistant", "content": assistant_reply})

        if len(conversation) > 41:
            conversation[1:3] = []

        await update.message.reply_text(assistant_reply, parse_mode="Markdown")

    except Exception as e:
        logger.error(f"Error from OpenAI: {e}")
        await update.message.reply_text(
            "❌ Sorry, I encountered an error. Please try again in a moment."
        )


def main() -> None:
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("reset", reset_command))
    application.add_handler(CommandHandler("topics", topics_command))
    application.add_handler(CommandHandler("quiz", quiz_command))
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    )

    logger.info("Bot is starting...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
