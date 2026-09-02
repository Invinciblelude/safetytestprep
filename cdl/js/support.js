window.SUPPORT_CONFIG = {
  product: "the CDL Practice Lab",
  credential: "a CDL, DMV exam result, license, or priority access",
  credentialEs: "una CDL, resultado de examen del DMV, licencia o acceso prioritario",
  bodyKey: "supportCdlBody",
  cashapp: ""
};

(function applyRootPay() {
  var p = window.STP_PAY;
  if (!p) return;
  if (p.cashapp) window.SUPPORT_CONFIG.cashapp = p.cashapp;
})();

(function () {
  function t(key) {
    return window.stpT ? window.stpT(key) : key;
  }
  function cashappBase() {
    let s = String((window.SUPPORT_CONFIG && window.SUPPORT_CONFIG.cashapp) || "").trim();
    if (!s) return "";
    if (s.indexOf("http") !== 0) {
      if (s.charAt(0) !== "$") s = "$" + s;
      s = "https://cash.app/" + s;
    }
    return s.replace(/\/$/, "");
  }

  function tagLabel() {
    let s = String((window.SUPPORT_CONFIG && window.SUPPORT_CONFIG.cashapp) || "").trim();
    if (!s) return "";
    if (s.indexOf("http") === 0) return "";
    if (s.charAt(0) !== "$") s = "$" + s;
    return s;
  }

  function hrefFor(amount) {
    return "";
  }

  function render(el, variant) {
    if (!el) return;
    const c = window.SUPPORT_CONFIG || {};
    const live = Boolean(tagLabel());
    const href = hrefFor("9.99") || hrefFor("10");
    const tag = tagLabel();
    const cred = (window.STP_LANG === "es" && c.credentialEs) ? c.credentialEs : (c.credential || "a credential");
    const body = t(c.bodyKey || "supportCdlBody");
    const cashLabel = t("supportCash");
    const needsUnlock = window.stpShowPaywall && !(window.stpHasFullAccess && window.stpHasFullAccess());
    const payPage = (document.documentElement.lang || "").toLowerCase().indexOf("es") === 0 ? "/es/support.html" : "/support.html";
    const payBlock = needsUnlock
      ? "<div class='support-amounts'><button type='button' class='tip-btn' data-stp-unlock>" + t("unlockCta") + "</button></div>"
      : "<div class='support-amounts'><a class='tip-btn' href='" + payPage + "#pay'>" + cashLabel + "</a></div>";

    if (variant === "home") {
      el.innerHTML =
        "<p class='tip-other'><a href='../support.html'>" + t("supportHome") + "</a></p>";
      return;
    }

    const cashNote = tag
      ? "<p class='tip-other'>" + t("supportCashNote").replace("{tag}", "<strong>" + tag + "</strong>") + "</p>"
      : "";

    el.innerHTML =
      "<p class='eyebrow'>" + t("supportEyebrow") + "</p>" +
      "<p>" + t("supportVince") + "</p>" +
      "<p>" + body + "</p>" +
      payBlock +
      cashNote +
      "<p class='tip-other'>" + t("supportOptional") + "</p>" +
      "<p class='tip-other'>" + t("supportDoesNot") + cred + ".</p>" +
      (live ? "" : "<p class='tip-other'>" + t("supportNotLive") + "</p>");
  }

  window.renderSupport = render;
  render(document.getElementById("support-home"), "home");
  render(document.getElementById("support-result"), "result");
})();
