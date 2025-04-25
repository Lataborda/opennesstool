import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

# ⚠️ Fix para numpy > 1.24
if not hasattr(np, 'Inf'):
    np.Inf = np.inf

# Título
st.title("Encuesta: Dimensiones de Apertura en la Innovación")
st.markdown("""
Esta herramienta permite evaluar cuatro dimensiones clave en iniciativas de innovación abierta:
- **Open Engagement**
- **Open Application & Adaptation**
- **Open Interaction Infrastructure**
- **Open Research**

Para cada dimensión se evalúan dos aspectos:
1. **Nivel de apertura** (1 = Bajo, 2 = Medio, 3 = Alto)
2. **Grado de estructuración/autonomía** (1 = Exógeno, 2 = Mixto, 3 = Endógeno)
""")

# Función para crear preguntas con radio buttons
def collect_scores(dim_name, questions, key_prefix):
    st.header(dim_name)
    scores = []
    for i, (question, options) in enumerate(questions):
        answer = st.radio(f"{i+1}. {question}", list(options.keys()), key=f"{key_prefix}_{i}")
        scores.append(options[answer])

    st.markdown("**¿Cómo se organizó esta dimensión?**")
    struct_labels = [
        "Las reglas y decisiones fueron impuestas por actores externos o jerárquicos",
        "Fue una mezcla entre reglas externas y mecanismos propios de coordinación",
        "La estructura fue generada de forma autónoma por los actores implicados"
    ]
    struct_dict = {
        struct_labels[0]: 3,
        struct_labels[1]: 2,
        struct_labels[2]: 1
    }
    selected_struct = st.radio("Grado de estructuración vs. autonomía", struct_labels, key=f"estructura_{key_prefix}")
    struct = struct_dict[selected_struct]

    return scores, struct

# Preguntas para cada dimensión
questions_collab = [
    ("¿Cuántos sectores distintos participaron activamente en la red del proyecto?", {
        "5 o más sectores": 3, "4 sectores": 2.5, "3 sectores": 2, "2 sectores": 1.5, "1 o ninguno": 1
    }),
    ("¿Cuántos actores estuvieron involucrados activamente en el proyecto?", {
        "Más de 5 actores": 3, "4 actores": 2.5, "3 actores": 2, "2 actores": 1.5, "1 actor o ninguno": 1
    }),
    ("¿Cómo describirías la gobernanza del proyecto?", {
        "Gobernanza clara y efectiva": 3, "Gobernanza mayormente efectiva": 2.5,
        "Moderada, con problemas": 2, "Poco clara o débil": 1.5, "Sin gobernanza": 1
    }),
    ("¿Cómo fue la escucha de ideas entre actores?", {
        "Escucha activa constante": 3, "Buena capacidad de escucha": 2.5,
        "Moderada": 2, "Escasa": 1.5, "Sin escucha": 1
    }),
    ("¿Cómo se adaptó el proyecto a cambios?", {
        "Alta adaptabilidad": 3, "Buena adaptación": 2.5, "Moderada": 2, "Limitada": 1.5, "Nula": 1
    }),
    ("¿Cómo respondió el proyecto a retos inesperados?", {
        "Respuesta inmediata y efectiva": 3, "Generalmente rápida": 2.5,
        "Moderada": 2, "Lenta y poco efectiva": 1.5, "Sin respuesta": 1
    })
]

questions_app = [
    ("¿Qué tan accesible es el conocimiento generado?", {
        "Libre y sin restricciones": 3, "Mayormente libre": 2.5, "Con restricciones significativas": 2,
        "Solo con permisos específicos": 1.5, "Cerrado": 1
    }),
    ("¿Se permite y facilita el uso, modificación o redistribución?", {
        "Sin restricciones": 3, "Con restricciones menores": 2.5, "Con restricciones importantes": 2,
        "Solo uso sin modificación": 1.5, "No se permite": 1
    }),
    ("¿Cómo participaron los actores en el diseño de soluciones?", {
        "Participación en todas las etapas": 3, "En diseño y validación": 2.5, "Solo validación": 2,
        "Colaboración mínima": 1.5, "Sin participación": 1
    })
]

questions_infra = [
    ("¿Qué nivel de confianza y transparencia hubo entre los socios?", {
        "Alta y total transparencia": 3, "Confianza generalmente alta": 2.5, "Moderada": 2,
        "Baja": 1.5, "Muy baja": 1
    }),
    ("¿Qué tan formalizadas estaban las reglas de comunicación?", {
        "Completamente formalizadas": 3, "Mayormente formalizadas": 2.5, "Parcialmente": 2,
        "Escasamente formalizadas": 1.5, "Sin reglas formales": 1
    }),
    ("¿Cómo eran los espacios de colaboración (digitales o físicos)?", {
        "Muy optimizados y digitalizados": 3, "Bien utilizados con algunas limitaciones": 2.5,
        "Contribución moderada y mixta": 2, "Informales y poco digitalizados": 1.5, "No facilitaban innovación": 1
    })
]

questions_research = [
    ("¿Qué tan estructurada fue la participación en la investigación?", {
        "Completamente estructurada y activa": 3, "Alta pero con limitaciones": 2.5,
        "Moderada con estructura parcial": 2, "Mínima con estructura débil": 1.5, "Sin participación": 1
    }),
    ("¿Cómo se reconocieron las contribuciones en el proceso de investigación?", {
        "Reconocimiento formal y explícito": 3, "Presente pero no sistemático": 2.5,
        "Ocasional": 2, "Mínimo": 1.5, "Sin reconocimiento": 1
    }),
    ("¿Existía una estrategia clara para la investigación abierta?", {
        "Completamente definida e implementada": 3, "Mayormente definida": 2.5, "Parcialmente desarrollada": 2,
        "Estrategia débil": 1.5, "Sin estrategia": 1
    })
]
st.divider()
scores_collab, struct_collab = collect_scores("1. Open Engagement ", questions_collab, "collab")
st.divider()
scores_app, struct_app = collect_scores("2. Open Application & Adaptation", questions_app, "app")
st.divider()
scores_infra, struct_infra = collect_scores("3. Open Interaction Infrastructure", questions_infra, "infra")
st.divider()
scores_research, struct_research = collect_scores("4. Open Research", questions_research, "research")

if st.button("Calcular puntuaciones"):
    def interpretar(score):
        if score >= 2.5:
            return "✅ Alto"
        elif score >= 2.0:
            return "🟡 Medio"
        elif score >= 1.5:
            return "🟠 Bajo"
        else:
            return "🔴 Cerrado"

    def interpretar_estructura(score):
        if score == 3:
            return "🟢 Endógeno (Autopoético)"
        elif score == 2:
            return "🟡 Mixto / Híbrido"
        else:
            return "🔴 Exógeno / Heterónomo"

    collab_score = sum(scores_collab)/len(scores_collab)
    app_score = sum(scores_app)/len(scores_app)
    infra_score = sum(scores_infra)/len(scores_infra)
    research_score = sum(scores_research)/len(scores_research)

    st.subheader("Resultados:",divider='blue')
    st.write(f"**Open Engagement **: {collab_score:.2f} → {interpretar(collab_score)} | Estructuración: {interpretar_estructura(struct_collab)}")
    st.write(f"**Open Application & Adaptation**: {app_score:.2f} → {interpretar(app_score)} | Estructuración: {interpretar_estructura(struct_app)}")
    st.write(f"**Open Interaction Infrastructure**: {infra_score:.2f} → {interpretar(infra_score)} | Estructuración: {interpretar_estructura(struct_infra)}")
    st.write(f"**Open Research**: {research_score:.2f} → {interpretar(research_score)} | Estructuración: {interpretar_estructura(struct_research)}")

    st.subheader("Matriz de Apertura vs. Regulación")
    fig, ax = plt.subplots(figsize=(8, 6))
    dim_positions = {
        "Engagement ": (collab_score, struct_collab),
        "Application": (app_score, struct_app),
        "Interaction": (infra_score, struct_infra),
        "Research": (research_score, struct_research)
    }

    offset_vectors = {
        "Engagement ": (-0.15, 0.15),
        "Application": (0.15, 0.15),
        "Interaction": (-0.15, -0.15),
        "Research": (0.15, -0.15)
    }

    for dim, (x, y) in dim_positions.items():
        ax.scatter(x, 4 - y, color="steelblue", s=200, edgecolors="black")
        dx, dy = offset_vectors[dim]
        ax.annotate(dim, xy=(x, 4 - y), xytext=(x + dx, 4 - y + dy),
                    arrowprops=dict(arrowstyle="->", lw=0.6), fontsize=9)

    ax.set_xlim(0.8, 3.2)
    ax.set_ylim(0.8, 3.2)
    ax.set_xticks([1, 2, 3])
    ax.set_xticklabels(["Bajo (1)", "Medio (2)", "Alto (3)"])
    ax.set_yticks([1, 2, 3])
    ax.set_yticklabels(["Más Regulador (1)", "Mixto (2)", "Más Autónomo  (3)"])
    ax.set_xlabel("Nivel de Apertura")
    ax.set_ylabel("Nivel de Regulación vs. Autonomía")
    ax.set_title("Matriz 2x2: Apertura vs. Regulación")
    ax.grid(True, linestyle="--", alpha=0.4)

    st.pyplot(fig)

st.divider()
st.markdown('*Copyright (C) 2025. CIRAD*')
st.caption('**Authors: Alejandro Taborda A., (latabordaa@unal.edu.co), Chloé Lecombe**')
st.image('aperto.png', width=250)
