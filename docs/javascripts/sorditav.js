/* Sorditav ja otsitav tabel lisas "Sõnastik".
   Klõps veeru pealkirjal sordib (teine klõps pöörab järjekorra), tabeli kohal on otsinguväli. */
(function () {
  var collator = new Intl.Collator("et", { numeric: true, sensitivity: "base" });

  function cellText(row, i) {
    var c = row.cells[i];
    return c ? c.textContent.trim() : "";
  }

  function makeSortable(table) {
    if (table.dataset.sorditav) return;
    table.dataset.sorditav = "1";
    var head = table.tHead, body = table.tBodies[0];
    if (!head || !body || body.rows.length < 8) return;

    Array.prototype.forEach.call(head.rows[0].cells, function (th, i) {
      th.classList.add("sorditav");
      th.setAttribute("role", "button");
      th.setAttribute("tabindex", "0");
      th.title = "Sordi selle veeru järgi";
      function sort() {
        var dir = th.dataset.suund === "kasvav" ? "kahanev" : "kasvav";
        Array.prototype.forEach.call(head.rows[0].cells, function (o) {
          delete o.dataset.suund;
          o.removeAttribute("aria-sort");
        });
        th.dataset.suund = dir;
        th.setAttribute("aria-sort", dir === "kasvav" ? "ascending" : "descending");
        var rows = Array.prototype.slice.call(body.rows);
        rows.sort(function (a, b) {
          var r = collator.compare(cellText(a, i), cellText(b, i));
          return dir === "kasvav" ? r : -r;
        });
        rows.forEach(function (r) { body.appendChild(r); });
      }
      th.addEventListener("click", sort);
      th.addEventListener("keydown", function (e) {
        if (e.key === "Enter" || e.key === " ") { e.preventDefault(); sort(); }
      });
    });

    if (body.rows.length >= 40) {
      var box = document.createElement("input");
      box.type = "search";
      box.className = "tabeliotsing";
      box.placeholder = "Otsi tabelist…";
      box.setAttribute("aria-label", "Otsi tabelist");
      box.addEventListener("input", function () {
        var q = box.value.trim().toLowerCase();
        Array.prototype.forEach.call(body.rows, function (r) {
          r.hidden = q !== "" && r.textContent.toLowerCase().indexOf(q) === -1;
        });
      });
      var wrap = table.closest(".md-typeset__scrollwrap") || table;
      wrap.parentNode.insertBefore(box, wrap);
    }
  }

  function init() {
    if (!/\/lisad\/sonastik\//.test(location.pathname)) return;
    document.querySelectorAll("article table").forEach(makeSortable);
  }

  if (typeof document$ !== "undefined") document$.subscribe(init);
  else document.addEventListener("DOMContentLoaded", init);
})();
