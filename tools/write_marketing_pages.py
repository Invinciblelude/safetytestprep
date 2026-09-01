#!/usr/bin/env python3
"""Generate English and Spanish marketing/SEO landers."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ORIGIN = "https://safetytestprep.com"


def json_esc(s):
    return (
        s.replace("\\", "\\\\")
        .replace('"', '\\"')
        .replace("\n", " ")
    )


def faq_schema(items, lang):
    ents = []
    for q, a in items:
        ents.append(
            '{"@type":"Question","name":"%s","acceptedAnswer":{"@type":"Answer","text":"%s"}}'
            % (json_esc(q), json_esc(a))
        )
    return ",".join(ents)


def breadcrumbs(slug, name, lang):
    home = ORIGIN + ("/es/" if lang == "es" else "/")
    home_name = "Inicio" if lang == "es" else "Home"
    url = ORIGIN + ("/es/" if lang == "es" else "/") + slug
    return (
        '{"@type":"BreadcrumbList","itemListElement":['
        '{"@type":"ListItem","position":1,"name":"%s","item":"%s"},'
        '{"@type":"ListItem","position":2,"name":"%s","item":"%s"}]}'
        % (json_esc(home_name), home, json_esc(name), url)
    )


def render(lang, slug, title, desc, h1, eyebrow, lede, banner, body, faqs, og="og-osha.jpg"):
    is_es = lang == "es"
    prefix = "../" if is_es else ""
    loc = ORIGIN + ("/es/" + slug if is_es else "/" + slug)
    en = ORIGIN + "/" + slug
    es = ORIGIN + "/es/" + slug
    locale = "es_US" if is_es else "en_US"
    skip = "Saltar al contenido" if is_es else "Skip to content"
    edu = (
        'Aviso de uso educativo: Este material es solo para estudio general. No es capacitación oficial de OSHA, Cal/OSHA, el DMV ni una certificación de RCP. No emite tarjeta, licencia ni garantiza un aprobado. <a href="disclaimer.html">Aviso completo</a> · <a href="contact.html">¿Ve un error?</a>'
        if is_es
        else 'Educational-use notice: This material is for general study only. It is not official OSHA, Cal/OSHA, DMV, or CPR training. It does not issue a card, license, or guaranteed pass. <a href="disclaimer.html">Full disclaimer</a> · <a href="contact.html">See an error?</a>'
    )
    faq_h = "Preguntas frecuentes" if is_es else "Common questions"
    faq_id = slug.replace(".html", "") + "-faq"
    faq_html = []
    for q, a in faqs:
        faq_html.append(
            "<details><summary>%s</summary><p>%s</p></details>" % (q, a)
        )
    schema = (
        '{"@context":"https://schema.org","@graph":['
        '{"@type":"WebPage","name":"%s","url":"%s","inLanguage":"%s","isPartOf":{"@id":"%s/#website"},'
        '"about":{"@type":"Thing","name":"Safety Test Prep"},'
        '"description":"%s"},'
        "%s,"
        '{"@type":"FAQPage","mainEntity":[%s]}]}'
        % (
            json_esc(title),
            loc,
            "es-US" if is_es else "en-US",
            ORIGIN,
            json_esc(desc),
            breadcrumbs(slug, h1, lang),
            faq_schema(faqs, lang),
        )
    )
    return f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{title}</title>
  <meta name="description" content="{desc}" />
  <link rel="canonical" href="{loc}" />
  <meta name="theme-color" content="#1d4e89" />
  <link rel="icon" href="{prefix}img/favicon.svg" type="image/svg+xml" />
  <meta property="og:type" content="website" />
  <meta property="og:site_name" content="Safety Test Prep" />
  <meta property="og:locale" content="{locale}" />
  <meta property="og:title" content="{title}" />
  <meta property="og:description" content="{desc}" />
  <meta property="og:url" content="{loc}" />
  <meta property="og:image" content="{ORIGIN}/img/{og}" />
  <meta property="og:image:width" content="1200" />
  <meta property="og:image:height" content="675" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{title}" />
  <meta name="twitter:description" content="{desc}" />
  <meta name="twitter:image" content="{ORIGIN}/img/{og}" />
  <link rel="stylesheet" href="{prefix}css/site.css" />
  <script type="application/ld+json">
  {schema}
  </script>
</head>
<body>
  <a class="skip" href="#main">{skip}</a>
  <div class="wrap" id="main">
    <nav data-stp-nav></nav>
    <p class="banner">{banner}</p>
    <p class="eyebrow">{eyebrow}</p>
    <h1>{h1}</h1>
    <p class="lede">{lede}</p>
{body}
    <p class="edu-bar">{edu}</p>
    <section class="faq" aria-labelledby="{faq_id}">
      <h2 id="{faq_id}">{faq_h}</h2>
      {"".join(faq_html)}
    </section>
    <p class="disclaimer-quiet"><a href="support.html">{'Mantenga Safety Test Prep gratis — apoyo opcional' if is_es else 'Keep Safety Test Prep free — optional support'}</a></p>
    <footer data-stp-footer></footer>
  </div>
  <script src="{prefix}js/chrome.js"></script>
</body>
</html>
"""


PAGES = []


def add(slug, en, es):
    PAGES.append((slug, en, es))


add(
    "what-we-are.html",
    dict(
        title="What Safety Test Prep is — and is not | Independent practice, not a card",
        desc="Safety Test Prep is free independent OSHA, California CDL, and CPR/AED practice. It is not OSHA Outreach, Cal/OSHA training, a DMV test, or a certification.",
        og="og-default.jpg",
        h1="What this site is, and what it is not",
        eyebrow="Credibility",
        banner="Independent educational practice. Not affiliated with OSHA, Cal/OSHA, the California DMV, AHA, or the Red Cross.",
        lede="Use this page when you share the site with a crew, a school, or a staffing office. One sentence: free original quizzes so people can study before a class, a permit, or a skills session — not a credential.",
        body="""
    <section class="price">
      <h2>What we are</h2>
      <p>A free study lab built in Sacramento by Vince. Original multiple-choice questions and flashcards for OSHA-topic knowledge, California CDL handbook knowledge, and CPR/AED fundamentals. English and Spanish. No account. No pass guarantee.</p>
    </section>
    <section class="price">
      <h2>What we are not</h2>
      <ul class="cover-list">
        <li>Not OSHA Outreach training and not an OSHA 10 or 30 card</li>
        <li>Not Cal/OSHA-required employer training, an IIPP, or a heat-illness program</li>
        <li>Not the California DMV knowledge test and not a commercial license</li>
        <li>Not an AHA or Red Cross CPR/AED certification</li>
        <li>Not a replacement for the authorized instructor, the skills session, or the employer’s site-specific training</li>
      </ul>
    </section>
    <section class="price">
      <h2>California notes</h2>
      <p>Federal OSHA and Cal/OSHA are not the same rulebook. Trigger heights, heat illness, and some construction rules differ in California. These quizzes teach common concepts. Your employer still owns the training that applies to <em>your</em> site. Confirm current rules with <a href="https://www.dir.ca.gov/dosh/" rel="noopener noreferrer" target="_blank">Cal/OSHA (DIR)</a> and <a href="https://www.osha.gov/training/outreach" rel="noopener noreferrer" target="_blank">federal OSHA Outreach</a>.</p>
    </section>
    <p class="btns">
      <a class="btn" href="trades.html">Practice by trade</a>
      <a class="btn ghost" href="for-teams.html">For employers and schools</a>
    </p>
""",
        faqs=[
            (
                "Can this site certify me?",
                "No. Only an authorized Outreach trainer, the California DMV, or an authorized CPR instructor can issue those credentials.",
            ),
            (
                "Is Outreach training required by OSHA?",
                "OSHA Outreach (the 10- and 30-hour classes) is voluntary education. Employers still must train workers on the hazards of their jobs. A card is not a license to skip that.",
            ),
        ],
    ),
    dict(
        title="Qué es Safety Test Prep — y qué no es | Práctica independiente, no una tarjeta",
        desc="Safety Test Prep es práctica independiente y gratis de OSHA, CDL de California y RCP/DEA. No es OSHA Outreach, capacitación de Cal/OSHA, un examen del DMV ni una certificación.",
        og="og-default.jpg",
        h1="Qué es este sitio, y qué no es",
        eyebrow="Credibilidad",
        banner="Práctica educativa independiente. No estamos afiliados a OSHA, Cal/OSHA, el DMV de California, AHA ni la Cruz Roja.",
        lede="Use esta página cuando comparta el sitio con un equipo, una escuela o una agencia de empleo. Una frase: cuestionarios originales y gratis para estudiar antes de una clase, un permiso o una sesión de destrezas — no una credencial.",
        body="""
    <section class="price">
      <h2>Qué somos</h2>
      <p>Un laboratorio de estudio gratis hecho en Sacramento por Vince. Preguntas originales y tarjetas sobre temas de OSHA, el manual de CDL de California y fundamentos de RCP/DEA. Inglés y español. Sin cuenta. Sin garantía de aprobado.</p>
    </section>
    <section class="price">
      <h2>Qué no somos</h2>
      <ul class="cover-list">
        <li>No somos capacitación OSHA Outreach ni una tarjeta OSHA 10 o 30</li>
        <li>No somos la capacitación que Cal/OSHA exige al empleador, un IIPP ni un programa de enfermedad por calor</li>
        <li>No somos el examen de conocimientos del DMV de California ni una licencia comercial</li>
        <li>No somos una certificación de RCP/DEA de AHA o de la Cruz Roja</li>
        <li>No sustituimos al instructor autorizado, la sesión de destrezas ni la capacitación específica del empleador</li>
      </ul>
    </section>
    <section class="price">
      <h2>Notas de California</h2>
      <p>OSHA federal y Cal/OSHA no son el mismo reglamento. Las alturas de disparo, la enfermedad por calor y algunas reglas de construcción difieren en California. Estos cuestionarios enseñan conceptos comunes. Su empleador sigue siendo dueño de la capacitación que aplica a <em>su</em> obra. Confirme las reglas vigentes con <a href="https://www.dir.ca.gov/dosh/" rel="noopener noreferrer" target="_blank">Cal/OSHA (DIR)</a> y <a href="https://www.osha.gov/training/outreach" rel="noopener noreferrer" target="_blank">OSHA Outreach federal</a>.</p>
    </section>
    <p class="btns">
      <a class="btn" href="trades.html">Práctica por oficio</a>
      <a class="btn ghost" href="for-teams.html">Para empleadores y escuelas</a>
    </p>
""",
        faqs=[
            (
                "¿Este sitio me certifica?",
                "No. Solo un instructor Outreach autorizado, el DMV de California o un instructor autorizado de RCP puede emitir esas credenciales.",
            ),
            (
                "¿OSHA exige la capacitación Outreach?",
                "OSHA Outreach (las clases de 10 y 30 horas) es educación voluntaria. El empleador igual debe capacitar a los trabajadores sobre los peligros de su trabajo. Una tarjeta no es licencia para saltarse eso.",
            ),
        ],
    ),
)

add(
    "trades.html",
    dict(
        title="Free OSHA Practice by Trade — Roofing, Electrical, HVAC &amp; Construction",
        desc="Free OSHA-topic practice quizzes grouped by trade: roofing, construction laborers, electricians, HVAC, and plumbing. Independent study — not a card.",
        h1="Free OSHA practice by trade",
        eyebrow="California trades",
        banner="Study the hazards of your work. This is independent practice, not the employer training Cal/OSHA still requires.",
        lede="OSHA quizzes on this site are organized by hazard. These pages point roofers, laborers, electricians, and HVAC/plumbing apprentices to the quizzes that match the work.",
        body="""
    <div class="grid cols-2">
      <article>
        <p class="card-kicker">Roofing</p>
        <h2>Roofers</h2>
        <p>Fall protection, ladders, and Focus Four before a roof or solar install.</p>
        <p style="margin-top:14px"><a class="btn" href="roofing-safety-practice.html">Roofing practice</a></p>
      </article>
      <article>
        <p class="card-kicker">Construction</p>
        <h2>Laborers &amp; first-day crews</h2>
        <p>Focus Four, trenches, PPE, and ladders for orientation study.</p>
        <p style="margin-top:14px"><a class="btn" href="construction-laborer-practice.html">Laborer practice</a></p>
      </article>
      <article>
        <p class="card-kicker">Electrical</p>
        <h2>Electricians</h2>
        <p>Electrical hazards, lockout/tagout, GFCI concepts, and PPE.</p>
        <p style="margin-top:14px"><a class="btn" href="electrician-safety-practice.html">Electrician practice</a></p>
      </article>
      <article>
        <p class="card-kicker">Mechanical</p>
        <h2>HVAC &amp; plumbing</h2>
        <p>LOTO, electrical, ladders, and confined-space awareness in the full bank.</p>
        <p style="margin-top:14px"><a class="btn" href="hvac-plumbing-safety-practice.html">HVAC &amp; plumbing</a></p>
      </article>
    </div>
    <section class="price">
      <h2>Also on this site</h2>
      <p><a href="california-cdl-practice.html">California CDL knowledge practice</a> for commercial drivers. <a href="cpr-aed-practice.html">CPR/AED practice</a> before a skills class. <a href="for-teams.html">Employers, staffing agencies, and trade schools</a> can send one link to a whole crew.</p>
    </section>
""",
        faqs=[
            (
                "Is this trade-specific OSHA training?",
                "No. These pages route you into existing OSHA-topic quizzes. They are not a substitute for employer or union training for your craft.",
            ),
            (
                "Do you have a Spanish version?",
                "Yes. Use the ES switch in the header, or open the same page under /es/.",
            ),
        ],
    ),
    dict(
        title="Práctica OSHA gratis por oficio — techado, eléctrico, HVAC y construcción",
        desc="Cuestionarios gratis de temas OSHA agrupados por oficio: techado, peones de construcción, electricistas, HVAC y plomería. Estudio independiente: no es una tarjeta.",
        h1="Práctica OSHA gratis por oficio",
        eyebrow="Oficios de California",
        banner="Estudie los peligros de su trabajo. Esto es práctica independiente, no la capacitación que Cal/OSHA sigue exigiendo al empleador.",
        lede="Los cuestionarios de OSHA en este sitio se organizan por peligro. Estas páginas dirigen a techadores, peones, electricistas y aprendices de HVAC/plomería a los cuestionarios que coinciden con el trabajo.",
        body="""
    <div class="grid cols-2">
      <article>
        <p class="card-kicker">Techado</p>
        <h2>Techadores</h2>
        <p>Protección contra caídas, escaleras y Focus Four antes de un techo o una instalación solar.</p>
        <p style="margin-top:14px"><a class="btn" href="roofing-safety-practice.html">Práctica de techado</a></p>
      </article>
      <article>
        <p class="card-kicker">Construcción</p>
        <h2>Peones y primer día</h2>
        <p>Focus Four, zanjas, EPP y escaleras para el estudio de orientación.</p>
        <p style="margin-top:14px"><a class="btn" href="construction-laborer-practice.html">Práctica de peón</a></p>
      </article>
      <article>
        <p class="card-kicker">Eléctrico</p>
        <h2>Electricistas</h2>
        <p>Peligros eléctricos, bloqueo/etiquetado, conceptos de GFCI y EPP.</p>
        <p style="margin-top:14px"><a class="btn" href="electrician-safety-practice.html">Práctica de electricista</a></p>
      </article>
      <article>
        <p class="card-kicker">Mecánico</p>
        <h2>HVAC y plomería</h2>
        <p>LOTO, eléctrico, escaleras y conciencia de espacios confinados en el banco completo.</p>
        <p style="margin-top:14px"><a class="btn" href="hvac-plumbing-safety-practice.html">HVAC y plomería</a></p>
      </article>
    </div>
    <section class="price">
      <h2>También en este sitio</h2>
      <p><a href="california-cdl-practice.html">Práctica de conocimientos de CDL de California</a> para conductores comerciales. <a href="cpr-aed-practice.html">Práctica de RCP/DEA</a> antes de una clase de destrezas. <a href="for-teams.html">Empleadores, agencias de empleo y escuelas de oficios</a> pueden enviar un enlace a todo el equipo.</p>
    </section>
""",
        faqs=[
            (
                "¿Esto es capacitación OSHA específica del oficio?",
                "No. Estas páginas lo llevan a cuestionarios existentes de temas OSHA. No sustituyen la capacitación del empleador o del sindicato para su oficio.",
            ),
            (
                "¿Hay versión en español?",
                "Sí. Use el interruptor ES en el encabezado, o abra la misma página en /es/.",
            ),
        ],
    ),
)

add(
    "roofing-safety-practice.html",
    dict(
        title="Roofing OSHA Practice Test — Free Fall Protection Quiz for Roofers",
        desc="Free roofing safety practice: fall protection, ladders, and Focus Four. Independent OSHA-topic study for roofers and solar crews in California. Not a card.",
        h1="Roofing OSHA practice test",
        eyebrow="Roofers · solar · framing",
        banner="Falls are the leading construction killer. This is practice, not a roofing certification and not Cal/OSHA-required employer training.",
        lede="Free original quizzes for people who work on roofs, solar arrays, and elevated decks. Start with fall protection, then ladders and the construction Focus Four. Paying here does not certify you.",
        body="""
    <p>Who it is for: new roofers, solar installers, and helpers who want to review fall hazards before a class or a first week on a California roof. What it covers: guardrails, personal fall arrest basics, ladder setup, and the Focus Four (falls, struck-by, caught-in/between, electrocution).</p>
    <p class="btns">
      <a class="btn" href="osha/fall-protection.html">Start fall protection (15 questions)</a>
      <a class="btn ghost" href="osha/ladder-safety.html">Ladder safety</a>
      <a class="btn ghost" href="osha/focus-four.html">Focus Four</a>
    </p>
    <section class="price">
      <h2>Three questions every new roofer should be able to answer</h2>
      <ol class="cover-list">
        <li>When is fall protection required on your site — and who decides that? Federal OSHA construction rules and Cal/OSHA Title 8 are not always the same trigger height. Confirm with your competent person.</li>
        <li>What is the difference between a guardrail system and a personal fall-arrest system? One keeps you from going over. The other is meant to stop a fall after it starts.</li>
        <li>What is the ladder 4:1 setup rule, and when is a ladder the wrong tool for a roof edge?</li>
      </ol>
      <p>Work those in the quizzes below, then read the explanation. Do not treat a practice score as permission to skip the harness your employer issued.</p>
    </section>
    <p>Related: <a href="osha/ppe.html">PPE</a> · <a href="osha-10-practice.html">Full OSHA 10/30 practice bank</a> · <a href="what-we-are.html">What this site is not</a></p>
    <section class="price sources">
      <h2>Official sources</h2>
      <p><a href="https://www.osha.gov/fall-protection" rel="noopener noreferrer" target="_blank">OSHA fall protection</a> · <a href="https://www.dir.ca.gov/dosh/" rel="noopener noreferrer" target="_blank">Cal/OSHA</a> · <span class="reviewed">Last reviewed: September 1, 2026.</span></p>
    </section>
""",
        faqs=[
            (
                "Is this a roofing OSHA 10 test?",
                "No. It is independent practice on fall and ladder topics roofers need. An OSHA 10 card still comes from an authorized Outreach trainer after the required hours.",
            ),
            (
                "Does California use the same 6-foot rule as federal OSHA?",
                "Not always. Cal/OSHA Title 8 can set different trigger heights and extra rules. Use the quiz for concepts, then confirm the number that applies to your employer and city.",
            ),
        ],
    ),
    dict(
        title="Examen de práctica OSHA para techado — cuestionario gratis de protección contra caídas",
        desc="Práctica gratis de seguridad en techado: protección contra caídas, escaleras y Focus Four. Estudio independiente de temas OSHA para techadores y cuadrillas solares en California. No es una tarjeta.",
        h1="Examen de práctica OSHA para techado",
        eyebrow="Techadores · solar · armazón",
        banner="Las caídas son la principal causa de muerte en construcción. Esto es práctica, no una certificación de techado ni la capacitación que Cal/OSHA exige al empleador.",
        lede="Cuestionarios originales y gratis para quienes trabajan en techos, sistemas solares y plataformas elevadas. Empiece con protección contra caídas, luego escaleras y el Focus Four de construcción. Pagar aquí no lo certifica.",
        body="""
    <p>Para quién: techadores nuevos, instaladores solares y ayudantes que quieren repasar peligros de caídas antes de una clase o la primera semana en un techo de California. Qué cubre: barandales, conceptos básicos de arresto personal de caídas, colocación de escaleras y el Focus Four (caídas, golpes, atrapamientos, electrocución).</p>
    <p class="btns">
      <a class="btn" href="osha/fall-protection.html">Empezar protección contra caídas (15 preguntas)</a>
      <a class="btn ghost" href="osha/ladder-safety.html">Seguridad en escaleras</a>
      <a class="btn ghost" href="osha/focus-four.html">Focus Four</a>
    </p>
    <section class="price">
      <h2>Tres preguntas que todo techador nuevo debería poder responder</h2>
      <ol class="cover-list">
        <li>¿Cuándo se exige protección contra caídas en su obra — y quién lo decide? Las reglas federales de OSHA para construcción y el Título 8 de Cal/OSHA no siempre usan la misma altura de disparo. Confírmelo con su persona competente.</li>
        <li>¿Cuál es la diferencia entre un sistema de barandales y un sistema personal de arresto de caídas? Uno evita que usted se vaya. El otro está pensado para detener una caída después de que empieza.</li>
        <li>¿Cuál es la regla 4:1 de las escaleras, y cuándo una escalera es la herramienta equivocada para el borde de un techo?</li>
      </ol>
      <p>Trabaje esas preguntas en los cuestionarios de abajo y lea la explicación. Un puntaje de práctica no es permiso para saltarse el arnés que le dio su empleador.</p>
    </section>
    <p>Relacionado: <a href="osha/ppe.html">EPP</a> · <a href="osha-10-practice.html">Banco completo de práctica OSHA 10/30</a> · <a href="what-we-are.html">Qué no es este sitio</a></p>
    <section class="price sources">
      <h2>Fuentes oficiales</h2>
      <p><a href="https://www.osha.gov/fall-protection" rel="noopener noreferrer" target="_blank">Protección contra caídas de OSHA</a> · <a href="https://www.dir.ca.gov/dosh/" rel="noopener noreferrer" target="_blank">Cal/OSHA</a> · <span class="reviewed">Última revisión: 1 de septiembre de 2026.</span></p>
    </section>
""",
        faqs=[
            (
                "¿Esto es un examen OSHA 10 de techado?",
                "No. Es práctica independiente sobre caídas y escaleras que necesitan los techadores. Una tarjeta OSHA 10 sigue saliendo de un instructor Outreach autorizado después de las horas exigidas.",
            ),
            (
                "¿California usa la misma regla de 6 pies que OSHA federal?",
                "No siempre. El Título 8 de Cal/OSHA puede fijar otras alturas de disparo y reglas extra. Use el cuestionario para los conceptos y confirme el número que aplica a su empleador y ciudad.",
            ),
        ],
    ),
)

add(
    "construction-laborer-practice.html",
    dict(
        title="Construction Laborer OSHA Practice — Free Focus Four &amp; First-Day Quiz",
        desc="Free OSHA practice for construction laborers and first-day crews: Focus Four, trenches, PPE, and ladders. Independent study — not orientation and not a card.",
        h1="Construction laborer OSHA practice",
        eyebrow="Laborers · helpers · first day",
        banner="Use this before orientation or an OSHA 10 class. It does not replace your employer’s site-specific training.",
        lede="Free original quizzes for general laborers, helpers, and anyone walking a California jobsite for the first time. Start with the Focus Four, then trenches, PPE, and ladders.",
        body="""
    <p>Who it is for: new hires, staffing-agency temps, and pre-apprentices who need plain-language practice before a toolbox talk or Outreach class. What it covers: the four leading construction killers, excavation basics, personal protective equipment, and ladder use.</p>
    <p class="btns">
      <a class="btn" href="osha/focus-four.html">Start Focus Four</a>
      <a class="btn ghost" href="osha/excavation.html">Excavation / trenching</a>
      <a class="btn ghost" href="osha/ppe.html">PPE</a>
      <a class="btn ghost" href="osha/ladder-safety.html">Ladders</a>
    </p>
    <section class="price">
      <h2>First-day study order</h2>
      <ol class="cover-list">
        <li>Focus Four — so you can name the hazards that kill the most construction workers</li>
        <li>Fall protection — even if you are not a roofer, ladders and openings are still on the site</li>
        <li>Excavation — if your crew digs, cave-ins are not a “someone else’s” problem</li>
        <li>The full OSHA lab — 808 questions when you want a longer mix before an OSHA 10 course</li>
      </ol>
      <p>California outdoor crews also need heat-illness training from the employer. That required training is not this website. This is homework you can do tonight.</p>
    </section>
    <p>Related: <a href="osha-10-practice.html">OSHA 10 practice test</a> · <a href="for-teams.html">Send this to a whole crew</a> · <a href="what-we-are.html">What we are not</a></p>
    <section class="price sources">
      <h2>Official sources</h2>
      <p><a href="https://www.osha.gov/construction" rel="noopener noreferrer" target="_blank">OSHA construction</a> · <a href="https://www.dir.ca.gov/dosh/HeatIllnessInfo.html" rel="noopener noreferrer" target="_blank">Cal/OSHA heat illness</a> · <span class="reviewed">Last reviewed: September 1, 2026.</span></p>
    </section>
""",
        faqs=[
            (
                "Does this count as new-hire orientation?",
                "No. Orientation, IIPP, and heat-illness training are the employer’s job. This is optional knowledge practice.",
            ),
            (
                "How many questions are in the OSHA lab?",
                "808 original questions and 143 flashcards. Topic quizzes such as Focus Four are shorter.",
            ),
        ],
    ),
    dict(
        title="Práctica OSHA para peones de construcción — Focus Four y primer día, gratis",
        desc="Práctica OSHA gratis para peones de construcción y cuadrillas de primer día: Focus Four, zanjas, EPP y escaleras. Estudio independiente: no es orientación ni una tarjeta.",
        h1="Práctica OSHA para peones de construcción",
        eyebrow="Peones · ayudantes · primer día",
        banner="Úselo antes de la orientación o de una clase OSHA 10. No sustituye la capacitación específica del empleador.",
        lede="Cuestionarios originales y gratis para peones, ayudantes y cualquiera que camine una obra de California por primera vez. Empiece con el Focus Four, luego zanjas, EPP y escaleras.",
        body="""
    <p>Para quién: contratados nuevos, temporales de agencia y preaprendices que necesitan práctica en lenguaje sencillo antes de una plática de seguridad o una clase Outreach. Qué cubre: las cuatro causas principales de muerte en construcción, conceptos de excavación, equipo de protección personal y uso de escaleras.</p>
    <p class="btns">
      <a class="btn" href="osha/focus-four.html">Empezar Focus Four</a>
      <a class="btn ghost" href="osha/excavation.html">Excavación / zanjas</a>
      <a class="btn ghost" href="osha/ppe.html">EPP</a>
      <a class="btn ghost" href="osha/ladder-safety.html">Escaleras</a>
    </p>
    <section class="price">
      <h2>Orden de estudio para el primer día</h2>
      <ol class="cover-list">
        <li>Focus Four — para nombrar los peligros que más matan en construcción</li>
        <li>Protección contra caídas — aunque no sea techador, en la obra hay escaleras y aberturas</li>
        <li>Excavación — si su cuadrilla cava, un derrumbe no es “problema de otro”</li>
        <li>El laboratorio OSHA completo — 808 preguntas cuando quiera un mix más largo antes de un curso OSHA 10</li>
      </ol>
      <p>Las cuadrillas al aire libre en California también necesitan capacitación sobre enfermedad por calor de parte del empleador. Esa capacitación exigida no es este sitio. Esto es la tarea que puede hacer esta noche.</p>
    </section>
    <p>Relacionado: <a href="osha-10-practice.html">Examen de práctica OSHA 10</a> · <a href="for-teams.html">Envíe esto a todo el equipo</a> · <a href="what-we-are.html">Qué no somos</a></p>
    <section class="price sources">
      <h2>Fuentes oficiales</h2>
      <p><a href="https://www.osha.gov/construction" rel="noopener noreferrer" target="_blank">Construcción OSHA</a> · <a href="https://www.dir.ca.gov/dosh/HeatIllnessInfo.html" rel="noopener noreferrer" target="_blank">Enfermedad por calor Cal/OSHA</a> · <span class="reviewed">Última revisión: 1 de septiembre de 2026.</span></p>
    </section>
""",
        faqs=[
            (
                "¿Esto cuenta como orientación de nuevo ingreso?",
                "No. La orientación, el IIPP y la capacitación de enfermedad por calor son trabajo del empleador. Esto es práctica opcional de conocimientos.",
            ),
            (
                "¿Cuántas preguntas hay en el laboratorio OSHA?",
                "808 preguntas originales y 143 tarjetas. Los cuestionarios por tema, como Focus Four, son más cortos.",
            ),
        ],
    ),
)

add(
    "electrician-safety-practice.html",
    dict(
        title="Electrician OSHA Practice Test — Free Electrical, LOTO &amp; GFCI Quiz",
        desc="Free electrician safety practice: electrical hazards, lockout/tagout, and PPE. Independent OSHA-topic study for apprentices — not a journeyman card.",
        h1="Electrician OSHA practice test",
        eyebrow="Electricians · apprentices",
        banner="Electrical work kills. This is knowledge practice, not NFPA 70E certification and not an OSHA card.",
        lede="Free original quizzes for electrical apprentices and helpers reviewing shock, arc, GFCI, and lockout/tagout concepts before a class or a plant job.",
        body="""
    <p>Who it is for: inside-wireman apprentices, residential helpers, and maintenance electricians who want a short written review. What it covers: electrical hazard recognition, energy control (LOTO), and related PPE. The full OSHA bank also has confined space, machine guarding, and more.</p>
    <p class="btns">
      <a class="btn" href="osha/electrical.html">Start electrical quiz</a>
      <a class="btn ghost" href="osha/lockout-tagout.html">Lockout / tagout</a>
      <a class="btn ghost" href="osha/ppe.html">PPE</a>
    </p>
    <section class="price">
      <h2>What this quiz will not do</h2>
      <p>It will not qualify you as a journey-level electrician, authorize you to work energized, or replace your employer’s LOTO procedure. If the equipment has a written energy-control procedure, that document wins — not a website score.</p>
    </section>
    <p>Related: <a href="osha/focus-four.html">Focus Four</a> (electrocution is one of the four) · <a href="osha-10-practice.html">OSHA 10/30 practice</a> · <a href="what-we-are.html">What we are not</a></p>
    <section class="price sources">
      <h2>Official sources</h2>
      <p><a href="https://www.osha.gov/electrical" rel="noopener noreferrer" target="_blank">OSHA electrical</a> · <a href="https://www.osha.gov/control-hazardous-energy" rel="noopener noreferrer" target="_blank">OSHA control of hazardous energy</a> · <span class="reviewed">Last reviewed: September 1, 2026.</span></p>
    </section>
""",
        faqs=[
            (
                "Is this the same as NFPA 70E training?",
                "No. NFPA 70E is a consensus standard used in many electrical-safety programs. This site is original OSHA-topic practice only.",
            ),
            (
                "Can I use this for an apprenticeship written test?",
                "You can use it as extra practice. It is not the official apprenticeship exam and is not affiliated with IBEW, IEC, or any JATC.",
            ),
        ],
    ),
    dict(
        title="Examen de práctica OSHA para electricistas — eléctrico, LOTO y GFCI, gratis",
        desc="Práctica gratis de seguridad para electricistas: peligros eléctricos, bloqueo/etiquetado y EPP. Estudio independiente de temas OSHA para aprendices — no es una tarjeta de oficial.",
        h1="Examen de práctica OSHA para electricistas",
        eyebrow="Electricistas · aprendices",
        banner="El trabajo eléctrico mata. Esto es práctica de conocimientos, no una certificación NFPA 70E ni una tarjeta OSHA.",
        lede="Cuestionarios originales y gratis para aprendices y ayudantes eléctricos que repasan choque, arco, GFCI y bloqueo/etiquetado antes de una clase o un trabajo en planta.",
        body="""
    <p>Para quién: aprendices de cableado interior, ayudantes residenciales y electricistas de mantenimiento que quieren un repaso escrito corto. Qué cubre: reconocimiento de peligros eléctricos, control de energía (LOTO) y EPP relacionado. El banco OSHA completo también tiene espacios confinados, resguardo de máquinas y más.</p>
    <p class="btns">
      <a class="btn" href="osha/electrical.html">Empezar cuestionario eléctrico</a>
      <a class="btn ghost" href="osha/lockout-tagout.html">Bloqueo / etiquetado</a>
      <a class="btn ghost" href="osha/ppe.html">EPP</a>
    </p>
    <section class="price">
      <h2>Lo que este cuestionario no hará</h2>
      <p>No lo calificará como electricista oficial, no lo autorizará a trabajar energizado ni sustituirá el procedimiento LOTO de su empleador. Si el equipo tiene un procedimiento escrito de control de energía, ese documento manda — no el puntaje de un sitio web.</p>
    </section>
    <p>Relacionado: <a href="osha/focus-four.html">Focus Four</a> (la electrocución es una de las cuatro) · <a href="osha-10-practice.html">Práctica OSHA 10/30</a> · <a href="what-we-are.html">Qué no somos</a></p>
    <section class="price sources">
      <h2>Fuentes oficiales</h2>
      <p><a href="https://www.osha.gov/electrical" rel="noopener noreferrer" target="_blank">Eléctrico OSHA</a> · <a href="https://www.osha.gov/control-hazardous-energy" rel="noopener noreferrer" target="_blank">Control de energía peligrosa OSHA</a> · <span class="reviewed">Última revisión: 1 de septiembre de 2026.</span></p>
    </section>
""",
        faqs=[
            (
                "¿Esto es lo mismo que la capacitación NFPA 70E?",
                "No. NFPA 70E es una norma de consenso que usan muchos programas de seguridad eléctrica. Este sitio es solo práctica original de temas OSHA.",
            ),
            (
                "¿Puedo usarlo para un examen escrito de aprendizaje?",
                "Puede usarlo como práctica extra. No es el examen oficial del aprendizaje y no está afiliado a IBEW, IEC ni a ningún JATC.",
            ),
        ],
    ),
)

add(
    "hvac-plumbing-safety-practice.html",
    dict(
        title="HVAC &amp; Plumbing OSHA Practice — Free LOTO, Electrical &amp; Ladder Quiz",
        desc="Free HVAC and plumbing safety practice: lockout/tagout, electrical hazards, and ladders. Independent OSHA-topic study for apprentices — not a license.",
        h1="HVAC and plumbing OSHA practice",
        eyebrow="HVAC · plumbing · mechanical",
        banner="Crawlspaces, rooftop units, and energized equipment are real hazards. This is practice, not a C-20 or C-36 license.",
        lede="Free original quizzes for HVAC and plumbing apprentices who need LOTO, electrical, and ladder review before a shop class or a service call.",
        body="""
    <p>Who it is for: residential and commercial mechanical apprentices, service helpers, and anyone who isolates energy on furnaces, condensers, or water heaters. What it covers: lockout/tagout, electrical shock awareness, and ladder safety. Fall protection still applies on rooftop units.</p>
    <p class="btns">
      <a class="btn" href="osha/lockout-tagout.html">Start lockout / tagout</a>
      <a class="btn ghost" href="osha/electrical.html">Electrical</a>
      <a class="btn ghost" href="osha/ladder-safety.html">Ladders</a>
      <a class="btn ghost" href="osha/fall-protection.html">Fall protection</a>
    </p>
    <section class="price">
      <h2>Why LOTO shows up on HVAC and plumbing work</h2>
      <p>If you service equipment that can start, discharge, or stay hot, energy control is part of the job — not only “the electrician’s job.” Practice the sequence here, then follow the procedure posted at your employer. Confined-space rules can also apply to tanks, vaults, and some crawlspaces; those items live in the full OSHA bank, not this short path.</p>
    </section>
    <p>Related: <a href="osha/hazard-communication.html">Hazard communication</a> · <a href="electrician-safety-practice.html">Electrician path</a> · <a href="what-we-are.html">What we are not</a></p>
    <section class="price sources">
      <h2>Official sources</h2>
      <p><a href="https://www.osha.gov/control-hazardous-energy" rel="noopener noreferrer" target="_blank">OSHA LOTO</a> · <a href="https://www.cslb.ca.gov/" rel="noopener noreferrer" target="_blank">California CSLB</a> (licenses are issued there, not here) · <span class="reviewed">Last reviewed: September 1, 2026.</span></p>
    </section>
""",
        faqs=[
            (
                "Will this help me pass a CSLB trade exam?",
                "It can help you review safety knowledge. It is not a CSLB exam prep course and does not issue a contractor license.",
            ),
            (
                "Do plumbers need fall protection practice?",
                "If you work on roofs, mezzanines, or unprotected sides, yes. Start with the fall-protection quiz, not only LOTO.",
            ),
        ],
    ),
    dict(
        title="Práctica OSHA de HVAC y plomería — LOTO, eléctrico y escaleras, gratis",
        desc="Práctica gratis de seguridad para HVAC y plomería: bloqueo/etiquetado, peligros eléctricos y escaleras. Estudio independiente de temas OSHA para aprendices — no es una licencia.",
        h1="Práctica OSHA de HVAC y plomería",
        eyebrow="HVAC · plomería · mecánico",
        banner="Los sótanos de arrastre, las unidades en techo y el equipo energizado son peligros reales. Esto es práctica, no una licencia C-20 ni C-36.",
        lede="Cuestionarios originales y gratis para aprendices de HVAC y plomería que necesitan repaso de LOTO, eléctrico y escaleras antes de una clase de taller o una llamada de servicio.",
        body="""
    <p>Para quién: aprendices mecánicos residenciales y comerciales, ayudantes de servicio y cualquiera que aísle energía en hornos, condensadores o calentadores de agua. Qué cubre: bloqueo/etiquetado, conciencia de choque eléctrico y seguridad en escaleras. La protección contra caídas sigue aplicando en unidades de techo.</p>
    <p class="btns">
      <a class="btn" href="osha/lockout-tagout.html">Empezar bloqueo / etiquetado</a>
      <a class="btn ghost" href="osha/electrical.html">Eléctrico</a>
      <a class="btn ghost" href="osha/ladder-safety.html">Escaleras</a>
      <a class="btn ghost" href="osha/fall-protection.html">Protección contra caídas</a>
    </p>
    <section class="price">
      <h2>Por qué LOTO aparece en HVAC y plomería</h2>
      <p>Si da servicio a equipo que puede arrancar, descargar o quedarse caliente, el control de energía es parte del trabajo — no solo “trabajo del electricista.” Practique la secuencia aquí y luego siga el procedimiento publicado en su empleador. Las reglas de espacios confinados también pueden aplicar a tanques, bóvedas y algunos sótanos de arrastre; esos temas están en el banco OSHA completo, no en esta ruta corta.</p>
    </section>
    <p>Relacionado: <a href="osha/hazard-communication.html">Comunicación de peligros</a> · <a href="electrician-safety-practice.html">Ruta de electricista</a> · <a href="what-we-are.html">Qué no somos</a></p>
    <section class="price sources">
      <h2>Fuentes oficiales</h2>
      <p><a href="https://www.osha.gov/control-hazardous-energy" rel="noopener noreferrer" target="_blank">LOTO OSHA</a> · <a href="https://www.cslb.ca.gov/" rel="noopener noreferrer" target="_blank">CSLB de California</a> (las licencias se emiten allá, no aquí) · <span class="reviewed">Última revisión: 1 de septiembre de 2026.</span></p>
    </section>
""",
        faqs=[
            (
                "¿Esto me ayuda a pasar un examen de oficio del CSLB?",
                "Puede ayudar a repasar conocimientos de seguridad. No es un curso de preparación del CSLB y no emite una licencia de contratista.",
            ),
            (
                "¿Los plomeros necesitan práctica de protección contra caídas?",
                "Si trabaja en techos, entrepisos o lados sin protección, sí. Empiece con el cuestionario de caídas, no solo LOTO.",
            ),
        ],
    ),
)

add(
    "for-teams.html",
    dict(
        title="Free OSHA Practice for Employers, Staffing Agencies &amp; Trade Schools",
        desc="Give your crew free OSHA, CDL, and CPR practice quizzes. Independent study resource for California contractors, staffing agencies, and trade schools. Not employer training.",
        og="og-default.jpg",
        h1="Free study resource for crews, staffing, and schools",
        eyebrow="For teams",
        banner="Send one link. People practice on their phone. You still own the required training, the IIPP, and the card if a class is required.",
        lede="Safety Test Prep is a free independent practice lab. Contractors, staffing agencies, and trade schools can point workers and students at trade pages and topic quizzes. There is no team login and no per-seat fee.",
        body="""
    <section class="price">
      <h2>The offer</h2>
      <p>Your people get free English and Spanish practice. You get a page you can put in an onboarding packet or a classroom slide. Optional: email Vince for a 10-minute call to pick the right starting quizzes for your trade. This does not replace Cal/OSHA-required employer training.</p>
      <p class="btns">
        <a class="btn" href="mailto:hello@safetytestprep.com?subject=Team%20resource%20%E2%80%94%20Safety%20Test%20Prep">Email for a team resource</a>
        <a class="btn ghost" href="trades.html">See trade pages</a>
      </p>
    </section>
    <div class="grid cols-2">
      <article>
        <h2>Contractors &amp; GCs</h2>
        <p>Share the roofing, laborer, or electrician page before a first week or an OSHA 10 course. Fall protection is the usual start for elevated work.</p>
      </article>
      <article>
        <h2>Staffing agencies</h2>
        <p>Temps often arrive without a 10-hour card. Send <a href="construction-laborer-practice.html">laborer practice</a> the night before orientation. It is homework, not your site orientation.</p>
      </article>
      <article>
        <h2>Trade schools &amp; pre-apprenticeship</h2>
        <p>Assign a topic quiz as homework. Students can switch to Spanish with one tap. You still teach the class; we do not grade transcripts.</p>
      </article>
      <article>
        <h2>What we will not do</h2>
        <p>We will not issue cards, keep a training roster, or claim your workers are “OSHA certified.” Read <a href="what-we-are.html">what we are not</a> before you post the link.</p>
      </article>
    </div>
    <section class="price">
      <h2>Links to send</h2>
      <ul class="cover-list">
        <li>Roofing crews: <a href="https://safetytestprep.com/roofing-safety-practice.html">safetytestprep.com/roofing-safety-practice.html</a></li>
        <li>New laborers: <a href="https://safetytestprep.com/construction-laborer-practice.html">safetytestprep.com/construction-laborer-practice.html</a></li>
        <li>Spanish home: <a href="https://safetytestprep.com/es/">safetytestprep.com/es/</a></li>
        <li>Full OSHA lab: <a href="https://safetytestprep.com/osha/">safetytestprep.com/osha/</a></li>
      </ul>
    </section>
    <p>Sacramento and Northern California crews: mention your trade and city in the email so the reply can point to the right quiz, not a generic dump of 808 questions.</p>
""",
        faqs=[
            (
                "Is there a team plan or roster?",
                "Not yet. Quizzes are free for everyone. Email if you want a suggested study order for your trade. Optional Cash App support does not buy seats.",
            ),
            (
                "Can this replace our OSHA 10 class?",
                "No. If you require an Outreach card, that still comes from an authorized trainer. This is unpaid study time.",
            ),
        ],
    ),
    dict(
        title="Práctica OSHA gratis para empleadores, agencias de empleo y escuelas de oficios",
        desc="Dé a su equipo cuestionarios gratis de OSHA, CDL y RCP. Recurso de estudio independiente para contratistas, agencias de empleo y escuelas de oficios de California. No es capacitación del empleador.",
        og="og-default.jpg",
        h1="Recurso de estudio gratis para cuadrillas, agencias y escuelas",
        eyebrow="Para equipos",
        banner="Envíe un enlace. La gente practica en el teléfono. Usted sigue siendo dueño de la capacitación exigida, el IIPP y la tarjeta si se exige una clase.",
        lede="Safety Test Prep es un laboratorio de práctica independiente y gratis. Contratistas, agencias de empleo y escuelas de oficios pueden dirigir a trabajadores y estudiantes a páginas de oficio y cuestionarios. No hay inicio de sesión de equipo ni cobro por asiento.",
        body="""
    <section class="price">
      <h2>La oferta</h2>
      <p>Su gente obtiene práctica gratis en inglés y español. Usted obtiene una página para el paquete de ingreso o una diapositiva. Opcional: escriba a Vince para una llamada de 10 minutos y elegir los cuestionarios de partida para su oficio. Esto no sustituye la capacitación que Cal/OSHA exige al empleador.</p>
      <p class="btns">
        <a class="btn" href="mailto:hello@safetytestprep.com?subject=Recurso%20para%20equipos%20%E2%80%94%20Safety%20Test%20Prep">Correo para un recurso de equipo</a>
        <a class="btn ghost" href="trades.html">Ver páginas de oficios</a>
      </p>
    </section>
    <div class="grid cols-2">
      <article>
        <h2>Contratistas y GCs</h2>
        <p>Comparta la página de techado, peones o electricistas antes de la primera semana o de un curso OSHA 10. La protección contra caídas suele ser el inicio para trabajo en altura.</p>
      </article>
      <article>
        <h2>Agencias de empleo</h2>
        <p>Los temporales a menudo llegan sin tarjeta de 10 horas. Envíe la <a href="construction-laborer-practice.html">práctica de peón</a> la noche antes de la orientación. Es tarea, no su orientación de obra.</p>
      </article>
      <article>
        <h2>Escuelas de oficios y preaprendizaje</h2>
        <p>Asigne un cuestionario por tema como tarea. Los estudiantes pueden pasar a español con un toque. Usted sigue impartiendo la clase; nosotros no calificamos transcripts.</p>
      </article>
      <article>
        <h2>Lo que no haremos</h2>
        <p>No emitiremos tarjetas, no guardaremos una lista de capacitación ni diremos que sus trabajadores están “certificados OSHA.” Lea <a href="what-we-are.html">qué no somos</a> antes de publicar el enlace.</p>
      </article>
    </div>
    <section class="price">
      <h2>Enlaces para enviar</h2>
      <ul class="cover-list">
        <li>Cuadrillas de techado: <a href="https://safetytestprep.com/es/roofing-safety-practice.html">safetytestprep.com/es/roofing-safety-practice.html</a></li>
        <li>Peones nuevos: <a href="https://safetytestprep.com/es/construction-laborer-practice.html">safetytestprep.com/es/construction-laborer-practice.html</a></li>
        <li>Inicio en español: <a href="https://safetytestprep.com/es/">safetytestprep.com/es/</a></li>
        <li>Laboratorio OSHA completo: <a href="https://safetytestprep.com/es/osha/">safetytestprep.com/es/osha/</a></li>
      </ul>
    </section>
    <p>Cuadrillas de Sacramento y el norte de California: mencione su oficio y ciudad en el correo para que la respuesta apunte al cuestionario correcto, no a un volcado genérico de 808 preguntas.</p>
""",
        faqs=[
            (
                "¿Hay un plan de equipo o una lista?",
                "Todavía no. Los cuestionarios son gratis para todos. Escriba si quiere un orden de estudio sugerido para su oficio. El apoyo opcional por Cash App no compra asientos.",
            ),
            (
                "¿Esto puede sustituir nuestra clase OSHA 10?",
                "No. Si usted exige una tarjeta Outreach, esa sigue saliendo de un instructor autorizado. Esto es tiempo de estudio no pagado.",
            ),
        ],
    ),
)


def main():
    for slug, en, es in PAGES:
        (ROOT / slug).write_text(render("en", slug, **en), encoding="utf-8")
        (ROOT / "es" / slug).write_text(render("es", slug, **es), encoding="utf-8")
        print("wrote", slug)


if __name__ == "__main__":
    main()
