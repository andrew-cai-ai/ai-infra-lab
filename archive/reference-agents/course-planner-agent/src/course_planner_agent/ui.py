"""Browser UI for the AI Course Planning Assistant MVP."""

from __future__ import annotations


def render_planner_ui() -> str:
    return """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>AI Course Planning Assistant</title>
  <style>
    :root {
      color-scheme: light;
      --ink: #202124;
      --muted: #667085;
      --line: #d7dde5;
      --soft: #f5f7fa;
      --paper: #ffffff;
      --brand: #b8202e;
      --brand-dark: #8c1420;
      --teal: #237b78;
      --gold: #b68a22;
      --green: #2d7d46;
      --red-soft: #fff1f2;
      --teal-soft: #ecf8f7;
      --gold-soft: #fff8e6;
      --shadow: 0 8px 22px rgba(31, 35, 40, 0.08);
    }

    * {
      box-sizing: border-box;
    }

    body {
      margin: 0;
      background: var(--soft);
      color: var(--ink);
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      letter-spacing: 0;
    }

    button,
    input,
    select {
      font: inherit;
    }

    .app-shell {
      min-height: 100vh;
      display: grid;
      grid-template-rows: auto 1fr;
    }

    .topbar {
      background: var(--paper);
      border-bottom: 1px solid var(--line);
      padding: 16px 24px;
      position: sticky;
      top: 0;
      z-index: 2;
    }

    .topbar-inner {
      max-width: 1360px;
      margin: 0 auto;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
    }

    .brand {
      display: flex;
      align-items: center;
      gap: 12px;
      min-width: 0;
    }

    .brand-mark {
      width: 40px;
      height: 40px;
      border-radius: 8px;
      display: grid;
      place-items: center;
      background: var(--brand);
      color: white;
      font-weight: 800;
      flex: 0 0 auto;
    }

    h1 {
      margin: 0;
      font-size: 20px;
      line-height: 1.2;
    }

    .subtitle {
      margin: 3px 0 0;
      color: var(--muted);
      font-size: 13px;
    }

    .status-pill {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      border: 1px solid #b7dfc3;
      background: #effaf2;
      color: var(--green);
      padding: 8px 10px;
      border-radius: 999px;
      font-size: 13px;
      white-space: nowrap;
    }

    .status-dot {
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: var(--green);
    }

    main {
      max-width: 1360px;
      width: 100%;
      margin: 0 auto;
      padding: 24px;
      display: grid;
      grid-template-columns: minmax(320px, 420px) 1fr;
      gap: 24px;
      align-items: start;
    }

    .panel {
      background: var(--paper);
      border: 1px solid var(--line);
      border-radius: 8px;
      box-shadow: var(--shadow);
    }

    .controls {
      position: sticky;
      top: 90px;
      max-height: calc(100vh - 114px);
      overflow: auto;
    }

    .panel-header {
      padding: 18px 18px 12px;
      border-bottom: 1px solid var(--line);
    }

    .panel-header h2 {
      font-size: 16px;
      margin: 0 0 4px;
    }

    .panel-header p {
      margin: 0;
      color: var(--muted);
      font-size: 13px;
      line-height: 1.45;
    }

    .form-body {
      padding: 18px;
      display: grid;
      gap: 18px;
    }

    .field {
      display: grid;
      gap: 8px;
    }

    label,
    .field-label {
      font-size: 13px;
      font-weight: 700;
      color: #344054;
    }

    input[type="text"],
    input[type="time"],
    select {
      width: 100%;
      min-height: 40px;
      border: 1px solid var(--line);
      border-radius: 6px;
      background: white;
      color: var(--ink);
      padding: 9px 10px;
    }

    input:focus,
    select:focus,
    button:focus-visible {
      outline: 3px solid rgba(184, 32, 46, 0.18);
      outline-offset: 2px;
    }

    .course-search {
      display: grid;
      grid-template-columns: 1fr auto;
      gap: 8px;
    }

    .small-button,
    .ghost-button {
      min-height: 40px;
      border: 1px solid var(--line);
      border-radius: 6px;
      background: white;
      color: #344054;
      padding: 8px 10px;
      cursor: pointer;
      white-space: nowrap;
    }

    .small-button:hover,
    .ghost-button:hover {
      border-color: #9aa6b2;
      background: #fafafa;
    }

    .course-list {
      display: grid;
      gap: 8px;
      max-height: 260px;
      overflow: auto;
      padding: 2px;
    }

    .course-choice {
      display: grid;
      grid-template-columns: 20px 1fr;
      gap: 8px;
      align-items: start;
      border: 1px solid var(--line);
      border-radius: 6px;
      padding: 9px;
      background: #fff;
    }

    .course-choice:hover {
      border-color: #aeb8c4;
    }

    .course-code {
      font-weight: 800;
      font-size: 13px;
    }

    .course-title {
      color: var(--muted);
      font-size: 12px;
      line-height: 1.35;
      margin-top: 2px;
    }

    .course-meta {
      color: #7a8699;
      font-size: 11px;
      margin-top: 5px;
    }

    .day-grid {
      display: grid;
      grid-template-columns: repeat(5, minmax(0, 1fr));
      gap: 6px;
    }

    .toggle input {
      position: absolute;
      opacity: 0;
      pointer-events: none;
    }

    .toggle span {
      display: grid;
      place-items: center;
      min-height: 38px;
      border: 1px solid var(--line);
      border-radius: 6px;
      background: white;
      color: #344054;
      cursor: pointer;
      font-size: 13px;
      font-weight: 700;
    }

    .toggle input:checked + span {
      background: var(--red-soft);
      color: var(--brand-dark);
      border-color: #e19aa2;
    }

    .time-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 10px;
    }

    .mode-grid {
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 6px;
    }

    .mode-grid .toggle span {
      min-height: 48px;
    }

    .actions {
      display: flex;
      gap: 10px;
      align-items: center;
    }

    .primary-button {
      width: 100%;
      min-height: 44px;
      border: 0;
      border-radius: 6px;
      background: var(--brand);
      color: white;
      font-weight: 800;
      cursor: pointer;
      padding: 10px 14px;
    }

    .primary-button:hover {
      background: var(--brand-dark);
    }

    .primary-button:disabled {
      background: #c9cdd3;
      cursor: progress;
    }

    .helper {
      color: var(--muted);
      font-size: 12px;
      line-height: 1.45;
    }

    .results {
      display: grid;
      gap: 18px;
      min-width: 0;
    }

    .summary-strip {
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 12px;
    }

    .metric {
      background: var(--paper);
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 14px;
      min-height: 82px;
    }

    .metric-value {
      font-size: 24px;
      font-weight: 850;
      line-height: 1.1;
    }

    .metric-label {
      margin-top: 6px;
      color: var(--muted);
      font-size: 12px;
    }

    .plan-grid {
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 14px;
    }

    .plan-card {
      display: grid;
      grid-template-rows: auto auto 1fr;
      min-height: 520px;
      background: var(--paper);
      border: 1px solid var(--line);
      border-radius: 8px;
      overflow: hidden;
    }

    .plan-card.recommended {
      border-color: #e19aa2;
      box-shadow: var(--shadow);
    }

    .plan-head {
      padding: 16px;
      border-bottom: 1px solid var(--line);
      display: flex;
      justify-content: space-between;
      gap: 12px;
      align-items: flex-start;
    }

    .plan-title {
      font-size: 16px;
      font-weight: 850;
      margin: 0;
    }

    .plan-rationale {
      margin: 6px 0 0;
      color: var(--muted);
      font-size: 12px;
      line-height: 1.45;
    }

    .badge {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      min-height: 26px;
      border-radius: 999px;
      padding: 4px 8px;
      font-size: 11px;
      font-weight: 800;
      white-space: nowrap;
    }

    .badge.easy,
    .badge.low {
      background: #edf8f0;
      color: var(--green);
    }

    .badge.balanced,
    .badge.medium {
      background: var(--gold-soft);
      color: #8a6517;
    }

    .badge.hard,
    .badge.high {
      background: var(--red-soft);
      color: var(--brand-dark);
    }

    .plan-stats {
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 1px;
      background: var(--line);
      border-bottom: 1px solid var(--line);
    }

    .plan-stat {
      background: #fbfcfd;
      padding: 10px 12px;
    }

    .plan-stat strong {
      display: block;
      font-size: 15px;
    }

    .plan-stat span {
      display: block;
      color: var(--muted);
      font-size: 11px;
      margin-top: 3px;
    }

    .course-rows {
      display: grid;
      gap: 0;
      align-content: start;
    }

    .course-row {
      padding: 14px 16px;
      border-bottom: 1px solid var(--line);
      display: grid;
      gap: 8px;
    }

    .course-row:last-child {
      border-bottom: 0;
    }

    .row-top {
      display: flex;
      justify-content: space-between;
      gap: 10px;
      align-items: flex-start;
    }

    .row-title {
      min-width: 0;
    }

    .row-title strong {
      display: block;
      font-size: 13px;
      overflow-wrap: anywhere;
    }

    .row-title span {
      display: block;
      color: var(--muted);
      font-size: 12px;
      margin-top: 3px;
      line-height: 1.35;
    }

    .score {
      color: var(--teal);
      font-size: 12px;
      font-weight: 800;
      white-space: nowrap;
    }

    .row-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 8px;
      color: #475467;
      font-size: 12px;
      line-height: 1.35;
    }

    .teacher-line {
      padding: 8px;
      border-radius: 6px;
      background: var(--teal-soft);
      color: #155e5b;
      font-size: 12px;
      line-height: 1.35;
    }

    .reason-list {
      margin: 0;
      padding-left: 16px;
      color: var(--muted);
      font-size: 12px;
      line-height: 1.45;
    }

    .excluded {
      background: var(--paper);
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 16px;
    }

    .excluded h2 {
      margin: 0 0 10px;
      font-size: 16px;
    }

    .excluded-list {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 8px;
    }

    .excluded-item {
      border: 1px solid var(--line);
      border-radius: 6px;
      padding: 10px;
      font-size: 12px;
      background: #fbfcfd;
    }

    .empty-state,
    .error-state {
      background: var(--paper);
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 24px;
      min-height: 220px;
      display: grid;
      align-content: center;
      gap: 8px;
      text-align: center;
    }

    .empty-state h2,
    .error-state h2 {
      margin: 0;
      font-size: 18px;
    }

    .empty-state p,
    .error-state p {
      margin: 0;
      color: var(--muted);
      line-height: 1.5;
    }

    .error-state {
      border-color: #e19aa2;
      background: var(--red-soft);
    }

    @media (max-width: 1180px) {
      main {
        grid-template-columns: 1fr;
      }

      .controls {
        position: static;
        max-height: none;
      }
    }

    @media (max-width: 900px) {
      .plan-grid,
      .summary-strip,
      .excluded-list {
        grid-template-columns: 1fr;
      }

      .plan-card {
        min-height: auto;
      }
    }

    @media (max-width: 640px) {
      .topbar {
        padding: 14px 16px;
      }

      .topbar-inner {
        align-items: flex-start;
        flex-direction: column;
      }

      main {
        padding: 16px;
      }

      .time-grid,
      .row-grid {
        grid-template-columns: 1fr;
      }
    }
  </style>
</head>
<body>
  <div class="app-shell">
    <header class="topbar">
      <div class="topbar-inner">
        <div class="brand">
          <div class="brand-mark" aria-hidden="true">YU</div>
          <div>
            <h1>AI Course Planning Assistant</h1>
            <p class="subtitle">York University multi-program planning MVP</p>
          </div>
        </div>
        <div class="status-pill"><span class="status-dot"></span><span>Mock York catalog connected</span></div>
      </div>
    </header>

    <main>
      <section class="panel controls" aria-label="Planner controls">
        <div class="panel-header">
          <h2>Student inputs</h2>
          <p>Choose completed courses, target requirements, availability, and planning style.</p>
        </div>

        <form id="planner-form" class="form-body">
          <div class="field">
            <label for="student-name">Student</label>
            <input id="student-name" type="text" value="York student" autocomplete="off">
          </div>

          <div class="field">
            <label for="program-select">Program</label>
            <select id="program-select"></select>
          </div>

          <div class="field">
            <label for="completed-filter">Completed courses</label>
            <div class="course-search">
              <input id="completed-filter" type="text" placeholder="Filter by code or title" autocomplete="off">
              <button class="small-button" type="button" data-select="completed">Clear</button>
            </div>
            <div id="completed-list" class="course-list" aria-label="Completed courses"></div>
          </div>

          <div class="field">
            <label for="required-filter">Courses still needed</label>
            <div class="course-search">
              <input id="required-filter" type="text" placeholder="Filter by code or title" autocomplete="off">
              <button class="small-button" type="button" data-select="required">Core</button>
            </div>
            <div id="required-list" class="course-list" aria-label="Required courses"></div>
          </div>

          <div class="field">
            <div class="field-label">Available days</div>
            <div class="day-grid" id="day-grid"></div>
          </div>

          <div class="field">
            <div class="field-label">Class time window</div>
            <div class="time-grid">
              <label>Start after
                <input id="earliest-start" type="time" value="09:00">
              </label>
              <label>End before
                <input id="latest-end" type="time" value="19:00">
              </label>
            </div>
          </div>

          <div class="field">
            <div class="field-label">Target mode</div>
            <div class="mode-grid" id="mode-grid">
              <label class="toggle"><input type="radio" name="mode" value="easy"><span>Easy</span></label>
              <label class="toggle"><input type="radio" name="mode" value="balanced" checked><span>Balanced</span></label>
              <label class="toggle"><input type="radio" name="mode" value="hard"><span>Hard</span></label>
            </div>
          </div>

          <div class="actions">
            <button id="generate-button" class="primary-button" type="submit">Generate plans</button>
          </div>

          <p class="helper">This MVP uses mock York program data. It recommends what to search for in the school enrollment system; it does not enroll the student.</p>
        </form>
      </section>

      <section class="results" aria-live="polite">
        <div id="results-root" class="empty-state">
          <h2>Ready to plan</h2>
          <p>Select a York program, pick completed courses and remaining requirements, then generate a course plan.</p>
        </div>
      </section>
    </main>
  </div>

  <script>
    const DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri"];

    const state = {
      programs: [],
      selectedProgram: "Kinesiology and Health Science",
      courses: [],
      defaultCompleted: [],
      defaultRequired: [],
      completedFilter: "",
      requiredFilter: "",
      selectedCompleted: new Set(),
      selectedRequired: new Set(),
    };

    const byId = (id) => document.getElementById(id);
    const escapeHtml = (value) => String(value)
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;")
      .replaceAll('"', "&quot;")
      .replaceAll("'", "&#039;");

    function renderPrograms() {
      byId("program-select").innerHTML = state.programs.map((program) => {
        const selected = program.name === state.selectedProgram ? "selected" : "";
        return `<option value="${escapeHtml(program.name)}" ${selected}>${escapeHtml(program.name)}</option>`;
      }).join("");
    }

    function renderDayToggles() {
      byId("day-grid").innerHTML = DAYS.map((day) => `
        <label class="toggle">
          <input type="checkbox" name="days" value="${day}" checked>
          <span>${day}</span>
        </label>
      `).join("");
    }

    function courseMatches(course, filterText) {
      const text = `${course.code} ${course.title}`.toLowerCase();
      return text.includes(filterText.trim().toLowerCase());
    }

    function renderCourseList(kind) {
      const filterText = kind === "completed" ? state.completedFilter : state.requiredFilter;
      const selected = kind === "completed" ? state.selectedCompleted : state.selectedRequired;
      const list = state.courses.filter((course) => courseMatches(course, filterText));
      const target = byId(`${kind}-list`);
      target.innerHTML = list.map((course) => {
        const checked = selected.has(course.code) ? "checked" : "";
        const prereq = course.prerequisites.length
          ? course.prerequisites.map((group) => group.join(" or ")).join("; ")
          : "No prerequisites";
        return `
          <label class="course-choice">
            <input type="checkbox" name="${kind}" value="${escapeHtml(course.code)}" ${checked}>
            <span>
              <span class="course-code">${escapeHtml(course.code)}</span>
              <span class="course-title">${escapeHtml(course.title)}</span>
              <span class="course-meta">${course.credits} credits | difficulty ${course.difficulty}/5 | ${escapeHtml(prereq)}</span>
            </span>
          </label>
        `;
      }).join("");
    }

    function selectedValues(name) {
      return Array.from(document.querySelectorAll(`input[name="${name}"]:checked`)).map((input) => input.value);
    }

    function payloadFromForm() {
      return {
        university: "York University",
        program: state.selectedProgram,
        completed_courses: Array.from(state.selectedCompleted),
        required_courses: Array.from(state.selectedRequired),
        preferred_schedule: {
          days: selectedValues("days"),
          earliest_start: byId("earliest-start").value || "09:00",
          latest_end: byId("latest-end").value || "19:00",
        },
        target_mode: document.querySelector('input[name="mode"]:checked').value,
      };
    }

    function renderMetric(value, label) {
      return `
        <div class="metric">
          <div class="metric-value">${escapeHtml(value)}</div>
          <div class="metric-label">${escapeHtml(label)}</div>
        </div>
      `;
    }

    function renderCourseRow(course) {
      const reasons = course.reasons.map((reason) => `<li>${escapeHtml(reason)}</li>`).join("");
      return `
        <article class="course-row">
          <div class="row-top">
            <div class="row-title">
              <strong>${escapeHtml(course.code)} | ${escapeHtml(course.title)}</strong>
              <span>Section ${escapeHtml(course.section)} | ${course.days.join(", ")} ${course.start}-${course.end}</span>
            </div>
            <span class="score">${course.score} pts</span>
          </div>
          <div class="teacher-line">
            Best matching instructor: <strong>${escapeHtml(course.professor)}</strong> (${course.professorRating}/5 mock rating)
          </div>
          <div class="row-grid">
            <div>Workload: ${course.estimatedWorkloadHours} hrs/week</div>
            <div>Difficulty: ${course.difficulty}/5</div>
            <div>Risk: <span class="badge ${course.workloadRisk}">${course.workloadRisk}</span></div>
            <div>Requirement: ${course.graduationRequirement ? "Yes" : "Supporting"}</div>
          </div>
          <ul class="reason-list">${reasons}</ul>
        </article>
      `;
    }

    function renderPlan(plan, recommendedTitle) {
      const isRecommended = plan.title === recommendedTitle;
      const courses = plan.courses.length
        ? plan.courses.map(renderCourseRow).join("")
        : '<article class="course-row"><div class="row-title"><strong>No valid courses</strong><span>Try widening availability or adding completed prerequisites.</span></div></article>';
      return `
        <article class="plan-card ${isRecommended ? "recommended" : ""}">
          <div class="plan-head">
            <div>
              <h2 class="plan-title">${escapeHtml(plan.title)}</h2>
              <p class="plan-rationale">${escapeHtml(plan.rationale)}</p>
            </div>
            <span class="badge ${plan.mode}">${isRecommended ? "Target" : plan.mode}</span>
          </div>
          <div class="plan-stats">
            <div class="plan-stat"><strong>${plan.totalCredits}</strong><span>credits</span></div>
            <div class="plan-stat"><strong>${plan.weeklyWorkloadHours}</strong><span>hrs/week</span></div>
            <div class="plan-stat"><strong>${plan.averageProfessorRating}</strong><span>avg rating</span></div>
          </div>
          <div class="course-rows">${courses}</div>
        </article>
      `;
    }

    function renderExcluded(excludedCourses) {
      if (!excludedCourses.length) {
        return "";
      }
      const items = excludedCourses.map((course) => `
        <div class="excluded-item">
          <strong>${escapeHtml(course.code)}</strong> ${escapeHtml(course.title)}
          <div class="course-title">${escapeHtml(course.reason)}</div>
        </div>
      `).join("");
      return `
        <section class="excluded">
          <h2>Why some courses were skipped</h2>
          <div class="excluded-list">${items}</div>
        </section>
      `;
    }

    function renderResults(data) {
      const targetPlan = data.plans.find((plan) => plan.title === data.recommendedPlan) || data.plans[1];
      byId("results-root").className = "results";
      byId("results-root").innerHTML = `
        <section class="summary-strip">
          ${renderMetric(data.recommendedPlan, "selected mode")}
          ${renderMetric(targetPlan.totalCredits, "target plan credits")}
          ${renderMetric(`${targetPlan.weeklyWorkloadHours} hrs`, "weekly workload")}
          ${renderMetric(targetPlan.averageProfessorRating, "avg professor rating")}
        </section>
        <section class="plan-grid">
          ${data.plans.map((plan) => renderPlan(plan, data.recommendedPlan)).join("")}
        </section>
        ${renderExcluded(data.excludedCourses)}
      `;
    }

    function renderError(message) {
      byId("results-root").className = "error-state";
      byId("results-root").innerHTML = `
        <h2>Planner could not run</h2>
        <p>${escapeHtml(message)}</p>
      `;
    }

    async function generatePlans() {
      const button = byId("generate-button");
      button.disabled = true;
      button.textContent = "Planning...";
      try {
        const response = await fetch("/plans", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payloadFromForm()),
        });
        if (!response.ok) {
          throw new Error(`API returned ${response.status}`);
        }
        renderResults(await response.json());
      } catch (error) {
        renderError(error.message || "Unknown planner error");
      } finally {
        button.disabled = false;
        button.textContent = "Generate plans";
      }
    }

    async function loadCourses() {
      const response = await fetch(`/mock-data/courses?program=${encodeURIComponent(state.selectedProgram)}`);
      const data = await response.json();
      state.selectedProgram = data.program;
      state.courses = data.courses;
      state.defaultCompleted = data.defaultCompletedCourses || [];
      state.defaultRequired = data.defaultRequiredCourses || [];
      state.selectedCompleted = new Set(state.defaultCompleted);
      state.selectedRequired = new Set(state.defaultRequired);
      renderCourseList("completed");
      renderCourseList("required");
      await generatePlans();
    }

    async function loadPrograms() {
      renderDayToggles();
      const response = await fetch("/mock-data/programs");
      const data = await response.json();
      state.programs = data.programs;
      renderPrograms();
      await loadCourses();
    }

    byId("completed-filter").addEventListener("input", (event) => {
      state.completedFilter = event.target.value;
      renderCourseList("completed");
    });

    byId("required-filter").addEventListener("input", (event) => {
      state.requiredFilter = event.target.value;
      renderCourseList("required");
    });

    document.querySelector('[data-select="completed"]').addEventListener("click", () => {
      state.selectedCompleted.clear();
      renderCourseList("completed");
    });

    document.querySelector('[data-select="required"]').addEventListener("click", () => {
      state.selectedRequired = new Set(state.defaultRequired);
      renderCourseList("required");
    });

    byId("program-select").addEventListener("change", async (event) => {
      state.selectedProgram = event.target.value;
      state.completedFilter = "";
      state.requiredFilter = "";
      byId("completed-filter").value = "";
      byId("required-filter").value = "";
      await loadCourses();
    });

    byId("completed-list").addEventListener("change", (event) => {
      if (event.target.name !== "completed") {
        return;
      }
      if (event.target.checked) {
        state.selectedCompleted.add(event.target.value);
      } else {
        state.selectedCompleted.delete(event.target.value);
      }
    });

    byId("required-list").addEventListener("change", (event) => {
      if (event.target.name !== "required") {
        return;
      }
      if (event.target.checked) {
        state.selectedRequired.add(event.target.value);
      } else {
        state.selectedRequired.delete(event.target.value);
      }
    });

    byId("planner-form").addEventListener("submit", (event) => {
      event.preventDefault();
      generatePlans();
    });

    loadPrograms().catch((error) => renderError(error.message || "Could not load mock York catalog"));
  </script>
</body>
</html>"""
