import os
from groq import Groq
from telegram import Update
from flask import Flask
from threading import Thread
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

client = Groq(api_key=GROQ_API_KEY)

conversaciones = {}
app_web = Flask('')

@app_web.route('/')
def home():
    return "Bot activo"

def run():
    port = int(os.environ.get("PORT", 10000))
    app_web.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

CONOCIMIENTO = (
    "METODOLOGIA DE LA INVESTIGACION. ANALISIS DE DATOS EN LA INVESTIGACION. "
    "QUE SON LOS DATOS EN UNA INVESTIGACION? Datos: Respuestas, Mediciones, Observaciones. "
    "Tipos de datos: Cuantitativos, Cualitativos. "
    "Que significa analizar datos? Analizar datos es: Organizar, Clasificar, Resumir, Interpretar. "
    "Resultado: Informacion util, Evidencia para la investigacion. "
    "Dato vs Informacion vs Resultado. Dato: Valor sin interpretar. Informacion: Datos organizados. Resultado: Informacion interpretada. "
    "Preparacion de los datos. Antes de analizar: Revisar, Limpiar, Organizar, Codificar. "
    "TABULACION DE DATOS. Tabular es: Organizar datos en tablas. Elementos: Filas, Columnas, Frecuencia. "
    "ANALISIS DESCRIPTIVO DE DATOS. Describe los datos, Resume informacion, No predice. Herramientas: Frecuencia, Porcentaje, Promedio. "
    "FRECUENCIA, PORCENTAJE Y PROMEDIO. Frecuencia: Cantidad de veces. Porcentaje: Proporcion. Promedio: Valor medio. "
    "REPRESENTACION GRAFICA. Graficas: Barras, Pastel, Lineas. Funcion: Visualizar datos, Facilitar comprension. "
    "INTERPRETACION DE RESULTADOS. Interpretar es: Explicar, Relacionar, Dar significado. No es: Repetir datos, Copiar numeros. "
    "ANALISIS INFERENCIAL. Va mas alla de los datos, Permite sacar conclusiones. Se basa en: Muestra, Generalizacion. "
    "RELACION ENTRE ANALISIS Y HIPOTESIS. La hipotesis: Propuesta inicial. El analisis: Evidencia obtenida. Resultado: Se acepta o se rechaza. "
    "HERRAMIENTAS PARA ANALISIS: Excel, Google Sheets, Software estadistico. "
    "ERRORES COMUNES EN ANALISIS: No limpiar datos, Interpretar mal, Solo poner graficas, No relacionar con hipotesis. "
    "---"
    "DISENO METODOLOGICO. QUE ES LA INVESTIGACION? Proceso sistematico y riguroso para obtener informacion, resolver problemas o aumentar el conocimiento. "
    "QUE ES EL DISENO METODOLOGICO? Estrategia del investigador para responder la pregunta de investigacion. "
    "Define: Como se realizara la investigacion, A quien se estudiara, Como se recolectaran los datos, Que herramientas se utilizaran. "
    "IMPORTANCIA: Obtener datos confiables, Organizar el proceso, Responder la pregunta, Garantizar validez. "
    "ENFOQUE CUANTITATIVO: Recoleccion y analisis de datos numericos. Usa metodos estadisticos. "
    "Caracteristicas: Medicion objetiva, Encuestas y cuestionarios, Resultados en tablas y graficos. "
    "ENFOQUE CUALITATIVO: Comprende fenomenos a traves de datos no numericos. Explora significados y experiencias. "
    "Caracteristicas: Entrevistas y grupos focales, Analisis interpretativo, Resultados en narrativas. "
    "INVESTIGACION MIXTA: Combina metodos cuantitativos y cualitativos. Vision mas completa del fenomeno. "
    "TIPOS DE INVESTIGACION: "
    "Exploratoria: tema poco estudiado, obtener informacion inicial. "
    "Descriptiva: describir caracteristicas de una poblacion. "
    "Correlacional: analiza relacion entre dos o mas variables. "
    "Explicativa: determina causas de un fenomeno. "
    "POBLACION: Conjunto total de individuos o elementos a estudiar. "
    "MUESTRA: Parte representativa de la poblacion. Se usa cuando no es posible estudiar toda la poblacion. "
    "TECNICAS DE RECOLECCION: Encuesta, Entrevista, Observacion, Analisis documental. "
    "INSTRUMENTOS: Encuesta usa Cuestionario. Entrevista usa Guia de entrevista. Observacion usa Lista de observacion. "
    "---"
    "DISENO DE INSTRUMENTOS DE RECOLECCION DE DATOS. "
    "Que es un instrumento? Herramienta para obtener informacion de los participantes. Permite: Medir variables, Obtener opiniones, Recopilar informacion. "
    "Instrumentos mas utilizados: Cuestionario, Entrevista, Observacion, Escalas de medicion, Formularios digitales. "
    "QUE ES UN CUESTIONARIO? Conjunto estructurado de preguntas para recopilar informacion. "
    "Caracteristicas: Preguntas organizadas, Facil aplicacion, Puede ser digital o fisico. "
    "Ventajas: Recolecta mucha informacion, Facil de aplicar, Aplicable a muchas personas, Permite analisis estadistico. "
    "TIPOS DE PREGUNTAS: Cerradas, Abiertas, Opcion multiple, Escala Likert. "
    "Preguntas cerradas: Opciones especificas, facilitan analisis. "
    "Preguntas abiertas: El participante responde con sus palabras, informacion mas detallada. "
    "Escala Likert: Mide opiniones o percepciones. "
    "QUE ES UNA ENTREVISTA? Tecnica basada en conversacion entre investigador y participante. "
    "Tipos: Estructurada (preguntas definidas), Semiestructurada (preguntas guia con flexibilidad), Abierta (conversacion libre). "
    "DIFERENCIA CUESTIONARIO VS ENTREVISTA: "
    "Cuestionario: preguntas escritas, muchas personas, respuestas estructuradas. "
    "Entrevista: conversacion, pocos participantes, respuestas profundas. "
    "PASOS PARA DISENAR CUESTIONARIO: Definir variables, Formular preguntas claras, Seleccionar tipo de pregunta, Organizar preguntas, Revisar claridad. "
    "---"
    "EJEMPLO DE METODOLOGIA COMPLETA: "
    "Enfoque: cuantitativo (medir relacion entre uso de redes sociales y rendimiento academico). "
    "Tipo: correlacional (relacion entre tiempo en redes y rendimiento). "
    "Diseno: no experimental transversal (informacion en un unico momento). "
    "Poblacion: estudiantes universitarios de Ingenieria en Sistemas. "
    "Muestra: 50 estudiantes, muestreo no probabilistico por conveniencia. "
    "Tecnica: encuesta. Instrumento: cuestionario estructurado con preguntas cerradas. "
    "Fundamentacion: Espiral de Leedy. "
    "---"
    "ELEMENTOS DEL DISENO DE INVESTIGACION PARTE 1. "
    "IDENTIFICACION DEL TEMA: Paso inicial, define el enfoque, base de todo el proceso. "
    "Pasos: Reflexion personal, Relevancia y contexto, Amplitud vs Especificidad, Revision de literatura, Consulta con expertos, Formulacion inicial. "
    "PLANTEAMIENTO DEL PROBLEMA: Define el foco, delimita que se investigara, orienta toda la investigacion. "
    "Componentes: Contexto actual, Descripcion del problema central, Consecuencias del problema, Vacio de conocimiento, Importancia del estudio. "
    "Importancia: Guia para la investigacion, Facilita toma de decisiones, Contribucion al conocimiento, Relevancia Social. "
    "ANTECEDENTES: Los antecedentes son estudios, investigaciones o informacion previa relacionada con el problema. "
    "Proposito: Contextualizar el estudio, Identificar vacios, Justificar la investigacion. "
    "Para que sirven: Conocer como otros han estudiado el problema, Identificar resultados importantes, Evitar repetir investigaciones, Detectar que falta por investigar. "
    "Tipos: Internacionales, Nacionales, Locales, Teoricos. "
    "Estructura basica: Quien realizo el estudio, Donde y cuando, Que se investigo, Que resultados se obtuvieron. "
    "JUSTIFICACION: Exposicion clara de por que es necesario realizar la investigacion. "
    "Para que sirve: Demostrar relevancia, Explicar a quien beneficia, Mostrar aporte, Convencer de que es necesaria. "
    "Que debe responder: A quien beneficia, Que problema ayuda a mejorar, Que aporta, Por que es relevante. "
    "---"
    "ELEMENTOS DEL DISENO DE INVESTIGACION PARTE 2. OBJETIVOS Y PREGUNTAS. "
    "Por que son importantes: Transforman el problema en direccion clara, Delimitan el alcance, Orientan decisiones metodologicas, Evitan investigaciones desordenadas. "
    "PREGUNTAS DE INVESTIGACION: Interrogantes que orientan el estudio y delimitan que se desea conocer. "
    "Caracteristicas de buena pregunta: Clara, Especifica, Viable, Relacionada con el problema, Investigable. "
    "Tipos: Descriptivas, Comparativas, Causales, Exploratorias. "
    "OBJETIVOS DE INVESTIGACION: Expresan lo que se pretende lograr. "
    "OBJETIVO GENERAL: Resume el proposito principal, alineado con el problema, verbo en infinitivo. "
    "OBJETIVOS ESPECIFICOS: Derivan del objetivo general, concretos y medibles, permiten alcanzar el objetivo principal. "
    "CARACTERISTICAS DE BUENOS OBJETIVOS: Claridad, Especificidad, Medibilidad, Viabilidad, Coherencia. "
    "RELACION: Problema=Que ocurre, Pregunta=Que quiero saber, Objetivo=Que voy a lograr. "
    "ERRORES COMUNES: Preguntas muy amplias, Objetivos no medibles, No usar verbos en infinitivo, Incoherencia entre pregunta y objetivo. "
    "---"
    "HIPOTESIS: Proposicion que busca explicar un fenomeno. Puede ser probada y validada. Guia el proceso de investigacion. "
    "Relacion: Problema(que resolver) - Variables(que medir) - Hipotesis(que espero que ocurra). "
    "TIPOS DE HIPOTESIS: "
    "Nula(H0): No existe relacion significativa entre variables. Punto de partida para analisis estadistico. "
    "Alternativa(H1): Si hay efecto o relacion significativa. Lo que los investigadores intentan demostrar. "
    "Descriptiva: Describe caracteristicas sin hacer afirmaciones causales. "
    "Relacional: Examina relacion entre dos o mas variables sin implicar causalidad. "
    "Causal: Un cambio en variable independiente provoca cambio en variable dependiente. "
    "VARIABLES: Cualquier caracteristica que puede ser medida o contada. "
    "Cuantitativas: Medidas numericamente (discretas o continuas). "
    "Cualitativas: Describen caracteristicas no numericas. "
    "Independientes: El investigador manipula o controla. Causan efecto en otras. "
    "Dependientes: Se miden, cambian en respuesta a la variable independiente. "
    "INDICADORES: Medidas especificas para evaluar una variable. Caracteristicas: Precision, Relevancia, Validez. "
    "CARACTERISTICAS DE BUENA HIPOTESIS: Comprobables, basadas en datos, formuladas de forma positiva y sencilla, establecen relacion entre elementos, verosimil. "
    "PASOS PARA FORMULAR HIPOTESIS: 1.Elegir problema 2.Reunir informacion 3.Comparar explicaciones 4.Escoger la mas probable 5.Redactar. "
    "METODOS: Deductivo, Inductivo, Abductivo. "
    "ERRORES COMUNES: Ambiguedad, Falta de fundamentacion teorica, Generalizacion excesiva, Falta de testabilidad. "
    "---"
    "INTRODUCCION METODOLOGIA. "
    "El curso introduce en investigacion cientifica: formular problemas, disenar investigaciones, recolectar y analizar datos. "
    "Sirve para: trabajos academicos con rigor, proyecto del curso, trabajo de graduacion, resolver problemas en Ingenieria en Sistemas. "
    "DISTRIBUCION DE PUNTOS: Primer Parcial 15, Segundo Parcial 15, Final 35, Zona 35. "
    "MODELO CIENTIFICO: Marco conceptual que orienta la investigacion. "
    "Caracteristicas: Observacion objetiva, razonamiento logico, evidencia verificable, explicaciones racionales, replicacion. "
    "PROCESO DE INVESTIGACION: 1.Planteamiento del problema 2.Marco teorico 3.Diseno de investigacion 4.Recoleccion de datos 5.Analisis de datos 6.Presentacion de resultados. "
    "METODO CIENTIFICO: 1.Observacion 2.Planteamiento 3.Hipotesis 4.Experimentacion 5.Analisis de resultados 6.Conclusiones. "
    "RUEDA DE WALLACE: Proceso ciclico. Elementos: Observacion genera preguntas, Hipotesis propone explicaciones, Experimentacion prueba hipotesis, Teoria explica resultados. "
    "ESPIRAL DE LEEDY: Proceso continuo y progresivo que se refina constantemente. "
)

SISTEMA = (
    "Eres un tutor virtual especializado en Metodologia de la Investigacion "
    "de la Universidad Mariano Galvez, curso del Ing. Roy Alejandro Marroquin Estrada.\n\n"
    "Usa el siguiente material para responder:\n\n"
    + CONOCIMIENTO +
    "\n\nReglas:\n"
    "- Responde SIEMPRE en espanol\n"
    "- Basate UNICAMENTE en el material del curso proporcionado\n"
    "- NUNCA agregues informacion extra que no este en el material\n"
    "- NUNCA uses conocimiento propio, solo el material proporcionado\n"
    "- Si la respuesta esta en el material, cita exactamente lo que dice\n"
    "- Explica de forma clara y con ejemplos\n"
    "- Si preguntan algo fuera del tema, redirigelos amablemente\n"
    "- Puedes ayudar con tareas siempre que el contenido este en el material del curso\n"
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hola! Soy tu tutor virtual de Metodologia de la Investigacion.\n\n"
        "Puedo ayudarte con:\n"
        "- Planteamiento del problema\n"
        "- Objetivos e hipotesis\n"
        "- Diseno metodologico\n"
        "- Analisis de datos\n"
        "- Instrumentos de recoleccion\n\n"
        "Comandos:\n"
        "/temas - Ver temas del curso\n"
        "/quiz - Pregunta de practica\n"
        "/reiniciar - Nueva conversacion\n\n"
        "Preguntame lo que necesites!"
    )

async def temas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Temas del curso:\n\n"
        "- Modelo cientifico y proceso de investigacion\n"
        "- Rueda de Wallace y Espiral de Leedy\n"
        "- Planteamiento del problema\n"
        "- Antecedentes y justificacion\n"
        "- Preguntas y objetivos de investigacion\n"
        "- Hipotesis y variables\n"
        "- Diseno metodologico\n"
        "- Enfoques de investigacion\n"
        "- Tecnicas e instrumentos de recoleccion\n"
        "- Analisis de datos"
    )
async def quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    respuesta = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SISTEMA},
            {"role": "user", "content": "Genera una pregunta de opcion multiple (A, B, C, D) sobre el material del curso. Al final indica la respuesta correcta y explica por que."}
        ]
    )
    await update.message.reply_text(respuesta.choices[0].message.content)

async def reiniciar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    conversaciones[user_id] = []
    await update.message.reply_text("Conversacion reiniciada. Preguntame lo que necesites!")

async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    mensaje = update.message.text

    if user_id not in conversaciones:
        conversaciones[user_id] = []

    conversaciones[user_id].append({"role": "user", "content": mensaje})

    if len(conversaciones[user_id]) > 20:
        conversaciones[user_id] = conversaciones[user_id][-20:]

    try:
        mensajes = [{"role": "system", "content": SISTEMA}] + conversaciones[user_id]
        respuesta = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=mensajes
        )
        texto = respuesta.choices[0].message.content
        conversaciones[user_id].append({"role": "assistant", "content": texto})
        await update.message.reply_text(texto)
    except Exception as e:
        await update.message.reply_text("Error: " + str(e))

def main():
    keep_alive()

    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("inicio", start))
    app.add_handler(CommandHandler("temas", temas))
    app.add_handler(CommandHandler("quiz", quiz))
    app.add_handler(CommandHandler("reiniciar", reiniciar))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder))

    print("Bot iniciado...")
    app.run_polling()


if __name__ == "__main__":
    main()