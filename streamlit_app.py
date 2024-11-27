#CUSTIONARIO SISTEMA GESTIÓN ANTI SOBORNO

# ====================
# 1. Cargar Librerias
# ====================

import random
import gradio as gr
import pandas as pd
from rapidfuzz import fuzz # Importar rapidfuzz para similitud flexible
from rapidfuzz import process
import os
from datetime import datetime

# =================================
# 2. Cargar balotario a diccionario
# =================================

preguntas_y_respuestas = [
    {"pregunta": "¿Qué norma certifica el SGAS?",
     "opciones": ["ISO 9001", "ISO 37001", "ISO 14001"],
     "respuesta": "ISO 37001",
     "tipo": "cerrada"},

    {"pregunta": "¿Qué herramienta permite identificar y priorizar los riesgos en el SGAS?",
     "opciones": ["Matriz de Riesgos", "Código de Ética", "Línea Ética"],
     "respuesta": "Matriz de Riesgos",
     "tipo": "cerrada"},

    {"pregunta": "¿Qué debe hacer un colaborador si identifica un riesgo relacionado a sus actividades?",
     "opciones": ["Informarlo a su jefe superior", "Tomar medidas inmediatas sin reportarlo", "Esperar a la auditoría para comunicarlo"],
     "respuesta": "Informarlo a su jefe superior",
     "tipo": "cerrada"},

    {"pregunta": "¿Qué responsabilidad tiene el Oficial de Cumplimiento en el SGAS?",
     "opciones": ["Asegurar cumplimiento e identificar riesgos de soborno y asesorar al trabajador", "Asegurar la operación e identificar riesgos eléctricos", "Capacitar trabajadores"],
     "respuesta": "Asegurar cumplimiento e identificar riesgos de soborno y asesorar al trabajador",
     "tipo": "cerrada"},

    {"pregunta": "Menciona los canales disponibles para realizar denuncias en Luz del Sur.",
     "respuesta": "Línea ética, Teléfono, correo, página web, web",
     "tipo": "abierta"},

    {"pregunta": "Menciona el número de la línea de ética para realizar denuncias en Luz del Sur.",
     "respuesta": "080000795",
     "tipo": "abierta"},

    {"pregunta": "¿Quién es el Oficial de Cumplimiento en Luz del Sur?",
     "respuesta": "Gillian Paredes",
     "tipo": "abierta"},

    {"pregunta": "Marca el correo electrónico disponible para realizar denuncias en Luz del Sur.",
     "opciones": ["lineaeticaluzdelsur@kpmg.com.ai", "lineaeticaluzdelsur@kpmg.com.ar", "lineaeticaluzdelsur@kpmgh.com.ar", "lineaeticaluzdelsur@kpmg.com.arg"],
     "respuesta": "lineaeticaluzdelsur@kpmg.com.ar",
     "tipo": "cerrada"},

    {"pregunta": "¿El SGAS está basado en la norma ISO 37001?",
     "opciones": ["Sí", "No"],
     "respuesta": "Sí",
     "tipo": "cerrada"},

    {"pregunta": "¿La Alta Dirección tiene un rol en la supervisión del SGAS?",
     "opciones": ["Sí", "No"],
     "respuesta": "Sí",
     "tipo": "cerrada"},

    {"pregunta": "¿El SGAS aplica solo al área de Finanzas?",
     "opciones": ["Sí", "No"],
     "respuesta": "No",
     "tipo": "cerrada"},

    {"pregunta": "¿La auditoría interna del SGAS se realiza anualmente?",
     "opciones": ["Sí", "No"],
     "respuesta": "Sí",
     "tipo": "cerrada"},

    {"pregunta": "¿El Código de Ética incluye lineamientos sobre la aceptación de regalos?",
     "opciones": ["Sí", "No"],
     "respuesta": "Sí",
     "tipo": "cerrada"},

    {"pregunta": "¿La Línea Ética es accesible para todos los empleados?",
     "opciones": ["Sí", "No"],
     "respuesta": "Sí",
     "tipo": "cerrada"},

    {"pregunta": "¿El SGAS prohíbe cualquier tipo de soborno?",
     "opciones": ["Sí", "No"],
     "respuesta": "Sí",
     "tipo": "cerrada"},

    {"pregunta": "¿El SGAS permite excepciones en la política de soborno?",
     "opciones": ["Sí", "No"],
     "respuesta": "No",
     "tipo": "cerrada"},

    {"pregunta": "¿El SGAS está alineado con los estándares internacionales en la lucha contra la corrupción?",
     "opciones": ["Sí", "No"],
     "respuesta": "Sí",
     "tipo": "cerrada"},

    {"pregunta": "¿Es posible modificar el SGAS sin aprobación de la Alta Dirección?",
     "opciones": ["Sí", "No"],
     "respuesta": "No",
     "tipo": "cerrada"},

    {"pregunta": "Selecciona los roles más importantes del SGAS.",
     "opciones": ["Gobierno-Dirección-Oficial", "Órgano de Gobierno-Alta Dirección-Oficial de Cumplimiento", "Órgano de Presidencia-Alta Dirección-Oficiales de Cumplimiento", "Órgano de Gobierno-Alta Dirección-Oficial de Cumplimiento-Empleados"],
     "respuesta": "Órgano de Gobierno-Alta Dirección-Oficial de Cumplimiento",
     "tipo": "cerrada"},

    {"pregunta": "Selecciona las acciones que forman parte del cumplimiento del SGAS.",
     "opciones": ["Realizar auditorías internas", "Capacitar a terceros", "Ignorar conflictos de interés"],
     "respuesta": "Realizar auditorías internas",
     "tipo": "cerrada"},

    {"pregunta": "Para Luz del Sur ¿Quien es el responsable de la Alta Dirección (AD)?",
     "respuesta": "El Gerente General Mario Gonzales",
     "tipo": "abierta"},

    {"pregunta": "Para Luz del Sur ¿Quién asume el rol del Órgano de Gobierno (OG)?",
     "respuesta": "El directorio de Luz del Sur",
     "tipo": "abierta"},

    {"pregunta": "¿La Línea Ética es accesible para todos los empleados?",
     "opciones": ["Sí", "No"],
     "respuesta": "Sí",
     "tipo": "cerrada"},

    {"pregunta": "¿El SGAS prohíbe cualquier tipo de soborno?",
     "opciones": ["Sí", "No"],
     "respuesta": "Sí",
     "tipo": "cerrada"},

    {"pregunta": "¿El SGAS permite excepciones en la política de soborno?",
     "opciones": ["Sí", "No"],
     "respuesta": "No",
     "tipo": "cerrada"},

    {"pregunta": "¿Qué actividades están prohibidas según el SGAS? a. Aceptar regalos excesivos b. Participar en conflictos de interés c. Realizar pagos ilícitos",
     "opciones": ["a y b", "b y c", "Solo c", "a, b y c"],
     "respuesta": "a, b y c",
     "tipo": "cerrada"},

    {"pregunta": "¿Qué actividades están permitidas para garantizar la transparencia en el SGAS?",
     "opciones": ["Revisión continua de políticas y auditorías externas", "Revisión continua de politicas y Auditorías internas", "Concesión de favores"],
     "respuesta": "Revisión continua de políticas y auditorías externas",
     "tipo": "cerrada"},

    {"pregunta": "¿Cómo contribuyo a la mejora continúa del SGAS?",
     "respuesta": "Reportando",
     "tipo": "abierta"},

    {"pregunta": "¿Que debo hacer si soy testigo de una situación de soborno?",
     "respuesta": "Reportar por teléfono, por correo, web",
     "tipo": "abierta"},

    {"pregunta": "¿Menciona 3 intereses que generan un conflicto de interés?",
     "respuesta": "Personales, familiares, financieras o políticos",
     "tipo": "abierta"},

    {"pregunta": "¿Quién es la parte afectada en una situación de soborno?",
     "respuesta": "La empresa, organización",
     "tipo": "abierta"},

    {"pregunta": "¿El Código de Conducta es un estándar que todos deben seguir?",
     "opciones": ["Sí", "No"],
     "respuesta": "Sí",
     "tipo": "cerrada"},

    {"pregunta": "¿Cuál es la consecuencia de un acto de soborno para la organización? a. Daño económico b. Consecuencias legales c. Daños de reputación",
     "opciones": ["a y b", "b y c", "Solo a", "a, b y c"],
     "respuesta": "a, b y c",
     "tipo": "cerrada"},

    {"pregunta": "¿Cuál es la consecuencia de un acto de soborno para el trabajador? a. Daño económico b. Consecuencias legales c. Despedido",
     "opciones": ["a y b", "b y c", "Solo c", "a, b y c"],
     "respuesta": "b y c",
     "tipo": "cerrada"},

    {"pregunta": "¿Cuál es la consecuencia de un acto de soborno para terceros y socios comerciales? a. Daño económico b. Consecuencias legales c. Sancionados según contrato",
     "opciones": ["a y b", "b y c", "Solo c", "a, b y c"],
     "respuesta": "Solo c",
     "tipo": "cerrada"},

        {"pregunta": "¿Qué norma certifica el SGAS?",
     "opciones": ["ISO 37001 Sistema de Gestión Antisoborno", "ISO 37001 Sistema de Gestión ambiental", "ISO 31001 Sistema de Gestión de seguridad", "ISO 37001 Sistema de Gestión de Ambiente y seguridad"],
     "respuesta": "ISO 37001 Sistema de Gestión Antisoborno",
     "tipo": "cerrada"},

    {"pregunta": "¿Qué significa SGAS?",
     "opciones": ["Sistema de Gestión Antisoborno", "Sistema de Gestión ambiental y seguridad", "Sistema de Gestión Antisoborno y salud", "Ninguna"],
     "respuesta": "Sistema de Gestión Antisoborno",
     "tipo": "cerrada"},

    {"pregunta": "Complete: el SGAS establece requisitos para ayudar a la empresa a prevenir, detectar y abordar el ______.",
     "opciones": ["Soborno", "Control", "Riesgo", "Peligro"],
     "respuesta": "Soborno",
     "tipo": "cerrada"},

    {"pregunta": "¿Cuáles son los roles del SGAS?",
     "opciones": ["Órgano de Gobierno (OG)", "Alta Dirección (AD)", "Oficial de cumplimiento (OC)", "Todas las anteriores"],
     "respuesta": "Todas las anteriores",
     "tipo": "cerrada"},

    {"pregunta": "En LDS, ¿quién representa al Órgano de Gobierno?",
     "opciones": ["El directorio", "Mario Gonzales, Gerente General", "Gillian Paredes, Gerente de Legal", "Ninguna de las anteriores"],
     "respuesta": "El directorio",
     "tipo": "cerrada"},

    {"pregunta": "En LDS, ¿quién representa a la Alta Dirección?",
     "opciones": ["El directorio", "Mario Gonzales, Gerente General", "Gillian Paredes, Gerente de Legal", "Ninguna de las anteriores"],
     "respuesta": "Mario Gonzales, Gerente General",
     "tipo": "cerrada"},

    {"pregunta": "En LDS, ¿quién representa al Oficial de Cumplimiento?",
     "opciones": ["El directorio", "Mario Gonzales, Gerente General", "Gillian Paredes, Gerente de Legal", "Ninguna de las anteriores"],
     "respuesta": "Gillian Paredes, Gerente de Legal",
     "tipo": "cerrada"},

    {"pregunta": "¿Qué establece la política de SGAS?",
     "opciones": ["a.Prohíbe el soborno (dar o recibir regalos o dinero, realizar fraude, malversar fondos)",
                  "b.Me permite realizar una denuncia sin represalias, en caso de que sea testigo de un comportamiento indebido",
                  "c.Busca la mejora continua identifica y revisa los riesgos y controles en cada proceso.",
                  "Todas las anteriores"],
     "respuesta": "Todas las anteriores",
     "tipo": "cerrada"},

    {"pregunta": "¿Qué contiene el código de ética?",
     "opciones": ["a.Señala los valores, normas y criterios que rigen el comportamiento señalando límites éticos",
                  "b.Su cumplimiento garantiza que actuemos en conformidad con los valores de la empresa",
                  "c.Resume buenas prácticas de la actividad empresarial",
                  "Todas las anteriores"],
     "respuesta": "Todas las anteriores",
     "tipo": "cerrada"},

    {"pregunta": "Menciona los canales disponibles para realizar denuncias en Luz del Sur.",
     "opciones": ["Línea ética", "Correo", "Página web", "Todas las anteriores"],
     "respuesta": "Todas las anteriores",
     "tipo": "cerrada"},

    {"pregunta": "Menciona el número de la línea de ética para realizar denuncias en Luz del Sur.",
     "opciones": ["051 617 5000", "0 800 00800", "0 800 00795", "01-2719000"],
     "respuesta": "0 800 00795",
     "tipo": "cerrada"},

    {"pregunta": "Menciona el correo electrónico para realizar denuncias en Luz del Sur.",
     "opciones": ["integridadluzdelsur@kpmg.com.ar", "lineaeticaluzdelsur@kpmg.com.ar",
                  "lineaeticaluzdelsur@kpmg.com", "Ninguna de las anteriores"],
     "respuesta": "lineaeticaluzdelsur@kpmg.com.ar",
     "tipo": "cerrada"},

    {"pregunta": "Menciona la página web para realizar denuncias en Luz del Sur.",
     "opciones": ["https://www.luzdelsur.com.pe/", "https:/lineaeticaluzdelsur.kpmg.com.ar/",
                  "https:/lineaeticaluzdelsur.lineaseticas.com/", "Todas las anteriores"],
     "respuesta": "https:/lineaeticaluzdelsur.kpmg.com.ar/",
     "tipo": "cerrada"},

    {"pregunta": "¿Qué herramienta permite identificar y priorizar los riesgos en el SGAS?",
     "opciones": ["Matriz de Riesgos Antisoborno", "MVAA", "IPER", "Ninguna"],
     "respuesta": "Matriz de Riesgos Antisoborno",
     "tipo": "cerrada"},

    {"pregunta": "¿Cómo contribuyes con el funcionamiento del SGAS?",
     "opciones": ["a.Cumpliendo con las políticas y procedimientos", "b.Aportando a la mejora continua",
                  "c.Denunciando", "Todas las anteriores"],
     "respuesta": "Todas las anteriores",
     "tipo": "cerrada"},

    {"pregunta": "¿Dónde encuentras las políticas y procedimientos?",
     "opciones": ["a.Intranet/Documentos organizacionales/documentos oficiales/nivel estratégico/política",
                  "b.Intranet/Documentos organizacionales/documentos oficiales/nivel táctico/reglamento",
                  "c.https://luzdelsurlds.sharepoint.com/sites/compliance",
                  "a, b y c"],
     "respuesta": "a, b y c",
     "tipo": "cerrada"},

    {"pregunta": "¿Qué debe hacer un colaborador si identifica un nuevo riesgo relacionado a sus actividades?",
     "opciones": ["a.Informar a su jefe superior", "b.Informar al oficial de cumplimiento",
                  "c.Lo informo cuando suceda", "a y b"],
     "respuesta": "a y b",
     "tipo": "cerrada"},

    {"pregunta": "Responsabilidad del Oficial de Cumplimiento en el SGAS: Asegurar cumplimiento e identificar riesgos de ______ y ____ al trabajador",
     "opciones": ["Salud - psicológico", "Soborno - asesorar", "Medio ambiente - contaminación", "Seguridad - daños"],
     "respuesta": "Soborno - asesorar",
     "tipo": "cerrada"},

    {"pregunta": "¿Qué encuentro en las políticas y procedimientos del SGAS? Todos los _______ identificados que aseguran la mitigación de los riesgos de ________ en las actividades que realizo.",
     "opciones": ["Casos - Medio ambiente", "Sobornos - ocurrir", "Controles - soborno", "Controles - seguridad"],
     "respuesta": "Controles - soborno",
     "tipo": "cerrada"},

    {"pregunta": "¿Cómo aporto a la mejora continua?",
     "opciones": ["a.Identificando nuevos riesgos", "b.Reportando a mi jefe", "c.Pedir la actualización de la matriz",
                  "d.Definir controles para mitigar", "e.Todas las anteriores"],
     "respuesta": "Todas las anteriores",
     "tipo": "cerrada"},

    {"pregunta": "Complete: Denuncio si soy testigo de un comportamiento __ ético o ____ a través de los Canales de Denuncia",
     "opciones": ["Cuasi - ilegal", "No - ilegal", "Cuasi - legal", "Anti – legal"],
     "respuesta": "No - ilegal",
     "tipo": "cerrada"},

    {"pregunta": "¿Por qué debo usar los canales de denuncia oficiales?",
     "opciones": ["a.Mi identidad está protegida", "b.No sufriré represalia", "c.Para que todos se enteren", "d.Por vergüenza a que me descubran", "a y b"],
     "respuesta": "a y b",
     "tipo": "cerrada"},

    {"pregunta": "¿Quiénes sufren las consecuencias de ser parte de un acto de soborno?",
     "opciones": ["La organización", "El colaborador", "Los terceros y socios comerciales", "Todos"],
     "respuesta": "Todos",
     "tipo": "cerrada"},

    {"pregunta": "¿Cómo le afectaría a la organización un acto de soborno?",
     "opciones": ["Legalmente", "Económicamente", "A su reputación", "Todos"],
     "respuesta": "Todos",
     "tipo": "cerrada"},

    {"pregunta": "¿Cómo afectaría al personal involucrado en el soborno?",
     "opciones": ["Sancionado o separado de la empresa", "Sufrir acciones legales", "Puede ser procesado por la justicia", "Todos"],
     "respuesta": "Todos",
     "tipo": "cerrada"},

    {"pregunta": "¿Cómo afectaría a los terceros o socios comerciales?",
     "opciones": ["Sanciones de acuerdo a los acuerdos comerciales", "Cobrar multas", "No contratar con él nuevamente", "Todos"],
     "respuesta": "Todos",
     "tipo": "cerrada"},

    {"pregunta": "Soborno: oferta, promesa, entrega, aceptación o solicitud de una _______, de cualquier valor que influye directa o indirectamente en el comportamiento a cambio de un _______ para actuar o dejar de actuar.",
     "opciones": ["Máquina - dinero", "Ventaja indebida - incentivo", "Capacitación - dinero"],
     "respuesta": "Ventaja indebida - incentivo",
     "tipo": "cerrada"},

    {"pregunta": "Conflicto de interés: situación donde los intereses __________, financieros y políticos de una persona interfieren con su capacidad de tomar _______ objetivas.",
     "opciones": ["Comerciales – conjeturas", "Comerciales - decisiones", "Personales, familiares – decisiones", "Personales, familiares – conjeturas"],
     "respuesta": "Personales, familiares – decisiones",
     "tipo": "cerrada"},

    {"pregunta": "Debida diligencia: es el proceso de evaluación que una empresa realiza antes de contratar a un nuevo proveedor, donde se investiga su historial ___________ para asegurar de que no tenga antecedentes de ________.",
     "opciones": ["Económico – deuda", "Policial – denuncias", "Financiero - deuda", "Financiero y reputación - soborno o corrupción"],
     "respuesta": "Financiero y reputación - soborno o corrupción",
     "tipo": "cerrada"},

    {"pregunta": "Parte interesada: persona u __________ que puede afectar o verse afectada por una _________ o actividad.",
     "opciones": ["Organización – decisión", "Grupo – decisión", "Organismo – compra", "Organización - mejora"],
     "respuesta": "Organización – decisión",
     "tipo": "cerrada"},

    {"pregunta": "Socio del negocio: parte _______ con la que la organización tiene, o planifica establecer alguna relación ______.",
     "opciones": ["Interna – comercial", "Interna – económica", "Externa – comercial", "Externa - económica"],
     "respuesta": "Externa – comercial",
     "tipo": "cerrada"},

    {"pregunta": "Matriz de riesgo: es una herramienta que permite identificar, ____________ los riesgos en un proceso u organización, facilitando la visualización y análisis de su impacto potencial.",
     "opciones": ["Mejorar y controlar", "Evaluar y priorizar", "Priorizar y ejecutar", "Controlar y ejecutar"],
     "respuesta": "Evaluar y priorizar",
     "tipo": "cerrada"},

    {"pregunta": "Órgano de Gobierno: Grupo u órgano que tiene la ________ final respecto de las actividades, la gobernanza y las políticas de una organización, y al cual la Alta Dirección informa y por el cual rinde cuentas.",
     "opciones": ["Dirección y control", "Operación", "Responsabilidad y autoridad", "Satisfacción"],
     "respuesta": "Responsabilidad y autoridad",
     "tipo": "cerrada"},

    {"pregunta": "Alta Dirección: Persona o grupo de personas que __________ una organización al más alto nivel, representada por nuestro Gerente General, Mario Gonzales",
     "opciones": ["Apoyan en", "Dirigen o controlan", "Reúne", "Manipula"],
     "respuesta": "Dirigen o controlan",
     "tipo": "cerrada"},

    {"pregunta": "¿Conoce algún acto de soborno reportado en la empresa?",
     "opciones": ["Sí", "No"],
     "respuesta": "No",
     "tipo": "cerrada"},

    {"pregunta": "¿Conoce alguna condición no prevista en su matriz de riesgo que no ha sido implementada?",
     "opciones": ["Desconozco", "Sí"],
     "respuesta": "Desconozco",
     "tipo": "cerrada"},

    {"pregunta": "¿Conoce de algún reporte de soborno denunciado por el cliente?",
     "opciones": ["Desconozco", "Sí"],
     "respuesta": "Desconozco",
     "tipo": "cerrada"},

    {"pregunta": "¿Cómo reduces la posibilidad de generar una condición de riesgo de soborno o cobro indebido?",
     "opciones": ["Nunca reunirme sin testigos", "No sé"],
     "respuesta": "Nunca reunirme sin testigos",
     "tipo": "cerrada"},

    {"pregunta": "¿Qué pasa si detecto que el conductor está pagando al policía para evitar una sanción de tránsito?",
     "opciones": ["Debo denunciarlo en la línea ética", "Nada"],
     "respuesta": "Debo denunciarlo en la línea ética",
     "tipo": "cerrada"},

    {"pregunta": "¿Qué pasa si el policía no redacta la constatación de acuerdo a lo encontrado en campo?",
     "opciones": ["Debo denunciarlo en la línea ética", "Nada"],
     "respuesta": "Debo denunciarlo en la línea ética",
     "tipo": "cerrada"},

    {"pregunta": "¿Qué haces si ves que una persona/empresa le ofrece dinero a un funcionario de LDS para que le compre un producto sin cumplir el proceso de licitación?",
     "opciones": ["Debo denunciarlo en la línea ética", "Nada"],
     "respuesta": "Debo denunciarlo en la línea ética",
     "tipo": "cerrada"},

    {"pregunta": "¿Qué pasa si tu primo ingresa como proveedor y tú eres el responsable de asignarle el trabajo?",
     "opciones": ["Aviso al oficial de cumplimiento", "Nada"],
     "respuesta": "Aviso al oficial de cumplimiento",
     "tipo": "cerrada"},

    {"pregunta": "Si por cualquier medio, te enteras que un proveedor que tiene contrato con LDS, tiene antecedentes o está cometiendo actos de soborno con otras empresas, ¿qué harías?",
     "opciones": ["Debo denunciarlo en la línea ética", "Nada"],
     "respuesta": "Debo denunciarlo en la línea ética",
     "tipo": "cerrada"},

    {"pregunta": "¿Qué haces si, durante la auditoría, te sientes nervioso y consideras que no puedes contestar adecuadamente?",
     "opciones": ["Me apoyo con el equipo consultor que acompaña al auditor", "Me arriesgo y contesto"],
     "respuesta": "Me apoyo con el equipo consultor que acompaña al auditor",
     "tipo": "cerrada"},

    {"pregunta": "¿Sabe usted si en una auditoría de Seguridad, Salud o Medio Ambiente se ha adulterado alguna información para evitar una multa?",
     "opciones": ["No", "Sí"],
     "respuesta": "No",
     "tipo": "cerrada"},

    {"pregunta": "¿Sabe usted si algún funcionario del municipio los ha extorsionado, conminado a una mejora en su barrio o solicitado un pago adelantado para no imponer una multa mayor?",
     "opciones": ["No", "Sí"],
     "respuesta": "No",
     "tipo": "cerrada"},

    {"pregunta": "¿Cómo te aseguras de que el contratista cumpla con el SGAS?",
     "opciones": ["a.Todos los contratistas fueron informados de nuestro SGAS",
                  "b.Según contrato, el contratista debe cumplir con todas las disposiciones impuestas por LDS",
                  "A y B"],
     "respuesta": "A y B",
     "tipo": "cerrada"},

    {"pregunta": "Si un amigo te pide que le reconectes el servicio sin autorización, cortado por deuda y te promete invitarte un almuerzo a fin de mes. ¿Es un conflicto de interés, soborno o falta a la debida diligencia?",
     "opciones": ["Soborno", "Conflicto de interés", "Falta a la debida diligencia", "Todos"],
     "respuesta": "Conflicto de interés",
     "tipo": "cerrada"},

    {"pregunta": "¿Quiénes conforman el comité de ética?",
     "opciones": ["Gerente de finanzas", "Gerente Legal", "Gerente de administración y recursos humanos", "Todos los nombrados"],
     "respuesta": "Todos los nombrados",
     "tipo": "cerrada"}
]

# Convertir la lista a un DataFrame
df_preguntas_y_respuestas = pd.DataFrame(preguntas_y_respuestas)

# =============
# 3. Funciones
# =============

# Función para limpiar la lista global de resultados antes de iniciar un nuevo test
def limpiar_resultados_globales():
    global todos_los_resultados
    todos_los_resultados = []  # Limpiar la lista antes de agregar nuevos resultados
    print("Lista de resultados globales limpiada.")

def inicializar_quizz(nombre):
    # Crear un estado nuevo para el participante si no existe
    estado_quizz_por_participante[nombre] = {
        "participante": nombre,
        "preguntas": random.sample(preguntas_y_respuestas, 10),  # Seleccionar 10 preguntas aleatorias sin repeticiones
        "indice_actual": 0,
        "puntaje": 0,
        "respuestas_usuario": [],
        "opciones_actuales": [],  # Reiniciar opciones actuales
    }
    # Mostrar la primera pregunta
    return mostrar_pregunta(nombre)

# Diccionario global para almacenar el estado de cada participante
estado_quizz_por_participante = {}

# Umbral de similitud para preguntas abiertas
UMBRAL_SIMILITUD = 50  # Ajustable según la tolerancia deseada

# Función para mostrar una pregunta
def mostrar_pregunta(nombre):
    estado_quizz = estado_quizz_por_participante[nombre]  # Obtener el estado del participante
    indice = estado_quizz["indice_actual"]
    if indice < len(estado_quizz["preguntas"]):  # Verificar si quedan preguntas por mostrar
        pregunta = estado_quizz["preguntas"][indice]

        # Numeración de la pregunta
        numero_pregunta = f"Pregunta {indice + 1}: "  # Numerar preguntas desde 1

        if pregunta["tipo"] == "cerrada":
            opciones = random.sample(pregunta["opciones"], len(pregunta["opciones"]))  # Desordenar opciones
            estado_quizz["opciones_actuales"] = opciones  # Guardar opciones desordenadas
            # Limpiar la selección previa para evitar que se marque por defecto
            return (
                gr.update(choices=opciones, label=numero_pregunta + pregunta["pregunta"], visible=True, value=None),  # No marcar opción por defecto
                gr.update(visible=False),  # Ocultar texto para preguntas abiertas
                gr.update(visible=True),  # Mostrar el botón "Responder"
                gr.update(visible=True)  # Mostrar el botón "Finalizar Quiz"
            )
        else:  # Pregunta abierta
            return (
                gr.update(visible=False),  # Ocultar opciones cerradas
                gr.update(visible=True, label=numero_pregunta + pregunta["pregunta"], value=""),  # Mostrar texto para preguntas abiertas con numeración
                gr.update(visible=True),  # Mostrar el botón "Responder"
                gr.update(visible=True)  # Mostrar el botón "Finalizar Quiz"
            )
    else:
        return mostrar_puntaje_final(nombre)

# Función para procesar la respuesta del usuario
def procesar_respuesta(respuesta_opcion, respuesta_texto, nombre):
    indice = estado_quizz_por_participante[nombre]["indice_actual"]
    pregunta = estado_quizz_por_participante[nombre]["preguntas"][indice]
    respuesta_correcta = pregunta["respuesta"]
    respuesta_usuario = respuesta_opcion if pregunta["tipo"] == "cerrada" else respuesta_texto.strip()

    # Validar respuesta según tipo
    es_correcta = False
    if pregunta["tipo"] == "cerrada" and respuesta_usuario in estado_quizz_por_participante[nombre]["opciones_actuales"]:
        es_correcta = respuesta_usuario == respuesta_correcta
    elif pregunta["tipo"] == "abierta":
        similitud = fuzz.ratio(respuesta_usuario.lower(), respuesta_correcta.lower())
        es_correcta = similitud >= UMBRAL_SIMILITUD

    # Guardar la respuesta del usuario en memoria, pero NO en el CSV aún
    estado_quizz_por_participante[nombre]["respuestas_usuario"].append({
        "participante": nombre,
        "pregunta": pregunta["pregunta"],
        "respuesta_correcta": respuesta_correcta,
        "respuesta_usuario": respuesta_usuario,
        "correcta": es_correcta
    })

    # Incrementar el puntaje si es correcta
    if es_correcta:
        estado_quizz_por_participante[nombre]["puntaje"] += 1

    # Incrementar el índice solo si se procesó correctamente
    estado_quizz_por_participante[nombre]["indice_actual"] += 1

    return mostrar_pregunta(nombre)

# Función para finalizar el quiz y mostrar el puntaje
def finalizar_quizz(nombre):
    # Llamamos a la función para guardar las respuestas solo cuando se finaliza el quiz
    guardar_resultados(nombre)

    return mostrar_puntaje_final(nombre)

# Función para mostrar el puntaje final con detalle de respuestas correctas e incorrectas
def mostrar_puntaje_final(nombre):
    estado_quizz = estado_quizz_por_participante[nombre]  # Obtener el estado del participante

    # Generar el desglose de aciertos y errores
    resultados_detalle = []
    for respuesta in estado_quizz["respuestas_usuario"]:
        acierto = "Correcta" if respuesta["correcta"] else "Incorrecta"
        resultados_detalle.append(f"{respuesta['pregunta']}\nTu respuesta: {respuesta['respuesta_usuario']}\nRespuesta correcta: {respuesta['respuesta_correcta']}\n{acierto}\n")

    resultados_detalle = "\n\n".join(resultados_detalle)

    return (
        gr.update(visible=False),  # Ocultar opciones cerradas
        gr.update(visible=False),  # Ocultar texto para preguntas abiertas
        gr.update(value=f"Quizz finalizado. Puntaje: {estado_quizz['puntaje']}/10.", visible=True),
        gr.update(value=resultados_detalle, visible=True),  # Mostrar el desglose de respuestas
        gr.update(visible=False)  # Ocultar el botón de respuesta
    )

# Función para guardar resultados en un archivo CSV
def guardar_resultados(nombre):
    # Añadir las respuestas del participante actual a la lista global
    estado_quizz = estado_quizz_por_participante[nombre]

    # Obtener la fecha actual
    fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Formato de fecha y hora: 2024-11-26 14:30:00

    # Crear el DataFrame con todas las respuestas del participante actual
    df = pd.DataFrame(estado_quizz["respuestas_usuario"])

    # Añadir la columna de fecha
    df['fecha_respuesta'] = fecha_actual

    # Verificar si el archivo CSV ya existe
    archivo_csv = "resultados.csv"
    file_exists = os.path.exists(archivo_csv)

    # Guardar las respuestas en el archivo CSV (si el archivo no existe, agrega encabezado)
    df.to_csv(archivo_csv, mode='a', header=not file_exists, index=False)

# Crear la interfaz con Gradio
with gr.Blocks() as interfaz:
    with gr.Row():
        gr.Markdown("# Quizz Interactivo: SGAS")
    with gr.Row():
        gr.Markdown("### Bienvenido. Por favor, ingresa tu nombre para iniciar el test.")
    with gr.Row():
        entrada_nombre = gr.Textbox(label="Nombre del Participante")
        boton_iniciar = gr.Button("🎯 Iniciar Test")
    with gr.Row():
        gr.Markdown("### Test consta de 10 preguntas. Por favor, haz clic en Finalizar Quiz después de responder la última pregunta .")
    with gr.Row():
        entrada_opciones = gr.Radio(choices=[], label="", visible=False)
        entrada_texto = gr.Textbox(label="", visible=False)
    with gr.Row():
        boton_responder = gr.Button("Responder", visible=False)
        boton_finalizar = gr.Button("Finalizar Quiz", visible=False)
    with gr.Row():
        resultado_quizz = gr.Textbox(label="Puntaje", visible=False)
        resultado_detalle = gr.Textbox(label="Resultados Detallados", visible=False)

    # Conexión de acciones
    boton_iniciar.click(inicializar_quizz, inputs=entrada_nombre, outputs=[entrada_opciones, entrada_texto, boton_responder, boton_finalizar])
    boton_responder.click(procesar_respuesta, inputs=[entrada_opciones, entrada_texto, entrada_nombre], outputs=[entrada_opciones, entrada_texto])
    boton_finalizar.click(finalizar_quizz, inputs=entrada_nombre, outputs=[entrada_opciones, entrada_texto, resultado_quizz, resultado_detalle, boton_responder])

# Lanzar la interfaz
interfaz.launch(share=True)
