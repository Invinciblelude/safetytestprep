/**
 * Cash App and crypto only (no PayPal).
 * cashapp: "https://cash.app/$YourTag"  or  "$YourTag"
 * Amount buttons open Cash App with /5 /9 /19.
 * cryptoUrl: Strike / BTCPay / a payment page
 * cryptoAddress: BTC (or other) address to copy
 */
window.SUPPORT_CONFIG = {
  product: "this OSHA practice lab",
  cashapp: "",
  cryptoUrl: "",
  cryptoAddress: "",
  cryptoLabel: "BTC"
};

(function applyRootPay() {
  var p = window.STP_PAY;
  if (!p) return;
  var c = window.SUPPORT_CONFIG;
  if (p.cashapp) c.cashapp = p.cashapp;
  if (p.cryptoUrl) c.cryptoUrl = p.cryptoUrl;
  if (p.cryptoAddress) c.cryptoAddress = p.cryptoAddress;
  if (p.cryptoLabel) c.cryptoLabel = p.cryptoLabel;
})();

(function () {
  const amounts = [
    { usd: 5, label: "$5", why: "Coffee" },
    { usd: 9, label: "$9", why: "A week online" },
    { usd: 19, label: "$19", why: "Both banks" }
  ];

  function cashappBase() {
    let s = String((window.SUPPORT_CONFIG && window.SUPPORT_CONFIG.cashapp) || "").trim();
    if (!s) return "";
    if (s.indexOf("http") !== 0) {
      if (s.charAt(0) !== "$") s = "$" + s;
      s = "https://cash.app/" + s;
    }
    return s.replace(/\/$/, "");
  }

  function hrefFor(amount) {
    const base = cashappBase();
    if (!base) return "";
    return base + "/" + amount;
  }

  function hasPay() {
    const c = window.SUPPORT_CONFIG || {};
    return Boolean(cashappBase() || c.cryptoUrl || c.cryptoAddress);
  }

  function render(el, variant) {
    if (!el) return;
    const c = window.SUPPORT_CONFIG || {};
    const product = c.product || "this practice lab";
    const live = hasPay();
    const amountHtml = amounts
      .map(function (row) {
        const href = hrefFor(row.usd);
        if (href) {
          return (
            "<a class='tip-btn' href='" +
            href +
            "' target='_blank' rel='noopener'>" +
            row.label +
            " <span>" +
            row.why +
            "</span></a>"
          );
        }
        return (
          "<span class='tip-btn disabled' title='Add your Cash App $cashtag in js/support.js'>" +
          row.label +
          " <span>" +
          row.why +
          "</span></span>"
        );
      })
      .join("");

    const bits = [];
    if (c.cryptoUrl) {
      bits.push(
        "<a href='" +
          c.cryptoUrl +
          "' target='_blank' rel='noopener'>Send crypto</a>"
      );
    }
    if (c.cryptoAddress) {
      bits.push(
        "<button type='button' class='tip-copy' data-copy='" +
          String(c.cryptoAddress).replace(/'/g, "") +
          "'>Copy " +
          (c.cryptoLabel || "crypto") +
          " address</button>"
      );
    }
    const other = bits.length
      ? "<p class='tip-other'>Crypto: " + bits.join(" · ") + ". Cash App can also receive bitcoin to the same $cashtag.</p>"
      : "<p class='tip-other'>Tip with Cash App ($5 / $9 / $19) or crypto. Not PayPal. The tests stay free.</p>";

    const lead =
      variant === "result"
        ? "If this mock helped, chip in so the next apprentice can study for free."
        : "The quizzes stay free. A tip keeps the lab online.";

    el.innerHTML =
      "<p class='eyebrow'>Support</p>" +
      "<strong>Leave a tip for " +
      product +
      "</strong>" +
      "<p>" +
      lead +
      " Cash App or crypto. This is a thank-you, not a tax-deductible donation, and not payment for an OSHA card.</p>" +
      "<div class='support-amounts'>" +
      amountHtml +
      "</div>" +
      other +
      (live ? "" : "<p class='tip-other'>Optional Cash App study support is not enabled yet. The quizzes stay free.</p>");

    el.querySelectorAll(".tip-copy").forEach(function (btn) {
      btn.addEventListener("click", function () {
        const addr = btn.getAttribute("data-copy") || "";
        if (!addr || !navigator.clipboard) return;
        navigator.clipboard.writeText(addr).then(function () {
          btn.textContent = "Copied";
        });
      });
    });
  }

  window.renderSupport = render;
  render(document.getElementById("support-home"), "home");
  render(document.getElementById("support-result"), "result");
})();
