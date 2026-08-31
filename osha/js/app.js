(function () {
  window.OSHA_QUESTIONS = window.OSHA_QUESTIONS || [];
  ["OSHA_QUESTIONS_SET2", "OSHA_QUESTIONS_SET3", "OSHA_QUESTIONS_SET4", "OSHA_QUESTIONS_SET5"].forEach((key) => {
    if (window[key] && window[key].length) {
      window.OSHA_QUESTIONS = window.OSHA_QUESTIONS.concat(window[key]);
    }
  });
  const knownKey = "osha-known-cards";
  const screens = {
    home: document.getElementById("screen-home"),
    quiz: document.getElementById("screen-quiz"),
    result: document.getElementById("screen-result"),
    flash: document.getElementById("screen-flash"),
    bank: document.getElementById("screen-bank")
  };
  const tabs = document.getElementById("tabs");

  let modeId = "osha10";
  let queue = [];
  let index = 0;
  let score = 0;
  let missed = [];
  let answered = false;
  let lastMode = "osha10";

  let deck = [];
  let deckIndex = 0;
  let flipped = false;
  let deckFilter = "all";

  function show(name) {
    Object.entries(screens).forEach(([key, el]) => {
      el.hidden = key !== name;
    });
    tabs.hidden = name === "home";
    tabs.querySelectorAll("button").forEach((btn) => {
      btn.setAttribute("aria-current", btn.dataset.view === (name === "result" ? "quiz" : name) ? "page" : "false");
    });
  }

  function shuffle(list) {
    const copy = list.slice();
    for (let i = copy.length - 1; i > 0; i -= 1) {
      const j = Math.floor(Math.random() * (i + 1));
      [copy[i], copy[j]] = [copy[j], copy[i]];
    }
    return copy;
  }

  function byCategory(cat) {
    return window.OSHA_QUESTIONS.filter((item) => item.category === cat);
  }

  function buildQuiz(id) {
    const spec = window.QUIZ_MODES[id];
    lastMode = id;
    modeId = id;
    missed = [];
    score = 0;
    index = 0;
    answered = false;
    if (spec.mix) {
      queue = [];
      Object.entries(spec.mix).forEach(([cat, count]) => {
        queue = queue.concat(shuffle(byCategory(cat)).slice(0, count));
      });
      queue = shuffle(queue).slice(0, spec.size);
    } else {
      const pool = spec.categories.flatMap(byCategory);
      queue = shuffle(pool).slice(0, Math.min(spec.size, pool.length));
    }
    document.getElementById("quiz-title").textContent = spec.title;
    renderQuestion();
    show("quiz");
  }

  function renderQuestion() {
    const item = queue[index];
    const spec = window.QUIZ_MODES[modeId] || { title: "Missed-question review" };
    answered = false;
    document.getElementById("quiz-progress").textContent = "Question " + (index + 1) + " of " + queue.length + " · Score " + score;
    document.getElementById("quiz-meter").style.width = ((index / queue.length) * 100) + "%";
    document.getElementById("quiz-topic").textContent = spec.title + " · " + item.topic;
    document.getElementById("quiz-prompt").textContent = item.q;
    const box = document.getElementById("quiz-choices");
    box.innerHTML = "";
    item.choices.forEach((choice, choiceIndex) => {
      const btn = document.createElement("button");
      btn.type = "button";
      btn.textContent = choice;
      btn.addEventListener("click", () => choose(choiceIndex, btn));
      box.appendChild(btn);
    });
    document.getElementById("quiz-explain").hidden = true;
    document.getElementById("btn-next").hidden = true;
  }

  function choose(choiceIndex, button) {
    if (answered) return;
    answered = true;
    const item = queue[index];
    const buttons = [...document.getElementById("quiz-choices").children];
    buttons[item.a].classList.add("correct");
    if (choiceIndex === item.a) {
      score += 1;
    } else {
      button.classList.add("wrong");
      missed.push({ item, picked: item.choices[choiceIndex] });
    }
    const explain = document.getElementById("quiz-explain");
    explain.hidden = false;
    explain.textContent = item.why;
    document.getElementById("btn-next").hidden = false;
    document.getElementById("quiz-progress").textContent = "Question " + (index + 1) + " of " + queue.length + " · Score " + score;
  }

  function nextQuestion() {
    if (index + 1 >= queue.length) {
      finishQuiz();
      return;
    }
    index += 1;
    renderQuestion();
  }

  function finishQuiz() {
    const spec = window.QUIZ_MODES[modeId] || { title: "Review", pass: Math.ceil(queue.length * 0.7) };
    const needed = spec.pass || Math.ceil(queue.length * 0.7);
    const passed = score >= needed;
    document.getElementById("result-kicker").textContent = spec.title;
    document.getElementById("result-score").textContent = score + " / " + queue.length + (passed ? " · Pass" : " · Keep studying");
    document.getElementById("result-detail").textContent =
      "Review the explanations below, then try another quiz or a different topic. This is independent practice only. A 10- or 30-hour card can only be issued by an authorized Outreach trainer.";
    const list = document.getElementById("missed-list");
    list.innerHTML = "";
    missed.forEach((row) => {
      const li = document.createElement("li");
      li.innerHTML = "<p><strong>" + row.item.q + "</strong></p><p>Your answer: " + row.picked + "</p><p>Correct: " + row.item.choices[row.item.a] + "</p><p>" + row.item.why + "</p>";
      list.appendChild(li);
    });
    document.getElementById("quiz-meter").style.width = "100%";
    show("result");
  }

  function knownSet() {
    try {
      return new Set(JSON.parse(localStorage.getItem(knownKey) || "[]"));
    } catch (err) {
      return new Set();
    }
  }

  function saveKnown(set) {
    localStorage.setItem(knownKey, JSON.stringify([...set]));
  }

  function filteredDeck() {
    const known = knownSet();
    let list = window.OSHA_FLASHCARDS.slice();
    if (["numbers", "rights", "jobsite", "health"].indexOf(deckFilter) !== -1) {
      list = list.filter((card) => card.deck === deckFilter);
    } else if (deckFilter === "unknown") {
      list = list.filter((card) => !known.has(card.id));
    }
    return shuffle(list);
  }

  function startFlash(filter) {
    deckFilter = filter || "all";
    deck = filteredDeck();
    deckIndex = 0;
    flipped = false;
    document.querySelectorAll(".flash-filters .chip").forEach((chip) => {
      chip.classList.toggle("active", chip.dataset.deck === deckFilter);
    });
    renderFlash();
    show("flash");
  }

  function renderFlash() {
    if (!deck.length) {
      document.getElementById("flash-progress").textContent = "0 cards in this filter";
      document.getElementById("flash-topic").textContent = "";
      document.getElementById("flash-text").textContent = "No cards left in this filter. Reset “Got it” cards by choosing All.";
      document.getElementById("flash-hint").textContent = "";
      return;
    }
    const card = deck[deckIndex];
    document.getElementById("flash-progress").textContent = (deckIndex + 1) + " / " + deck.length + " · " + window.OSHA_FLASHCARDS.length + " in bank";
    document.getElementById("flash-topic").textContent = card.topic;
    document.getElementById("flash-text").textContent = flipped ? card.back : card.front;
    document.getElementById("flash-hint").textContent = flipped ? "Tap to hide answer" : "Tap to reveal";
  }

  function markKnown(isKnown) {
    if (!deck.length) return;
    const card = deck[deckIndex];
    const set = knownSet();
    if (isKnown) set.add(card.id);
    else set.delete(card.id);
    saveKnown(set);
    nextFlash();
  }

  function nextFlash() {
    if (!deck.length) return;
    deckIndex = (deckIndex + 1) % deck.length;
    flipped = false;
    renderFlash();
  }

  function renderBank(filter) {
    const cats = ["all", "intro", "focusFour", "fallProtection", "ladders", "stairways", "excavation", "electrical", "ppe", "hazcom", "loto", "materials", "tools", "health", "fire", "walking", "confined", "forklift", "hazwoper", "bloodborne", "welding", "steel", "concrete", "respiratory", "machineguard", "aerial", "demolition", "recordkeeping", "firstaid", "psm", "sanitation", "signs", "vehicles", "ergonomics"];
    const select = document.getElementById("bank-filter");
    if (!select.options.length) {
      const labels = {
        all: "All questions (" + window.OSHA_QUESTIONS.length + ")",
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
      };
      cats.forEach((cat) => {
        const opt = document.createElement("option");
        opt.value = cat;
        opt.textContent = labels[cat];
        select.appendChild(opt);
      });
      select.addEventListener("change", () => renderBank(select.value));
    }
    select.value = filter || "all";
    const list = document.getElementById("bank-list");
    list.innerHTML = "";
    window.OSHA_QUESTIONS.filter((item) => filter === "all" || !filter || item.category === filter).forEach((item, i) => {
      const div = document.createElement("div");
      div.className = "bank-item";
      div.innerHTML = "<p class='topic'>" + item.category + " · " + item.topic + "</p><p><strong>" + (i + 1) + ". " + item.q + "</strong></p>" +
        item.choices.map((choice, idx) => "<div>" + (idx === item.a ? "✓ " : "") + choice + "</div>").join("") +
        "<p class='ans'>" + item.why + "</p>";
      list.appendChild(div);
    });
    show("bank");
  }

  document.querySelectorAll("[data-mode]").forEach((btn) => {
    btn.addEventListener("click", () => {
      const mode = btn.dataset.mode;
      if (mode === "flashcards") startFlash("all");
      else if (mode === "bank") renderBank("all");
      else buildQuiz(mode);
    });
  });

  tabs.querySelectorAll("button").forEach((btn) => {
    btn.addEventListener("click", () => {
      const view = btn.dataset.view;
      if (view === "home") show("home");
      else if (view === "quiz") buildQuiz(lastMode);
      else if (view === "flashcards") startFlash(deckFilter);
      else renderBank(document.getElementById("bank-filter").value || "all");
    });
  });

  document.getElementById("btn-next").addEventListener("click", nextQuestion);
  document.getElementById("btn-quit").addEventListener("click", () => show("home"));
  document.getElementById("btn-home").addEventListener("click", () => show("home"));
  const another = document.getElementById("btn-quick10");
  if (another) {
    another.addEventListener("click", () => buildQuiz("quick10"));
  }
  document.getElementById("btn-retry").addEventListener("click", () => buildQuiz(lastMode));
  document.getElementById("btn-review").addEventListener("click", () => {
    if (!missed.length) return;
    queue = missed.map((row) => row.item);
    missed = [];
    score = 0;
    index = 0;
    modeId = lastMode;
    document.getElementById("quiz-title").textContent = "Missed-question review";
    renderQuestion();
    show("quiz");
  });

  document.getElementById("flip-card").addEventListener("click", () => {
    flipped = !flipped;
    renderFlash();
  });
  document.getElementById("btn-known").addEventListener("click", () => markKnown(true));
  document.getElementById("btn-unknown").addEventListener("click", () => markKnown(false));
  document.getElementById("btn-flash-next").addEventListener("click", nextFlash);
  document.querySelectorAll(".flash-filters .chip").forEach((chip) => {
    chip.addEventListener("click", () => startFlash(chip.dataset.deck));
  });

  window.startOshaQuiz = function (id) {
    if (id && window.QUIZ_MODES[id]) buildQuiz(id);
  };
  window.startOshaQuiz(new URLSearchParams(window.location.search).get("quiz"));
})();
