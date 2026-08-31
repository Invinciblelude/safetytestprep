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
      '<a href="' + b + 'privacy.html">Privacy</a> · ' +
      '<a href="' + b + 'terms.html">Terms</a> · ' +
      '<a href="' + b + 'disclaimer.html">Disclaimer</a> · ' +
      '<a href="' + b + 'support.html">Keep the labs free — optional support</a></p>' +
      "<p>© 2026 Safety Test Prep. Independent educational practice only. No certifications, cards, licenses, or government credentials are issued. Not affiliated with or endorsed by OSHA, the U.S. Department of Labor, the California DMV, the American Heart Association, the American Red Cross, or any government agency.</p>";
  }

  var mail = document.getElementById("contact-mail");
  if (mail) {
    var email = (window.STP_SITE && window.STP_SITE.contactEmail) || "hello@safetytestprep.com";
    mail.href = "mailto:" + email;
    mail.textContent = email;
  }
})();
