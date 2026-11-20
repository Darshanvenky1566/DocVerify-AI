const form = document.querySelector("#login-form");
const signIn = form.querySelector("button[type=submit]");
const status = document.querySelector("#status");
const dashboard = document.querySelector("#review-dashboard");
const queue = document.querySelector("#review-queue");
const signOut = document.querySelector("#logout");

let token;

async function request(path, options = {}) {
  const headers = new Headers(options.headers);
  if (token) headers.set("Authorization", `Bearer ${token}`);

  const response = await fetch(`/api${path}`, { ...options, headers });
  if (!response.ok) {
    const body = await response.json().catch(() => null);
    const message = typeof body?.detail === "string"
      ? body.detail
      : `Request failed (${response.status}).`;
    throw new Error(message);
  }
  return response;
}
function renderApplication(application) {
  const item = document.createElement("li");
  const title = document.createElement("strong");
  title.textContent = `${application.title} (#${application.id})`;

  const view = document.createElement("button");
  view.type = "button";
  view.textContent = "Show documents";

  const documents = document.createElement("ul");
  const path = `/reviews/${application.id}/documents`;
  item.append(title, " ", view, documents);

  view.addEventListener("click", async () => {
    view.disabled = true;
    status.textContent = "Loading documents…";

    try {
      const files = await (await request(path)).json();
      documents.replaceChildren();

      for (const file of files) {
        const row = document.createElement("li");
        const download = document.createElement("button");
        download.type = "button";
        download.textContent = `Download ${file.filename}`;

        download.addEventListener("click", async () => {
          download.disabled = true;
          status.textContent = "Downloading…";
          try {
            const response = await request(`${path}/${file.id}/download`);
            const url = URL.createObjectURL(await response.blob());
            const link = document.createElement("a");
            link.href = url;
            link.download = file.filename;
            document.body.append(link);
            link.click();
            link.remove();
            setTimeout(() => URL.revokeObjectURL(url), 1000);
            status.textContent = "Download started.";
          } catch (error) {
            status.textContent = error.message;
          } finally {
            download.disabled = false;
          }
        });

        row.append(download);
        documents.append(row);
      }

      status.textContent = files.length ? "" : "No documents attached.";
    } catch (error) {
      status.textContent = error.message;
    } finally {
      view.disabled = false;
    }
  });
  const decisionForm = document.createElement("form");

  const decisionLabel = document.createElement("label");
  decisionLabel.textContent = "Decision ";
  const decision = document.createElement("select");
  decision.required = true;
  decision.append(
    new Option("Choose a decision", ""),
    new Option("Approve", "approved"),
    new Option("Reject", "rejected"),
  );
  decisionLabel.append(decision);

  const reasonLabel = document.createElement("label");
  reasonLabel.textContent = " Reason ";
  const reason = document.createElement("input");
  reason.required = true;
  reasonLabel.append(reason);

  const submit = document.createElement("button");
  submit.type = "submit";
  submit.textContent = "Save decision";
  decisionForm.append(decisionLabel, reasonLabel, " ", submit);
  item.append(decisionForm);

  decisionForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    const explanation = reason.value.trim();
    if (!explanation) {
      status.textContent = "Enter a reason for the decision.";
      reason.focus();
      return;
    }

    submit.disabled = true;
    status.textContent = "Saving decision…";

    try {
      await request(`/reviews/${application.id}/decision`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          decision: decision.value,
          reason: explanation,
        }),
      });
      item.remove();
      status.textContent = `Application #${application.id} ${decision.value}.`;
    } catch (error) {
      status.textContent = error.message;
    } finally {
      submit.disabled = false;
    }
  });

  return item;
}
form.addEventListener("submit", async (event) => {
  event.preventDefault();
  signIn.disabled = true;
  status.textContent = "Signing in…";

  try {
    const response = await request("/auth/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(Object.fromEntries(new FormData(form))),
    });
    ({ access_token: token } = await response.json());

    const applications = await (await request("/reviews/queue")).json();
    queue.replaceChildren();
    for (const application of applications) {
      queue.append(renderApplication(application));
    }

    form.reset();
    form.closest("section").hidden = true;
    dashboard.hidden = false;
    status.textContent = applications.length ? "" : "No applications awaiting review.";
    signOut.focus();
  } catch (error) {
    if (token) await request("/auth/logout", { method: "POST" }).catch(() => {});
    token = undefined;
    status.textContent = error.message;
  } finally {
    signIn.disabled = false;
  }
});

signOut.addEventListener("click", async () => {
  signOut.disabled = true;
  try {
    await request("/auth/logout", { method: "POST" });
    token = undefined;
    queue.replaceChildren();
    dashboard.hidden = true;
    form.closest("section").hidden = false;
    status.textContent = "Signed out.";
    form.elements.email.focus();
  } catch (error) {
    status.textContent = error.message;
  } finally {
    signOut.disabled = false;
  }
});

signIn.disabled = false;