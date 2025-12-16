document.querySelectorAll('input[name="resumeType"]').forEach(radio => {
  radio.addEventListener("change", () => {
    const type = document.querySelector('input[name="resumeType"]:checked').value;
    const resumeText = document.getElementById("resumeText");
    const resumeFile = document.getElementById("resumeFile");

    resumeText.style.display = "block";
    resumeFile.style.display = type === "upload" ? "block" : "none";
  });
});


async function uploadResumeFile() {
  const file = document.getElementById("resumeFile").files[0];
  if (!file) throw new Error("Please select a resume file");

  const formData = new FormData();
  formData.append("file", file);

  const resumeTextarea = document.getElementById("resumeText");
  resumeTextarea.value = "Extracting resume content...";

  const res = await fetch("http://127.0.0.1:5000/upload_resume", {
    method: "POST",
    body: formData
  });

  const data = await res.json();
  if (data.error) throw new Error(data.error);

  resumeTextarea.value = data.text || "No text extracted";
  return resumeTextarea.value;
}


const analyzeBtn = document.getElementById("analyzeBtn");
const btnText = analyzeBtn.querySelector(".btn-text");
const loader = document.getElementById("loader");

analyzeBtn.addEventListener("click", async () => {
  const jd = document.getElementById("jd").value.trim();
  if (!jd) return alert("Please paste Job Description");

  try {
    let resumeText = "";
    const mode = document.querySelector('input[name="resumeType"]:checked').value;

    if (mode === "paste") {
      resumeText = document.getElementById("resumeText").value.trim();
    } else {
      resumeText = await uploadResumeFile();
    }

    if (!resumeText) throw new Error("Resume content is empty");

  
    btnText.style.display = "none";
    analyzeBtn.disabled = true;
    loader.style.display = "flex";

    document.getElementById("score").innerHTML = "";
    document.getElementById("suggestions").innerHTML = "";
    document.getElementById("courses").innerHTML = "";

    const res = await fetch("http://127.0.0.1:5000/analyze", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ job_description: jd, resume: resumeText })
    });

    const data = await res.json();
    if (data.error) throw new Error(data.error);

    const score = Number(data.score || 0);
    const status = score >= 8 ? "Strong Match" : score >= 5 ? "Good Match" : "Weak Match";

    document.getElementById("score").innerHTML =
      `<b>Score:</b> ${score}/10<br><b>Status:</b> ${status}`;

    document.getElementById("suggestions").innerHTML =
      data.resume_suggestions?.length
        ? `<ul>${data.resume_suggestions.map(s => `<li>${s}</li>`).join("")}</ul>`
        : "<p>No resume suggestions.</p>";

    document.getElementById("courses").innerHTML =
      data.courses?.length
        ? `<ul>${data.courses.map(c => `<li>${c}</li>`).join("")}</ul>`
        : "<p>No courses recommended.</p>";

  } catch (err) {
    alert("Error: " + err.message);
  }

  loader.style.display = "none";
  btnText.style.display = "inline";
  analyzeBtn.disabled = false;
});
