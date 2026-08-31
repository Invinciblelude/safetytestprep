function stpCashBase() {
  const cfg = window.STP_PAY || {};
  let s = String(cfg.cashapp || "").trim();
  if (!s) return "";
  if (s.indexOf("http") !== 0) {
    if (s.charAt(0) !== "$") s = "$" + s;
    s = "https://cash.app/" + s;
  }
  return s.replace(/\/$/, "");
}

function stpWirePay() {
  const cfg = window.STP_PAY || {};
  const base = stpCashBase();
  document.querySelectorAll("[data-cash]").forEach(function (a) {
    const amt = a.getAttribute("data-cash");
    if (!base) {
      a.classList.add("disabled");
      a.removeAttribute("href");
      return;
    }
    a.href = base + "/" + amt;
    a.target = "_blank";
    a.rel = "noopener";
  });
  const warn = document.getElementById("pay-warn");
  if (warn) warn.hidden = Boolean(base);
  const cashLine = document.getElementById("cash-line");
  if (cashLine) {
    let tag = String(cfg.cashapp || "").trim();
    if (base && tag && tag.indexOf("http") !== 0) {
      if (tag.charAt(0) !== "$") tag = "$" + tag;
      cashLine.textContent = "Cash App: " + tag;
    } else {
      cashLine.textContent = "";
    }
  }
  const crypto = document.getElementById("crypto-line");
  if (crypto) {
    const bits = [];
    if (cfg.cryptoUrl) bits.push("<a href='" + cfg.cryptoUrl + "' target='_blank' rel='noopener'>Send crypto</a>");
    if (cfg.cryptoAddress) bits.push((cfg.cryptoLabel || "BTC") + ": " + cfg.cryptoAddress);
    crypto.innerHTML = bits.length ? bits.join(" · ") : "";
  }
}

document.addEventListener("DOMContentLoaded", stpWirePay);
