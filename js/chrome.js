(function () {
  var foot = document.querySelector("[data-stp-footer]");
  var nav = document.querySelector("[data-stp-nav]");
  var base = "";
  if (foot) base = foot.getAttribute("data-base") || "";
  if (nav && nav.getAttribute("data-base") != null) base = nav.getAttribute("data-base") || base;

  if (nav) {
    nav.className = (nav.className + " nav").trim();
    nav.innerHTML =
      '<a href="' + base + 'index.html">Home</a>' +
      '<a href="' + base + 'about.html">About</a>' +
      '<a href="' + base + 'osha-10-practice.html">OSHA topics</a>' +
      '<a href="' + base + 'california-cdl-practice.html">CDL knowledge</a>' +
      '<a href="' + base + 'cpr-aed-practice.html">CPR/AED</a>' +
      '<a href="' + base + 'index.html#pay">Study support</a>';
  }

  if (foot) {
    if (foot.className.indexOf("legal-foot") === -1) foot.className = (foot.className + " legal-foot").trim();
    var b = foot.getAttribute("data-base") || base;
    foot.innerHTML =
      "<p>© 2026 Safety Test Prep. All rights reserved.</p>" +
      "<p>Independent educational practice resources. Not affiliated with or endorsed by OSHA, the U.S. Department of Labor, any state DMV, the American Heart Association, the American Red Cross, or any government agency.</p>" +
      '<p class="foot-links">' +
      '<a href="' + b + 'about.html">About</a> · ' +
      '<a href="' + b + 'contact.html">Contact</a> · ' +
      '<a href="' + b + 'privacy.html">Privacy</a> · ' +
      '<a href="' + b + 'terms.html">Terms</a> · ' +
      '<a href="' + b + 'disclaimer.html">Disclaimer</a> · ' +
      '<a href="' + b + 'accessibility.html">Accessibility</a> · ' +
      '<a href="' + b + 'copyright.html">Copyright / DMCA</a>' +
      "</p>";
  }

  var mail = document.getElementById("contact-mail");
  if (mail) {
    var email = (window.STP_SITE && window.STP_SITE.contactEmail) || "hello@safetytestprep.com";
    mail.href = "mailto:" + email;
    mail.textContent = email;
  }
})();
