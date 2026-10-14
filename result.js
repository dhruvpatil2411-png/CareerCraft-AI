// ========================================
// CareerLens AI - Gemini AI Result
// ========================================

import {
    collection,
    addDoc
} from "https://www.gstatic.com/firebasejs/11.10.0/firebase-firestore.js";

import {
    db
} from "./firebase.js";


// ========================================
// GET STUDENT DATA
// ========================================

const profileData =
    JSON.parse(
        localStorage.getItem("careerLensProfile")
    );

const skillData =
    JSON.parse(
        localStorage.getItem("careerLensSkills")
    );


// ========================================
// CHECK DATA
// ========================================

if (!profileData || !skillData) {

    alert("Please complete the assessment first.");

    window.location.href = "assessment.html";

    throw new Error("Assessment data missing.");

}


// ========================================
// SHOW NAME
// ========================================

document.getElementById("userName").textContent =
    profileData.name;


// ========================================
// LOADING STATE
// ========================================

document.getElementById("careerName").textContent =
    "AI is analyzing your profile...";

document.getElementById("careerDescription").textContent =
    "Please wait while CareerLens AI creates your personalized career analysis.";

document.getElementById("matchScore").textContent =
    "--";


// ========================================
// GEMINI AI REQUEST
// ========================================

async function getAIAnalysis() {

    console.log("🤖 Sending student profile to AI...");

    const studentData = {

        name: profileData.name,

        age: profileData.age,

        education: profileData.education,

        interest: profileData.interest,

        goal: profileData.goal,

        skills: skillData.skills,

        skillLevel: skillData.level

    };


    console.log(
        "Student data:",
        studentData
    );


    const response = await fetch(
        "https://careercraft-ai-backend-2k0d.onrender.com/api/analyze",
        {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify(studentData)

        }
    );


    const data = await response.json();


    if (!response.ok) {

        console.error(
            "AI server error:",
            data
        );

        throw new Error(
            data.error ||
            "AI analysis failed."
        );

    }


    console.log(
        "✅ AI response received:",
        data
    );


    return data;

}


// ========================================
// DISPLAY AI RESULT
// ========================================

function displayAIResult(result) {


    // ------------------------------------
    // Career
    // ------------------------------------

    document.getElementById(
        "careerName"
    ).textContent =
        result.career;


    document.getElementById(
        "careerDescription"
    ).textContent =
        result.why_this_career;


    // ------------------------------------
    // Match Score
    // ------------------------------------

    document.getElementById(
        "matchScore"
    ).textContent =
        result.match_score + "%";


    // ------------------------------------
    // Strengths
    // ------------------------------------

    const strengthList =
        document.getElementById(
            "strengthList"
        );

    strengthList.innerHTML = "";


    result.strengths.forEach(
        function(strength) {

            const li =
                document.createElement("li");

            li.textContent =
                "✓ " + strength;

            strengthList.appendChild(li);

        }
    );


    // ------------------------------------
    // Skill Gaps
    // ------------------------------------

    const gapList =
        document.getElementById(
            "gapList"
        );

    gapList.innerHTML = "";


    result.skill_gaps.forEach(
        function(gap) {

            const li =
                document.createElement("li");

            li.textContent =
                "📌 " + gap;

            gapList.appendChild(li);

        }
    );


    // ------------------------------------
    // Roadmap
    // ------------------------------------

    const roadmapContainer =
        document.querySelector(
            ".roadmap"
        );


    if (roadmapContainer) {

        roadmapContainer.innerHTML = "";


        result.roadmap.forEach(
            function(step) {

                const stepDiv =
                    document.createElement("div");

                stepDiv.className =
                    "roadmap-step";


                stepDiv.innerHTML = `

                    <div class="step-number">
                        ${String(step.step).padStart(2, "0")}
                    </div>

                    <div>

                        <h3>
                            ${step.title}
                        </h3>

                        <p>
                            ${step.description}
                        </p>

                    </div>

                `;


                roadmapContainer.appendChild(
                    stepDiv
                );

            }
        );

    }


    // ------------------------------------
    // Recommended Projects
    // ------------------------------------

    const projectList =
        document.querySelector(
            ".project-list"
        );


    if (projectList) {

        projectList.innerHTML = "";


        result.projects.forEach(
            function(project, index) {

                const projectDiv =
                    document.createElement("div");

                projectDiv.className =
                    "project-item";


                projectDiv.innerHTML = `

                    <span>
                        ${String(index + 1).padStart(2, "0")}
                    </span>

                    <div>

                        <h3>
                            ${project}
                        </h3>

                        <p>
                            AI-recommended portfolio project
                        </p>

                    </div>

                `;


                projectList.appendChild(
                    projectDiv
                );

            }
        );

    }

}


// ========================================
// SAVE AI RESULT TO FIRESTORE
// ========================================

async function saveStudentData(
    aiResult
) {

    const studentData = {

        name:
            profileData.name,

        age:
            Number(profileData.age),

        education:
            profileData.education,

        interest:
            profileData.interest,

        goal:
            profileData.goal || "",

        skills:
            skillData.skills,

        skillLevel:
            skillData.level,

        recommendedCareer:
            aiResult.career,

        matchScore:
            aiResult.match_score,

        whyThisCareer:
            aiResult.why_this_career,

        strengths:
            aiResult.strengths,

        skillGaps:
            aiResult.skill_gaps,

        roadmap:
            aiResult.roadmap,

        projects:
            aiResult.projects,

        interviewTips:
            aiResult.interview_tips,

        createdAt:
            new Date().toISOString()

    };


    console.log(
        "🔥 Saving AI result to Firestore..."
    );


    const docRef =
        await addDoc(

            collection(
                db,
                "students"
            ),

            studentData

        );


    console.log(
        "✅ Firestore document created:",
        docRef.id
    );

}


// ========================================
// MAIN
// ========================================

async function runCareerLensAI() {

    try {

        console.log(
            "================================"
        );

        console.log(
            "🚀 CareerLens AI analysis started"
        );

        console.log(
            "================================"
        );


        // Get Gemini result

        const aiResult =
            await getAIAnalysis();


        // Display result

        displayAIResult(
            aiResult
        );


        // Save result

        await saveStudentData(
            aiResult
        );


        console.log(
            "================================"
        );

        console.log(
            "🎉 CareerLens AI completed!"
        );

        console.log(
            "================================"
        );


    }

    catch (error) {

        console.error(
            "❌ CareerLens AI Error:",
            error
        );


        document.getElementById(
            "careerName"
        ).textContent =
            "AI Analysis Failed";


        document.getElementById(
            "careerDescription"
        ).textContent =
            "Something went wrong while analyzing your profile. Please check that the backend server is running.";


        document.getElementById(
            "matchScore"
        ).textContent =
            "--";


        alert(
            "❌ AI analysis failed. Check the browser Console."
        );

    }

}


// ========================================
// START
// ========================================

runCareerLensAI();