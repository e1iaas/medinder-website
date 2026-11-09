// Both tools run only in the browser: nothing typed here is sent or stored.
const T = window.T;
const $ = (id) => document.getElementById(id);
const say = (s, vars) => s.replace(/\{(\w+)\}/g, (_, k) => vars[k]);
const clock = new Intl.DateTimeFormat(T.lang, { hour: "numeric", minute: "2-digit" });

const doseTool = $("dose-tool");
if (doseTool) {
  const draw = () => {
    const [h, m] = ($("first").value || "08:00").split(":").map(Number);
    const every = Number($("every").value);
    const count = Math.max(1, Math.round(24 / every));
    const items = [];
    for (let i = 0; i < count; i++) {
      const minutes = h * 60 + m + i * every * 60;
      const d = new Date(2000, 0, 1, 0, minutes);
      const late = minutes >= 24 * 60 ? ` <span>(${T.next_day})</span>` : "";
      items.push(`<li>${say(T.dose, { n: i + 1 })}<b>${clock.format(d)}${late}</b></li>`);
    }
    $("dose-result").innerHTML = `<p><strong>${say(T.doses, { n: count })}</strong></p><ol>${items.join("")}</ol>`;
  };
  doseTool.addEventListener("input", draw);
  draw();
}

const chartTool = $("chart-tool");
if (chartTool) {
  const meds = [{ name: "", times: ["08:00"] }];
  const esc = (s) => s.replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" })[c]);
  // Monday first; 2024-01-01 was a Monday
  const days = [...Array(7)].map((_, i) => new Intl.DateTimeFormat(T.lang, { weekday: "short" }).format(new Date(2024, 0, 1 + i)));

  const chart = () => {
    const rows = meds.flatMap((med) => med.times.filter(Boolean).map((t) => {
      const [h, m] = t.split(":").map(Number);
      return `<tr><td><b>${esc(med.name || T.name)}</b><br>${clock.format(new Date(2000, 0, 1, h, m))}</td>${days.map(() => '<td class="box"></td>').join("")}</tr>`;
    }));
    $("chart").innerHTML = `<h2>${esc($("chart-title").value)}</h2><table><thead><tr><th>${T.name}</th>${days.map((d) => `<th>${d}</th>`).join("")}</tr></thead><tbody>${rows.join("")}</tbody></table>`;
  };

  const form = () => {
    $("rows").innerHTML = meds.map((med, i) => `
      <div class="med" data-i="${i}">
        <label>${T.name}<input type="text" data-k="name" value="${esc(med.name)}" placeholder="${esc(T.name_ph)}"></label>
        <span><b>${T.times}</b></span>
        <div class="times">${med.times.map((t, j) => `<input type="time" aria-label="${T.time} ${j + 1}" data-k="time" data-j="${j}" value="${t}">`).join("")}</div>
        <button type="button" class="linkbtn" data-act="time">+ ${T.add_time}</button>
        ${meds.length > 1 ? `<button type="button" class="linkbtn" data-act="remove">${T.remove}</button>` : ""}
      </div>`).join("");
    chart();
  };

  $("rows").addEventListener("input", (e) => {
    const med = meds[e.target.closest(".med").dataset.i];
    if (e.target.dataset.k === "name") med.name = e.target.value;
    else med.times[e.target.dataset.j] = e.target.value;
    chart();
  });
  $("rows").addEventListener("click", (e) => {
    const act = e.target.dataset.act;
    if (!act) return;
    const i = Number(e.target.closest(".med").dataset.i);
    if (act === "time") meds[i].times.push("20:00");
    else meds.splice(i, 1);
    form();
  });
  $("add-row").addEventListener("click", () => { meds.push({ name: "", times: ["08:00"] }); form(); });
  $("chart-title").addEventListener("input", chart);
  $("print").addEventListener("click", () => window.print());
  form();
}
