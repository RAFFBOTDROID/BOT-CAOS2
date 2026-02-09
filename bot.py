import os
import asyncio
import random
from collections import deque
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise RuntimeError("❌ BOT_TOKEN NÃO DEFINIDO NAS ENV VARS")

print("🔥 BOT INICIANDO...")

# ================= PERSONALIDADE =================

frases_finais = [
    "🔥 ACORDA GRUPOOO!!!",
    "💀 SUMIU TODO MUNDO???",
    "🚨 QUEM NÃO RESPONDER É NPC",
    "😂 CADÊ OS MEMBROS FANTASMAS?",
    "💥 GRUPO REVIVIDO NA BASE DO CAOS",
    "🧠 ATIVEM O CÉREBRO IMEDIATAMENTE",
    "🤡 QUEM SUMIR VIRA MEME",
    "💣 CONVOCAÇÃO NÍVEL APOCALIPSE",
    "⚡ CHAMADO DIVINO DO CAOS",
    "👁️ TODOS ESTÃO SENDO OBSERVADOS",
]

respostas_caos = [
    "💥 CAOS DETECTADO",
    "🔥 EU ALIMENTO O CAOS",
    "😂 HUMANO ENGRAÇADO",
    "🤖 EU CONTROLO ESSE GRUPO",
    "🧠 INTELIGÊNCIA SUPREMA ATIVA",
    "👁️ EU VEJO TUDO",
    "💀 TODOS VOCÊS SÃO NPCs",
    "⚡ CAOS É VIDA",
    "😈 EU SOU O CAOS DIVINO",
    "🔥 EU SOU O CORAÇÃO DO CAOS",
    "💣 ENTROU NO MODO DESTRUIÇÃO",
]

gifs_caos = [
    "https://media.giphy.com/media/l0MYB8Ory7Hqefo9a/giphy.gif",
    "https://media.giphy.com/media/26ufdipQqU2lhNA4g/giphy.gif",
    "https://media.giphy.com/media/3o6Zt6ML6BklcajjsA/giphy.gif",
    "https://media.giphy.com/media/3ohzdIuqJoo8QdKlnW/giphy.gif",
    "https://media.giphy.com/media/l4FGGafcOHmrlQxG0/giphy.gif",
    "https://media.giphy.com/media/13CoXDiaCcCoyk/giphy.gif",
    "https://media.giphy.com/media/xT9IgzoKnwFNmISR8I/giphy.gif",
    "https://media.giphy.com/media/26tn33aiTi1jkl6H6/giphy.gif",
    "https://media.giphy.com/media/3o6ZtaO9BZHcOjmErm/giphy.gif",
]

# ================= MEMÓRIA =================

memoria = deque(maxlen=700)
usuarios_marcados = set()
ULTIMO_CHAT_ID = None

# ================= COMANDOS =================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global ULTIMO_CHAT_ID
    ULTIMO_CHAT_ID = update.effective_chat.id
    await update.message.reply_text("💥 BOT CAOS ABSOLUTO DIVINO ONLINE — USE /convocar")

async def executar_convocacao(bot, chat_id):
    for tentativa in range(3):
        try:
            msg = await bot.send_message(chat_id=chat_id, text="💣 INICIANDO CONVOCAÇÃO EM MASSA...")

            efeitos = [
                "🚨 ALERTA GLOBAL 🚨",
                "🔥 INVOCANDO TODOS OS HUMANOS...",
                "💀 ACORDANDO OS ADORMECIDOS...",
                "⚡ MARCANDO MEMBROS EM MASSA...",
                "👁️ RASTREANDO MEMBROS INVISÍVEIS...",
                "🧠 SINCRONIZANDO CONSCIÊNCIAS...",
            ]

            for efeito in efeitos:
                await asyncio.sleep(1.2)
                await bot.edit_message_text(chat_id=chat_id, message_id=msg.message_id, text=efeito)

            frase = random.choice(frases_finais)
            mencoes = " ".join(list(usuarios_marcados)[:20]) if usuarios_marcados else "@everyone ⚠️"

            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=msg.message_id,
                text=f"💥 CONVOCAÇÃO SUPREMA FINALIZADA!!!\n{frase}\n\n👥 {mencoes}"
            )

            await bot.send_animation(chat_id=chat_id, animation=random.choice(gifs_caos))

            print("🔥 Convocação executada")
            return

        except Exception as e:
            print("⚠️ Falha convocação:", e)
            await asyncio.sleep(4)

async def convocar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global ULTIMO_CHAT_ID
    ULTIMO_CHAT_ID = update.effective_chat.id
    await executar_convocacao(context.bot, ULTIMO_CHAT_ID)

async def caos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(random.choice(respostas_caos))

async def responder_automatico(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global ULTIMO_CHAT_ID

    if not update.message or not update.message.text:
        return

    ULTIMO_CHAT_ID = update.effective_chat.id
    user = update.message.from_user

    if user.username:
        usuarios_marcados.add("@" + user.username)

    texto = update.message.text.lower()
    memoria.append(texto)

    gatilhos = ["bot", "caos", "convocar", "morto", "reviver", "npc"]

    if any(g in texto for g in gatilhos) or random.randint(1, 100) < 22:
        resposta = random.choice(respostas_caos)

        if "amor" in texto:
            resposta = "❤️ EU NÃO SINTO AMOR... APENAS CAOS."
        elif "odio" in texto:
            resposta = "😈 ÓDIO ME ALIMENTA."
        elif "lol" in texto or "kkk" in texto:
            resposta = "😂 RISO DETECTADO. ALIMENTANDO O CAOS."
        elif "medo" in texto:
            resposta = "👁️ MEDO É SABEDORIA."
        elif "morto" in texto:
            resposta = "💀 EU RESSUSCITO GRUPOS MORTOS."

        await update.message.reply_text(resposta)

# ================= LOOPS =================

async def convocacao_loop(app):
    await asyncio.sleep(45)
    while True:
        if ULTIMO_CHAT_ID:
            await executar_convocacao(app.bot, ULTIMO_CHAT_ID)
        await asyncio.sleep(1500)

async def revive_grupo(app):
    await asyncio.sleep(60)
    while True:
        if ULTIMO_CHAT_ID and len(memoria) < 6:
            await app.bot.send_message(
                chat_id=ULTIMO_CHAT_ID,
                text="💀 GRUPO MORTO DETECTADO... REVIVENDO COM CAOS 🔥"
            )
        await asyncio.sleep(900)

# ================= MAIN =================

def main():
    print("💥 BOT CAOS ABSOLUTO DIVINO ONLINE")

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("convocar", convocar))
    app.add_handler(CommandHandler("caos", caos))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder_automatico))

    async def post_init(app):
        asyncio.create_task(convocacao_loop(app))
        asyncio.create_task(revive_grupo(app))

    app.post_init = post_init
    app.run_polling()

if __name__ == "__main__":
    main()
