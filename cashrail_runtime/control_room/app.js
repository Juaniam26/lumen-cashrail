const refreshButton = document.querySelector("#refresh");
const rerunReadinessButton = document.querySelector("#rerun-readiness");
const walkthroughButton = document.querySelector("#walkthrough");
const walkthroughPanel = document.querySelector("#walkthrough-panel");
const runtimeState = document.querySelector("#runtime-state");
const sourceLabel = document.querySelector("#source-label");
const updatedAt = document.querySelector("#updated-at");
const verifiedProfit = document.querySelector("#verified-profit");
const readinessStatus = document.querySelector("#readiness-status");
const gateCount = document.querySelector("#gate-count");

function money(cents, currency) {
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency,
    maximumFractionDigits: 0,
  }).format(cents / 100);
}

async function rerunReadiness() {
  rerunReadinessButton.disabled = true;
  rerunReadinessButton.setAttribute("aria-busy", "true");
  runtimeState.textContent = "Running a safe readiness check…";
  try {
    const response = await fetch("/v1/control-room/readiness-check", {
      method: "POST",
      headers: { Accept: "application/json" },
      cache: "no-store",
    });
    if (!response.ok) throw new Error("Readiness check unavailable");
    const check = await response.json();
    readinessStatus.textContent = check.result.replace("_", " ");
    gateCount.textContent = `${check.passed} of ${check.total} gates passed`;
    sourceLabel.textContent = "Fresh readiness check";
    updatedAt.textContent = `Checked ${new Intl.DateTimeFormat("en-US", {
      hour: "numeric",
      minute: "2-digit",
    }).format(new Date(check.checked_at))}`;
    runtimeState.textContent = "Check complete · no bot started · no external action taken";
  } catch {
    runtimeState.textContent = "Readiness check failed · previous report preserved";
  } finally {
    rerunReadinessButton.disabled = false;
    rerunReadinessButton.removeAttribute("aria-busy");
  }
}

async function refreshStatus() {
  refreshButton.disabled = true;
  refreshButton.setAttribute("aria-busy", "true");
  runtimeState.textContent = "Checking Cashrail…";
  try {
    const response = await fetch("/v1/control-room/snapshot", {
      headers: { Accept: "application/json" },
      cache: "no-store",
    });
    if (!response.ok) throw new Error("Snapshot unavailable");
    const snapshot = await response.json();
    verifiedProfit.textContent = money(
      snapshot.money.verified_net_profit,
      snapshot.money.currency,
    );
    sourceLabel.textContent = "Live read-only snapshot";
    updatedAt.textContent = `Updated ${new Intl.DateTimeFormat("en-US", {
      hour: "numeric",
      minute: "2-digit",
    }).format(new Date(snapshot.updated_at))}`;
    runtimeState.textContent = snapshot.external_execution_enabled
      ? "Controller online · external execution enabled"
      : "Controller online · external execution locked";
  } catch {
    sourceLabel.textContent = "Last known Bot 1 report";
    runtimeState.textContent = "Live status unavailable · showing the last known report";
  } finally {
    refreshButton.disabled = false;
    refreshButton.removeAttribute("aria-busy");
  }
}

walkthroughButton.addEventListener("click", () => {
  const opening = walkthroughPanel.hidden;
  walkthroughPanel.hidden = !opening;
  walkthroughButton.textContent = opening ? "Hide walkthrough" : "Show me how it works";
  walkthroughButton.setAttribute("aria-expanded", String(opening));
  if (opening) walkthroughPanel.scrollIntoView({ behavior: "smooth", block: "nearest" });
});

refreshButton.addEventListener("click", refreshStatus);
rerunReadinessButton.addEventListener("click", rerunReadiness);
refreshStatus();
