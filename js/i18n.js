(function () {
  var lang = (document.documentElement.getAttribute("lang") || "en").toLowerCase();
  window.STP_LANG = lang.indexOf("es") === 0 ? "es" : "en";

  window.STP_UI = {
    en: {
      question: "Question",
      of: "of",
      score: "Score",
      pass: "Pass",
      keepStudying: "Keep studying",
      yourAnswer: "Your answer: ",
      correct: "Correct: ",
      missedReview: "Missed-question review",
      next: "Next",
      copied: "Copied",
      copy: "Copy",
      linkCopied: "Link copied",
      copyLinkBelow: "Copy the link below",
      copyThisLink: "Copy this link",
      tapReveal: "Tap to reveal",
      tapHide: "Tap to hide answer",
      noCards: "No cards left in this filter. Reset “Got it” cards by choosing All.",
      zeroCards: "0 cards in this filter",
      inBank: " in bank",
      oshaResult:
        "Review the explanations below, then try another quiz or a different topic. This is independent practice only. A 10- or 30-hour card can only be issued by an authorized Outreach trainer.",
      cdlNeed:
        "You need {n} correct (80%). Official DMV tests are separate by subject; this set is for practice only.",
      cprNeed:
        "You need {n} correct (about 84% on AHA written exams). The skills test is given by an authorized instructor; this set is practice only and does not issue a card.",
      supportCash: "Support Safety Test Prep — $9.99 via Cash App",
      supportHome: "Keep Safety Test Prep free — optional support",
      supportEyebrow: "Keep the lab open",
      supportVince:
        "I’m Vince. I built Safety Test Prep to make practical safety study tools easier to access for workers, job seekers, and people entering the trades.",
      supportOptional: "Payment is optional. If you cannot contribute right now, keep studying.",
      supportDoesNot: "Support does not purchase ",
      supportCashNote:
        "Cash App: {tag}. Note: Safety Test Prep support. The account may display as Andy Lau until the display name is updated.",
      supportNotLive: "Cash App is not enabled yet.",
      supportOshaBody:
        "You used original OSHA-topic questions, answer explanations, and flashcards—without an account or paywall. Safety Test Prep is free to use. If this quiz helped you prepare for work, training, or a new role, optional support of $9.99 helps fund research, question writing, review, and updates.",
      supportCdlBody:
        "You used original handbook-based CDL practice questions and explanations—without an account or paywall. Safety Test Prep is free to use. If this quiz helped you prepare, optional support of $9.99 helps fund research, question writing, review, and updates.",
      supportCprBody:
        "You used original CPR/AED knowledge-review questions and explanations—without an account or paywall. Safety Test Prep is free to use. If this quiz helped you prepare, optional support of $9.99 helps fund research, question writing, review, and updates."
    },
    es: {
      question: "Pregunta",
      of: "de",
      score: "Puntaje",
      pass: "Aprobado",
      keepStudying: "Siga estudiando",
      yourAnswer: "Su respuesta: ",
      correct: "Correcta: ",
      missedReview: "Repaso de preguntas falladas",
      next: "Siguiente",
      copied: "Copiado",
      copy: "Copiar",
      linkCopied: "Enlace copiado",
      copyLinkBelow: "Copie el enlace de abajo",
      copyThisLink: "Copie este enlace",
      tapReveal: "Toque para ver la respuesta",
      tapHide: "Toque para ocultar la respuesta",
      noCards: "No quedan tarjetas en este filtro. Elija Todas para volver a ver las que marcó “Ya lo sé”.",
      zeroCards: "0 tarjetas en este filtro",
      inBank: " en el banco",
      oshaResult:
        "Revise las explicaciones y luego pruebe otro cuestionario. Esto es práctica independiente. Una tarjeta de 10 o 30 horas solo la emite un instructor autorizado de Outreach.",
      cdlNeed:
        "Necesita {n} correctas (80%). Los exámenes oficiales del DMV son por materia; este conjunto es solo práctica.",
      cprNeed:
        "Necesita {n} correctas (cerca del 84% en los exámenes escritos de AHA). La prueba de destrezas la da un instructor autorizado; este conjunto es solo práctica y no emite una tarjeta.",
      supportCash: "Apoye Safety Test Prep — $9.99 por Cash App",
      supportHome: "Mantenga Safety Test Prep gratis — apoyo opcional",
      supportEyebrow: "Mantenga el laboratorio abierto",
      supportVince:
        "Soy Vince. Creé Safety Test Prep para que las herramientas de estudio de seguridad sean más fáciles de usar para trabajadores, personas que buscan empleo y quienes entran a los oficios.",
      supportOptional: "El pago es opcional. Si no puede aportar ahora, siga estudiando.",
      supportDoesNot: "El apoyo no compra ",
      supportCashNote:
        "Cash App: {tag}. Nota: apoyo a Safety Test Prep. La cuenta puede aparecer como Andy Lau hasta que se actualice el nombre.",
      supportNotLive: "Cash App aún no está activado.",
      supportOshaBody:
        "Usó preguntas originales sobre temas de OSHA, explicaciones y tarjetas — sin cuenta ni muro de pago. Safety Test Prep es gratis. Si este cuestionario le ayudó a prepararse para el trabajo, una capacitación o un puesto nuevo, un apoyo opcional de $9.99 financia investigación, redacción, revisión y actualizaciones.",
      supportCdlBody:
        "Usó preguntas originales de CDL basadas en el manual, con explicaciones — sin cuenta ni muro de pago. Safety Test Prep es gratis. Si este cuestionario le ayudó a prepararse, un apoyo opcional de $9.99 financia investigación, redacción, revisión y actualizaciones.",
      supportCprBody:
        "Usó preguntas originales de repaso de RCP/DEA, con explicaciones — sin cuenta ni muro de pago. Safety Test Prep es gratis. Si este cuestionario le ayudó a prepararse, un apoyo opcional de $9.99 financia investigación, redacción, revisión y actualizaciones."
    }
  };

  window.STP_BANKS = {
    en: {
      osha: {
        all: "All questions ({n})",
        intro: "Introduction to OSHA",
        focusFour: "Focus Four",
        fallProtection: "Fall Protection",
        ladders: "Ladders & Scaffolds",
        stairways: "Stairways",
        excavation: "Excavation & Trenching",
        electrical: "Electrical Safety",
        ppe: "PPE",
        hazcom: "Hazard Communication",
        loto: "Lockout / Tagout",
        materials: "Cranes, Rigging & Materials",
        tools: "Hand & Power Tools",
        health: "Health Hazards",
        fire: "Fire & Emergency Action",
        walking: "Walking-Working Surfaces",
        confined: "Confined Spaces",
        forklift: "Powered Industrial Trucks",
        hazwoper: "HAZWOPER",
        bloodborne: "Bloodborne Pathogens",
        welding: "Welding & Hot Work",
        steel: "Steel Erection",
        concrete: "Concrete & Masonry",
        respiratory: "Respiratory Protection",
        machineguard: "Machine Guarding",
        aerial: "Aerial Lifts / MEWPs",
        demolition: "Demolition",
        recordkeeping: "Recordkeeping (1904)",
        firstaid: "Medical & First Aid",
        psm: "Process Safety Management",
        sanitation: "Sanitation",
        signs: "Signs, Signals & Barricades",
        vehicles: "Motor Vehicles & Equipment",
        ergonomics: "Ergonomics"
      },
      cdl: {
        all: "All questions ({n})",
        general: "General Knowledge",
        airBrakes: "Air Brakes",
        combination: "Combination Vehicles",
        pretrip: "Pre-Trip",
        doubles: "Doubles / Triples",
        tanker: "Tank Vehicles",
        hazmat: "Hazardous Materials",
        passenger: "Passenger"
      },
      cpr: {
        all: "All questions ({n})",
        chain: "Chain of Survival",
        adultCpr: "Adult CPR",
        aed: "AED",
        childCpr: "Child CPR",
        infantCpr: "Infant CPR",
        airway: "Airway & Rescue Breaths",
        choking: "Choking / FBAO",
        team: "Team CPR",
        blsSpecial: "Special Situations",
        firstAid: "First Aid",
        ppe: "PPE & Bloodborne Pathogens",
        legal: "Legal, Consent & When to Stop"
      }
    },
    es: {
      osha: {
        all: "Todas las preguntas ({n})",
        intro: "Introducción a OSHA",
        focusFour: "Focus Four",
        fallProtection: "Protección contra caídas",
        ladders: "Escaleras y andamios",
        stairways: "Escaleras fijas",
        excavation: "Excavación y zanjas",
        electrical: "Seguridad eléctrica",
        ppe: "EPP",
        hazcom: "Comunicación de peligros",
        loto: "Bloqueo / etiquetado (LOTO)",
        materials: "Grúas, aparejos y materiales",
        tools: "Herramientas manuales y eléctricas",
        health: "Peligros para la salud",
        fire: "Incendio y plan de emergencia",
        walking: "Superficies de trabajo",
        confined: "Espacios confinados",
        forklift: "Montacargas / PIT",
        hazwoper: "HAZWOPER",
        bloodborne: "Patógenos sanguíneos",
        welding: "Soldadura y trabajo en caliente",
        steel: "Montaje de acero",
        concrete: "Concreto y mampostería",
        respiratory: "Protección respiratoria",
        machineguard: "Protección de máquinas",
        aerial: "Plataformas aéreas / MEWP",
        demolition: "Demolición",
        recordkeeping: "Registros (1904)",
        firstaid: "Médico y primeros auxilios",
        psm: "Gestión de seguridad de procesos",
        sanitation: "Saneamiento",
        signs: "Señales y barricadas",
        vehicles: "Vehículos y equipo",
        ergonomics: "Ergonomía"
      },
      cdl: {
        all: "Todas las preguntas ({n})",
        general: "Conocimientos generales",
        airBrakes: "Frenos de aire",
        combination: "Vehículos combinados",
        pretrip: "Inspección previa",
        doubles: "Dobles / triples",
        tanker: "Tanques",
        hazmat: "Materiales peligrosos",
        passenger: "Pasajeros"
      },
      cpr: {
        all: "Todas las preguntas ({n})",
        chain: "Cadena de supervivencia",
        adultCpr: "RCP en adultos",
        aed: "DEA",
        childCpr: "RCP en niños",
        infantCpr: "RCP en lactantes",
        airway: "Vía aérea y ventilaciones",
        choking: "Atragantamiento / OVACE",
        team: "RCP en equipo",
        blsSpecial: "Situaciones especiales",
        firstAid: "Primeros auxilios",
        ppe: "EPP y patógenos sanguíneos",
        legal: "Legal, consentimiento y cuándo detenerse"
      }
    }
  };

  window.stpT = function (key) {
    var pack = window.STP_UI[window.STP_LANG] || window.STP_UI.en;
    return pack[key] || window.STP_UI.en[key] || key;
  };

  window.stpBankLabel = function (lab, key, count) {
    var lang = window.STP_LANG || "en";
    var pack = (window.STP_BANKS[lang] && window.STP_BANKS[lang][lab]) || window.STP_BANKS.en[lab] || {};
    var label = pack[key] || (window.STP_BANKS.en[lab] && window.STP_BANKS.en[lab][key]) || key;
    if (count != null) label = String(label).replace("{n}", String(count));
    return label;
  };
})();
