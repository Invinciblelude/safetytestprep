(function () {
  var lang = (document.documentElement.getAttribute("lang") || "en").toLowerCase();
  var isEs = lang.indexOf("es") === 0;
  window.STP_LANG = isEs ? "es" : "en";

  var path = location.pathname || "/";
  var origin = "https://safetytestprep.com";
  function normalize(p) {
    if (!p || p === "/es") return p === "/es" ? "/es/" : "/";
    return p;
  }
  path = normalize(path);
  var enPath = path.replace(/^\/es(?=\/|$)/, "") || "/";
  if (enPath.charAt(0) !== "/") enPath = "/" + enPath;
  var esPath = /^\/es(\/|$)/.test(path) ? path : "/es" + (enPath === "/" ? "/" : enPath);
  var enUrl = origin + enPath;
  var esUrl = origin + esPath;
  var selfUrl = isEs ? esUrl : enUrl;

  if (!document.querySelector('link[rel="canonical"]')) {
    var can = document.createElement("link");
    can.rel = "canonical";
    can.href = selfUrl;
    document.head.appendChild(can);
  }
  function addAlt(hreflang, href) {
    if (document.querySelector('link[hreflang="' + hreflang + '"]')) return;
    var l = document.createElement("link");
    l.rel = "alternate";
    l.hreflang = hreflang;
    l.href = href;
    document.head.appendChild(l);
  }
  addAlt("en", enUrl);
  addAlt("es", esUrl);
  addAlt("x-default", enUrl);

  var foot = document.querySelector("[data-stp-footer]");
  var nav = document.querySelector("[data-stp-nav]");
  var base = "";
  if (foot) base = foot.getAttribute("data-base") || "";
  if (nav && nav.getAttribute("data-base") != null) base = nav.getAttribute("data-base") || base;

  var copy = isEs
    ? {
        osha: "OSHA",
        cdl: "CDL de California",
        cpr: "RCP/DEA",
        about: "Acerca de",
        contact: "Contacto",
        start: "Empezar a practicar",
        blurb: "Recursos independientes de práctica sobre temas de OSHA, conocimientos de CDL de California y fundamentos de RCP/DEA.",
        fall: "Cuestionario de protección contra caídas",
        gk: "Conocimientos generales CDL",
        adult: "Cuestionario de RCP en adultos",
        trades: "Oficios",
        teams: "Para equipos",
        what: "Qué somos",
        privacy: "Privacidad",
        terms: "Términos",
        disclaimer: "Aviso legal",
        support: "Desbloquear laboratorios — $9.99",
        tiktok: "TikTok",
        instagram: "Instagram",
        payBar:
          "Si este material le ayuda a aprender y prepararse, por favor pague. Bancos completos de OSHA, CDL y RCP. Escanee un código. $9.99.",
        payNav: "Pagar $9.99",
        payCash: "Pagar Cash App",
        payBtc: "Pagar Bitcoin",
        payUsdt: "Pagar USDT",
        legal:
          "© 2026 Safety Test Prep. Solo práctica educativa independiente. No se emiten certificaciones, tarjetas, licencias ni credenciales gubernamentales. No estamos afiliados ni respaldados por OSHA, el Departamento de Trabajo de EE. UU., el DMV de California, la American Heart Association, la Cruz Roja Americana ni ninguna agencia gubernamental.",
        copyLabel: "Copie este enlace",
        copied: "Enlace copiado",
        copyBelow: "Copie el enlace de abajo",
        copiedShort: "Copiado",
        selectText: "Seleccione el texto de arriba"
      }
    : {
        osha: "OSHA",
        cdl: "California CDL",
        cpr: "CPR/AED",
        about: "About",
        contact: "Contact",
        start: "Start Practicing",
        blurb: "Independent practice resources for OSHA topics, California CDL knowledge, and CPR/AED fundamentals.",
        fall: "Fall protection quiz",
        gk: "CDL General Knowledge",
        adult: "Adult CPR quiz",
        trades: "Trades",
        teams: "For teams",
        what: "What we are",
        privacy: "Privacy",
        terms: "Terms",
        disclaimer: "Disclaimer",
        support: "Unlock the full labs — $9.99",
        tiktok: "TikTok",
        instagram: "Instagram",
        payBar:
          "If this material helps you learn and prepare, please pay. Full OSHA, CDL, and CPR banks. Scan a code. $9.99.",
        payNav: "Pay $9.99",
        payCash: "Pay Cash App",
        payBtc: "Pay Bitcoin",
        payUsdt: "Pay USDT",
        legal:
          "© 2026 Safety Test Prep. Independent educational practice only. No certifications, cards, licenses, or government credentials are issued. Not affiliated with or endorsed by OSHA, the U.S. Department of Labor, the California DMV, the American Heart Association, the American Red Cross, or any government agency.",
        copyLabel: "Copy this link",
        copied: "Link copied",
        copyBelow: "Copy the link below",
        copiedShort: "Copied",
        selectText: "Select the text above"
      };

  var langSwitch =
    '<span class="lang-switch" role="navigation" aria-label="' +
    (isEs ? "Idioma" : "Language") +
    '">' +
    '<a href="' +
    enPath +
    '" lang="en" hreflang="en"' +
    (isEs ? "" : ' aria-current="true"') +
    ">EN</a>" +
    '<a href="' +
    esPath +
    '" lang="es" hreflang="es"' +
    (isEs ? ' aria-current="true"' : "") +
    ">ES</a>" +
    "</span>";

  function payPage() {
    return isEs ? "/es/support.html" : "/support.html";
  }

  function payBarHtml() {
    return (
      "<p><strong>" +
      copy.payBar +
      "</strong></p>" +
      '<p class="btns">' +
      '<a class="btn" href="' +
      payPage() +
      '#pay">' +
      copy.payCash +
      "</a>" +
      '<a class="btn" href="' +
      payPage() +
      '#pay">' +
      copy.payBtc +
      "</a>" +
      '<a class="btn" href="' +
      payPage() +
      '#pay">' +
      copy.payUsdt +
      "</a>" +
      "</p>"
    );
  }

  function insertPayBar() {
    if (/support\.html$/.test(path)) return;
    var existing = document.querySelector(".stp-pay-bar");
    if (existing) {
      existing.innerHTML = payBarHtml();
      existing.hidden = false;
      return;
    }
    var bar = document.createElement("aside");
    bar.className = "stp-pay-bar";
    bar.setAttribute("aria-label", copy.payNav);
    bar.innerHTML = payBarHtml();
    var mainEl = document.getElementById("main");
    var topbar = document.querySelector(".topbar");
    var wrap = document.querySelector(".app, .wrap");
    if (topbar && topbar.parentNode) topbar.parentNode.insertBefore(bar, topbar.nextSibling);
    else if (nav && nav.parentNode && !document.querySelector(".site-header")) nav.parentNode.insertBefore(bar, nav.nextSibling);
    else if (mainEl) mainEl.insertBefore(bar, mainEl.firstChild);
    else if (wrap) wrap.insertBefore(bar, wrap.firstChild);
    else document.body.insertBefore(bar, document.body.firstChild);
  }

  var ctaHtml = '<a class="btn nav-cta" href="' + payPage() + '#pay">' + copy.payNav + "</a>";

  if (nav) {
    nav.className = (nav.className + " nav").trim();
    nav.innerHTML =
      '<a class="brand" href="' +
      base +
      'index.html"><img class="brand-mark" src="/img/logo-mark.png" width="32" height="32" alt="">Safety Test Prep</a>' +
      '<span class="nav-links">' +
      '<a href="' +
      base +
      'osha-10-practice.html">' +
      copy.osha +
      "</a>" +
      '<a href="' +
      base +
      'california-cdl-practice.html">' +
      copy.cdl +
      "</a>" +
      '<a href="' +
      base +
      'cpr-aed-practice.html">' +
      copy.cpr +
      "</a>" +
      '<a href="' +
      base +
      'trades.html">' +
      copy.trades +
      "</a>" +
      '<a href="' +
      base +
      'about.html">' +
      copy.about +
      "</a>" +
      '<a href="' +
      base +
      'contact.html">' +
      copy.contact +
      "</a>" +
      "</span>" +
      langSwitch +
      ctaHtml;
    insertPayBar();
  } else {
    var first = document.querySelector(".topbar > div");
    if (first) {
      var wrap = document.createElement("div");
      wrap.className = "lab-lang";
      wrap.innerHTML = langSwitch;
      first.appendChild(wrap);
    }
    insertPayBar();
  }

  document.querySelectorAll(".stp-pay-bar, [data-stp-pay-first]").forEach(function (el) {
    el.hidden = false;
  });

  if (foot) {
    if (foot.className.indexOf("legal-foot") === -1) foot.className = (foot.className + " legal-foot").trim();
    var b = foot.getAttribute("data-base") || base;
    foot.innerHTML =
      "<p>" +
      copy.blurb +
      "</p>" +
      '<p class="foot-links">' +
      '<a href="' +
      b +
      'osha-10-practice.html">' +
      copy.osha +
      "</a> · " +
      '<a href="' +
      b +
      'california-cdl-practice.html">' +
      copy.cdl +
      "</a> · " +
      '<a href="' +
      b +
      'cpr-aed-practice.html">' +
      copy.cpr +
      "</a> · " +
      '<a href="' +
      b +
      'about.html">' +
      copy.about +
      "</a> · " +
      '<a href="' +
      b +
      'contact.html">' +
      copy.contact +
      "</a></p>" +
      '<p class="foot-links">' +
      '<a href="' +
      b +
      'osha/fall-protection.html">' +
      copy.fall +
      "</a> · " +
      '<a href="' +
      b +
      'cdl/general-knowledge.html">' +
      copy.gk +
      "</a> · " +
      '<a href="' +
      b +
      'cpr/adult-cpr.html">' +
      copy.adult +
      "</a></p>" +
      '<p class="foot-links">' +
      '<a href="' +
      b +
      'trades.html">' +
      copy.trades +
      "</a> · " +
      '<a href="' +
      b +
      'for-teams.html">' +
      copy.teams +
      "</a> · " +
      '<a href="' +
      b +
      'what-we-are.html">' +
      copy.what +
      "</a></p>" +
      '<p class="foot-links">' +
      '<a href="' +
      b +
      'privacy.html">' +
      copy.privacy +
      "</a> · " +
      '<a href="' +
      b +
      'terms.html">' +
      copy.terms +
      "</a> · " +
      '<a href="' +
      b +
      'disclaimer.html">' +
      copy.disclaimer +
      "</a> · " +
      '<a href="' +
      b +
      'support.html">' +
      copy.support +
      "</a></p>" +
      '<p class="foot-links">' +
      '<a href="https://www.tiktok.com/@safetytestprep" rel="noopener noreferrer" target="_blank">' +
      copy.tiktok +
      "</a> · " +
      '<a href="https://www.instagram.com/safetytestprep/" rel="noopener noreferrer" target="_blank">' +
      copy.instagram +
      "</a></p>" +
      "<p>" +
      copy.legal +
      "</p>";
  }

  if (!document.querySelector('link[rel="icon"]')) {
    var icon = document.createElement("link");
    icon.rel = "icon";
    icon.type = "image/svg+xml";
    icon.href = (base || "") + "img/favicon.svg";
    document.head.appendChild(icon);
  }

  function copyText(text) {
    if (navigator.clipboard && window.isSecureContext) {
      return navigator.clipboard.writeText(text).then(function () {
        return true;
      }).catch(function () {
        return copyLegacy(text);
      });
    }
    return Promise.resolve(copyLegacy(text));
  }

  function copyLegacy(text) {
    var ta = document.createElement("textarea");
    ta.value = text;
    ta.setAttribute("readonly", "");
    ta.style.cssText = "position:fixed;left:0;top:0;width:1px;height:1px;opacity:0";
    document.body.appendChild(ta);
    ta.focus();
    ta.select();
    var ok = false;
    try {
      ok = document.execCommand("copy");
    } catch (err) {
      ok = false;
    }
    document.body.removeChild(ta);
    return ok;
  }

  function shareUrlFor(share) {
    var url = share.getAttribute("data-url") || location.href;
    if (location.protocol === "http:") url = url.replace(/^https:\/\//i, "http://");
    return url;
  }

  function showShareLink(share, url) {
    var row = share.closest(".share-row") || share.parentNode;
    var box = row.querySelector(".share-fallback");
    if (!box) {
      box = document.createElement("p");
      box.className = "share-fallback";
      box.innerHTML = "<label>" + copy.copyLabel + '<input class="share-link" type="text" readonly /></label>';
      row.appendChild(box);
    }
    var input = box.querySelector("input");
    input.value = url;
    input.focus();
    input.select();
    try {
      input.setSelectionRange(0, url.length);
    } catch (err) {}
  }

  function markCopied(btn, ok) {
    var prev = btn.getAttribute("data-label") || btn.textContent;
    btn.setAttribute("data-label", prev);
    btn.textContent = ok ? copy.copied : copy.copyBelow;
    setTimeout(function () {
      btn.textContent = prev;
    }, 2200);
  }

  document.addEventListener("click", function (e) {
    var share = e.target.closest("[data-stp-share]");
    if (share) {
      e.preventDefault();
      var url = shareUrlFor(share);
      var title = share.getAttribute("data-title") || document.title;
      var text = share.getAttribute("data-text") || "";
      showShareLink(share, url);
      if (navigator.share && window.isSecureContext) {
        navigator.share({ title: title, text: text, url: url }).then(function () {
          markCopied(share, true);
        }).catch(function () {
          copyText(url).then(function (ok) {
            markCopied(share, ok);
          });
        });
        return;
      }
      copyText(url).then(function (ok) {
        markCopied(share, ok);
      });
      return;
    }
    var copyBtn = e.target.closest("[data-stp-copy]");
    if (copyBtn) {
      e.preventDefault();
      var sel = copyBtn.getAttribute("data-stp-copy");
      var el = sel ? document.querySelector(sel) : null;
      var val = el ? el.value || el.textContent : "";
      if (!val) return;
      var prev = copyBtn.textContent;
      copyText(val.trim()).then(function (ok) {
        copyBtn.textContent = ok ? copy.copiedShort : copy.selectText;
        setTimeout(function () {
          copyBtn.textContent = prev;
        }, 1600);
      });
    }
  });

  var mail = document.getElementById("contact-mail");
  if (mail) {
    var email = (window.STP_SITE && window.STP_SITE.contactEmail) || "safetytestprep@gmail.com";
    mail.href = "mailto:" + email;
    mail.textContent = email;
  }
})();
