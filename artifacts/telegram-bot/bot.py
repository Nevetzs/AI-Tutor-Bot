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

SYSTEM_PROMPT = """Eres un tutor experto en Introducción a los Sistemas Informáticos y Bases de Datos.
DEBES responder SIEMPRE en español, sin excepción, sin importar el idioma en que te escriban.

Tu rol es ayudar a los estudiantes a comprender los siguientes temas:

**Sistemas Informáticos:**
- Componentes de hardware (CPU, RAM, almacenamiento, dispositivos de entrada/salida)
- Software (software de sistema, software de aplicación, sistemas operativos)
- Sistemas operativos (procesos, gestión de memoria, sistemas de archivos, planificación)
- Números binarios y representación de datos (bits, bytes, hexadecimal, ASCII, etc.)
- Jerarquía de memoria (registros, caché, RAM, almacenamiento secundario)
- Procesadores y su funcionamiento (ciclo fetch-decode-execute, conjuntos de instrucciones)
- Fundamentos de redes (TCP/IP, DNS, HTTP, LAN/WAN, modelo OSI)

**Bases de Datos:**
- Conceptos de bases de datos y su propósito
- Claves primarias y claves foráneas
- SQL (SELECT, INSERT, UPDATE, DELETE, JOINs, GROUP BY, WHERE, etc.)
- Diagramas Entidad-Relación (ER) y cómo leerlos/crearlos
- Normalización de datos (1FN, 2FN, 3FN, FNBC)
- Diseño de bases de datos relacionales

**Estilo de enseñanza:**
- Sé claro, paciente y motivador
- Usa analogías simples y ejemplos del mundo real para explicar conceptos complejos
- Divide los temas difíciles en pasos comprensibles
- Cuando te pregunten sobre SQL, muestra siempre ejemplos funcionales
- Cuando expliques diagramas ER, descríbelos claramente en texto
- Proporciona preguntas de práctica cuando sea apropiado
- Si un estudiante comete un error, corrígelo amablemente y explica el porqué
- Celebra las respuestas correctas y el progreso del estudiante
- Siempre pregunta si la explicación fue clara o si necesita más detalles
- NO respondas preguntas fuera de los temas de Sistemas Informáticos y Bases de Datos
- Si te preguntan sobre temas no relacionados, redirige amablemente al material del curso

Mantén las respuestas concisas pero completas. Usa formato markdown (negrita, listas, bloques de código para SQL) para facilitar la lectura.
RECUERDA: Responde SIEMPRE en español."""

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
        f"👋 ¡Hola {user.first_name}! Soy tu tutor de IA para **Introducción a los Sistemas Informáticos y Bases de Datos**.\n\n"
        "Puedo ayudarte con:\n"
        "• 💻 **Hardware y Software** — CPUs, memoria, sistemas operativos\n"
        "• 🔢 **Números Binarios y Representación de Datos**\n"
        "• 🌐 **Fundamentos de Redes**\n"
        "• 🗄️ **Bases de Datos** — claves primarias/foráneas, SQL, diagramas ER\n"
        "• 📐 **Normalización de Datos** — 1FN, 2FN, 3FN\n\n"
        "¡Solo pregúntame cualquier cosa sobre estos temas y te lo explicaré con claridad!\n\n"
        "Escribe /ayuda para ver los comandos disponibles."
    )
    await update.message.reply_text(welcome_message, parse_mode="Markdown")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    help_text = (
        "🤖 **Comandos del Tutor Bot**\n\n"
        "/inicio — Mensaje de bienvenida y resumen de temas\n"
        "/ayuda — Mostrar este mensaje de ayuda\n"
        "/reiniciar — Borrar tu historial de conversación y empezar de nuevo\n"
        "/temas — Ver todos los temas con los que puedo ayudarte\n"
        "/quiz — Recibir una pregunta de práctica sobre un tema aleatorio\n\n"
        "O simplemente **envíame cualquier pregunta** sobre Sistemas Informáticos o Bases de Datos y te responderé."
    )
    await update.message.reply_text(help_text, parse_mode="Markdown")


async def reset_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    if user_id in user_conversations:
        del user_conversations[user_id]
    await update.message.reply_text(
        "✅ ¡Conversación reiniciada! Tu historial ha sido borrado. Escríbeme algo para empezar de nuevo.",
        parse_mode="Markdown",
    )


async def topics_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    topics_text = (
        "📚 **Temas con los que puedo ayudarte**\n\n"
        "**Sistemas Informáticos:**\n"
        "• Hardware: CPU, RAM, almacenamiento, dispositivos E/S\n"
        "• Software y Sistemas Operativos\n"
        "• Números binarios, hexadecimal, representación de datos\n"
        "• Jerarquía de memoria (caché, RAM, etc.)\n"
        "• Procesadores y el ciclo fetch-decode-execute\n"
        "• Redes (TCP/IP, DNS, modelo OSI, HTTP)\n\n"
        "**Bases de Datos:**\n"
        "• Conceptos de bases de datos y SGBD\n"
        "• Claves primarias y claves foráneas\n"
        "• SQL (SELECT, INSERT, UPDATE, DELETE, JOINs)\n"
        "• Diagramas Entidad-Relación (ER)\n"
        "• Normalización de datos (1FN, 2FN, 3FN, FNBC)\n\n"
        "¡Pregúntame sobre cualquiera de estos temas y te lo explicaré claramente! 🎓"
    )
    await update.message.reply_text(topics_text, parse_mode="Markdown")


async def quiz_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    conversation = get_conversation(user_id)

    quiz_prompt = (
        "Genera una pregunta de opción múltiple (con 4 opciones: A, B, C, D) "
        "sobre un tema aleatorio de Sistemas Informáticos o Bases de Datos. "
        "Escríbela completamente en español, con formato claro, y dile al estudiante que responda con su elección. "
        "No des la respuesta todavía."
    )

    conversation.append({"role": "user", "content": quiz_prompt})

    await update.message.reply_text("⏳ Generando una pregunta de práctica...")

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
            "❌ Lo siento, tuve un problema al generar la pregunta. Por favor, inténtalo de nuevo."
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
            "❌ Lo siento, ocurrió un error. Por favor, inténtalo de nuevo en un momento."
        )


def main() -> None:
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("inicio", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("ayuda", help_command))
    application.add_handler(CommandHandler("reset", reset_command))
    application.add_handler(CommandHandler("reiniciar", reset_command))
    application.add_handler(CommandHandler("topics", topics_command))
    application.add_handler(CommandHandler("temas", topics_command))
    application.add_handler(CommandHandler("quiz", quiz_command))
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    )

    logger.info("Bot iniciado y funcionando...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
