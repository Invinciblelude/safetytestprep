(function () {
  const cfg = window.STP_PAY || {};
  function cashBase() {
    let s = String(cfg.cashapp || "").trim();
    if (!s) return "";
    if (s.indexOf("http") !== 0) {
      if (s.charAt(0) !== "$") s = "$" + s;
      s = "https://cash.app/" + s;
    }
    return s.replace(/\/$/, "");
  }
  const base = cashBase();
  document.querySelectorAll("[data-cash]").forEach(function (a) {
    const amt = a.getAttribute("data-cash");
    if (!base) {
      a.classList.add("disabled");
      a.removeAttribute("href");
      return;
    }
    a.href = base + "/" + amt;
  });
  const warn = document.getElementById("pay-warn");
  if (warn) warn.hidden = Boolean(base);
  const crypto = document.getElementById("crypto-line");
  if (crypto) {
    const bits = [];
    if (cfg.cryptoUrl) bits.push("<a href='" + cfg.cryptoUrl + "' target='_blank' rel='noopener'>Send crypto</a>");
    if (cfg.cryptoAddress) bits.push((cfg.cryptoLabel || "BTC") + ": " + cfg.cryptoAddress);
    crypto.innerHTML = bits.length ? bits.join(" · ") : "";
  }
})();
