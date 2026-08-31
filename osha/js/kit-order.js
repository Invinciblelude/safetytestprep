(function () {
  const cfg = window.OSHA_KIT_CONFIG || {};
  const email = (cfg.orderEmail || "").trim();
  const ready = email.indexOf("@") > 0 && email !== "PUT_YOUR_EMAIL_HERE";
  const warn = document.getElementById("email-warn");
  if (warn) warn.hidden = ready;

  const pay = document.getElementById("pay-hint");
  if (pay) {
    const bits = [];
    if (cfg.zelle) bits.push("Zelle: " + cfg.zelle);
    if (cfg.cashapp) bits.push("Cash App: " + cfg.cashapp);
    if (cfg.paypal) bits.push("PayPal: " + cfg.paypal);
    if (bits.length) {
      pay.textContent = "After you send this, pay $34 via " + bits.join(" · ") + ". The kit ships after that payment lands.";
    }
  }

  function err(msg) {
    const el = document.getElementById("order-error");
    if (el) el.textContent = msg;
  }

  function build() {
    if (!ready) {
      err("Owner: put your email in js/kit-config.js and reload.");
      return null;
    }
    const name = document.getElementById("name").value.trim();
    const buyerEmail = document.getElementById("buyer-email").value.trim();
    const addr = document.getElementById("addr").value.trim();
    const city = document.getElementById("city").value.trim();
    const zip = document.getElementById("zip").value.trim();
    const phone = document.getElementById("phone").value.trim();
    if (!name || !buyerEmail || !addr || !city || !zip) {
      err("Name, email, and ship-to address are required.");
      return null;
    }
    const body = [
      "Jobsite gate kit — $34",
      "Buyer: " + name,
      "Email: " + buyerEmail,
      "Phone: " + phone,
      "Ship to:",
      addr,
      city + " " + zip,
      "",
      "Do not buy on Amazon until $34 has landed.",
      "Then ship glasses + hi-vis + gloves + earplugs to this address."
    ].join("\n");
    err("");
    return { name: name, body: body };
  }

  const form = document.getElementById("kit-form");
  if (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      const order = build();
      if (!order) return;
      window.location.href =
        "mailto:" + encodeURIComponent(email) +
        "?subject=" + encodeURIComponent("Gate kit $34 — " + order.name) +
        "&body=" + encodeURIComponent(order.body);
    });
  }

  const copyBtn = document.getElementById("copy-order");
  if (copyBtn) {
    copyBtn.addEventListener("click", function () {
      const order = build();
      if (!order) return;
      const text = "To: " + email + "\nSubject: Gate kit $34 — " + order.name + "\n\n" + order.body;
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(function () {
          copyBtn.textContent = "Copied — paste into email";
        });
      }
    });
  }
})();
