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
      scanQr: "Scan with your wallet",
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
      unlockCta: "Unlock the full bank — $9.99",
      supportCash: "Pay $safetytestprep",
      supportHome: "Unlock the full labs — $9.99",
      supportEyebrow: "Unlock the full bank",
      supportVince:
        "I’m Vince. I built Safety Test Prep to make practical safety study tools easier to access for workers, job seekers, and people entering the trades.",
      supportOptional: "Fall protection, CDL General Knowledge, and Adult CPR stay free if you are not ready to pay.",
      supportDoesNot: "Payment does not purchase ",
      supportCashNote:
        "Cash App: {tag}. Confirm $safetytestprep and the name Safety Test Prep. Send $9.99. Bitcoin and USDT (Tron) are also accepted.",
      supportNotLive: "Cash App is not enabled yet.",
      supportOshaBody:
        "Fall protection is free. The rest of this OSHA lab — mocks, flashcards, and the 808-question bank — is $9.99 for 30 days on this device. Payment does not buy a card.",
      supportCdlBody:
        "CDL General Knowledge is free. Air Brakes, Combination, endorsements, flashcards, and the full bank are $9.99 for 30 days on this device. Payment does not buy a license.",
      supportCprBody:
        "Adult CPR is free. AED, pediatric, first aid, flashcards, and the 435-question bank are $9.99 for 30 days on this device. Payment does not buy a certification."
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
      scanQr: "Escanee con su cartera",
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
      unlockCta: "Desbloquear el banco completo — $9.99",
      supportCash: "Pagar $safetytestprep",
      supportHome: "Desbloquear los laboratorios — $9.99",
      supportEyebrow: "Desbloquear el banco completo",
      supportVince:
        "Soy Vince. Creé Safety Test Prep para que las herramientas de estudio de seguridad sean más fáciles de usar para trabajadores, personas que buscan empleo y quienes entran a los oficios.",
      supportOptional: "Protección contra caídas, conocimientos generales de CDL y RCP en adultos siguen gratis si no está listo para pagar.",
      supportDoesNot: "El pago no compra ",
      supportCashNote:
        "Cash App: {tag}. Confirme $safetytestprep y el nombre Safety Test Prep. Envíe $9.99. También se aceptan Bitcoin y USDT (Tron).",
      supportNotLive: "Cash App aún no está activado.",
      supportOshaBody:
        "Protección contra caídas es gratis. El resto de este laboratorio OSHA — simulacros, tarjetas y el banco de 808 preguntas — cuesta $9.99 por 30 días en este dispositivo. El pago no compra una tarjeta.",
      supportCdlBody:
        "Conocimientos generales de CDL es gratis. Frenos de aire, combinación, endosos, tarjetas y el banco completo cuestan $9.99 por 30 días en este dispositivo. El pago no compra una licencia.",
      supportCprBody:
        "RCP en adultos es gratis. DEA, pediatría, primeros auxilios, tarjetas y el banco de 435 preguntas cuestan $9.99 por 30 días en este dispositivo. El pago no compra una certificación."
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
