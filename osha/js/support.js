window.SUPPORT_CONFIG = {
  product: "the OSHA Practice Lab",
  credential: "OSHA training, a completion card, certification, a license, an exam score, or priority access",
  cashapp: ""
};

(function applyRootPay() {
  var p = window.STP_PAY;
  if (!p) return;
  if (p.cashapp) window.SUPPORT_CONFIG.cashapp = p.cashapp;
})();

(function () {
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
    const base = cashappBase();
    if (!base) return "";
    return base + "/" + amount;
  }

  function render(el, variant) {
    if (!el) return;
    const c = window.SUPPORT_CONFIG || {};
    const live = Boolean(cashappBase());
    const href = hrefFor("9.99") || hrefFor("10");
    const tag = tagLabel();
    const btn = href
      ? "<a class='tip-btn' href='" + href + "' target='_blank' rel='noopener'>Support Safety Test Prep — $9.99 via Cash App</a>"
      : "<span class='tip-btn disabled'>Support Safety Test Prep — $9.99 via Cash App</span>";

    if (variant === "home") {
      el.innerHTML =
        "<p class='tip-other'><a href='../support.html'>Keep Safety Test Prep free — optional support</a></p>";
      return;
    }

    el.innerHTML =
      "<p class='eyebrow'>Keep the lab open</p>" +
      "<p>I’m Vince. I built Safety Test Prep to make practical safety study tools easier to access for workers, job seekers, and people entering the trades.</p>" +
      "<p>You used original OSHA-topic questions, answer explanations, and flashcards—without an account or paywall. Safety Test Prep is free to use. If this quiz helped you prepare for work, training, or a new role, optional support of $9.99 helps fund research, question writing, review, and updates.</p>" +
      "<div class='support-amounts'>" +
      btn +
      "</div>" +
      (tag && href
        ? "<p class='tip-other'>Cash App: <a href='" + cashappBase() + "' target='_blank' rel='noopener'>" + tag + "</a>. Note: Safety Test Prep support. The account may display as Andy Lau until the display name is updated.</p>"
        : "") +
      "<p class='tip-other'>Payment is optional. If you cannot contribute right now, keep studying.</p>" +
      "<p class='tip-other'>Support does not purchase " +
      (c.credential || "a credential") +
      ".</p>" +
      (live ? "" : "<p class='tip-other'>Cash App is not enabled yet.</p>");
  }

  window.renderSupport = render;
  render(document.getElementById("support-home"), "home");
  render(document.getElementById("support-result"), "result");
})();
