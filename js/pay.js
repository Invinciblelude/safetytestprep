function stpIsEs() {
  return (document.documentElement.lang || "").toLowerCase().indexOf("es") === 0;
}

function stpPayPage() {
  return stpIsEs() ? "/es/support.html" : "/support.html";
}

function stpCashTag() {
  let s = String((window.STP_PAY && window.STP_PAY.cashapp) || "$safetytestprep").trim();
  if (!s) return "$safetytestprep";
  if (s.charAt(0) !== "$") s = "$" + s;
  return s;
}

function stpCashBase() {
  return "";
}

function stpEscapeHtml(s) {
  return String(s)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/"/g, "&quot;");
}

function stpCashQrHtml() {
  const cfg = window.STP_PAY || {};
  const qr = cfg.cashQr || "/img/qr-cashapp.png";
  const tag = stpCashTag();
  const scan = stpIsEs() ? "Escanee con Cash App" : "Scan with Cash App";
  const note = stpIsEs()
    ? "Confirme $safetytestprep y el nombre Safety Test Prep. Envíe $9.99."
    : "Confirm $safetytestprep and the name Safety Test Prep. Send $9.99.";
  return (
    "<div class='crypto-row cash-qr-row' id='cash'>" +
    "<img class='crypto-qr' src='" +
    stpEscapeHtml(qr) +
    "' width='180' height='180' alt='Cash App " +
    stpEscapeHtml(tag) +
    "'>" +
    "<div class='crypto-meta'><p class='crypto-scan'>" +
    stpEscapeHtml(scan) +
    "</p><strong>Cash App</strong><br><code>" +
    stpEscapeHtml(tag) +
    "</code> <button type='button' class='tip-copy' data-copy='" +
    stpEscapeHtml(tag) +
    "'>" +
    (window.stpT ? window.stpT("copy") : "Copy") +
    "</button><em>" +
    note +
    "</em></div></div>"
  );
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

function stpCryptoNote(item) {
  if (stpIsEs() && item.noteEs) return item.noteEs;
  return item.note || "";
}

function stpCryptoHtml() {
  const scan = window.stpT ? window.stpT("scanQr") : "Scan with your wallet";
  return stpCryptoItems()
    .map(function (item) {
      const noteText = stpCryptoNote(item);
      const note = noteText ? "<em>" + stpEscapeHtml(noteText) + "</em>" : "";
      const qr = item.qr
        ? "<img class='crypto-qr' src='" +
          stpEscapeHtml(item.qr) +
          "' width='180' height='180' alt='" +
          stpEscapeHtml(item.label) +
          " QR'>"
        : "";
      return (
        "<div class='crypto-row'>" +
        qr +
        "<div class='crypto-meta'><p class='crypto-scan'>" +
        stpEscapeHtml(scan) +
        "</p><strong>" +
        stpEscapeHtml(item.label) +
        "</strong><br><code>" +
        stpEscapeHtml(item.address) +
        "</code> <button type='button' class='tip-copy' data-copy='" +
        stpEscapeHtml(item.address) +
        "'>" +
        (window.stpT ? window.stpT("copy") : "Copy") +
        "</button>" +
        note +
        "</div></div>"
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
  const payPage = stpPayPage();
  document.querySelectorAll("[data-cash]").forEach(function (a) {
    a.classList.remove("disabled");
    a.href = payPage + "#cash";
    a.removeAttribute("target");
    a.removeAttribute("rel");
  });
  const warn = document.getElementById("pay-warn");
  if (warn) warn.hidden = true;
  const cashLine = document.getElementById("cash-line");
  if (cashLine) {
    cashLine.innerHTML = "Cash App: <strong>" + stpEscapeHtml(stpCashTag()) + "</strong>";
  }
  const cashQr = document.getElementById("cash-qr");
  if (cashQr) {
    cashQr.innerHTML = stpCashQrHtml();
    stpBindCopy(cashQr);
  }
  const crypto = document.getElementById("crypto-line");
  if (crypto) {
    crypto.innerHTML = stpCryptoHtml();
    stpBindCopy(crypto);
  }
}

document.addEventListener("DOMContentLoaded", stpWirePay);
