(function () {
  var foot = document.querySelector("[data-stp-footer]");
  var nav = document.querySelector("[data-stp-nav]");
  var base = "";
  if (foot) base = foot.getAttribute("data-base") || "";
  if (nav && nav.getAttribute("data-base") != null) base = nav.getAttribute("data-base") || base;

  if (nav) {
    nav.className = (nav.className + " nav").trim();
    nav.innerHTML =
      '<a class="brand" href="' + base + 'index.html">Safety Test Prep</a>' +
      '<span class="nav-links">' +
      '<a href="' + base + 'osha-10-practice.html">OSHA</a>' +
      '<a href="' + base + 'california-cdl-practice.html">California CDL</a>' +
      '<a href="' + base + 'cpr-aed-practice.html">CPR/AED</a>' +
      '<a href="' + base + 'about.html">About</a>' +
      '<a href="' + base + 'contact.html">Contact</a>' +
      "</span>" +
      '<a class="btn ghost nav-cta" href="' + base + 'osha/">Start Practicing</a>';
  }

  if (foot) {
    if (foot.className.indexOf("legal-foot") === -1) foot.className = (foot.className + " legal-foot").trim();
    var b = foot.getAttribute("data-base") || base;
    foot.innerHTML =
      "<p>Independent practice resources for OSHA topics, California CDL knowledge, and CPR/AED fundamentals.</p>" +
      '<p class="foot-links">' +
      '<a href="' + b + 'osha-10-practice.html">OSHA</a> · ' +
      '<a href="' + b + 'california-cdl-practice.html">California CDL</a> · ' +
      '<a href="' + b + 'cpr-aed-practice.html">CPR/AED</a> · ' +
      '<a href="' + b + 'about.html">About</a> · ' +
      '<a href="' + b + 'contact.html">Contact</a></p>' +
      '<p class="foot-links">' +
      '<a href="' + b + 'osha/fall-protection.html">Fall protection quiz</a> · ' +
      '<a href="' + b + 'cdl/general-knowledge.html">CDL General Knowledge</a> · ' +
      '<a href="' + b + 'cpr/adult-cpr.html">Adult CPR quiz</a></p>' +
      '<p class="foot-links">' +
      '<a href="' + b + 'privacy.html">Privacy</a> · ' +
      '<a href="' + b + 'terms.html">Terms</a> · ' +
      '<a href="' + b + 'disclaimer.html">Disclaimer</a> · ' +
      '<a href="' + b + 'support.html">Keep the labs free — optional support</a></p>' +
      "<p>© 2026 Safety Test Prep. Independent educational practice only. No certifications, cards, licenses, or government credentials are issued. Not affiliated with or endorsed by OSHA, the U.S. Department of Labor, the California DMV, the American Heart Association, the American Red Cross, or any government agency.</p>";
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
      box.innerHTML = '<label>Copy this link<input class="share-link" type="text" readonly /></label>';
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
    btn.textContent = ok ? "Link copied" : "Copy the link below";
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
    var copy = e.target.closest("[data-stp-copy]");
    if (copy) {
      e.preventDefault();
      var sel = copy.getAttribute("data-stp-copy");
      var el = sel ? document.querySelector(sel) : null;
      var val = el ? (el.value || el.textContent) : "";
      if (!val) return;
      var prev = copy.textContent;
      copyText(val.trim()).then(function (ok) {
        copy.textContent = ok ? "Copied" : "Select the text above";
        setTimeout(function () { copy.textContent = prev; }, 1600);
      });
    }
  });

  var mail = document.getElementById("contact-mail");
  if (mail) {
    var email = (window.STP_SITE && window.STP_SITE.contactEmail) || "hello@safetytestprep.com";
    mail.href = "mailto:" + email;
    mail.textContent = email;
  }
})();
