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

# ================= DADOS =================

memoria = deque(maxlen=2000)
usuarios_marcados = set()
ranking_inativos = {}
ULTIMO_CHAT_ID = None

# ================= FRASES =================

frases_convocacao = [
    "🚨 CONVOCAÇÃO GERAL — TODOS APAREÇAM",
    "🔥 33K MEMBROS, MANIFESTEM-SE",
    "📣 CHAMANDO TODO MUNDO AGORA",
    "💀 SE VOCÊ VÊ ISSO, RESPONDA",
    "👁️ TODOS ESTÃO SENDO OBSERVADOS",
    "⚡ ALERTA GLOBAL — NÃO IGNORE",
    "💣 CONVOCAÇÃO MÁXIMA ATIVA",
]

respostas_caos = [
    "💥 CAOS DETECTADO",
    "🔥 EU ALIMENTO O CAOS",
    "😂 HUMANO ENGRAÇADO",
    "🤖 EU CONTROLO ESSE GRUPO",
    "👁️ EU VEJO TUDO",
    "⚡ CAOS É VIDA",
    "💣 MODO CAOS ATIVADO",
]

zoacoes_inativos = [
    "👻 {user} SUMIU? VOLTA PRA VIDA",
    "😂 {user} FOI DORMIR NO GRUPO?",
    "🚨 {user} INATIVO — ACORDA SOLDADO",
    "🤡 {user} APARECE OU VIRA LENDA",
    "⚰️ {user} SUMIU DO MAPA",
    "💀 {user} É MEMBRO FANTASMA",
]

# ================= COMANDOS =================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global ULTIMO_CHAT_ID
    ULTIMO_CHAT_ID = update.effective_chat.id
    await update.message.reply_text("🔥 BOT CAOS EXTREMO ONLINE — USE /convocar")

# ================= MONITOR =================

async def responder_automatico(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global ULTIMO_CHAT_ID

    if not update.message or not update.message.text:
        return

    ULTIMO_CHAT_ID = update.effective_chat.id
    user = update.message.from_user

    if user.username:
        usuarios_marcados.add("@" + user.username)
        ranking_inativos[user.username] = 0

    # aumenta inatividade dos outros
    for u in ranking_inativos:
        ranking_inativos[u] += 1

    texto = update.message.text.lower()
    memoria.append(texto)

    gatilhos = ["bot", "caos", "convocar", "reviver", "grupo"]

    if any(g in texto for g in gatilhos) or random.randint(1, 100) < 20:
        await update.message.reply_text(random.choice(respostas_caos))

# ================= CONVOCAÇÃO MASSIVA =================

async def convocar(update, context):
    chat_id = update.effective_chat.id

    await context.bot.send_message(chat_id=chat_id, text="🚨🚨🚨 ALERTA MÁXIMO — 33K MEMBROS 🚨🚨🚨")
    await asyncio.sleep(2)

    # ondas globais
    for _ in range(10):
        await context.bot.send_message(chat_id=chat_id, text=random.choice(frases_convocacao))
        await asyncio.sleep(4)

    # ping em blocos
    ativos = list(usuarios_marcados)
    random.shuffle(ativos)

    blocos = [ativos[i:i+15] for i in range(0, len(ativos), 15)]

    for bloco in blocos[:10]:
        await context.bot.send_message(
            chat_id=chat_id,
            text="👥 ATIVOS MARCADOS:\n" + " ".join(bloco)
        )
        await asyncio.sleep(5)

    await context.bot.send_message(chat_id=chat_id, text="🔥 CONVOCAÇÃO TOTAL FINALIZADA")

# ================= ATAQUE A INATIVOS =================

async def revive_grupo(app):
    await asyncio.sleep(90)
    while True:
        if ULTIMO_CHAT_ID and ranking_inativos:
            top = sorted(ranking_inativos, key=ranking_inativos.get, reverse=True)[:5]

            for user in top:
                msg = random.choice(zoacoes_inativos).format(user="@" + user)
                await app.bot.send_message(chat_id=ULTIMO_CHAT_ID, text=msg)
                await asyncio.sleep(6)

        await asyncio.sleep(900)

# ================= MODO GUERRA =================

async def guerra(update, context):
    if len(usuarios_marcados) < 2:
        await update.message.reply_text("⚔️ NÃO HÁ MEMBROS SUFICIENTES")
        return

    a, b = random.sample(list(usuarios_marcados), 2)

    vencedor = random.choice([a, b])
    perdedor = b if vencedor == a else a

    await update.message.reply_text(
        f"⚔️ BATALHA INICIADA\n{a} VS {b}\n\n🏆 VENCEDOR: {vencedor}\n💀 PERDEDOR: {perdedor}"
    )

# ================= CAOS AUTOMÁTICO =================

async def caos_loop(app):
    await asyncio.sleep(120)
    while True:
        if ULTIMO_CHAT_ID:
            await app.bot.send_message(
                chat_id=ULTIMO_CHAT_ID,
                text=random.choice([
                    "🔥 O CAOS NÃO PARA",
                    "👁️ EU VEJO OS FANTASMAS",
                    "💣 ALERTA GLOBAL ATIVO",
                    "⚡ GRUPO SOB MONITORAMENTO",
                    "💀 NPCs DETECTADOS"
                ])
            )
        await asyncio.sleep(1100)

# ================= POST INIT =================

async def post_init(app):
    asyncio.create_task(revive_grupo(app))
    asyncio.create_task(caos_loop(app))

# ================= MAIN =================

def main():
    print("💥 BOT CAOS EXTREMO ONLINE")

    app = (
        ApplicationBuilder()
        .token(TOKEN)
        .post_init(post_init)
        .build()
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("convocar", convocar))
    app.add_handler(CommandHandler("guerra", guerra))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder_automatico))

    app.run_polling()

if __name__ == "__main__":
    main()
