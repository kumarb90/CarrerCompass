document.getElementById("suggestBtn").addEventListener("click", suggestJobs);

async function suggestJobs() {
  const resume = document.getElementById("resumeText").value.trim();
  const jobResults = document.getElementById("jobResults");

  if (!resume) {
    alert("Please paste your resume");
    return;
  }
  jobResults.innerHTML = `
    <div class="loading">
      <div class="spinner"></div>
      <span>Analyzing your resume...</span>
    </div>
  `;

  try {
    const res = await fetch("http://127.0.0.1:5000/suggest_jobs", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ resume })
    });

    const data = await res.json();
    jobResults.innerHTML = "";

    if (!data.jobs || data.jobs.length === 0) {
      jobResults.innerHTML = "<p>No job suggestions found.</p>";
      return;
    }

    data.jobs.forEach(job => {
      const role = job.role || job.title || "Relevant Role";
      const company = job.company || "Company";
      const description =
        job.description || job.summary || "No description available.";

      const div = document.createElement("div");
      div.className = "job-card";
      div.innerHTML = `
        <h3>${role}</h3>
        <div class="company">${company}</div>
        <p>${description}</p>
      `;

      jobResults.appendChild(div);
    });

  } catch (error) {
    console.error(error);
    jobResults.innerHTML = "<p>Error fetching job suggestions.</p>";
  }
}
