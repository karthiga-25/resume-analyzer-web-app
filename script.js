const roleInfoData = {
    "frontend developer": "HTML, CSS, JavaScript, React",
    "backend developer": "Python, SQL, APIs",
    "full stack developer": "Frontend + Backend",
    "devops engineer": "Docker, AWS, CI/CD",
    "data scientist": "Python, ML, Pandas, NumPy",
    "data analyst": "SQL, Excel, Power BI, Tableau",
    "mobile developer": "Android, Flutter, Kotlin",
    "software tester": "Manual Testing, Selenium",
    "cyber security": "Network Security, Ethical Hacking",
    "cloud engineer": "AWS, Azure, GCP"
};

// 🔹 Show role info
function showRoleInfo(){
    let role = document.getElementById("role").value;
    document.getElementById("roleInfo").innerText =
        role ? "Skills: " + roleInfoData[role] : "";
}

// 🔹 Display result
function displayResult(data){

    if(data.error){
        document.getElementById("result").innerHTML =
            `<p style="color:red">${data.error}</p>`;
        return;
    }

    let percent = data.score;

    let skills = data.found.map(s => `<span class="tag">${s}</span>`).join("");
    let missing = data.missing.map(s => `<span class="tag missing">${s}</span>`).join("");

    let circle = `
        <div class="circle" style="background: conic-gradient(green ${percent}%, gray ${percent}%);">
            ${percent}%
        </div>
    `;

    document.getElementById("result").innerHTML = `
        ${circle}
        <h3>Skills</h3>${skills}
        <h3>Missing</h3>${missing}
        <h3>Suggestions</h3>${data.suggestions.join("<br>")}
    `;
}

// 🔹 TEXT ANALYZE
function analyzeText(){
    let text = document.getElementById("resumeText").value;
    let role = document.getElementById("role").value;

    if(!role){
        alert("Please select a role!");
        return;
    }

    if(text.trim() === ""){
        alert("Paste resume first!");
        return;
    }

    fetch("http://127.0.0.1:8000/analyze-text",{
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify({text,role})
    })
    .then(res => res.json())
    .then(displayResult)
    .catch(err => console.log(err));
}

// 🔹 PDF ANALYZE
function analyzePDF(){
    let file = document.getElementById("pdfFile").files[0];
    let role = document.getElementById("role").value;

    if(!role){
        alert("Please select a role!");
        return;
    }

    if(!file){
        alert("Please select a PDF!");
        return;
    }

    let formData = new FormData();
    formData.append("file", file);
    formData.append("role", role);

    fetch("http://127.0.0.1:8000/analyze-pdf",{
        method:"POST",
        body:formData
    })
    .then(res => res.json())
    .then(displayResult)
    .catch(err => console.log(err));
}