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

  function escapeHtml(s) {
    if (typeof stpEscapeHtml === "function") return stpEscapeHtml(s);
    return String(s)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/"/g, "&quot;");
  }

  function shownPassword() {
    return (window.STP_PAY && window.STP_PAY.labPassword) || "";
  }

  function copy() {
    if (es()) {
      return {
        title: "Desbloquee el banco completo — $9.99",
        lead:
          "1. Pague $9.99. 2. La contraseña aparece abajo. 3. Desbloquee. Eso abre el banco, las tarjetas y los simulacros 30 días en este dispositivo. Las muestras siguen gratis. No es una tarjeta ni una licencia.",
        crypto: "O envíe unos $9.99 en Bitcoin, o $9.99 USDT (solo Tron / TRC-20).",
        free: "Seguir con el cuestionario gratis de " + freeLabel(),
        note: "Escanee el código de Cash App. $safetytestprep (nombre: Safety Test Prep). Envíe $9.99.",
        passAfter: "Después de pagar, esta es la contraseña:",
        copyBtn: "Copiar",
        passBtn: "Desbloquear 30 días en este dispositivo",
        close: "Volver",
        days: "Acceso completo en este dispositivo hasta ",
        unlocked: "Acceso completo activo. Puede empezar cualquier cuestionario en OSHA, CDL o RCP."
      };
    }
    return {
      title: "Unlock the full practice bank — $9.99",
      lead:
        "1. Pay $9.99. 2. The password is below. 3. Unlock. That opens the bank, flashcards, and mocks for 30 days on this device. Sample quizzes stay free. This is not a card or a license.",
      crypto: "Or send about $9.99 in Bitcoin, or $9.99 USDT (Tron / TRC-20 only).",
      free: "Keep the free " + freeLabel() + " quiz",
      note: "Scan the Cash App code. $safetytestprep (name: Safety Test Prep). Send $9.99.",
      passAfter: "After you pay, this is the password:",
      copyBtn: "Copy",
      passBtn: "Unlock 30 days on this device",
      close: "Back",
      days: "Full access on this device until ",
      unlocked: "Full access is on. You can start any quiz in the OSHA, CDL, or CPR lab."
    };
  }

  function passShowHtml() {
    var c = copy();
    var pw = shownPassword();
    if (!pw) return "";
    return (
      '<div class="stp-pass-show">' +
      "<p>" +
      c.passAfter +
      "</p>" +
      "<p><code>" +
      escapeHtml(pw) +
      '</code> <button type="button" class="tip-copy" data-copy="' +
      escapeHtml(pw) +
      '">' +
      c.copyBtn +
      "</button></p>" +
      "</div>"
    );
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

  function normPass(s) {
    return String(s || "")
      .replace(/\s+/g, "")
      .toUpperCase();
  }

  window.stpPasswordOk = function (typed) {
    var want = shownPassword();
    if (!want) return false;
    return normPass(typed) === normPass(want);
  };

  function afterUnlock() {
    var mode = pending;
    pending = "";
    window.stpHidePaywall();
    if (!mode) return;
    var btn = document.querySelector('[data-mode="' + mode + '"]');
    if (btn) btn.click();
  }

  function grantNow() {
    window.stpGrantFullAccess();
    afterUnlock();
  }

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
      cryptoBlock +
      passShowHtml() +
      '<p class="btns">' +
      '<button type="button" class="btn" data-stp-grant>' +
      c.passBtn +
      "</button>" +
      '<a class="btn ghost" href="' +
      freeHref() +
      '">' +
      c.free +
      "</a>" +
      "</p>" +
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

  function fillShownPass() {
    var html = passShowHtml();
    document.querySelectorAll("[data-stp-show-pass]").forEach(function (el) {
      el.innerHTML = html;
      if (typeof stpBindCopy === "function") stpBindCopy(el);
    });
  }

  function markLocks() {
    var open = window.stpHasFullAccess();
    document.querySelectorAll("[data-mode]").forEach(function (btn) {
      var mode = btn.getAttribute("data-mode");
      if (open || window.stpModeIsFree(mode)) btn.classList.remove("is-locked");
      else btn.classList.add("is-locked");
    });
    var note = document.getElementById("stp-unlock-status");
    if (note) {
      if (open) {
        var d = new Date(until());
        note.hidden = false;
        note.textContent = copy().days + d.toLocaleDateString();
      } else {
        note.hidden = true;
      }
    }
    var form = document.getElementById("stp-pass-form");
    if (form) form.hidden = open;
    document.querySelectorAll("[data-stp-grant]").forEach(function (btn) {
      btn.hidden = open;
    });
    var ok = document.getElementById("stp-unlock-ok");
    if (ok) {
      ok.hidden = !open;
      if (open) ok.textContent = copy().unlocked;
    }
  }

  document.addEventListener("click", function (e) {
    if (e.target.closest("[data-stp-paywall-close]")) {
      e.preventDefault();
      pending = "";
      window.stpHidePaywall();
      return;
    }
    if (e.target.closest("[data-stp-grant]")) {
      e.preventDefault();
      grantNow();
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

  document.addEventListener("DOMContentLoaded", function () {
    fillShownPass();
    markLocks();
  });
  fillShownPass();
  markLocks();
})();
