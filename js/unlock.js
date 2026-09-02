(function () {
  var KEY = "stp-full-until";
  var DAYS = 30;
  var FREE = {
    osha: ["fallProtection"],
    cdl: ["general"],
    cpr: ["adultCpr"]
  };

  function es() {
    return (document.documentElement.lang || "").toLowerCase().indexOf("es") === 0;
  }

  function lab() {
    var p = (location.pathname || "").toLowerCase();
    if (p.indexOf("/osha") !== -1) return "osha";
    if (p.indexOf("/cdl") !== -1) return "cdl";
    if (p.indexOf("/cpr") !== -1) return "cpr";
    return "";
  }

  function freeHref() {
    var L = lab();
    var esPre = es() ? "/es" : "";
    if (L === "cdl") return esPre + "/cdl/general-knowledge.html";
    if (L === "cpr") return esPre + "/cpr/adult-cpr.html";
    return esPre + "/osha/fall-protection.html";
  }

  function freeLabel() {
    if (lab() === "cdl") return es() ? "conocimientos generales de CDL" : "CDL General Knowledge";
    if (lab() === "cpr") return es() ? "RCP en adultos" : "Adult CPR";
    return es() ? "protección contra caídas" : "fall protection";
  }

  function copy() {
    if (es()) {
      return {
        nowTitle: "Pague $9.99 primero",
        nowLead:
          "Escanee el código de Cash App y envíe $9.99 a $safetytestprep. El cuestionario de muestra sigue gratis.",
        title: "Desbloquee el banco completo — $9.99",
        lead:
          "Los cuestionarios de muestra siguen gratis. El banco completo, las tarjetas y los simulacros en este laboratorio cuestan $9.99 por 30 días en este dispositivo. Pague $9.99 en Cash App, o con Bitcoin o USDT. No es una tarjeta, licencia ni certificación.",
        pay: "Pagar $9.99 en Cash App",
        crypto: "O envíe unos $9.99 en Bitcoin, o $9.99 USDT (solo Tron / TRC-20).",
        free: "Seguir con el cuestionario gratis de " + freeLabel(),
        note: "Escanee el código de Cash App. $safetytestprep (nombre: Safety Test Prep). Envíe $9.99.",
        close: "Volver",
        days: "Acceso completo en este dispositivo hasta "
      };
    }
    return {
        nowTitle: "Pay $9.99 first",
        nowLead:
          "Scan the Cash App code and send $9.99 to $safetytestprep. The sample quiz stays free.",
        title: "Unlock the full practice bank — $9.99",
        lead:
          "Sample quizzes stay free. The full question bank, flashcards, and mock exams in this lab are $9.99 for 30 days on this device. Pay $9.99 in Cash App, or with Bitcoin or USDT. This is not a card, license, or certification.",
        pay: "Pay $9.99 with Cash App",
        crypto: "Or send about $9.99 in Bitcoin, or $9.99 USDT (Tron / TRC-20 only).",
        free: "Keep the free " + freeLabel() + " quiz",
        note: "Scan the Cash App code. $safetytestprep (name: Safety Test Prep). Send $9.99.",
        close: "Back",
        days: "Full access on this device until "
    };
  }

  function until() {
    try {
      return parseInt(localStorage.getItem(KEY) || "0", 10) || 0;
    } catch (err) {
      return 0;
    }
  }

  window.stpHasFullAccess = function () {
    return Date.now() < until();
  };

  window.stpGrantFullAccess = function () {
    try {
      localStorage.setItem(KEY, String(Date.now() + DAYS * 24 * 60 * 60 * 1000));
    } catch (err) {}
    markLocks();
  };

  window.stpModeIsFree = function (mode) {
    if (!mode) return false;
    var list = FREE[lab()] || [];
    return list.indexOf(mode) !== -1;
  };

  var pending = "";

  window.stpAllowStart = function (mode) {
    if (window.stpHasFullAccess()) return true;
    if (window.stpModeIsFree(mode)) return true;
    pending = mode || "";
    window.stpShowPaywall();
    return false;
  };

  function cashHref() {
    return "";
  }

  function ensurePanel() {
    var el = document.getElementById("stp-paywall");
    if (el) return el;
    el = document.createElement("div");
    el.id = "stp-paywall";
    el.className = "stp-paywall";
    el.hidden = true;
    el.setAttribute("role", "dialog");
    el.setAttribute("aria-modal", "true");
    document.body.appendChild(el);
    return el;
  }

  window.stpShowPaywall = function () {
    var c = copy();
    var el = ensurePanel();
    var cashQr =
      typeof stpCashQrHtml === "function" ? '<div class="stp-paywall-cash">' + stpCashQrHtml() + "</div>" : "";
    var cryptoBlock =
      typeof stpCryptoHtml === "function" && stpCryptoHtml()
        ? '<div class="stp-paywall-crypto"><p class="stp-paywall-note">' + c.crypto + "</p>" + stpCryptoHtml() + "</div>"
        : "";
    el.innerHTML =
      '<div class="stp-paywall-card">' +
      "<h2>" +
      c.title +
      "</h2>" +
      "<p>" +
      c.lead +
      "</p>" +
      '<p class="stp-paywall-note">' +
      c.note +
      "</p>" +
      cashQr +
      '<p class="btns">' +
      '<a class="btn" href="' +
      freeHref() +
      '">' +
      c.free +
      "</a>" +
      "</p>" +
      cryptoBlock +
      '<p><button type="button" class="btn ghost" data-stp-paywall-close>' +
      c.close +
      "</button></p>" +
      "</div>";
    el.hidden = false;
    document.body.style.overflow = "hidden";
    if (typeof stpBindCopy === "function") stpBindCopy(el);
  };

  window.stpHidePaywall = function () {
    var el = document.getElementById("stp-paywall");
    if (el) el.hidden = true;
    document.body.style.overflow = "";
  };

  function markLocks() {
    var open = window.stpHasFullAccess();
    document.querySelectorAll("[data-mode]").forEach(function (btn) {
      var mode = btn.getAttribute("data-mode");
      if (open || window.stpModeIsFree(mode)) btn.classList.remove("is-locked");
      else btn.classList.add("is-locked");
    });
    var note = document.getElementById("stp-unlock-status");
    if (!note) return;
    if (open) {
      var d = new Date(until());
      note.hidden = false;
      note.textContent = copy().days + d.toLocaleDateString();
    } else {
      note.hidden = true;
    }
  }

  document.addEventListener("click", function (e) {
    if (e.target.closest("[data-stp-paywall-close]")) {
      e.preventDefault();
      pending = "";
      window.stpHidePaywall();
      return;
    }
    if (e.target.closest("[data-stp-unlock]")) {
      e.preventDefault();
      window.stpShowPaywall();
    }
  });

  document.addEventListener("keydown", function (e) {
    if (e.key !== "Escape") return;
    var el = document.getElementById("stp-paywall");
    if (!el || el.hidden) return;
    pending = "";
    window.stpHidePaywall();
  });

  document.addEventListener("DOMContentLoaded", markLocks);
  markLocks();
})();
