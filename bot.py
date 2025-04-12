from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler
import random
import json
import os

# CONFIGURACIÓN
TOKEN = '7171960881:AAFt0byYjkyJ_xqyVwvt-MwXBSmjTi_IYQY'
ADMIN_ID = 6530497064
usuarios = {}
ARCHIVO_USUARIOS = 'usuarios.json'

if os.path.exists(ARCHIVO_USUARIOS):
    with open(ARCHIVO_USUARIOS, 'r') as f:
        usuarios = json.load(f)

def guardar_usuarios():
    with open(ARCHIVO_USUARIOS, 'w') as f:
        json.dump(usuarios, f)

# START
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = str(user.id)
    username = user.username or "SinUsername"
    nombre = user.full_name or "SinNombre"

    mensaje = (
        "🎉 ¡GRAN SORTEO ACTIVO!

"
        "Por ser parte de esta comunidad fiel, Zuby y nosotros queremos darte las gracias como mereces.
"
        "Gracias por estar ahí siempre.

"
        "✨ Esto es por ti y por Zuby.
"
        "💛 ¡Tu apoyo es lo que nos mueve!

"
        "🎁 Sorteamos:
"
        "🎟️ 2 suscripciones IPTV de 12 meses
"
        "🎟️ 5 suscripciones P2PTV de 1 mes

"
        "🗓️ Fecha: 20 de abril a las 20:00
"
        "📺 7000+ canales en vivo
"
        "🎬 8000+ películas y series on-demand

"
        "🧪 Prueba gratuita de 5 horas
"
        "💰 Planes desde 15€/mes
"
        "💳 Pago: Tarjeta, Transferencia, PayPal

"
        "📌 Requisitos:
"
        "📡 IPTV:
"
        "• Funciona en todos los dispositivos
"
        "• Eventos deportivos: usar VPN

"
        "🔗 P2PTV:
"
        "• Sin VPN
"
        "• Solo Android/Firestick/TV Box/PC/Mac
"
        "❌ No funciona en iPhone ni Smart TVs LG/Samsung

"
        "👇 ¡Participa ahora!"
    )

    botones = [[InlineKeyboardButton("🎟️ Participar en el sorteo", callback_data="participar")]]
    if user.id == ADMIN_ID:
        botones.append([
            InlineKeyboardButton("📋 Ver participantes", callback_data="ver_participantes"),
            InlineKeyboardButton("🎯 Hacer sorteo", callback_data="hacer_sorteo")
        ])

    await update.message.reply_text(mensaje, reply_markup=InlineKeyboardMarkup(botones))

# CALLBACKS
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
                f"🎉 Te has registrado correctamente al sorteo.

"
                f"🎟️ Número: {numero}
"
                f"👤 Usuario: @{username}
"
                f"📛 Nombre: {nombre}"
            )
        else:
            texto = (
                f"Ya estás registrado.

"
                f"🎟️ Número: {usuarios[user_id]['numero']}
"
                f"👤 Usuario: @{username}
"
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
            "📡 ¿Qué es P2PTV?

"
            "P2PTV funciona con tecnología peer-to-peer, donde los usuarios comparten contenido entre sí. No depende de servidores centrales ni puede ser bloqueado en España.

"
            "✔️ Carga rápida
✔️ Cero cortes
✔️ Calidad top
✔️ Inbloqueable

"
            "✅ Compatible con:
• Firestick de Amazon
• TV Box Android
• Chromecast Google TV
• Smart TV Android
• PC, Mac, tablet Android

"
            "❌ No compatible con iPhone ni Smart TVs LG o Samsung sin Android

"
            "🚀 ¿Cómo pedir la demo?

"
            "1. Instala la app “Downloader” desde tu Android
"
            "2. Abre la app y escribe este código: 3674863
"
            "3. Instala la app de P2PTV
"
            "4. Envíame por privado:
"
            "   • Una captura con la app instalada
"
            "   • La frase “QUIERO DEMO”

"
            "⏳ Recibirás acceso por 5 horas sin compromiso.

"
            "📩 Contáctame directo: @lamanodelreytv 👑"
        )

    elif query.data == "ver_participantes" and user.id == ADMIN_ID:
        if not usuarios:
            await query.message.reply_text("No hay participantes aún.")
            return
        texto = "📋 Participantes registrados:

"
        for uid, datos in usuarios.items():
            texto += f"🎟️ {datos['numero']} - @{datos['username']} - {datos['nombre']}
"
        await query.message.reply_text(texto)

    elif query.data == "hacer_sorteo" and user.id == ADMIN_ID:
        if len(usuarios) < 7:
            await query.message.reply_text("❌ No hay suficientes participantes (mínimo 7).")
            return
        participantes = list(usuarios.items())
        random.shuffle(participantes)
        ganadores = participantes[:7]
        mensaje = "🎉 RESULTADOS DEL SORTEO 🎉

"
        for i, (uid, datos) in enumerate(ganadores):
            premio = "12 meses IPTV" if i < 2 else "1 mes P2PTV"
            mensaje += (
                f"🏆 Ganador {i+1}: @{datos['username']} - {datos['nombre']} "
                f"(Número {datos['numero']})
🎁 Premio: {premio}

"
            )
            await context.bot.send_message(
                chat_id=int(uid),
                text=f"🎉 ¡Felicidades! Has ganado: {premio}
Contáctanos: @lamanodelreytv"
            )
        await query.message.reply_text(mensaje)

# /listado solo admin
async def listado(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("❌ Solo el administrador puede usar este comando.")
        return
    if not usuarios:
        await update.message.reply_text("No hay participantes registrados.")
        return
    texto = "📋 Listado de participantes:

"
    for uid, datos in usuarios.items():
        texto += f"ID: {uid} - Número: {datos['numero']} - @{datos['username']} - {datos['nombre']}
"
    await update.message.reply_text(texto)

# /miid
async def mi_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"🆔 Tu ID es: {update.effective_user.id}")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("listado", listado))
app.add_handler(CommandHandler("miid", mi_id))
app.add_handler(CallbackQueryHandler(handle_callback))
print("✅ Bot corriendo...")
app.run_polling()