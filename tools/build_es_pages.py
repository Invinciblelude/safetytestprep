#!/usr/bin/env python3
"""Generate Spanish /es/ HTML twins. Run from repo root or any cwd."""
from __future__ import annotations

import json
import os
import re
from pathlib import Path

ROOT = Path("/Users/invinciblelude/safetytestprep")
ES = ROOT / "es"
ORIGIN = "https://safetytestprep.com"


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def site_head(title: str, desc: str, canonical: str, extra: str = "", robots: str = "") -> str:
    robots_tag = f'  <meta name="robots" content="{robots}" />\n' if robots else ""
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{title}</title>
  <meta name="description" content="{desc}" />
{robots_tag}  <link rel="canonical" href="{canonical}" />
  <meta name="theme-color" content="#0b0f0c" />
  <link rel="icon" href="../img/favicon.svg" type="image/svg+xml" />
  <meta property="og:type" content="website" />
  <meta property="og:site_name" content="Safety Test Prep" />
  <meta property="og:locale" content="es_US" />
  <meta property="og:title" content="{title}" />
  <meta property="og:description" content="{desc}" />
  <meta property="og:url" content="{canonical}" />
  <meta property="og:image" content="{ORIGIN}/img/og-default.jpg" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{title}" />
  <meta name="twitter:description" content="{desc}" />
  <meta name="twitter:image" content="{ORIGIN}/img/og-default.jpg" />
  <link rel="stylesheet" href="../css/site.css" />
{extra}</head>
"""


def wrap_site(title, desc, slug, body, extra="", robots="", scripts=None):
    canonical = f"{ORIGIN}/es/{slug}" if slug else f"{ORIGIN}/es/"
    if scripts is None:
        scripts = ['<script src="../js/chrome.js"></script>']
    return (
        site_head(title, desc, canonical, extra, robots)
        + f"""<body>
  <a class="skip" href="#main">Saltar al contenido</a>
  <div class="wrap" id="main">
    <nav data-stp-nav></nav>
{body}
    <footer data-stp-footer></footer>
  </div>
  {chr(10).join(scripts)}
</body>
</html>
"""
    )


def lander_html(p: dict) -> str:
    folder = p["folder"]
    slug = p["slug"]
    url = f"{ORIGIN}/es/{folder}/{slug}"
    og = p.get("og", f"{ORIGIN}/img/og-default.jpg")
    n = p.get("n", 15)
    faqs = p["faqs"]
    covers = "".join(f"        <li>{item}</li>\n" for item in p["covers"])
    related = p["related"]
    faq_html = ""
    for q, a in faqs:
        faq_html += f"""      <details>
        <summary>{q}</summary>
        <p>{a}</p>
      </details>
"""
    ld = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Quiz",
                "name": p["h1"],
                "url": url,
                "educationalUse": "practice",
                "isAccessibleForFree": True,
                "numberOfQuestions": n,
                "inLanguage": "es",
                "provider": {"@type": "Organization", "name": "Safety Test Prep", "url": ORIGIN + "/"},
            },
            {
                "@type": "FAQPage",
                "mainEntity": [
                    {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub("<[^>]+>", "", a)}}
                    for q, a in faqs
                ],
            },
        ],
    }
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{p["title"]}</title>
  <meta name="description" content="{p["desc"]}" />
  <link rel="canonical" href="{url}" />
  <meta name="theme-color" content="#0b0f0c" />
  <link rel="icon" href="../../img/favicon.svg" type="image/svg+xml" />
  <meta property="og:type" content="website" />
  <meta property="og:site_name" content="Safety Test Prep" />
  <meta property="og:locale" content="es_US" />
  <meta property="og:title" content="{p["title"]}" />
  <meta property="og:description" content="{p["desc"]}" />
  <meta property="og:url" content="{url}" />
  <meta property="og:image" content="{og}" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:image" content="{og}" />
  <link rel="stylesheet" href="../../css/site.css" />
  <script type="application/ld+json">
  {json.dumps(ld, ensure_ascii=False)}
  </script>
</head>
<body>
  <div class="wrap">
    <nav data-stp-nav data-base="../"></nav>
    <p class="eyebrow">{p["eyebrow"]}</p>
    <h1>{p["h1"]}</h1>
    <p class="lede">{p["lede"]}</p>
    <p>{p["meta"]}</p>
    <p class="edu-bar">{p["edu"]} <a href="../disclaimer.html">Aviso legal</a> · <a href="../contact.html">¿Ve un error? Avísenos.</a></p>
    <p class="share-row">
      <a class="btn" href="index.html?quiz={p["quiz"]}">{p["cta"]}</a>
      <button type="button" class="btn ghost" data-stp-share data-url="{url}" data-title="{p["h1"]}" data-text="{p["share"]}">Compartir este cuestionario</button>
    </p>
    <section class="price">
      <h2>Qué cubre este cuestionario</h2>
      <ul class="cover-list">
{covers}      </ul>
    </section>
    <section class="faq" aria-labelledby="q-faq">
      <h2 id="q-faq">Preguntas frecuentes</h2>
{faq_html}    </section>
    <section class="related">
      <h2>Otros cuestionarios gratis</h2>
      <p>{related}</p>
    </section>
    <section class="price sources">
      <h2>Fuente oficial</h2>
      <p>{p["source"]}</p>
    </section>
    <footer data-stp-footer data-base="../"></footer>
  </div>
  <script src="../../js/chrome.js"></script>
</body>
</html>
"""


def apply_pairs(text: str, pairs: list[tuple[str, str]]) -> str:
    for a, b in pairs:
        text = text.replace(a, b)
    return text


def lab_from_english(en_path: Path, out_path: Path, lab: str, pairs: list[tuple[str, str]]) -> None:
    html = en_path.read_text(encoding="utf-8")
    html = html.replace('<html lang="en">', '<html lang="es">')
    html = html.replace('og:locale" content="en_US"', 'og:locale" content="es_US"')
    html = html.replace('"inLanguage":"en"', '"inLanguage":"es"')
    html = html.replace("https://safetytestprep.com/" + lab + "/", f"https://safetytestprep.com/es/{lab}/")
    html = html.replace('href="../img/', 'href="../../img/')
    html = html.replace('href="css/app.css"', f'href="../../{lab}/css/app.css"')
    html = html.replace('href="../disclaimer.html"', 'href="../disclaimer.html"')
    html = html.replace('src="js/questions.js', f'src="../../{lab}/js/es/questions.js')
    html = html.replace('src="js/questions-set2.js"', f'src="../../{lab}/js/es/questions-set2.js"')
    html = html.replace('src="js/questions-set3.js"', f'src="../../{lab}/js/es/questions-set3.js"')
    html = html.replace('src="js/questions-set4.js"', f'src="../../{lab}/js/es/questions-set4.js"')
    html = html.replace('src="js/questions-set5.js"', f'src="../../{lab}/js/es/questions-set5.js"')
    html = html.replace('src="js/flashcards.js"', f'src="../../{lab}/js/es/flashcards.js"')
    html = html.replace('src="../js/config.js"', 'src="../../js/config.js"')
    html = html.replace('src="../js/i18n.js"', 'src="../../js/i18n.js"')
    html = html.replace('src="../js/pay.js"', 'src="../../js/pay.js"')
    html = html.replace('src="js/support.js"', f'src="../../{lab}/js/support.js"')
    html = html.replace('src="js/app.js', f'src="../../{lab}/js/app.js')
    html = html.replace('src="../js/chrome.js"', 'src="../../js/chrome.js"')
    html = apply_pairs(html, pairs)
    write(out_path, html)


OSHA_PAIRS = [
    ("Free OSHA 10 &amp; 30 Practice Test (808 Questions)", "Examen de práctica OSHA 10 y 30 gratis (808 preguntas)"),
    ("Free OSHA 10 and OSHA 30 practice tests and flashcards. 808 original questions on 29 CFR 1910 and 1926. Not an official DOL Outreach card.",
     "Cuestionarios y tarjetas de práctica OSHA 10 y OSHA 30. 808 preguntas originales sobre 29 CFR 1910 y 1926. No es una tarjeta oficial de Outreach del DOL."),
    ("Free OSHA 10 and OSHA 30 practice tests and flashcards. 808 original questions. Not an official DOL Outreach card.",
     "Cuestionarios y tarjetas de práctica OSHA 10 y OSHA 30. 808 preguntas originales. No es una tarjeta oficial de Outreach del DOL."),
    ("Free OSHA 10 and OSHA 30 Practice Test", "Examen de práctica OSHA 10 y OSHA 30 gratis"),
    ("Is this an official OSHA 10 or OSHA 30 test?", "¿Este es un examen oficial de OSHA 10 o OSHA 30?"),
    ("No. This lab is independent educational practice. Outreach cards are issued only by authorized trainers after the required course hours.",
     "No. Este laboratorio es práctica educativa independiente. Las tarjetas de Outreach solo las emiten instructores autorizados después de las horas del curso."),
    ("How many OSHA practice questions are included?", "¿Cuántas preguntas de práctica OSHA incluye?"),
    ("808 original multiple-choice questions and 143 flashcards covering construction and general-industry topics.",
     "808 preguntas originales de opción múltiple y 143 tarjetas sobre construcción e industria general."),
    ("OSHA Practice Lab", "Laboratorio de práctica OSHA"),
    ("OSHA-topic study quizzes. Not official DOL questions. A 10- or 30-hour card can only be issued by an authorized Outreach trainer.",
     "Cuestionarios de estudio sobre temas de OSHA. No son preguntas oficiales del DOL. Una tarjeta de 10 o 30 horas solo la emite un instructor autorizado de Outreach."),
    ("Educational use only. Not OSHA Outreach training, a completion card, or a guaranteed pass.",
     "Solo uso educativo. No es capacitación OSHA Outreach, una tarjeta de finalización ni un aprobado garantizado."),
    ("See an error?", "¿Ve un error?"),
    (">Home</button>", ">Inicio</button>"),
    (">Quiz</button>", ">Cuestionario</button>"),
    (">Flashcards</button>", ">Tarjetas</button>"),
    (">Question bank</button>", ">Banco de preguntas</button>"),
    ("OSHA-topic practice quizzes", "Cuestionarios de práctica sobre temas de OSHA"),
    ("Review common construction and general-industry safety concepts with original multiple-choice questions and flashcards.",
     "Repase conceptos comunes de seguridad en construcción e industria general con preguntas originales de opción múltiple y tarjetas."),
    ("808 practice questions · 143 flashcards · 33 topics<br>Last reviewed: August 31, 2026",
     "808 preguntas de práctica · 143 tarjetas · 33 temas<br>Última revisión: 31 de agosto de 2026"),
    ("Start a 10-Question Quiz", "Empezar un cuestionario de 10 preguntas"),
    ("Browse Question Bank", "Ver el banco de preguntas"),
    ("Start with 10 randomized questions, review each explanation, and continue when ready.",
     "Empiece con 10 preguntas al azar, lea cada explicación y continúe cuando esté listo."),
    ("Independent educational practice only. This lab is not OSHA Outreach training, does not issue a completion card, and does not guarantee an exam result. For current Outreach information, visit the",
     "Solo práctica educativa independiente. Este laboratorio no es capacitación OSHA Outreach, no emite una tarjeta de finalización y no garantiza un resultado de examen. Para información actual de Outreach, visite el"),
    ("official OSHA Outreach Training Program", "Programa oficial de capacitación OSHA Outreach"),
    ("OSHA 10 Construction", "OSHA 10 Construcción"),
    ("OSHA 10 General Industry", "OSHA 10 Industria general"),
    ("OSHA 30 Construction", "OSHA 30 Construcción"),
    ("OSHA 30 General Industry", "OSHA 30 Industria general"),
    ("25-question mock", "Simulacro de 25 preguntas"),
    ("50-question mock", "Simulacro de 50 preguntas"),
    ("40-question standards mix", "Mezcla de normas de 40 preguntas"),
    ("Focus Four, falls, ladders, trenches, electrical, PPE, HazCom, tools. 18 to pass.",
     "Focus Four, caídas, escaleras, zanjas, electricidad, EPP, HazCom, herramientas. 18 para aprobar."),
    ("Walking-working, fire/EAP, electrical, HazCom, LOTO, machine guarding. 18 to pass.",
     "Superficies de trabajo, incendio/EAP, electricidad, HazCom, LOTO, protección de máquinas. 18 para aprobar."),
    ("Adds steel, concrete, welding, demolition, aerial lifts, vehicles, recordkeeping. 35 to pass.",
     "Suma acero, concreto, soldadura, demolición, plataformas aéreas, vehículos y registros. 35 para aprobar."),
    ("Adds confined space, respirators, BBP, forklifts, PSM, first aid. 35 to pass.",
     "Suma espacios confinados, respiradores, BBP, montacargas, PSM y primeros auxilios. 35 para aprobar."),
    ("Recordkeeping, walking-working, LOTO, HazCom, guarding, confined space, PSM.",
     "Registros, superficies de trabajo, LOTO, HazCom, protección, espacios confinados, PSM."),
    ("143 flashcards", "143 tarjetas"),
    ("Key numbers, worker rights, jobsite rules, health. Flip, mark known, shuffle.",
     "Cifras clave, derechos del trabajador, reglas de obra, salud. Voltee, marque lo que ya sabe, mezcle."),
    ("Topic banks", "Bancos por tema"),
    ("Each card is a quiz drawn from that category. Browse the full bank to study with answers showing.",
     "Cada tarjeta es un cuestionario de esa categoría. Vea el banco completo para estudiar con las respuestas visibles."),
    ("Introduction to OSHA", "Introducción a OSHA"),
    ("Rights, inspections, citations", "Derechos, inspecciones, citaciones"),
    ("Falls, struck-by, caught-in, electrocution", "Caídas, golpes, atrapamientos, electrocución"),
    ("Fall Protection", "Protección contra caídas"),
    ("15 questions · 6-foot rule, PFAS, guardrails", "15 preguntas · regla de 6 pies, PFAS, barandales"),
    ("Ladders &amp; Scaffolds", "Escaleras y andamios"),
    ("4:1 ratio, inspections, 10-foot rule", "Relación 4:1, inspecciones, regla de 10 pies"),
    ("Stairways", "Escaleras fijas"),
    ("Subpart X, landings, rails", "Subparte X, descansos, pasamanos"),
    ("Excavation &amp; Trenching", "Excavación y zanjas"),
    ("5-foot rule, soil types, spoil", "Regla de 5 pies, tipos de suelo, escombro"),
    ("Electrical Safety", "Seguridad eléctrica"),
    ("10-foot rule, GFCI, 50 volts", "Regla de 10 pies, GFCI, 50 voltios"),
    ("Hierarchy, payment, ANSI ratings", "Jerarquía, pago, clasificaciones ANSI"),
    ("Hazard Communication", "Comunicación de peligros"),
    ("Lockout / Tagout", "Bloqueo / etiquetado"),
    ("Energy control, verify, group LOTO", "Control de energía, verificar, LOTO grupal"),
    ("Cranes &amp; Rigging", "Grúas y aparejos"),
    ("Suspended loads, load charts", "Cargas suspendidas, tablas de carga"),
    ("Hand &amp; Power Tools", "Herramientas manuales y eléctricas"),
    ("Guards, powder-actuated, grinders", "Guardas, accionadas por pólvora, esmeriles"),
    ("Health Hazards", "Peligros para la salud"),
    ("Silica, lead, heat, CO, asbestos", "Sílice, plomo, calor, CO, asbesto"),
    ("Fire &amp; EAP", "Incendio y EAP"),
    ("PASS, classes, exits, hot work", "PASS, clases, salidas, trabajo en caliente"),
    ("Walking-Working Surfaces", "Superficies de trabajo"),
    ("Housekeeping, holes, GI 4-foot rule", "Orden y limpieza, huecos, regla de 4 pies en industria general"),
    ("Confined Spaces", "Espacios confinados"),
    ("Permit, atmosphere, rescue", "Permiso, atmósfera, rescate"),
    ("Forklifts / PIT", "Montacargas / PIT"),
    ("1910.178 training, stability, docks", "Capacitación 1910.178, estabilidad, muelles"),
    ("Bloodborne Pathogens", "Patógenos sanguíneos"),
    ("Welding &amp; Hot Work", "Soldadura y trabajo en caliente"),
    ("Cylinders, fire watch, fumes", "Cilindros, vigilancia de incendio, humos"),
    ("Steel Erection", "Montaje de acero"),
    ("Subpart R, 15-foot rule, connectors", "Subparte R, regla de 15 pies, conectores"),
    ("Concrete &amp; Masonry", "Concreto y mampostería"),
    ("Impalement, shoring, LAZ", "Empalamiento, apuntalamiento, LAZ"),
    ("Respiratory Protection", "Protección respiratoria"),
    ("1910.134, fit test, APF", "1910.134, prueba de ajuste, APF"),
    ("Machine Guarding", "Protección de máquinas"),
    ("Point of operation, saws, interlocks", "Punto de operación, sierras, enclavamientos"),
    ("Aerial Lifts / MEWPs", "Plataformas aéreas / MEWP"),
    ("Harness, capacity, power lines", "Arnés, capacidad, líneas eléctricas"),
    ("Demolition", "Demolición"),
    ("Engineering survey, utilities, chutes", "Estudio de ingeniería, servicios, tolvas"),
    ("Recordkeeping", "Registros"),
    ("300 / 300A / 301, recordable vs first aid", "300 / 300A / 301, registrable vs primeros auxilios"),
    ("Medical &amp; First Aid", "Médico y primeros auxilios"),
    ("Eyewash, kits, 1926.50", "Lavaojos, botiquines, 1926.50"),
    ("Process Safety (PSM)", "Seguridad de procesos (PSM)"),
    ("Sanitation", "Saneamiento"),
    ("Water, toilets, hygiene facilities", "Agua, sanitarios, higiene"),
    ("Signs &amp; Barricades", "Señales y barricadas"),
    ("Danger/Caution, MUTCD, flaggers", "Peligro/Precaución, MUTCD, bandereros"),
    ("Site Vehicles", "Vehículos de obra"),
    ("Backup alarms, ROPS, haul roads", "Alarmas de reversa, ROPS, caminos de acarreo"),
    ("Ergonomics", "Ergonomía"),
    ("NIOSH lift, MSDs, vibration", "Levantamiento NIOSH, TME, vibración"),
    ("100-question marathon", "Maratón de 100 preguntas"),
    ("All 33 categories mixed", "Las 33 categorías mezcladas"),
    ("Browse all questions", "Ver todas las preguntas"),
    ("Full bank with answers", "Banco completo con respuestas"),
    ("Best study order", "Mejor orden de estudio"),
    ("Learn worker rights and employer duties (Introduction to OSHA), then the construction Focus Four.",
     "Aprenda los derechos del trabajador y deberes del empleador (Introducción a OSHA), luego el Focus Four de construcción."),
    ("Drill Fall Protection, Excavation, Electrical, and PPE until you consistently score 80% or higher.",
     "Practique protección contra caídas, excavación, electricidad y EPP hasta obtener 80% o más de forma constante."),
    ("Add LOTO, HazCom, health hazards, and confined spaces for OSHA 30 depth.",
     "Sume LOTO, HazCom, peligros para la salud y espacios confinados para la profundidad de OSHA 30."),
    ("Take the 25- and 50-question mocks, then review every missed item in the question bank.",
     "Haga los simulacros de 25 y 50 preguntas y luego revise cada acierto fallado en el banco."),
    ("Official sources:", "Fuentes oficiales:"),
    ("Last reviewed August 31, 2026.", "Última revisión: 31 de agosto de 2026."),
    ("See an error? Tell us.", "¿Ve un error? Avísenos."),
    ("Common questions", "Preguntas frecuentes"),
    ("Is this an official OSHA 10 test?", "¿Este es un examen oficial de OSHA 10?"),
    ("No. Original practice only. It does not issue a card and does not copy DOL exams.",
     "No. Solo práctica original. No emite una tarjeta y no copia exámenes del DOL."),
    ("How do I start?", "¿Cómo empiezo?"),
    ("Take the 10-question mix, then drill", "Haga la mezcla de 10 preguntas y luego practique"),
    ("fall protection", "protección contra caídas"),
    ("until you score 80% or higher.", "hasta obtener 80% o más."),
    ("Question 1", "Pregunta 1"),
    (">Next</button>", ">Siguiente</button>"),
    (">Quit</button>", ">Salir</button>"),
    ("id=\"result-kicker\">Result", "id=\"result-kicker\">Resultado"),
    (">Retake</button>", ">Repetir</button>"),
    (">Review missed</button>", ">Repasar falladas</button>"),
    (">Try another 10-question quiz</button>", ">Probar otro cuestionario de 10</button>"),
    (">Home</button>", ">Inicio</button>"),
    (">Flashcards</p>", ">Tarjetas</p>"),
    (">All</button>", ">Todas</button>"),
    (">Key numbers</button>", ">Cifras clave</button>"),
    (">Rights &amp; OSHA</button>", ">Derechos y OSHA</button>"),
    (">Jobsite</button>", ">Obra</button>"),
    (">Health</button>", ">Salud</button>"),
    (">Still learning</button>", ">Sigo aprendiendo</button>"),
    ('aria-label="Flip card"', 'aria-label="Voltear tarjeta"'),
    ("Tap to reveal", "Toque para ver la respuesta"),
    (">Got it</button>", ">Ya lo sé</button>"),
    (">Skip</button>", ">Saltar</button>"),
    ("Full question bank", "Banco completo de preguntas"),
    ("All practice items", "Todos los ítems de práctica"),
    ("Disclaimer", "Aviso legal"),
]

CDL_PAIRS = [
    ("Free California Class A CDL Practice Test", "Examen de práctica CDL Clase A de California gratis"),
    ("Free California Class A CDL practice tests: General Knowledge, Air Brakes, Combination Vehicles, endorsements, and pre-trip. Not official DMV questions.",
     "Exámenes de práctica CDL Clase A de California: conocimientos generales, frenos de aire, vehículos combinados, endosos e inspección previa. No son preguntas oficiales del DMV."),
    ("Are these official California DMV CDL questions?", "¿Estas son preguntas oficiales del DMV de California?"),
    ("No. These are original practice items modeled on the public California Commercial Driver Handbook. Only the DMV issues a CDL.",
     "No. Son ítems de práctica originales basados en el manual público de conductores comerciales de California. Solo el DMV emite una CDL."),
    ("Which CDL tests can I practice here?", "¿Qué exámenes de CDL puedo practicar aquí?"),
    ("General Knowledge, Air Brakes, Combination Vehicles, pre-trip inspection, and endorsement topics including doubles, tanker, HazMat, and passenger.",
     "Conocimientos generales, frenos de aire, vehículos combinados, inspección previa y temas de endoso: dobles, tanques, HazMat y pasajeros."),
    ("CDL Practice Lab", "Laboratorio de práctica CDL"),
    ("California CDL practice resources modeled on the public Commercial Driver Handbook. Not official DMV questions. Only the DMV issues a CDL.",
     "Recursos de práctica de CDL de California basados en el manual público. No son preguntas oficiales del DMV. Solo el DMV emite una CDL."),
    ("Educational use only. Not a DMV test, a license, or a guaranteed pass.",
     "Solo uso educativo. No es un examen del DMV, una licencia ni un aprobado garantizado."),
    (">Home</button>", ">Inicio</button>"),
    (">Quiz</button>", ">Cuestionario</button>"),
    (">Flashcards</button>", ">Tarjetas</button>"),
    (">Question bank</button>", ">Banco de preguntas</button>"),
    ("California CDL knowledge practice", "Práctica de conocimientos de CDL de California"),
    ("Review commercial-driver knowledge topics with original handbook-based questions. This is study help, not the DMV.",
     "Repase temas de conocimientos para conductores comerciales con preguntas originales basadas en el manual. Esto es ayuda de estudio, no el DMV."),
    ("General Knowledge · Air Brakes · Combination Vehicles<br>Last reviewed: August 31, 2026",
     "Conocimientos generales · Frenos de aire · Vehículos combinados<br>Última revisión: 31 de agosto de 2026"),
    ("Start a 10-Question Quiz", "Empezar un cuestionario de 10 preguntas"),
    ("Browse Question Bank", "Ver el banco de preguntas"),
    ("Start with 10 randomized questions, review each explanation, and continue when ready.",
     "Empiece con 10 preguntas al azar, lea cada explicación y continúe cuando esté listo."),
    ("Independent educational practice only. Only the California DMV issues a CDL. Confirm current requirements in the",
     "Solo práctica educativa independiente. Solo el DMV de California emite una CDL. Confirme los requisitos actuales en el"),
    ("California Commercial Driver Handbook", "Manual de conductores comerciales de California"),
    ("50-question mock exam", "Simulacro de 50 preguntas"),
    ("All 7 categories: General Knowledge, Air Brakes, Combination, Doubles/Triples, Tanker, HazMat, Passenger. 80% to pass.",
     "Las 7 categorías: conocimientos generales, frenos de aire, combinación, dobles/triples, tanques, HazMat, pasajeros. 80% para aprobar."),
    ("General Knowledge · 50", "Conocimientos generales · 50"),
    ("Safe driving, space, cargo, emergencies, inspections, California commercial rules. 40 correct to pass.",
     "Conducción segura, espacio, carga, emergencias, inspecciones, reglas comerciales de California. 40 correctas para aprobar."),
    ("Air Brakes · 25", "Frenos de aire · 25"),
    ("System parts, pressures, leak tests, spring brakes, ABS, inspections. 20 correct to pass.",
     "Partes del sistema, presiones, pruebas de fugas, frenos de resorte, ABS, inspecciones. 20 correctas para aprobar."),
    ("Combination Vehicles · 20", "Vehículos combinados · 20"),
    ("Fifth wheel, coupling, air lines, off-tracking, rollovers, jackknife. 16 correct to pass.",
     "Quinta rueda, acoplamiento, líneas de aire, desvío, volcaduras, tijera. 16 correctas para aprobar."),
    ("Pre-Trip Inspection · 20", "Inspección previa · 20"),
    ("Engine, steering, suspension, brakes, coupling, in-cab air-brake tests.",
     "Motor, dirección, suspensión, frenos, acoplamiento, pruebas de frenos de aire en cabina."),
    ("110 flashcards", "110 tarjetas"),
    ("Air brake numbers and coupling/uncoupling steps. Flip, mark known, shuffle.",
     "Cifras de frenos de aire y pasos de acoplar/desacoplar. Voltee, marque lo que ya sabe, mezcle."),
    ("Doubles / Triples", "Dobles / triples"),
    ("T endorsement", "Endoso T"),
    ("Tank Vehicles", "Vehículos tanque"),
    ("N endorsement", "Endoso N"),
    ("Hazardous Materials", "Materiales peligrosos"),
    ("H endorsement", "Endoso H"),
    ("Passenger", "Pasajeros"),
    ("P endorsement", "Endoso P"),
    ("GK full bank", "Banco completo de conocimientos generales"),
    ("Every general-knowledge item", "Todos los ítems de conocimientos generales"),
    ("Air Brakes full bank", "Banco completo de frenos de aire"),
    ("Every air-brake item", "Todos los ítems de frenos de aire"),
    ("Combination full bank", "Banco completo de combinación"),
    ("Every combination item", "Todos los ítems de combinación"),
    ("Pre-Trip full bank", "Banco completo de inspección previa"),
    ("Every inspection item", "Todos los ítems de inspección"),
    ("Browse all questions", "Ver todas las preguntas"),
    ("Full bank with answers", "Banco completo con respuestas"),
    ("Best free study order", "Mejor orden de estudio gratis"),
    ("Read California CDL handbook sections for General Knowledge, Air Brakes, and Combination Vehicles.",
     "Lea las secciones del manual de CDL de California de conocimientos generales, frenos de aire y vehículos combinados."),
    ("Take the subject tests here until you consistently score 90% or higher.",
     "Haga las pruebas por materia aquí hasta obtener 90% o más de forma constante."),
    ("Write down every missed topic, not just the missed question.",
     "Anote cada tema fallado, no solo la pregunta."),
    ("Drill the 50-question mock and the flashcards before permit day.",
     "Practique el simulacro de 50 preguntas y las tarjetas antes del día del permiso."),
    ("Official sources:", "Fuentes oficiales:"),
    ("Last reviewed August 31, 2026.", "Última revisión: 31 de agosto de 2026."),
    ("See an error? Tell us.", "¿Ve un error? Avísenos."),
    ("Common questions", "Preguntas frecuentes"),
    ("Are these official DMV questions?", "¿Estas son preguntas oficiales del DMV?"),
    ("No. Original handbook-style practice. Only the California DMV issues a CDL.",
     "No. Práctica original al estilo del manual. Solo el DMV de California emite una CDL."),
    ("What should I study first?", "¿Qué debo estudiar primero?"),
    ("Question 1", "Pregunta 1"),
    (">Next</button>", ">Siguiente</button>"),
    (">Quit</button>", ">Salir</button>"),
    ("id=\"result-kicker\">Result", "id=\"result-kicker\">Resultado"),
    (">Retake</button>", ">Repetir</button>"),
    (">Review missed</button>", ">Repasar falladas</button>"),
    (">Home</button>", ">Inicio</button>"),
    (">Flashcards</p>", ">Tarjetas</p>"),
    (">All</button>", ">Todas</button>"),
    (">Air Brakes</button>", ">Frenos de aire</button>"),
    (">Coupling</button>", ">Acoplamiento</button>"),
    (">Still learning</button>", ">Sigo aprendiendo</button>"),
    ('aria-label="Flip card"', 'aria-label="Voltear tarjeta"'),
    ("Tap to reveal", "Toque para ver la respuesta"),
    (">Got it</button>", ">Ya lo sé</button>"),
    (">Skip</button>", ">Saltar</button>"),
    ("Full question bank", "Banco completo de preguntas"),
    ("All practice items", "Todos los ítems de práctica"),
    ("Disclaimer", "Aviso legal"),
    ("See an error?", "¿Ve un error?"),
]

CPR_PAIRS = [
    ("Free CPR &amp; AED Practice Test (435 Questions)", "Examen de práctica de RCP y DEA gratis (435 preguntas)"),
    ("Free CPR, AED, choking, and first aid practice tests and flashcards. 435 original questions modeled on AHA BLS and Heartsaver. Not an official certification.",
     "Cuestionarios y tarjetas de RCP, DEA, atragantamiento y primeros auxilios. 435 preguntas originales basadas en AHA BLS y Heartsaver. No es una certificación oficial."),
    ("Free CPR, AED, choking, and first aid practice tests. Not an official certification.",
     "Cuestionarios de RCP, DEA, atragantamiento y primeros auxilios. No es una certificación oficial."),
    ("Free CPR and AED Practice Test", "Examen de práctica de RCP y DEA gratis"),
    ("Does this CPR practice test certify me?", "¿Este examen de práctica de RCP me certifica?"),
    ("No. A CPR/AED card requires an authorized instructor and a skills session. This is knowledge review only, not medical advice.",
     "No. Una tarjeta de RCP/DEA requiere un instructor autorizado y una sesión de destrezas. Esto es solo repaso de conocimientos, no consejo médico."),
    ("How many CPR/AED questions are included?", "¿Cuántas preguntas de RCP/DEA incluye?"),
    ("435 original questions and 115 flashcards covering adult, child, and infant CPR, AED use, choking, and first aid.",
     "435 preguntas originales y 115 tarjetas sobre RCP en adultos, niños y lactantes, uso del DEA, atragantamiento y primeros auxilios."),
    ("CPR &amp; AED Practice Lab", "Laboratorio de práctica RCP y DEA"),
    ("CPR/AED knowledge review modeled on publicly taught BLS and Heartsaver science. Not official AHA or Red Cross questions. A card requires an in-person skills session with an authorized instructor.",
     "Repaso de RCP/DEA basado en la ciencia pública de BLS y Heartsaver. No son preguntas oficiales de AHA ni de la Cruz Roja. Una tarjeta requiere una sesión de destrezas en persona con un instructor autorizado."),
    ("Educational use only. Not medical advice, not a certification course, and not a guaranteed pass. In an emergency, call 911.",
     "Solo uso educativo. No es consejo médico, ni un curso de certificación, ni un aprobado garantizado. En una emergencia, llame al 911."),
    (">Home</button>", ">Inicio</button>"),
    (">Quiz</button>", ">Cuestionario</button>"),
    (">Flashcards</button>", ">Tarjetas</button>"),
    (">Question bank</button>", ">Banco de preguntas</button>"),
    ("CPR/AED knowledge review", "Repaso de conocimientos de RCP/DEA"),
    ("Refresh core emergency-response and CPR/AED knowledge with original practice questions and flashcards before a skills class.",
     "Repase conocimientos básicos de respuesta a emergencias y RCP/DEA con preguntas originales y tarjetas antes de una clase de destrezas."),
    ("435 practice questions · 115 flashcards · 12 topics<br>Last reviewed: August 31, 2026",
     "435 preguntas de práctica · 115 tarjetas · 12 temas<br>Última revisión: 31 de agosto de 2026"),
    ("Start a 10-Question Quiz", "Empezar un cuestionario de 10 preguntas"),
    ("Browse Question Bank", "Ver el banco de preguntas"),
    ("Start with 10 randomized questions, review each explanation, and continue when ready.",
     "Empiece con 10 preguntas al azar, lea cada explicación y continúe cuando esté listo."),
    ("Independent educational practice only. This is not medical advice, not a certification course, and does not issue a card. In an emergency, call 911.",
     "Solo práctica educativa independiente. Esto no es consejo médico, ni un curso de certificación, y no emite una tarjeta. En una emergencia, llame al 911."),
    ("Heartsaver CPR AED", "Heartsaver RCP DEA"),
    ("25-question mock", "Simulacro de 25 preguntas"),
    ("Adult CPR, AED, rescue breaths, choking. 21 to pass (84%).",
     "RCP en adultos, DEA, ventilaciones, atragantamiento. 21 para aprobar (84%)."),
    ("BLS Provider", "Proveedor BLS"),
    ("Team CPR, bag-mask, peds ratios, advanced airway. 21 to pass.",
     "RCP en equipo, bolsa-mascarilla, relaciones pediátricas, vía aérea avanzada. 21 para aprobar."),
    ("Heartsaver First Aid CPR AED", "Heartsaver primeros auxilios RCP DEA"),
    ("35-question mock", "Simulacro de 35 preguntas"),
    ("Adds bleeding, stroke, heart attack, shock, anaphylaxis. 25 to pass.",
     "Suma hemorragia, accidente cerebrovascular, infarto, choque, anafilaxia. 25 para aprobar."),
    ("Pediatric BLS", "BLS pediátrico"),
    ("Child and infant CPR, 15:2, choking, breaths. 21 to pass.",
     "RCP en niños y lactantes, 15:2, atragantamiento, ventilaciones. 21 para aprobar."),
    ("AED skills drill", "Práctica de destrezas DEA"),
    ("20-question mock", "Simulacro de 20 preguntas"),
    ("Pads, shock, special situations, pad placement. 14 to pass.",
     "Parches, descarga, situaciones especiales, colocación. 14 para aprobar."),
    ("115 flashcards", "115 tarjetas"),
    ("Rates, depths, ratios, sequences. Flip, mark known, shuffle.",
     "Frecuencias, profundidades, relaciones, secuencias. Voltee, marque lo que ya sabe, mezcle."),
    ("Topic banks", "Bancos por tema"),
    ("Each card is a quiz drawn from that category. Browse the full bank to study with answers showing.",
     "Cada tarjeta es un cuestionario de esa categoría. Vea el banco completo para estudiar con las respuestas visibles."),
    ("Chain of Survival", "Cadena de supervivencia"),
    ("Scene, 911, recognition", "Escena, 911, reconocimiento"),
    ("Adult CPR", "RCP en adultos"),
    ("Rate, depth, 30:2, recoil", "Frecuencia, profundidad, 30:2, recoíl"),
    (">AED</strong>", ">DEA</strong>"),
    ("Pads, shock, special cases", "Parches, descarga, casos especiales"),
    ("Child CPR", "RCP en niños"),
    ("1 year to puberty", "1 año hasta la pubertad"),
    ("Infant CPR", "RCP en lactantes"),
    ("Thumbs, brachial, 1.5 in", "Pulgares, braquial, 1.5 pulg"),
    ("Airway &amp; breaths", "Vía aérea y ventilaciones"),
    ("Mask, bag, pulse present", "Mascarilla, bolsa, pulso presente"),
    ("Choking / FBAO", "Atragantamiento / OVACE"),
    ("Adult, child, infant", "Adulto, niño, lactante"),
    ("Team CPR", "RCP en equipo"),
    ("Roles, CCF, feedback", "Roles, CCF, retroalimentación"),
    ("Special situations", "Situaciones especiales"),
    ("Opioid, drowning, pregnancy", "Opioides, ahogamiento, embarazo"),
    ("First aid", "Primeros auxilios"),
    ("Bleeding, stroke, shock", "Hemorragia, ACV, choque"),
    ("PPE &amp; BBP", "EPP y BBP"),
    ("Gloves, barriers, exposure", "Guantes, barreras, exposición"),
    ("Legal &amp; consent", "Legal y consentimiento"),
    ("Good Samaritan, when to stop", "Buen samaritano, cuándo detenerse"),
    ("100-question marathon", "Maratón de 100 preguntas"),
    ("All 12 categories mixed", "Las 12 categorías mezcladas"),
    ("Browse all questions", "Ver todas las preguntas"),
    ("Full bank with answers", "Banco completo con respuestas"),
    ("Study materials — numbers to memorize", "Material de estudio — cifras para memorizar"),
    ("High-quality adult CPR", "RCP de alta calidad en adultos"),
    ("Rate 100–120 compressions per minute", "Frecuencia 100–120 compresiones por minuto"),
    ("Depth at least 2 inches (5 cm), not more than 2.4 inches (6 cm)",
     "Profundidad de al menos 2 pulgadas (5 cm), no más de 2.4 pulgadas (6 cm)"),
    ("Complete chest recoil every time", "Recoíl completo del pecho cada vez"),
    ("Minimize pauses — try to keep interruptions under 10 seconds",
     "Minimice pausas — trate de mantener interrupciones bajo 10 segundos"),
    ("Adult ratio 30:2 (one or two rescuers) until an advanced airway is in place",
     "Relación en adultos 30:2 (uno o dos rescatistas) hasta colocar una vía aérea avanzada"),
    ("Switch compressors about every 2 minutes", "Cambie de reanimador aproximadamente cada 2 minutos"),
    ("Child and infant differences", "Diferencias en niños y lactantes"),
    ("Child: about 1 year to puberty. Infant: younger than 1 year (not newborns in the delivery room)",
     "Niño: de cerca de 1 año hasta la pubertad. Lactante: menor de 1 año (no recién nacidos en sala de partos)"),
    ("Two rescuers: 15:2 for child and infant. One rescuer: 30:2",
     "Dos rescatistas: 15:2 en niño y lactante. Un rescatista: 30:2"),
    ("Child depth about 2 inches (one-third of chest). Infant about 1.5 inches (4 cm)",
     "Profundidad en niño cerca de 2 pulgadas (un tercio del pecho). Lactante cerca de 1.5 pulgadas (4 cm)"),
    ("Infant pulse: brachial. Child: carotid or femoral. Adult: carotid",
     "Pulso en lactante: braquial. Niño: carótida o femoral. Adulto: carótida"),
    ("If pulse is present but breathing is inadequate: rescue breaths — adult 1 every 6 seconds; infant/child 1 every 2–3 seconds",
     "Si hay pulso pero la respiración es inadecuada: ventilaciones — adulto 1 cada 6 segundos; lactante/niño 1 cada 2–3 segundos"),
    ("AED in one pass", "DEA en un solo paso"),
    ("Turn it on. Bare the chest. Attach pads. Clear. Shock if advised. Resume CPR immediately",
     "Enciéndalo. Descubra el pecho. Coloque parches. Despeje. Descargue si lo indica. Reanude RCP de inmediato"),
    ("Adult pads on adults. Pediatric pads/key if available for infants and small children",
     "Parches de adulto en adultos. Parches/llave pediátricos si hay para lactantes y niños pequeños"),
    ("No pediatric pads? Adult pads are OK — do not let them touch. Anterior-posterior placement if needed",
     "¿Sin parches pediátricos? Los de adulto sirven — no deben tocarse. Colocación anterior-posterior si hace falta"),
    ("Dry a wet chest. Remove a medicine patch and wipe. Shave dense hair if pads will not stick",
     "Seque un pecho mojado. Quite un parche de medicamento y limpie. Afeite vello denso si los parches no pegan"),
    ("Do not place a pad directly over a pacemaker or ICD — put it beside the device",
     "No coloque un parche directo sobre un marcapasos o DAI — póngalo al lado del dispositivo"),
    ("Choking", "Atragantamiento"),
    ("Mild: can cough or speak — stand by and encourage coughing",
     "Leve: puede toser o hablar — observe y anime a toser"),
    ("Severe adult/child: abdominal thrusts. Pregnant or obese: chest thrusts",
     "Grave en adulto/niño: compresiones abdominales. Embarazada u obesa: compresiones torácicas"),
    ("Unresponsive: start CPR. Look in the mouth before breaths. Remove an object only if you see it",
     "Sin respuesta: inicie RCP. Mire la boca antes de ventilar. Quite un objeto solo si lo ve"),
    ("Conscious infant: 5 back slaps, then 5 chest thrusts. Repeat. No abdominal thrusts on infants",
     "Lactante consciente: 5 palmadas en la espalda, luego 5 compresiones torácicas. Repita. No use abdominales en lactantes"),
    ("Best study order", "Mejor orden de estudio"),
    ("Memorize the adult numbers (rate, depth, 30:2, 10-second pulse check) and the AED sequence.",
     "Memorice las cifras de adulto (frecuencia, profundidad, 30:2, chequeo de pulso de 10 segundos) y la secuencia del DEA."),
    ("Drill child vs infant ratios, pulse sites, and choking until you stop mixing them up.",
     "Practique relaciones niño vs lactante, sitios de pulso y atragantamiento hasta dejar de mezclarlos."),
    ("Add team CPR, bag-mask, opioid, and first aid if your course is BLS or Heartsaver First Aid CPR AED.",
     "Sume RCP en equipo, bolsa-mascarilla, opioides y primeros auxilios si su curso es BLS o Heartsaver First Aid CPR AED."),
    ("Take the 25-question mocks until you consistently score 21 or higher, then review every miss in the bank.",
     "Haga los simulacros de 25 hasta obtener 21 o más de forma constante y luego revise cada fallo en el banco."),
    ("Official sources:", "Fuentes oficiales:"),
    ("Follow the handbook your instructor issued — this lab is practice, not a substitute for the course. Last reviewed August 31, 2026.",
     "Siga el manual que le dio su instructor — este laboratorio es práctica, no sustituye el curso. Última revisión: 31 de agosto de 2026."),
    ("See an error? Tell us.", "¿Ve un error? Avísenos."),
    ("Common questions", "Preguntas frecuentes"),
    ("Does this quiz certify me in CPR?", "¿Este cuestionario me certifica en RCP?"),
    ("No. A card requires an authorized instructor and a skills session. This is knowledge review only. In an emergency, call 911.",
     "No. Una tarjeta requiere un instructor autorizado y una sesión de destrezas. Esto es solo repaso de conocimientos. En una emergencia, llame al 911."),
    ("Where should I start?", "¿Por dónde empiezo?"),
    ("Question 1", "Pregunta 1"),
    (">Next</button>", ">Siguiente</button>"),
    (">Quit</button>", ">Salir</button>"),
    ("id=\"result-kicker\">Result", "id=\"result-kicker\">Resultado"),
    (">Retake</button>", ">Repetir</button>"),
    (">Review missed</button>", ">Repasar falladas</button>"),
    (">Home</button>", ">Inicio</button>"),
    (">Flashcards</p>", ">Tarjetas</p>"),
    (">All</button>", ">Todas</button>"),
    (">Key numbers</button>", ">Cifras clave</button>"),
    (">Sequences</button>", ">Secuencias</button>"),
    (">AED</button>", ">DEA</button>"),
    (">Peds</button>", ">Pediátrico</button>"),
    (">First aid</button>", ">Primeros auxilios</button>"),
    (">Still learning</button>", ">Sigo aprendiendo</button>"),
    ('aria-label="Flip card"', 'aria-label="Voltear tarjeta"'),
    ("Tap to reveal", "Toque para ver la respuesta"),
    (">Got it</button>", ">Ya lo sé</button>"),
    (">Skip</button>", ">Saltar</button>"),
    ("Full question bank", "Banco completo de preguntas"),
    ("All practice items", "Todos los ítems de práctica"),
    ("Disclaimer", "Aviso legal"),
    ("See an error?", "¿Ve un error?"),
]


def write_home() -> None:
    extra = """  <script type="application/ld+json">
  {"@context":"https://schema.org","@graph":[{"@type":"Organization","@id":"https://safetytestprep.com/#org","name":"Safety Test Prep","url":"https://safetytestprep.com/","logo":{"@type":"ImageObject","url":"https://safetytestprep.com/img/share-square.jpg"},"email":"hello@safetytestprep.com","founder":{"@type":"Person","name":"Vince"}},{"@type":"WebSite","@id":"https://safetytestprep.com/es/#website","name":"Safety Test Prep","url":"https://safetytestprep.com/es/","inLanguage":"es-US","publisher":{"@id":"https://safetytestprep.com/#org"},"description":"Exámenes de práctica gratis de OSHA, CDL de California y RCP/DEA. Solo práctica educativa independiente."},{"@type":"FAQPage","mainEntity":[{"@type":"Question","name":"¿Estos son exámenes oficiales de OSHA, DMV o RCP?","acceptedAnswer":{"@type":"Answer","text":"No. Safety Test Prep publica cuestionarios originales de práctica independiente. No emite tarjetas OSHA, licencias CDL ni certificaciones de RCP/DEA."}},{"@type":"Question","name":"¿Los exámenes de práctica de OSHA, CDL y RCP son gratis?","acceptedAnswer":{"@type":"Answer","text":"Sí. Los cuestionarios y las tarjetas son gratis. El apoyo opcional no compra una tarjeta, licencia ni puntaje de examen."}},{"@type":"Question","name":"¿Por dónde debo empezar?","acceptedAnswer":{"@type":"Answer","text":"Empiece con el cuestionario de protección contra caídas para temas de OSHA, conocimientos generales de CDL de California para el permiso, o RCP en adultos para el repaso de emergencias."}}]}]}
  </script>
"""
    body = """    <section class="hero">
      <div>
        <p class="eyebrow">Safety Test Prep</p>
        <h1>Exámenes de práctica gratis de OSHA, CDL y RCP.</h1>
        <p class="lede">Cuestionarios independientes para temas de OSHA 10/30, conocimientos de CDL de California y fundamentos de RCP/DEA. No se emiten tarjetas, licencias ni certificaciones.</p>
        <div class="btns">
          <a class="btn" href="osha/">Explorar práctica OSHA</a>
          <a class="btn ghost" href="cdl/">Práctica de CDL de California</a>
          <a class="btn ghost" href="cpr/">Repaso de RCP/DEA</a>
        </div>
      </div>
      <aside class="preview">
        <div>
          <p class="eyebrow">Empiece con OSHA</p>
          <strong>Cuestionario de protección contra caídas</strong>
          <p>15 preguntas · Unos 5 minutos</p>
        </div>
        <p><a class="btn" href="osha/fall-protection.html">Empezar cuestionario</a></p>
      </aside>
    </section>
    <section class="paths" aria-label="Rutas de estudio">
      <div class="grid">
        <article>
          <p class="card-kicker">01</p>
          <h2>Práctica OSHA</h2>
          <p>Repase temas prácticos de seguridad en obra, incluida la protección contra caídas, EPP, seguridad en escaleras y reconocimiento de peligros.</p>
          <p style="margin-top:14px"><a class="btn" href="osha/">Explorar OSHA</a></p>
        </article>
        <article>
          <p class="card-kicker">02</p>
          <h2>CDL de California</h2>
          <p>Repase conocimientos para conductores comerciales con apoyo de estudio enfocado en California.</p>
          <p style="margin-top:14px"><a class="btn" href="cdl/">Explorar CDL</a></p>
        </article>
        <article>
          <p class="card-kicker">03</p>
          <h2>Repaso de RCP/DEA</h2>
          <p>Refresque conocimientos básicos de respuesta a emergencias y RCP/DEA antes de una capacitación formal.</p>
          <p style="margin-top:14px"><a class="btn" href="cpr/">Explorar RCP/DEA</a></p>
        </article>
      </div>
    </section>
    <section class="featured" aria-labelledby="featured-title">
      <div>
        <p class="eyebrow">Práctica destacada</p>
        <h2 id="featured-title">Cuestionario de protección contra caídas</h2>
        <p class="lede">Repase peligros comunes de caídas, barandales, arresto de caídas, riesgos de escaleras y decisiones más seguras en la obra.</p>
        <p class="reviewed">15 preguntas · 5 minutos · Última revisión 31 de agosto de 2026</p>
        <p style="margin-top:16px"><a class="btn" href="osha/fall-protection.html">Empezar el cuestionario de caídas</a></p>
      </div>
      <div class="tags" aria-label="Temas">
        <a class="tag" href="osha/fall-protection.html">Caídas</a>
        <a class="tag" href="osha/ladder-safety.html">Escaleras</a>
        <a class="tag" href="osha/ppe.html">EPP</a>
        <a class="tag" href="osha/hazard-communication.html">HazCom</a>
        <a class="tag" href="osha/focus-four.html">Focus Four</a>
        <a class="tag" href="osha/excavation.html">Zanjas</a>
        <a class="tag" href="osha/electrical.html">Eléctrico</a>
        <a class="tag" href="osha/lockout-tagout.html">Bloqueo</a>
        <a class="tag" href="cdl/general-knowledge.html">Conocimientos generales CDL</a>
        <a class="tag" href="cdl/combination-vehicles.html">Vehículos combinados</a>
        <a class="tag" href="cpr/adult-cpr.html">RCP en adultos</a>
        <a class="tag" href="cpr/aed.html">DEA</a>
      </div>
    </section>
    <section class="section">
      <h2>Cómo funciona</h2>
      <div class="steps">
        <div class="step"><span>Paso 1</span><strong>Elija un tema</strong></div>
        <div class="step"><span>Paso 2</span><strong>Responda preguntas originales de práctica</strong></div>
        <div class="step"><span>Paso 3</span><strong>Lea la explicación y consulte las fuentes oficiales</strong></div>
      </div>
      <p class="disclaimer-quiet">Safety Test Prep es práctica educativa independiente. No emite tarjetas OSHA, licencias CDL, certificaciones de RCP/DEA ni credenciales gubernamentales.</p>
    </section>
    <section class="section panel">
      <p class="eyebrow">Hecho con experiencia de trabajo real</p>
      <h2>Soy Vince.</h2>
      <p>Creé Safety Test Prep para compartir apoyo de estudio práctico, informado por experiencia en obras, operaciones de restaurante, conducción y respuesta a emergencias.</p>
      <p>El sitio está pensado para revisar fundamentos de seguridad en lenguaje sencillo antes de una capacitación formal, un examen o un puesto nuevo.</p>
      <p style="margin-top:12px"><a href="about.html">Más sobre Safety Test Prep</a></p>
    </section>
    <section class="section faq" aria-labelledby="home-faq">
      <h2 id="home-faq">Preguntas frecuentes</h2>
      <details>
        <summary>¿Estos son exámenes oficiales de OSHA, DMV o RCP?</summary>
        <p>No. Son cuestionarios originales de práctica independiente. Safety Test Prep no emite tarjetas OSHA, licencias CDL ni certificaciones de RCP/DEA.</p>
      </details>
      <details>
        <summary>¿Los exámenes de práctica son gratis?</summary>
        <p>Sí. Los cuestionarios y las tarjetas de OSHA, CDL de California y RCP/DEA son gratis. El apoyo opcional después de un cuestionario no compra una credencial.</p>
      </details>
      <details>
        <summary>¿Por dónde debo empezar?</summary>
        <p>Use el <a href="osha/fall-protection.html">cuestionario de protección contra caídas</a> para temas de OSHA, <a href="cdl/general-knowledge.html">conocimientos generales de CDL de California</a> para el permiso, o <a href="cpr/adult-cpr.html">RCP en adultos</a> antes de una clase de destrezas.</p>
      </details>
    </section>
    <section class="section">
      <h2>Verifique con fuentes oficiales</h2>
      <p class="disclaimer-quiet">Los requisitos de capacitación, licencias y credenciales pueden cambiar. Use los recursos oficiales de abajo para confirmar lo que le aplica.</p>
      <div class="resource-grid">
        <a href="https://www.osha.gov/training/outreach" rel="noopener noreferrer" target="_blank">Programa de capacitación OSHA Outreach</a>
        <a href="https://www.dmv.ca.gov/portal/driver-handbooks/" rel="noopener noreferrer" target="_blank">Manual de conductores comerciales de California</a>
        <a href="https://cpr.heart.org/" rel="noopener noreferrer" target="_blank">Buscador de cursos de la American Heart Association</a>
        <a href="https://www.redcross.org/take-a-class" rel="noopener noreferrer" target="_blank">Buscador de clases de la Cruz Roja Americana</a>
      </div>
    </section>
"""
    html = wrap_site(
        "Exámenes de práctica gratis de OSHA, CDL y RCP | Safety Test Prep",
        "Exámenes de práctica gratis de OSHA 10/30, CDL de California y RCP/DEA con preguntas originales y explicaciones. Estudio independiente: no se emiten tarjetas, licencias ni certificaciones.",
        "",
        body,
        extra,
        scripts=['<script src="../js/config.js"></script>', '<script src="../js/chrome.js"></script>'],
    )
    # wrap_site used slug "" -> canonical /es/  but title path used es/  — fix wrap: slug "" became ORIGIN/es/  wait wrap uses `/es/{slug}` if slug else `/es/`
    write(ES / "index.html", html.replace('id="main">\n    <nav', '>\n    <nav').replace('<div class="wrap" id="main">', '<main id="main" class="wrap home-wrap">').replace('    <footer data-stp-footer></footer>\n  </div>', '    <footer data-stp-footer></footer>\n  </main>'))


def simple_page(filename, title, desc, eyebrow, h1, blocks, extra_scripts=None, robots=""):
    inner = f'    <p class="eyebrow">{eyebrow}</p>\n    <h1>{h1}</h1>\n'
    inner += "\n".join(blocks)
    scripts = extra_scripts or ['<script src="../js/chrome.js"></script>']
    write(ES / filename, wrap_site(title, desc, filename, inner, scripts=scripts, robots=robots))


def study_help(lab: str, title: str, desc: str, eyebrow: str, h1: str, disc: str, edu: str, body: str) -> None:
    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{title}</title>
  <meta name="description" content="{desc}" />
  <meta name="robots" content="noindex, follow" />
  <link rel="canonical" href="{ORIGIN}/es/{lab}/study-help.html" />
  <link rel="stylesheet" href="../../{lab}/css/app.css" />
</head>
<body>
  <div class="app">
    <header class="topbar">
      <div>
        <p class="eyebrow">{eyebrow}</p>
        <h1>{h1}</h1>
      </div>
      <p class="disclaimer">{disc}</p>
    </header>
    <p class="edu-bar">{edu} <a href="../disclaimer.html">Aviso legal</a></p>
    <section class="hero">
{body}
    </section>
    <footer data-stp-footer data-base="../"></footer>
  </div>
  <script src="../../js/chrome.js"></script>
</body>
</html>
"""
    write(ES / lab / "study-help.html", html)


def sitemap() -> None:
    paths = [
        "/",
        "/about.html",
        "/why.html",
        "/contact.html",
        "/privacy.html",
        "/terms.html",
        "/disclaimer.html",
        "/accessibility.html",
        "/copyright.html",
        "/legal.html",
        "/support.html",
        "/osha-10-practice.html",
        "/california-cdl-practice.html",
        "/cpr-aed-practice.html",
        "/osha/",
        "/osha/fall-protection.html",
        "/osha/ladder-safety.html",
        "/osha/ppe.html",
        "/osha/hazard-communication.html",
        "/osha/focus-four.html",
        "/osha/excavation.html",
        "/osha/electrical.html",
        "/osha/lockout-tagout.html",
        "/cdl/",
        "/cdl/general-knowledge.html",
        "/cdl/air-brakes.html",
        "/cdl/combination-vehicles.html",
        "/cpr/",
        "/cpr/adult-cpr.html",
        "/cpr/aed.html",
    ]
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">',
    ]
    for p in paths:
        en = ORIGIN + p
        es = ORIGIN + ("/es/" if p == "/" else "/es" + p)
        lines.append("  <url>")
        lines.append(f"    <loc>{en}</loc>")
        lines.append("    <lastmod>2026-09-01</lastmod>")
        lines.append(f'    <xhtml:link rel="alternate" hreflang="en" href="{en}"/>')
        lines.append(f'    <xhtml:link rel="alternate" hreflang="es" href="{es}"/>')
        lines.append(f'    <xhtml:link rel="alternate" hreflang="x-default" href="{en}"/>')
        lines.append("  </url>")
        lines.append("  <url>")
        lines.append(f"    <loc>{es}</loc>")
        lines.append("    <lastmod>2026-09-01</lastmod>")
        lines.append(f'    <xhtml:link rel="alternate" hreflang="en" href="{en}"/>')
        lines.append(f'    <xhtml:link rel="alternate" hreflang="es" href="{es}"/>')
        lines.append(f'    <xhtml:link rel="alternate" hreflang="x-default" href="{en}"/>')
        lines.append("  </url>")
    lines.append("</urlset>")
    (ROOT / "sitemap.xml").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    write_home()

    simple_page(
        "about.html",
        "Acerca de Safety Test Prep — Vince, práctica independiente",
        "Soy Vince. Safety Test Prep es práctica educativa independiente para temas de OSHA, conocimientos de CDL de California y fundamentos de RCP/DEA. No emito tarjetas ni licencias.",
        "Acerca de Safety Test Prep",
        "Soy Vince.",
        [
            '<p class="lede">Creé Safety Test Prep para compartir apoyo de estudio práctico basado en experiencia real en obras, operaciones de restaurante, conducción y respuesta a emergencias.</p>',
            '<section class="price"><p>La meta es simple: ayudar a trabajadores, personas que buscan empleo y quienes cambian de carrera a revisar fundamentos de seguridad en lenguaje sencillo y practicar antes de una capacitación formal, un examen o un puesto nuevo.</p><p>Safety Test Prep ofrece solo materiales de práctica educativa independiente. No emito tarjetas OSHA, licencias CDL, certificaciones de RCP/DEA, credenciales médicas ni certificados aprobados por el gobierno.</p></section>',
            '<p class="reviewed">Última revisión: 31 de agosto de 2026. <a href="contact.html">¿Ve un error? Avísenos.</a></p>',
        ],
    )
    simple_page(
        "why.html",
        "Por qué existe Safety Test Prep — para quién es y por qué un aporte",
        "Práctica no oficial de OSHA, CDL y RCP para que pueda estudiar gratis. El apoyo opcional por Cash App mantiene los laboratorios en línea. No es una organización benéfica. No es una certificación.",
        "Safety Test Prep",
        "Por qué existe este sitio",
        [
            '<p class="lede">Quien está por tomar una clase de OSHA, un permiso de CDL de California o un examen escrito de RCP necesita práctica que pueda usar esta noche — sin comprar un “banco oficial” robado y sin creer que un sitio web puede emitir la tarjeta.</p>',
            '<section class="price"><h2>Para quién es</h2><p>Aprendices y ayudantes que estudian OSHA 10 o 30 antes de un curso real de Outreach. Estudiantes de permiso que practican conocimientos generales, frenos de aire y vehículos combinados antes del DMV. Quien repasa RCP/DEA antes de una clase de destrezas. Si necesita la <em>credencial</em>, igual va con un instructor autorizado, el DMV o un instructor de AHA/Cruz Roja. Este laboratorio es la tarea.</p></section>',
            '<section class="price"><h2>Por qué lo construí</h2><p>Soy Vince, en Sacramento. Escribí bancos originales de práctica para que los cuestionarios sean gratis y honestos — basados en las normas y el manual, no copiados de un examen cerrado. Los mantengo en línea. No opero un centro de capacitación y no lo apruebo a usted.</p></section>',
            '<section class="price"><h2>Por qué alguien pagaría</h2><p>Los exámenes siguen siendo gratis de todos modos. Si un simulacro le ayudó, <strong>$9 / $19 / $39 en Cash App o cripto</strong> es apoyo opcional de estudio: hosting, preguntas nuevas y mis costos de vida mientras lo mantengo. Es una <strong>propina</strong>, no una donación, no recaudación de fondos, no deducible de impuestos y no un certificado. Ya recibió la práctica. Pagar es cómo el siguiente estudiante todavía lo encuentra aquí.</p><p><a class="btn" href="support.html">Montos de apoyo al estudio</a> · <a href="legal.html">Lo que no podemos vender</a></p></section>',
        ],
    )
    simple_page(
        "contact.html",
        "Contacto Safety Test Prep",
        "Contacte a Safety Test Prep por errores, actualizaciones de contenido o los laboratorios de práctica independiente.",
        "Contacto",
        "¿Ve un error? Avísenos.",
        [
            '<p class="lede">El correo es la mejor forma de contactarnos por correcciones de contenido, accesibilidad o avisos DMCA. No tomamos preguntas de certificación: no podemos emitir una tarjeta ni una licencia.</p>',
            '<section class="price"><h2>Correo</h2><p><a id="contact-mail" href="mailto:hello@safetytestprep.com">hello@safetytestprep.com</a></p><p>Para correcciones de contenido, accesibilidad o avisos de derechos de autor. No podemos emitir tarjetas OSHA, licencias CDL ni certificaciones de RCP.</p></section>',
        ],
        extra_scripts=['<script src="../js/config.js"></script>', '<script src="../js/chrome.js"></script>'],
    )
    simple_page(
        "privacy.html",
        "Política de privacidad — Safety Test Prep",
        "Política de privacidad de Safety Test Prep. Qué recopilamos, qué no, y cómo pueden contactarnos las personas en California.",
        "Privacidad",
        "Política de privacidad",
        [
            '<p class="reviewed">Fecha de vigencia: 31 de agosto de 2026. Anotaremos cambios materiales en esta página con una fecha nueva.</p>',
            '<section class="price"><h2>Quiénes somos</h2><p>Safety Test Prep es un sitio educativo independiente en safetytestprep.com. Contacto: <a id="contact-mail" href="mailto:hello@safetytestprep.com">hello@safetytestprep.com</a>.</p></section>',
            '<section class="price"><h2>Información que recopilamos</h2><p>No exigimos una cuenta. No operamos una lista de correo ni un formulario de contacto en este sitio.</p><p><strong>Progreso del cuestionario en su dispositivo.</strong> Las marcas de tarjetas “ya lo sé” se guardan en el almacenamiento local del navegador. Esa información permanece en su dispositivo a menos que la borre. Nosotros no recibimos una copia.</p><p><strong>Registros de alojamiento.</strong> El sitio está en GitHub Pages. GitHub puede recopilar datos técnicos estándar como dirección IP, tipo de navegador, URL de referencia y marcas de tiempo, según su propia política de privacidad. No operamos un producto de analítica aparte en estas páginas.</p><p><strong>Pagos.</strong> Los pagos opcionales pasan por Cash App o una red de cripto que usted elija. Esas empresas (o redes) procesan el pago. No recopilamos números de tarjeta en este sitio. Puede usar los laboratorios de práctica sin pagar.</p><p><strong>Correo que nos envía.</strong> Si nos escribe, recibimos lo que incluya en el mensaje para poder responderle.</p></section>',
            '<section class="price"><h2>Cómo usamos la información</h2><p>El almacenamiento del dispositivo solo recuerda el progreso de las tarjetas. El correo solo se usa para responderle. No vendemos información personal. No usamos el sitio para publicidad de terceros.</p></section>',
            '<section class="price"><h2>Con quién compartimos</h2><p>No vendemos ni alquilamos listas de visitantes. El alojamiento lo provee GitHub. Si paga, Cash App o la red de cripto que use es un tercero. Podemos divulgar información si la ley lo exige.</p></section>',
            '<section class="price"><h2>Sus opciones (incluido California)</h2><p>Puede borrar el almacenamiento local de su navegador para quitar las marcas de tarjetas. Puede dejar de usar el sitio en cualquier momento. Para revisar o pedir cambios a información personal que nos envió por correo, escriba a la dirección de arriba. Anunciaremos cambios de política actualizando esta página y la fecha de vigencia.</p></section>',
            '<section class="price"><h2>Niños</h2><p>Este sitio está pensado para adultos que se preparan para estudio laboral, de CDL o de una clase de destrezas. No recopilamos a sabiendas información personal de niños menores de 13 años.</p></section>',
        ],
        extra_scripts=['<script src="../js/config.js"></script>', '<script src="../js/chrome.js"></script>'],
    )
    simple_page(
        "terms.html",
        "Términos de uso — Safety Test Prep",
        "Términos de uso de los materiales de práctica educativa independiente de Safety Test Prep.",
        "Términos",
        "Términos de uso",
        [
            '<p class="reviewed">Fecha de vigencia: 31 de agosto de 2026. Este es un aviso de términos del sitio, no consejo legal. Pida a un abogado de California que lo revise antes de confiar en él como contrato.</p>',
            '<section class="price"><h2>El servicio</h2><p>Safety Test Prep ofrece cuestionarios educativos originales y páginas de estudio relacionadas. Usar el sitio significa que acepta estos términos y el <a href="disclaimer.html">aviso legal</a>.</p></section>',
            '<section class="price"><h2>Sin certificación ni promesa de resultados</h2><p>No certificamos, licenciamos, autorizamos ni aprobamos a nadie. No garantizamos que apruebe un examen, una clase o una prueba de destrezas. El contenido es solo para estudio general y puede estar incompleto o desactualizarse cuando cambien los requisitos oficiales.</p></section>',
            '<section class="price"><h2>Pago opcional</h2><p>Los laboratorios de práctica se pueden usar pague o no. Si el material le ayudó, puede pagar $9.99 por Cash App. Ese pago es voluntario. No es una donación, no es deducible de impuestos y no es pago por una tarjeta, licencia o aprobado garantizado. Los procesadores de pago tienen sus propios términos.</p></section>',
            '<section class="price"><h2>Su uso</h2><p>No copie los bancos de preguntas para venderlos como “exámenes oficiales”, no extraiga el sitio para un volcado competidor ni presente nuestros materiales como capacitación gubernamental o OSHA Outreach. Puede usar los cuestionarios para su propio estudio.</p></section>',
            '<section class="price"><h2>Propiedad intelectual</h2><p>Las preguntas originales, las explicaciones y el texto del sitio son de Safety Test Prep salvo que se indique. Los nombres OSHA, DMV, AHA y Cruz Roja se usan solo para describir el tipo de tema de estudio. Esas organizaciones son dueñas de sus marcas. Vea <a href="copyright.html">Derechos de autor / DMCA</a>.</p></section>',
            '<section class="price"><h2>Limitación</h2><p>El sitio se ofrece tal cual. No somos responsables de resultados de exámenes, decisiones laborales ni resultados de respuesta a emergencias. La ley de California rige estos términos, excluyendo las normas de conflicto de leyes. Si un tribunal declara inaplicable un término, el resto sigue vigente.</p></section>',
        ],
    )
    simple_page(
        "disclaimer.html",
        "Aviso legal — Safety Test Prep no es OSHA, DMV ni certificación de RCP",
        "Aviso educativo de Safety Test Prep: solo práctica independiente. No está afiliado a OSHA, DOL, ningún DMV, AHA ni la Cruz Roja. Sin tarjetas ni licencias.",
        "Aviso legal",
        "Aviso de uso educativo",
        [
            '<p class="lede">Este material es solo para fines educativos y de estudio general. No es capacitación oficial del gobierno, OSHA Outreach, DMV, RCP/DEA, médica, legal, de licencias ni específica del empleador. No otorga una tarjeta, certificado, licencia ni garantía de aprobar un examen. Confirme los requisitos actuales con su empleador, proveedor de capacitación, agencia de licencias o autoridad local.</p>',
            '<section class="price"><h2>Sitio independiente</h2><p>Safety Test Prep ofrece materiales de práctica educativa independiente. No emitimos tarjetas OSHA, licencias CDL, certificaciones de RCP/DEA ni credenciales gubernamentales. No somos un instructor de OSHA, un emisor de certificaciones, un sitio gubernamental ni un proveedor de capacitación médica.</p></section>',
            '<section class="price"><h2>OSHA</h2><p>Safety Test Prep es un sitio educativo independiente y no está afiliado, respaldado ni autorizado por la Occupational Safety and Health Administration (OSHA) ni el Departamento de Trabajo de EE. UU. No proporcionamos tarjetas de finalización del Programa de capacitación OSHA Outreach. La capacitación Outreach es voluntaria y una tarjeta de finalización solo puede emitirse por el proceso autorizado aplicable.</p><p>No usamos logotipos de OSHA ni del DOL. Los cuestionarios son materiales originales de estudio sobre temas de OSHA, no un examen oficial de OSHA.</p><p><a href="https://www.osha.gov/training/outreach" rel="noopener noreferrer" target="_blank">Programa de capacitación OSHA Outreach</a></p></section>',
            '<section class="price"><h2>CDL</h2><p>Los requisitos de CDL, el contenido del examen escrito, los endosos y los procedimientos de licencia varían por estado y pueden cambiar. Safety Test Prep no está afiliado a ningún Departamento de Vehículos Motorizados ni autoridad de licencias. Siempre verifique los requisitos actuales con la agencia oficial de licencias de su estado.</p><p>Las páginas orientadas a California son práctica basada en el manual, no preguntas oficiales del DMV. <a href="https://www.dmv.ca.gov/portal/driver-handbooks/" rel="noopener noreferrer" target="_blank">Manual de conductores comerciales de California</a></p></section>',
            '<section class="price"><h2>RCP/DEA</h2><p>El contenido de RCP/DEA se ofrece solo para repaso educativo general y no es consejo médico ni un sustituto de capacitación con instructor, evaluación práctica de destrezas, servicios de emergencia, requisitos del empleador o un curso de certificación reconocido. En una emergencia, llame al 911 o a su número local de emergencias y siga las instrucciones del despachador.</p><p>No copiamos preguntas de examen de la American Heart Association, la Cruz Roja Americana ni proveedores de cursos de pago. Una tarjeta requiere un instructor autorizado y una prueba de destrezas.</p></section>',
            '<section class="price"><h2>Apoyo de estudio frente a una credencial</h2><p>Los montos opcionales de Cash App o cripto son propinas para mantener los laboratorios en línea. No son donaciones, no son deducibles de impuestos y no son pago por certificación. <a href="legal.html">Lo que puede y no puede pagar</a>.</p></section>',
            '<p class="reviewed">Última revisión: 31 de agosto de 2026. <a href="contact.html">¿Ve un error? Avísenos.</a> · <a href="accessibility.html">Accesibilidad</a> · <a href="copyright.html">Derechos de autor / DMCA</a></p>',
        ],
    )
    simple_page(
        "accessibility.html",
        "Accesibilidad — Safety Test Prep",
        "Declaración de accesibilidad de Safety Test Prep. Cómo pedir una versión más usable de una página o cuestionario.",
        "Accesibilidad",
        "Accesibilidad",
        [
            '<p class="lede">Buscamos que el sitio se lea bien en un teléfono, con encabezados claros, botones visibles y cuestionarios que se puedan usar con el teclado. No hemos completado una auditoría formal WCAG.</p>',
            '<section class="price"><h2>Límites conocidos</h2><p>Los laboratorios de práctica usan un tema oscuro y controles de cuestionario propios. Algunos navegadores antiguos o herramientas de asistencia pueden no anunciar cada cambio de estado. El color no es la única pista de respuestas correctas o incorrectas, pero el contraste no está certificado.</p></section>',
            '<section class="price"><h2>Pedir ayuda</h2><p>Si una página o un cuestionario es difícil de usar, escriba a <a id="contact-mail" href="mailto:hello@safetytestprep.com">hello@safetytestprep.com</a> con la URL y lo que necesita (por ejemplo texto más grande, una versión solo texto de una pregunta o un problema de teclado). Trabajaremos en un arreglo práctico.</p></section>',
            '<p class="reviewed">Última revisión: 31 de agosto de 2026.</p>',
        ],
        extra_scripts=['<script src="../js/config.js"></script>', '<script src="../js/chrome.js"></script>'],
    )
    simple_page(
        "copyright.html",
        "Derechos de autor / DMCA — Safety Test Prep",
        "Aviso de derechos de autor y DMCA para los materiales originales de práctica de Safety Test Prep.",
        "Derechos de autor",
        "Derechos de autor / DMCA",
        [
            '<p class="lede">Los cuestionarios originales, las explicaciones y el texto del sitio en Safety Test Prep están protegidos por derechos de autor. Escribimos las preguntas con nuestras palabras a partir de principios de seguridad de acceso público y fuentes oficiales públicas. No copiamos bancos de proveedores comerciales, diapositivas de cursos ni exámenes cerrados.</p>',
            '<section class="price"><h2>Marcas de otras personas</h2><p>OSHA, el Departamento de Trabajo de EE. UU., DMV, American Heart Association y Cruz Roja Americana son dueños de sus nombres y logotipos. No usamos sus sellos ni logotipos. Las menciones describen el tipo de tema que usted puede estar estudiando, no afiliación ni respaldo.</p></section>',
            '<section class="price"><h2>Si cree que usamos su trabajo</h2><p>Envíe un aviso al estilo DMCA a <a id="contact-mail" href="mailto:hello@safetytestprep.com">hello@safetytestprep.com</a> con: su información de contacto, una descripción de la obra, la URL en este sitio, una declaración de que tiene una creencia de buena fe de que el uso no está autorizado, una declaración bajo pena de perjurio de que la información es precisa y de que usted es el dueño o agente autorizado, y su firma física o electrónica.</p><p>Revisaremos avisos completos. Esta página no sustituye registrar un agente DMCA designado ante la Oficina de Derechos de Autor de EE. UU. si necesita ese puerto seguro.</p></section>',
            '<p class="reviewed">Última revisión: 31 de agosto de 2026.</p>',
        ],
        extra_scripts=['<script src="../js/config.js"></script>', '<script src="../js/chrome.js"></script>'],
    )
    simple_page(
        "legal.html",
        "Qué puede pagar — Safety Test Prep",
        "Apoyo opcional de estudio por Cash App para Safety Test Prep. No es una certificación, donación ni regalo deducible de impuestos.",
        '<a href="index.html">Safety Test Prep</a>',
        "Qué puede pagar",
        [
            '<p class="lede">Ayuda de estudio: preguntas de práctica, tarjetas y mantener los laboratorios en línea. Cash App o cripto. Opcional. No es recaudación de fondos. No es una 501(c)(3). No es deducible de impuestos.</p>',
            "<p>Safety Test Prep ofrece materiales de práctica educativa independiente. No emitimos tarjetas OSHA, licencias CDL, certificaciones de RCP/DEA ni credenciales gubernamentales.</p>",
            '<section class="price"><h2>Lo que no puede pagar aquí</h2><p>Una tarjeta OSHA 10 o 30. Una CDL de California. Una tarjeta de RCP de AHA o Cruz Roja. Un aprobado garantizado. Saltar la clase oficial, el DMV o la sesión de destrezas. Si un anuncio dice que “lo certificamos”, ese anuncio está mal.</p><p>Una tarjeta de 10/30 requiere un instructor autorizado de Outreach. Una CDL la emite el DMV. Una tarjeta de RCP requiere un instructor autorizado y una prueba de destrezas.</p><p><a href="disclaimer.html">Aviso educativo completo</a> · <a href="terms.html">Términos de uso</a></p></section>',
        ],
    )
    simple_page(
        "support.html",
        "Apoye Safety Test Prep",
        "Apoyo opcional por Cash App o cripto para Safety Test Prep. Las contribuciones no compran certificaciones, licencias ni tarjetas.",
        "Apoyo opcional",
        "Mantenga los laboratorios gratis",
        [
            '<p class="lede">Safety Test Prep es gratis. Si un cuestionario le ayudó a prepararse para el trabajo, una capacitación o un puesto nuevo, un apoyo opcional de $9.99 financia investigación, redacción de preguntas, revisión y actualizaciones. El pago no compra una tarjeta, licencia ni resultado de examen.</p>',
            '<section class="price" id="pay"><h2>Cash App</h2><p>Soy Vince. Construí esto para que trabajadores y personas que buscan empleo puedan estudiar sin un muro de pago.</p><p id="pay-warn">Cash App aún no está activado.</p><p id="cash-line"></p><div class="btns"><a class="btn" data-cash="9.99">Apoye Safety Test Prep — $9.99 por Cash App</a></div><p>Pague a <strong>$safetytestprep</strong>. Cash App debe mostrar el nombre <strong>Safety Test Prep</strong>. Verifique el $ antes de enviar.</p></section>',
            '<section class="price"><h2>Otras formas de apoyar</h2><p>Las transferencias de cripto son voluntarias e irreversibles. Verifique la red y la dirección antes de enviar. USDT debe enviarse solo en la red TRX / Tron.</p><div id="crypto-line"></div></section>',
        ],
        extra_scripts=[
            '<script src="../js/config.js"></script>',
            '<script src="../js/i18n.js"></script>',
            '<script src="../js/pay.js"></script>',
            '<script src="../js/chrome.js"></script>',
        ],
    )

    lander_og_osha = f"{ORIGIN}/img/og-osha.jpg"
    landers = [
        dict(folder="osha", slug="fall-protection.html", quiz="fallProtection", n=15, og=lander_og_osha,
             title="Cuestionario de protección contra caídas — estudio OSHA (no es una tarjeta)",
             desc="Cuestionario gratis de 15 preguntas sobre protección contra caídas: regla de 6 pies, barandales, PFAS, tapas de huecos y andamios. Estudio independiente. No es capacitación OSHA ni una tarjeta.",
             eyebrow="OSHA · Tema de obra", h1="Cuestionario de protección contra caídas",
             lede="Repase conceptos comunes de prevención de caídas para construcción y trabajo en obra. Este cuestionario independiente cubre reconocimiento de peligros, planificación, barandales, sistemas personales de arresto de caídas, riesgos de escaleras y prácticas de trabajo más seguras.",
             meta="15 preguntas · Unos 5 minutos · Última revisión: 31 de agosto de 2026",
             edu="Solo práctica educativa. Este cuestionario no es capacitación OSHA y no otorga una tarjeta ni certificación OSHA.",
             cta="Empezar el cuestionario de 15 preguntas", share="Cuestionario gratis de 15 preguntas sobre protección contra caídas. Estudio independiente — no es una tarjeta OSHA.",
             covers=["Cuándo se suele exigir protección contra caídas en construcción (el disparador de 6 pies) frente a industria general",
                     "Altura y resistencia de barandales, tapas de huecos y sistemas convencionales de protección contra caídas",
                     "Partes del arresto personal de caídas (anclaje, arnés, dispositivo de conexión) y límites de caída libre",
                     "Altura de protección contra caídas en andamios y por qué no se usan cinturones corporales para arresto de caídas"],
             faqs=[("¿Este es un examen oficial de OSHA?", "No. Son preguntas originales de práctica. No se copian de un examen del DOL y terminar el cuestionario no emite una tarjeta OSHA 10 o 30."),
                   ("¿Para quién es?", "Trabajadores, aprendices y personas que estudian antes de una clase autorizada de Outreach y quieren revisar cifras y decisiones de obra en lenguaje sencillo."),
                   ("¿Dónde debo verificar las reglas?", "Use los materiales de protección contra caídas de OSHA y 29 CFR 1926 Subparte M. El programa de su empleador y un instructor autorizado son el camino oficial para una tarjeta.")],
             related='<a href="ladder-safety.html">Seguridad en escaleras</a> · <a href="focus-four.html">Focus Four</a> · <a href="ppe.html">EPP</a> · <a href="index.html">Todos los temas OSHA</a>',
             source='<a href="https://www.osha.gov/fall-protection" rel="noopener noreferrer" target="_blank">OSHA protección contra caídas</a> (29 CFR 1926 Subparte M y reglas relacionadas de superficies de trabajo). Preguntas originales; no copiadas de un curso comercial.'),
        dict(folder="osha", slug="ladder-safety.html", quiz="ladders", n=18, og=lander_og_osha,
             title="Cuestionario de seguridad en escaleras — estudio OSHA (no es una tarjeta)",
             desc="Cuestionario gratis de 18 preguntas sobre escaleras y andamios: montaje 4:1, extensión de 3 pies, inspecciones y reglas de caídas en andamios. Estudio independiente. No es una tarjeta OSHA.",
             eyebrow="OSHA · Tema de obra", h1="Cuestionario de seguridad en escaleras",
             lede="Repase montaje de escaleras portátiles, subida, inspecciones y conceptos relacionados de protección contra caídas en andamios usados en construcción y mantenimiento.",
             meta="18 preguntas · Unos 6 minutos · Última revisión: 31 de agosto de 2026",
             edu="Solo práctica educativa. Este cuestionario no es capacitación OSHA y no otorga una tarjeta ni certificación OSHA.",
             cta="Empezar el cuestionario de 18 preguntas", share="Cuestionario gratis de 18 preguntas sobre escaleras y andamios. Estudio independiente — no es una tarjeta OSHA.",
             covers=["Ángulo de montaje 4:1, extensión de tres pies y amarre o sujeción de la escalera",
                     "Inspeccionar rieles, peldaños y pies antes de subir",
                     "Contacto de tres puntos y mirar hacia la escalera al subir",
                     "Base del andamio, soleras de lodo y cuándo aplica la protección contra caídas en andamios"],
             faqs=[("¿Este es un examen oficial de OSHA?", "No. Solo práctica original. Una tarjeta de finalización sigue requiriendo un instructor autorizado de Outreach."),
                   ("¿Para quién es?", "Trabajadores de construcción y mantenimiento que revisan lo básico de escaleras y andamios antes de una clase, una obra nueva o una prueba de conocimientos en el trabajo.")],
             related='<a href="fall-protection.html">Protección contra caídas</a> · <a href="focus-four.html">Focus Four</a> · <a href="index.html">Todos los temas OSHA</a>',
             source='<a href="https://www.osha.gov/ladders" rel="noopener noreferrer" target="_blank">OSHA escaleras</a> (29 CFR 1926 Subparte X y reglas relacionadas de andamios). Preguntas originales; no copiadas de un curso comercial.'),
        dict(folder="osha", slug="ppe.html", quiz="ppe", n=18, og=lander_og_osha,
             title="Cuestionario de EPP — estudio OSHA (no es una tarjeta)",
             desc="Cuestionario gratis de 18 preguntas sobre equipo de protección personal: jerarquía de controles, pago del empleador y clasificaciones ANSI. Estudio independiente. No es una tarjeta OSHA.",
             eyebrow="OSHA · Tema de obra", h1="Cuestionario de EPP",
             lede="Repase cuándo se necesita equipo de protección personal, quién lo paga y cómo se relaciona con la jerarquía de controles en la obra.",
             meta="18 preguntas · Unos 6 minutos · Última revisión: 31 de agosto de 2026",
             edu="Solo práctica educativa. Este cuestionario no es capacitación OSHA y no otorga una tarjeta ni certificación OSHA.",
             cta="Empezar el cuestionario de 18 preguntas", share="Cuestionario gratis de EPP. Estudio independiente — no es una tarjeta OSHA.",
             covers=["Jerarquía de controles y por qué el EPP es el último recurso",
                     "Cuándo el empleador debe pagar el EPP",
                     "Clasificaciones ANSI comunes para protección de ojos, cabeza y pies",
                     "Ajuste, inspección y cuándo retirar el equipo dañado"],
             faqs=[("¿Este es un examen oficial de OSHA?", "No. Solo práctica original. Una tarjeta OSHA 10 o 30 la emite un instructor autorizado de Outreach."),
                   ("¿Para quién es?", "Trabajadores y supervisores que quieren revisar reglas de EPP en lenguaje sencillo antes de una clase o una obra nueva.")],
             related='<a href="fall-protection.html">Protección contra caídas</a> · <a href="hazard-communication.html">HazCom</a> · <a href="index.html">Todos los temas OSHA</a>',
             source='<a href="https://www.osha.gov/ppe" rel="noopener noreferrer" target="_blank">OSHA EPP</a> (29 CFR 1910.132 y 1926 Subparte E). Preguntas originales; no copiadas de un curso comercial.'),
        dict(folder="osha", slug="hazard-communication.html", quiz="hazcom", n=18, og=lander_og_osha,
             title="Cuestionario de comunicación de peligros — estudio GHS / SDS (no es una tarjeta)",
             desc="Cuestionario gratis de 18 preguntas sobre comunicación de peligros: GHS, SDS y pictogramas. Estudio independiente. No es una tarjeta OSHA.",
             eyebrow="OSHA · Tema de obra", h1="Cuestionario de comunicación de peligros",
             lede="Repase etiquetas GHS, hojas de datos de seguridad (SDS) y derechos del trabajador para entender los productos químicos en el trabajo.",
             meta="18 preguntas · Unos 6 minutos · Última revisión: 31 de agosto de 2026",
             edu="Solo práctica educativa. Este cuestionario no es capacitación OSHA y no otorga una tarjeta ni certificación OSHA.",
             cta="Empezar el cuestionario de 18 preguntas", share="Cuestionario gratis de HazCom. Estudio independiente — no es una tarjeta OSHA.",
             covers=["Las 16 secciones de una SDS y dónde encontrar primeros auxilios y EPP",
                     "Pictogramas GHS y palabras de aviso",
                     "Etiquetado secundario y contenedores de trabajo",
                     "Derechos del trabajador a información sobre productos químicos"],
             faqs=[("¿Este es un examen oficial de OSHA?", "No. Solo práctica original. No copia un examen del DOL y no emite una tarjeta."),
                   ("¿Para quién es?", "Cualquiera que maneje productos químicos en la obra o en un taller y quiera revisar GHS y SDS antes de una clase.")],
             related='<a href="ppe.html">EPP</a> · <a href="lockout-tagout.html">LOTO</a> · <a href="index.html">Todos los temas OSHA</a>',
             source='<a href="https://www.osha.gov/hazcom" rel="noopener noreferrer" target="_blank">OSHA Hazard Communication</a> (29 CFR 1910.1200). Preguntas originales; no copiadas de un curso comercial.'),
        dict(folder="osha", slug="focus-four.html", quiz="focusFour", n=15, og=lander_og_osha,
             title="Cuestionario Focus Four — estudio de peligros de construcción OSHA",
             desc="Cuestionario gratis de 15 preguntas sobre el Focus Four de construcción: caídas, golpes, atrapamientos y electrocución. Estudio independiente. No es una tarjeta OSHA.",
             eyebrow="OSHA · Tema de obra", h1="Cuestionario Focus Four",
             lede="Repase los cuatro peligros principales de construcción que OSHA destaca en Outreach: caídas, golpes por objetos, atrapamientos y electrocución.",
             meta="15 preguntas · Unos 5 minutos · Última revisión: 31 de agosto de 2026",
             edu="Solo práctica educativa. Este cuestionario no es capacitación OSHA y no otorga una tarjeta ni certificación OSHA.",
             cta="Empezar el cuestionario de 15 preguntas", share="Cuestionario gratis Focus Four. Estudio independiente — no es una tarjeta OSHA.",
             covers=["Por qué las caídas siguen siendo la causa principal de muertes en construcción",
                     "Golpes por cargas, tráfico y herramientas",
                     "Atrapamientos en zanjas, entre equipos y en espacios estrechos",
                     "Electrocución, distancias a líneas y GFCI"],
             faqs=[("¿Este es un examen oficial de OSHA?", "No. Solo práctica original para estudiar los temas del Focus Four antes de una clase de Outreach."),
                   ("¿Para quién es?", "Trabajadores de construcción y aprendices que se preparan para OSHA 10 o 30.")],
             related='<a href="fall-protection.html">Protección contra caídas</a> · <a href="excavation.html">Excavación</a> · <a href="electrical.html">Eléctrico</a> · <a href="index.html">Todos los temas OSHA</a>',
             source='<a href="https://www.osha.gov/construction" rel="noopener noreferrer" target="_blank">OSHA Construction</a>. Preguntas originales; no copiadas de un curso comercial.'),
        dict(folder="osha", slug="excavation.html", quiz="excavation", n=18, og=lander_og_osha,
             title="Cuestionario de excavación y zanjas — estudio OSHA",
             desc="Cuestionario gratis de 18 preguntas sobre excavación: regla de 5 pies, tipos de suelo y escombro. Estudio independiente. No es una tarjeta OSHA.",
             eyebrow="OSHA · Tema de obra", h1="Cuestionario de excavación y zanjas",
             lede="Repase protección de zanjas, tipos de suelo, colocación de escombro y cuándo se necesita una persona competente.",
             meta="18 preguntas · Unos 6 minutos · Última revisión: 31 de agosto de 2026",
             edu="Solo práctica educativa. Este cuestionario no es capacitación OSHA y no otorga una tarjeta ni certificación OSHA.",
             cta="Empezar el cuestionario de 18 preguntas", share="Cuestionario gratis de excavación y zanjas. Estudio independiente — no es una tarjeta OSHA.",
             covers=["Regla general de 5 pies y cuándo se exige protección",
                     "Tipos de suelo y sistemas de protección",
                     "Escombro a por lo menos 2 pies del borde",
                     "Persona competente, medios de salida y atmósfera"],
             faqs=[("¿Este es un examen oficial de OSHA?", "No. Solo práctica original. Una tarjeta OSHA sigue requiriendo un instructor autorizado."),
                   ("¿Para quién es?", "Cuadrillas de excavación, operadores y supervisores que revisan números de zanjas antes de una clase o una obra.")],
             related='<a href="focus-four.html">Focus Four</a> · <a href="fall-protection.html">Protección contra caídas</a> · <a href="index.html">Todos los temas OSHA</a>',
             source='<a href="https://www.osha.gov/trenching-excavation" rel="noopener noreferrer" target="_blank">OSHA trenching</a> (29 CFR 1926 Subparte P). Preguntas originales; no copiadas de un curso comercial.'),
        dict(folder="osha", slug="electrical.html", quiz="electrical", n=18, og=lander_og_osha,
             title="Cuestionario de seguridad eléctrica — estudio OSHA (no es una tarjeta)",
             desc="Cuestionario gratis de 18 preguntas sobre seguridad eléctrica: regla de 10 pies, GFCI y 50 voltios. Estudio independiente. No es una tarjeta OSHA.",
             eyebrow="OSHA · Tema de obra", h1="Cuestionario de seguridad eléctrica",
             lede="Repase distancias a líneas energizadas, GFCI, umbrales de 50 voltios y prácticas de obra alrededor de energía eléctrica.",
             meta="18 preguntas · Unos 6 minutos · Última revisión: 31 de agosto de 2026",
             edu="Solo práctica educativa. Este cuestionario no es capacitación OSHA y no otorga una tarjeta ni certificación OSHA.",
             cta="Empezar el cuestionario de 18 preguntas", share="Cuestionario gratis de seguridad eléctrica. Estudio independiente — no es una tarjeta OSHA.",
             covers=["Regla de 10 pies cerca de líneas aéreas y distancias mayores a más voltaje",
                     "GFCI en obras y herramientas portátiles",
                     "El umbral de 50 voltios y LOTO eléctrico",
                     "Cables dañados, tierra y trabajo en húmedo"],
             faqs=[("¿Este es un examen oficial de OSHA?", "No. Solo práctica original. No emite una tarjeta OSHA."),
                   ("¿Para quién es?", "Electricistas, ayudantes y cualquier persona de obra que trabaje cerca de energía y quiera revisar las cifras clave.")],
             related='<a href="lockout-tagout.html">LOTO</a> · <a href="focus-four.html">Focus Four</a> · <a href="index.html">Todos los temas OSHA</a>',
             source='<a href="https://www.osha.gov/electrical" rel="noopener noreferrer" target="_blank">OSHA electrical</a> (29 CFR 1910 Subparte S y 1926 Subparte K). Preguntas originales; no copiadas de un curso comercial.'),
        dict(folder="osha", slug="lockout-tagout.html", quiz="loto", n=18, og=lander_og_osha,
             title="Cuestionario de bloqueo y etiquetado — estudio LOTO OSHA (no es una tarjeta)",
             desc="Cuestionario gratis de 18 preguntas sobre LOTO: control de energía, verificación y LOTO grupal. Estudio independiente. No es una tarjeta OSHA.",
             eyebrow="OSHA · Tema de obra", h1="Cuestionario de bloqueo / etiquetado",
             lede="Repase el control de energía peligrosa, verificación de cero energía y reglas de LOTO grupal usadas en mantenimiento e industria general.",
             meta="18 preguntas · Unos 6 minutos · Última revisión: 31 de agosto de 2026",
             edu="Solo práctica educativa. Este cuestionario no es capacitación OSHA y no otorga una tarjeta ni certificación OSHA.",
             cta="Empezar el cuestionario de 18 preguntas", share="Cuestionario gratis de LOTO. Estudio independiente — no es una tarjeta OSHA.",
             covers=["Cuándo aplica 1910.147 frente a trabajo eléctrico en vivo",
                     "Aislar, bloquear, etiquetar y verificar",
                     "Dispositivos personales frente a LOTO grupal",
                     "Excepciones de recableado menor y trabajo de producción"],
             faqs=[("¿Este es un examen oficial de OSHA?", "No. Solo práctica original. Una tarjeta OSHA 10 o 30 la emite un instructor autorizado de Outreach."),
                   ("¿Para quién es?", "Personal de mantenimiento, operadores y supervisores que revisan LOTO antes de una clase o un procedimiento en planta.")],
             related='<a href="electrical.html">Eléctrico</a> · <a href="ppe.html">EPP</a> · <a href="index.html">Todos los temas OSHA</a>',
             source='<a href="https://www.osha.gov/control-hazardous-energy" rel="noopener noreferrer" target="_blank">OSHA LOTO</a> (29 CFR 1910.147). Preguntas originales; no copiadas de un curso comercial.'),
        dict(folder="cdl", slug="general-knowledge.html", quiz="general", n=50, og=f"{ORIGIN}/img/og-default.jpg",
             title="Cuestionario de conocimientos generales CDL de California — no oficial",
             desc="Práctica gratis de conocimientos generales para CDL de California. Ítems originales al estilo del manual. No son preguntas oficiales del DMV.",
             eyebrow="CDL de California", h1="Cuestionario de conocimientos generales",
             lede="Repase conducción segura, espacio, carga, emergencias, inspecciones y reglas comerciales de California antes del permiso del DMV.",
             meta="50 preguntas en el laboratorio · Última revisión: 31 de agosto de 2026",
             edu="Solo práctica educativa. Esto no es un examen del DMV y no otorga una CDL.",
             cta="Empezar el cuestionario de conocimientos generales", share="Práctica no oficial de conocimientos generales CDL de California. No son preguntas del DMV ni una licencia.",
             covers=["Conducción segura, adelantamientos y espacio",
                     "Inspecciones, emergencias y carga",
                     "Reglas comerciales de California en el manual público",
                     "Cómo este banco se relaciona con el permiso, no con el examen oficial"],
             faqs=[("¿Estas son preguntas oficiales del DMV?", "No. Práctica original al estilo del manual. Solo el DMV de California emite una CDL y administra los exámenes oficiales."),
                   ("¿Qué debo estudiar después?", "Siga con <a href=\"air-brakes.html\">frenos de aire</a> y <a href=\"combination-vehicles.html\">vehículos combinados</a>.")],
             related='<a href="air-brakes.html">Frenos de aire</a> · <a href="combination-vehicles.html">Vehículos combinados</a> · <a href="index.html">Todo el laboratorio CDL</a>',
             source='<a href="https://www.dmv.ca.gov/portal/driver-handbooks/" rel="noopener noreferrer" target="_blank">Manual de conductores comerciales de California</a>. Preguntas originales; no copiadas del examen del DMV.'),
        dict(folder="cdl", slug="air-brakes.html", quiz="airBrakes", n=25, og=f"{ORIGIN}/img/og-default.jpg",
             title="Cuestionario de frenos de aire CDL de California — no oficial",
             desc="Práctica gratis de frenos de aire para CDL de California. No son preguntas oficiales del DMV.",
             eyebrow="CDL de California", h1="Cuestionario de frenos de aire",
             lede="Repase partes del sistema, presiones, pruebas de fugas, frenos de resorte, ABS e inspecciones antes del examen de endoso de frenos de aire.",
             meta="25 preguntas en el laboratorio · Última revisión: 31 de agosto de 2026",
             edu="Solo práctica educativa. Esto no es un examen del DMV y no otorga una CDL.",
             cta="Empezar el cuestionario de frenos de aire", share="Práctica no oficial de frenos de aire CDL de California. No son preguntas del DMV.",
             covers=["Compresor, tanques, secador y válvulas",
                     "Presiones de corte y de corte inferior",
                     "Pruebas de fugas y frenos de resorte",
                     "ABS y qué hacer si una luz de advertencia se enciende"],
             faqs=[("¿Estas son preguntas oficiales del DMV?", "No. Práctica original al estilo del manual. Solo el DMV emite una CDL."),
                   ("¿Para quién es?", "Solicitantes de Clase A y B que necesitan el conocimiento de frenos de aire antes del mostrador del DMV.")],
             related='<a href="general-knowledge.html">Conocimientos generales</a> · <a href="combination-vehicles.html">Vehículos combinados</a> · <a href="index.html">Todo el laboratorio CDL</a>',
             source='<a href="https://www.dmv.ca.gov/portal/driver-handbooks/" rel="noopener noreferrer" target="_blank">Manual de conductores comerciales de California</a>. Preguntas originales; no copiadas del examen del DMV.'),
        dict(folder="cdl", slug="combination-vehicles.html", quiz="combination", n=20, og=f"{ORIGIN}/img/og-default.jpg",
             title="Cuestionario de vehículos combinados CDL de California — no oficial",
             desc="Práctica gratis de vehículos combinados para CDL de California. No son preguntas oficiales del DMV.",
             eyebrow="CDL de California", h1="Cuestionario de vehículos combinados",
             lede="Repase quinta rueda, acoplamiento, líneas de aire, desvío, volcaduras y tijera antes del examen de combinación.",
             meta="20 preguntas en el laboratorio · Última revisión: 31 de agosto de 2026",
             edu="Solo práctica educativa. Esto no es un examen del DMV y no otorga una CDL.",
             cta="Empezar el cuestionario de vehículos combinados", share="Práctica no oficial de vehículos combinados CDL de California. No son preguntas del DMV.",
             covers=["Inspección y bloqueo de la quinta rueda",
                     "Líneas de aire, válvulas de cierre y líneas cruzadas",
                     "Desvío, volcaduras y tijera",
                     "Acoplar y desacoplar en el orden correcto"],
             faqs=[("¿Estas son preguntas oficiales del DMV?", "No. Práctica original al estilo del manual. Solo el DMV emite una CDL."),
                   ("¿Qué debo estudiar primero?", "Empiece con <a href=\"general-knowledge.html\">conocimientos generales</a>, luego frenos de aire y este cuestionario.")],
             related='<a href="general-knowledge.html">Conocimientos generales</a> · <a href="air-brakes.html">Frenos de aire</a> · <a href="index.html">Todo el laboratorio CDL</a>',
             source='<a href="https://www.dmv.ca.gov/portal/driver-handbooks/" rel="noopener noreferrer" target="_blank">Manual de conductores comerciales de California</a>. Preguntas originales; no copiadas del examen del DMV.'),
        dict(folder="cpr", slug="adult-cpr.html", quiz="adultCpr", n=20, og=f"{ORIGIN}/img/og-default.jpg",
             title="Cuestionario de RCP en adultos — repaso de conocimientos (no es una tarjeta)",
             desc="Cuestionario gratis de RCP en adultos: frecuencia, profundidad, 30:2 y recoíl. No es certificación de AHA ni Cruz Roja.",
             eyebrow="RCP/DEA", h1="Cuestionario de RCP en adultos",
             lede="Repase las cifras de RCP de alta calidad en adultos antes de una clase de destrezas. Esto no es consejo médico y no sustituye la práctica con un instructor.",
             meta="Cuestionario del laboratorio · Última revisión: 31 de agosto de 2026",
             edu="Solo práctica educativa. Esto no es consejo médico ni una certificación. En una emergencia, llame al 911.",
             cta="Empezar el cuestionario de RCP en adultos", share="Repaso gratis de RCP en adultos. No es una tarjeta de certificación.",
             covers=["Frecuencia 100–120 y profundidad de al menos 2 pulgadas",
                     "Relación 30:2 y recoíl completo",
                     "Chequeo de pulso de 10 segundos y minimizar pausas",
                     "Cuándo iniciar RCP y cuándo usar un DEA"],
             faqs=[("¿Este cuestionario me certifica en RCP?", "No. Una tarjeta requiere un instructor autorizado y una sesión de destrezas. En una emergencia, llame al 911."),
                   ("¿Por dónde empiezo después?", "Siga con el <a href=\"aed.html\">cuestionario de DEA</a>.")],
             related='<a href="aed.html">DEA</a> · <a href="index.html">Todo el laboratorio RCP/DEA</a>',
             source='<a href="https://cpr.heart.org/" rel="noopener noreferrer" target="_blank">American Heart Association CPR</a> · <a href="https://www.redcross.org/take-a-class" rel="noopener noreferrer" target="_blank">Clases de la Cruz Roja</a>. No estamos afiliados a ninguno.'),
        dict(folder="cpr", slug="aed.html", quiz="aed", n=20, og=f"{ORIGIN}/img/og-default.jpg",
             title="Cuestionario de DEA — repaso de conocimientos (no es una tarjeta)",
             desc="Cuestionario gratis de DEA: parches, descarga y situaciones especiales. No es certificación de AHA ni Cruz Roja.",
             eyebrow="RCP/DEA", h1="Cuestionario de DEA",
             lede="Repase encender el aparato, colocar parches, despejar, descargar si lo indica y reanudar RCP de inmediato.",
             meta="Cuestionario del laboratorio · Última revisión: 31 de agosto de 2026",
             edu="Solo práctica educativa. Esto no es consejo médico ni una certificación. En una emergencia, llame al 911.",
             cta="Empezar el cuestionario de DEA", share="Repaso gratis de DEA. No es una tarjeta de certificación.",
             covers=["Secuencia: encender, parches, despejar, descargar, RCP",
                     "Parches de adulto frente a pediátricos",
                     "Pecho mojado, parches de medicamento y marcapasos",
                     "No demorar la RCP por el DEA"],
             faqs=[("¿Esto me da una tarjeta de RCP?", "No. Busque una clase de destrezas con AHA o Cruz Roja. No estamos afiliados a ninguno."),
                   ("¿Qué debo estudiar primero?", "Empiece con <a href=\"adult-cpr.html\">RCP en adultos</a>, luego este cuestionario.")],
             related='<a href="adult-cpr.html">RCP en adultos</a> · <a href="index.html">Todo el laboratorio RCP/DEA</a>',
             source='<a href="https://cpr.heart.org/" rel="noopener noreferrer" target="_blank">American Heart Association CPR</a>. Preguntas originales; no copiadas de un examen de certificación.'),
    ]
    for item in landers:
        write(ES / item["folder"] / item["slug"], lander_html(item))

    # Guide landers
    simple_page(
        "osha-10-practice.html",
        "Examen de práctica OSHA 10 gratis (808 preguntas) — no es una tarjeta OSHA",
        "Examen de práctica OSHA 10 y OSHA 30: 808 preguntas originales sobre protección contra caídas, Focus Four, EPP y más. No es un examen oficial de OSHA ni una tarjeta Outreach. Última revisión 31 de agosto de 2026.",
        "Estudio de temas OSHA",
        "Examen de práctica OSHA 10 gratis",
        [
            '<p class="banner">Prepárese para conceptos de cursos OSHA Outreach. Esto no es un examen oficial de OSHA y no emite una tarjeta.</p>',
            '<p class="lede">808 ítems originales de opción múltiple sobre conceptos comunes de seguridad en construcción e industria general, basados en las normas públicas 29 CFR 1910 y 1926. Para trabajadores de construcción, supervisores y estudiantes de cursos OSHA. Pagar aquí no lo certifica.</p>',
            "<p>Para quién es: personas que estudian antes de una clase autorizada de Outreach. Qué cubre: Focus Four, caídas, escaleras, zanjas, electricidad, EPP, HazCom y bancos de temas relacionados.</p>",
            '<p><a class="btn" href="osha/">Empezar el laboratorio de temas OSHA</a></p>',
            '<p>Cuestionarios por tema: <a href="osha/fall-protection.html">Protección contra caídas</a> · <a href="osha/focus-four.html">Focus Four</a> · <a href="osha/ladder-safety.html">Seguridad en escaleras</a> · <a href="osha/excavation.html">Excavación</a> · <a href="osha/electrical.html">Eléctrico</a> · <a href="osha/ppe.html">EPP</a> · <a href="osha/lockout-tagout.html">Bloqueo / etiquetado</a> · <a href="osha/hazard-communication.html">Comunicación de peligros</a></p>',
            '<p class="edu-bar">Aviso de uso educativo: Este material es solo para fines educativos y de estudio general. No es capacitación oficial del gobierno ni OSHA Outreach. No otorga una tarjeta, certificado ni garantía de aprobar. Confirme los requisitos actuales con su empleador o proveedor de capacitación. <a href="disclaimer.html">Aviso legal completo</a> · <a href="contact.html">¿Ve un error? Avísenos.</a></p>',
            '<section class="faq" aria-labelledby="osha-guide-faq"><h2 id="osha-guide-faq">Preguntas frecuentes</h2><details><summary>¿Este es un examen oficial de OSHA 10?</summary><p>No. Solo práctica original. Una tarjeta de 10 o 30 horas la da un instructor autorizado de Outreach después de las horas requeridas.</p></details><details><summary>¿Es gratis?</summary><p>Sí. Empiece con una mezcla de 10 preguntas o un cuestionario de tema como <a href="osha/fall-protection.html">protección contra caídas</a>.</p></details></section>',
            '<section class="price sources"><h2>Fuente oficial</h2><p><a href="https://www.osha.gov/training/outreach" rel="noopener noreferrer" target="_blank">Programa de capacitación OSHA Outreach</a> — los instructores autorizados emiten tarjetas, no este sitio. <span class="reviewed">Última revisión: 31 de agosto de 2026.</span></p></section>',
            '<p class="disclaimer-quiet"><a href="support.html">Mantenga Safety Test Prep gratis — apoyo opcional</a></p>',
        ],
    )
    simple_page(
        "california-cdl-practice.html",
        "Examen de práctica CDL de California gratis — conocimientos generales, frenos de aire y combinación",
        "Examen de práctica CDL de California para conocimientos generales, frenos de aire y vehículos combinados. Ítems originales basados en el manual. No son preguntas oficiales del DMV.",
        "Conocimientos de CDL",
        "Examen de práctica CDL de California gratis",
        [
            '<p class="banner">Preparación para el examen de conocimientos de conductor comercial. Solo el DMV de California emite una CDL.</p>',
            '<p class="lede">Estudie conocimientos generales, frenos de aire y vehículos combinados antes de sentarse en el DMV. Ítems originales basados en el manual público de conductores comerciales de California — no preguntas oficiales del DMV. Pagar aquí no lo aprueba y no salta el DMV.</p>',
            "<p>Para quién es: estudiantes de permiso y solicitantes de licencia comercial. Qué cubre: práctica de conocimientos basada en el manual, incluidos fundamentos de frenos de aire y vehículos combinados.</p>",
            '<p><a class="btn" href="cdl/">Empezar el laboratorio de conocimientos CDL</a></p>',
            '<p>Cuestionarios por tema: <a href="cdl/general-knowledge.html">Conocimientos generales</a> · <a href="cdl/air-brakes.html">Frenos de aire</a> · <a href="cdl/combination-vehicles.html">Vehículos combinados</a></p>',
            '<p class="edu-bar">Aviso de uso educativo: Este material es solo para fines educativos y de estudio general. No es capacitación oficial del DMV ni de licencias. No otorga una licencia ni garantía de aprobar. Verifique los requisitos actuales con el DMV de California. <a href="disclaimer.html">Aviso legal completo</a> · <a href="contact.html">¿Ve un error? Avísenos.</a></p>',
            '<section class="faq"><h2>Preguntas frecuentes</h2><details><summary>¿Estas son preguntas oficiales del DMV?</summary><p>No. Práctica original al estilo del manual. Solo el DMV de California emite una CDL y administra los exámenes oficiales.</p></details><details><summary>¿Qué debo estudiar primero?</summary><p>Empiece con <a href="cdl/general-knowledge.html">conocimientos generales</a>, luego <a href="cdl/air-brakes.html">frenos de aire</a> y <a href="cdl/combination-vehicles.html">vehículos combinados</a>.</p></details></section>',
            '<section class="price sources"><h2>Fuente oficial</h2><p><a href="https://www.dmv.ca.gov/portal/driver-handbooks/" rel="noopener noreferrer" target="_blank">Manual de conductores comerciales de California</a>. <span class="reviewed">Última revisión: 31 de agosto de 2026.</span></p></section>',
            '<p class="disclaimer-quiet"><a href="support.html">Mantenga Safety Test Prep gratis — apoyo opcional</a></p>',
        ],
    )
    simple_page(
        "cpr-aed-practice.html",
        "Examen de práctica de RCP y DEA gratis (435 preguntas) — no es una certificación",
        "Examen de práctica de RCP y DEA: 435 preguntas originales sobre RCP en adultos, uso del DEA, atragantamiento y primeros auxilios. No es certificación de AHA ni Cruz Roja.",
        "RCP/DEA",
        "Examen de práctica de RCP y DEA gratis",
        [
            '<p class="banner">Solo repaso de conocimientos de RCP/DEA. Una tarjeta requiere un instructor autorizado y una sesión de destrezas.</p>',
            '<p class="lede">435 ítems originales para quienes repasan RCP en adultos, niños y lactantes, uso del DEA y atragantamiento antes de una clase de destrezas. Esto no es consejo médico y no sustituye la capacitación práctica. Pagar aquí no lo certifica. En una emergencia, llame al 911.</p>',
            "<p>Para quién es: estudiantes que se preparan para un curso reconocido de RCP/DEA. Qué cubre: cadena de supervivencia, compresiones, pasos del DEA y repaso de conocimientos relacionados.</p>",
            '<p><a class="btn" href="cpr/">Empezar el laboratorio de RCP/DEA</a></p>',
            '<p>Cuestionarios por tema: <a href="cpr/adult-cpr.html">RCP en adultos</a> · <a href="cpr/aed.html">DEA</a></p>',
            '<p class="edu-bar">Aviso de uso educativo: Este material es solo para fines educativos y de estudio general. No es certificación de RCP/DEA, consejo médico ni un sustituto de capacitación con instructor. No otorga una tarjeta ni garantía de aprobar. <a href="disclaimer.html">Aviso legal completo</a> · <a href="contact.html">¿Ve un error? Avísenos.</a></p>',
            '<section class="faq"><h2>Preguntas frecuentes</h2><details><summary>¿Esto me da una tarjeta de RCP?</summary><p>No. Busque una clase de destrezas con la American Heart Association o la Cruz Roja. No estamos afiliados a ninguno.</p></details><details><summary>¿Por dónde empiezo?</summary><p>Empiece con <a href="cpr/adult-cpr.html">RCP en adultos</a>, luego el <a href="cpr/aed.html">cuestionario de DEA</a>.</p></details></section>',
            '<section class="price sources"><h2>Capacitación autorizada (no nosotros)</h2><p><a href="https://cpr.heart.org/" rel="noopener noreferrer" target="_blank">RCP de la American Heart Association</a> · <a href="https://www.redcross.org/take-a-class" rel="noopener noreferrer" target="_blank">Clases de la Cruz Roja</a>. No estamos afiliados a ninguno. <span class="reviewed">Última revisión: 31 de agosto de 2026.</span></p></section>',
            '<p class="disclaimer-quiet"><a href="support.html">Mantenga Safety Test Prep gratis — apoyo opcional</a></p>',
        ],
    )

    study_help(
        "osha",
        "Práctica de temas OSHA — no es una tarjeta de certificación",
        "Este laboratorio es ayuda de estudio no oficial sobre temas de OSHA. No emite una tarjeta de Outreach del DOL.",
        "Ayuda de estudio · no es una tarjeta",
        "Cómo se permite que exista este laboratorio OSHA",
        "Una tarjeta de 10 o 30 horas solo la emite un instructor autorizado de OSHA Outreach después de las horas requeridas. Este sitio es solo práctica.",
        "Solo uso educativo. No es capacitación OSHA Outreach ni una tarjeta de finalización.",
        """      <h2>Lo que puede decirle a la gente (y a Google)</h2>
      <p>Cuestionarios de <strong>práctica</strong> sobre temas de OSHA y estudio de seguridad en el trabajo. Preguntas originales basadas en 29 CFR 1910 y 1926. No son ítems oficiales del DOL. Úselo para prepararse para conceptos de cursos OSHA Outreach.</p>
      <h2>Lo que no puede decir</h2>
      <p>No diga que esto es un examen oficial de OSHA, un cuestionario certificado por OSHA, ni que pagar aquí obtiene una tarjeta. No use el logotipo de OSHA ni del DOL.</p>
      <h2>Aviso específico de OSHA</h2>
      <p>Safety Test Prep no está afiliado, respaldado ni autorizado por OSHA ni el Departamento de Trabajo de EE. UU. La capacitación Outreach es voluntaria. Las tarjetas de finalización solo se emiten por instructores autorizados. <a href="https://www.osha.gov/training/outreach" rel="noopener noreferrer" target="_blank">Programa de capacitación OSHA Outreach</a>.</p>
      <p><a href="index.html">Empezar un cuestionario de práctica</a> · <a href="../contact.html">¿Ve un error? Avísenos.</a></p>""",
    )
    study_help(
        "cdl",
        "Recursos de práctica CDL de California — no es el examen del DMV",
        "Preparación no oficial para el examen de conocimientos CDL Clase A de California. No son preguntas del DMV. Pagar aquí no emite una licencia.",
        "Ayuda de estudio · no es una licencia",
        "Cómo se permite que exista este laboratorio CDL",
        "Ítems originales basados en el manual de conductores comerciales de California. No son preguntas oficiales del DMV. Solo el DMV emite una CDL.",
        "Solo uso educativo. No es un examen del DMV ni una licencia.",
        """      <h2>Lo que puede decirle a la gente (y a Google)</h2>
      <p>Recursos de <strong>práctica de CDL</strong> de California para conocimientos generales, frenos de aire y vehículos combinados. Estudie para el permiso. Luego tome el examen real en el DMV.</p>
      <h2>Lo que no puede decir</h2>
      <p>No diga que esto es el examen oficial del DMV, que nosotros lo aprobamos, o que pagar salta el DMV. No use sellos del DMV ni “CDL garantizada”.</p>
      <h2>Aviso específico de CDL</h2>
      <p>Los requisitos varían por estado y pueden cambiar. No estamos afiliados a ningún DMV. Siempre verifique con la agencia oficial de licencias. <a href="https://www.dmv.ca.gov/portal/driver-handbooks/" rel="noopener noreferrer" target="_blank">Manual de conductores comerciales de California</a>.</p>
      <p><a href="index.html">Empezar un cuestionario de práctica</a> · <a href="../contact.html">¿Ve un error? Avísenos.</a></p>""",
    )
    study_help(
        "cpr",
        "Repaso de conocimientos de RCP/DEA — no es una tarjeta de AHA ni Cruz Roja",
        "Repaso no oficial de conocimientos de RCP/DEA. No es certificación de la American Heart Association ni de la Cruz Roja.",
        "Ayuda de estudio · no es una tarjeta",
        "Cómo se permite que exista este laboratorio de RCP",
        "Ítems originales sobre fundamentos de respuesta a emergencias. No son preguntas oficiales de AHA ni de la Cruz Roja. Una tarjeta requiere una sesión de destrezas con un instructor autorizado.",
        "Solo uso educativo. No es consejo médico ni un curso de certificación. En una emergencia, llame al 911.",
        """      <h2>Lo que puede decirle a la gente (y a Google)</h2>
      <p><strong>Repaso de conocimientos</strong> de RCP/DEA gratis. Úselo para estudiar antes de una clase real. Esto no sustituye las destrezas prácticas.</p>
      <h2>Lo que no puede decir</h2>
      <p>No diga que esto es certificación oficial de AHA o Cruz Roja, que queda certificado después de pagar, o que puede saltarse a un instructor. No use esos logotipos. No presente esto como consejo médico.</p>
      <h2>Aviso específico de RCP/DEA</h2>
      <p>El contenido es solo repaso educativo general. En una emergencia, llame al 911 o a su número local de emergencias y siga las instrucciones del despachador. Busque una clase de destrezas con un proveedor autorizado — no estamos afiliados a AHA ni a la Cruz Roja.</p>
      <p><a href="index.html">Empezar un cuestionario de práctica</a> · <a href="../contact.html">¿Ve un error? Avísenos.</a></p>""",
    )

    lab_from_english(ROOT / "osha" / "index.html", ES / "osha" / "index.html", "osha", OSHA_PAIRS)
    lab_from_english(ROOT / "cdl" / "index.html", ES / "cdl" / "index.html", "cdl", CDL_PAIRS)
    lab_from_english(ROOT / "cpr" / "index.html", ES / "cpr" / "index.html", "cpr", CPR_PAIRS)

    sitemap()
    print("Wrote Spanish pages under", ES)
    print("html files", len(list(ES.rglob("*.html"))))


if __name__ == "__main__":
    main()
