from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler
import random
import json
import os

TOKEN = os.getenv("TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))
usuarios = {}
ARCHIVO_USUARIOS = 'usuarios.json'

if os.path.exists(ARCHIVO_USUARIOS):
    with open(ARCHIVO_USUARIOS, 'r') as f:
        usuarios = json.load(f)

def guardar_usuarios():
    with open(ARCHIVO_USUARIOS, 'w') as f:
        json.dump(usuarios, f)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = str(user.id)
    username = user.username or "SinUsername"
    nombre = user.full_name or "SinNombre"

    mensaje = (
        "🎉 ¡GRAN SORTEO ACTIVO!\n\n"
        "Por ser parte de esta comunidad fiel, Zuby y nosotros queremos darte las gracias como mereces.\n"
        "Gracias por estar ahí siempre.\n\n"
        "✨ Esto es por ti y por Zuby.\n"
        "💛 ¡Tu apoyo es lo que nos mueve!\n\n"
        "🎁 Sorteamos:\n"
        "🎟️ 2 suscripciones IPTV de 12 meses\n"
        "🎟️ 5 suscripciones P2PTV de 1 mes\n\n"
        "🗓️ Fecha: 20 de abril a las 20:00\n"
        "📺 7000+ canales en vivo\n"
        "🎬 8000+ películas y series on-demand\n\n"
        "🧪 Prueba gratuita de 5 horas\n"
        "💰 Planes desde 15€/mes\n"
        "💳 Pago: Tarjeta, Transferencia, PayPal\n\n"
        "📌 Requisitos:\n"
        "📡 IPTV:\n"
        "• Funciona en todos los dispositivos\n"
        "• Eventos deportivos: usar VPN\n\n"
        "🔗 P2PTV:\n"
        "• Sin VPN\n"
        "• Solo Android/Firestick/TV Box/PC/Mac\n"
        "❌ No funciona en iPhone ni Smart TVs LG/Samsung\n\n"
        "👇 ¡Participa ahora!"
    )

    botones = [[InlineKeyboardButton("🎟️ Participar en el sorteo", callback_data="participar")]]
    if user.id == ADMIN_ID:
        botones.append([
            InlineKeyboardButton("📋 Ver participantes", callback_data="ver_participantes"),
            InlineKeyboardButton("🎯 Hacer sorteo", callback_data="hacer_sorteo")
        ])

    await update.message.reply_text(mensaje, reply_markup=InlineKeyboardMarkup(botones))

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user = query.from_user
    user_id = str(user.id)
    username = user.username or "SinUsername"
    nombre = user.full_name or "SinNombre"

    if query.data == "participar":
        if user_id not in usuarios:
            numero = random.randint(100, 999)
            while numero in [u["numero"] for u in usuarios.values()]:
                numero = random.randint(100, 999)
            usuarios[user_id] = {
                "numero": numero,
                "username": username,
                "nombre": nombre
            }
            guardar_usuarios()
            texto = (
                f"🎉 Te has registrado correctamente al sorteo.\n\n"
                f"🎟️ Número: {numero}\n"
                f"👤 Usuario: @{username}\n"
                f"📛 Nombre: {nombre}"
            )
        else:
            texto = (
                f"Ya estás registrado.\n\n"
                f"🎟️ Número: {usuarios[user_id]['numero']}\n"
                f"👤 Usuario: @{username}\n"
                f"📛 Nombre: {nombre}"
            )

        botones = [[InlineKeyboardButton("🚀 Solicitar demo gratuita", callback_data="demo")]]
        await query.edit_message_text(texto, reply_markup=InlineKeyboardMarkup(botones))

    elif query.data == "demo":
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"📨 El usuario @{username} ha solicitado una demo gratuita."
        )
        await query.message.reply_text(
            "📡 ¿Qué es P2PTV?\n\n"
            "P2PTV funciona con tecnología peer-to-peer, donde los usuarios comparten contenido entre sí. "
            "No depende de servidores centrales ni puede ser bloqueado en España.\n\n"
            "✔️ Carga rápida\n✔️ Cero cortes\n✔️ Calidad top\n✔️ Inbloqueable\n\n"
            "✅ Compatible con:\n• Firestick de Amazon\n• TV Box Android\n• Chromecast Google TV\n• Smart TV Android\n• PC, Mac, tablet Android\n\n"
            "❌ No compatible con:\n• iPhone\n• Smart TVs LG/Samsung sin Android\n\n"
            "🚀 ¿Cómo pedir la demo?\n\n"
            "1. Instala la app “Downloader” desde tu Android\n"
            "2. Abre la app y escribe este código: 3674863\n"
            "3. Instala la app de P2PTV\n"
            "4. Envíame por privado:\n"
            "   • Una captura con la app instalada\n"
            "   • La frase “QUIERO DEMO”\n\n"
            "⏳ Acceso por 5 horas gratis\n📩 Contáctame: @lamanodelreytv 👑"
        )

    elif query.data == "ver_participantes" and int(user_id) == ADMIN_ID:
        texto = "📋 Participantes registrados:\n\n"
        for uid, datos in usuarios.items():
            texto += f"🎟️ {datos['numero']} - @{datos['username']} - {datos['nombre']}\n"
        await query.message.reply_text(texto if usuarios else "No hay participantes aún.")

    elif query.data == "hacer_sorteo" and int(user_id) == ADMIN_ID:
        if len(usuarios) < 7:
            await query.message.reply_text("❌ No hay suficientes participantes (mínimo 7).")
            return
        participantes = list(usuarios.items())
        random.shuffle(participantes)
        ganadores = participantes[:7]
        mensaje = "🎉 RESULTADOS DEL SORTEO 🎉\n\n"
        for i, (uid, datos) in enumerate(ganadores):
            premio = "12 meses IPTV" if i < 2 else "1 mes P2PTV"
            mensaje += f"🏆 Ganador {i+1}: @{datos['username']} - {datos['nombre']} (Nº {datos['numero']})\n🎁 Premio: {premio}\n\n"
            await context.bot.send_message(
                chat_id=int(uid),
                text=f"🎉 ¡Felicidades! Has ganado: {premio}\nContáctanos: @lamanodelreytv"
            )
        await query.message.reply_text(mensaje)

async def listado(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("❌ Solo el administrador puede usar este comando.")
        return
    texto = "📋 Listado de participantes:\n\n"
    for uid, datos in usuarios.items():
        texto += f"ID: {uid} - Número: {datos['numero']} - @{datos['username']} - {datos['nombre']}\n"
    await update.message.reply_text(texto if usuarios else "No hay participantes registrados.")

async def mi_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"🆔 Tu ID es: {update.effective_user.id}")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("listado", listado))
app.add_handler(CommandHandler("miid", mi_id))
app.add_handler(CallbackQueryHandler(handle_callback))
print("✅ Bot corriendo...")
app.run_polling()
