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

function stpEscapeHtml(s) {
  return String(s)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/"/g, "&quot;");
}

function stpCryptoItems() {
  const cfg = window.STP_PAY || {};
  if (Array.isArray(cfg.crypto) && cfg.crypto.length) return cfg.crypto;
  const items = [];
  if (cfg.cryptoAddress) {
    items.push({
      label: cfg.cryptoLabel || "Crypto",
      address: cfg.cryptoAddress,
      note: cfg.cryptoNote || ""
    });
  }
  return items;
}

function stpCryptoHtml() {
  return stpCryptoItems()
    .map(function (item) {
      const note = item.note ? "<br><em>" + stpEscapeHtml(item.note) + "</em>" : "";
      return (
        "<p class='crypto-row'><strong>" +
        stpEscapeHtml(item.label) +
        "</strong><br><code>" +
        stpEscapeHtml(item.address) +
        "</code> <button type='button' class='tip-copy' data-copy='" +
        stpEscapeHtml(item.address) +
        "'>" +
        (window.stpT ? window.stpT("copy") : "Copy") +
        "</button>" +
        note +
        "</p>"
      );
    })
    .join("");
}

function stpBindCopy(root) {
  const scope = root || document;
  scope.querySelectorAll(".tip-copy").forEach(function (btn) {
    btn.addEventListener("click", function () {
      const addr = btn.getAttribute("data-copy") || "";
      if (!addr) return;
      const done = function () {
        btn.textContent = window.stpT ? window.stpT("copied") : "Copied";
      };
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(addr).then(done);
        return;
      }
      const ta = document.createElement("textarea");
      ta.value = addr;
      document.body.appendChild(ta);
      ta.select();
      document.execCommand("copy");
      ta.remove();
      done();
    });
  });
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
    a.classList.remove("disabled");
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
      cashLine.innerHTML = "Cash App: <a href='" + base + "' target='_blank' rel='noopener'>" + stpEscapeHtml(tag) + "</a>";
    } else {
      cashLine.textContent = "";
    }
  }
  const crypto = document.getElementById("crypto-line");
  if (crypto) {
    crypto.innerHTML = stpCryptoHtml();
    stpBindCopy(crypto);
  }
}

document.addEventListener("DOMContentLoaded", stpWirePay);
