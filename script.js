// ===============================
// CareerLens AI - Skills Logic
// ===============================

const analyzeButton = document.querySelector(".continue-area a");

analyzeButton.addEventListener("click", function (event) {

    // Stop the link from opening immediately
    event.preventDefault();

    // Store selected skills
    const selectedSkills = [];

    const checkboxes = document.querySelectorAll(
        '.skill-card input[type="checkbox"]'
    );

    checkboxes.forEach(function (checkbox) {

        if (checkbox.checked) {

            const skillName = checkbox.value;

            selectedSkills.push(skillName);
        }

    });


    // Get overall skill level
    const skillLevel =
        document.getElementById("skillLevel").value;


    // Check if at least one skill is selected
    if (selectedSkills.length === 0) {

        alert("Please select at least one skill.");

        return;
    }


    // Check skill level
    if (skillLevel === "") {

        alert("Please select your overall skill level.");

        return;
    }


    // Create data object
    const skillData = {

        skills: selectedSkills,

        level: skillLevel

    };


    // Save temporarily in browser
    localStorage.setItem(
        "careerLensSkills",
        JSON.stringify(skillData)
    );


    // Go to result page
    window.location.href = "result.html";

});