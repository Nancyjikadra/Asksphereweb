function toggleTheme() {
    const html = document.documentElement;
    const currentTheme = html.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    html.setAttribute('data-theme', newTheme);
}

async function getAnswer(question) {
    try {
        const response = await fetch("https://nxnccy-ask.hf.space/api/predict", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": "Bearer hf_jwt_eyJhbGciOiJFZERTQSJ9.eyJyZWFkIjp0cnVlLCJwZXJtaXNzaW9ucyI6eyJyZXBvLmNvbnRlbnQucmVhZCI6dHJ1ZSwiaW5mZXJlbmNlLnNlcnZlcmxlc3Mud3JpdGUiOmZhbHNlfSwib25CZWhhbGZPZiI6eyJraW5kIjoidXNlciIsIl9pZCI6IjY2NTM2ZTUzMzNmYzc0NDE1Mzk1ZmU1NCIsInVzZXIiOiJueG5jY3kiLCJpc1BybyI6ZmFsc2UsImlzRW50ZXJwcmlzZU1lbWJlciI6ZmFsc2V9LCJpYXQiOjE3Mzc5MDIwMDIsInN1YiI6Ii9zcGFjZXMvbnhuY2N5L2FzayIsImV4cCI6MTczNzkwMjE3NSwiaXNzIjoiaHR0cHM6Ly9odWdnaW5nZmFjZS5jbyJ9.fC1DYsEuLNe0-_xLDHkNQjG5E8YHQFG2L0nMeOqbU9SrTIetVv8o_nIrZm1V_NOOUqY0z0heSDM07uVIRHtjAA" // Replace with your actual token
            },
            body: JSON.stringify({ question }),
        });

        if (!response.ok) {
            const errorText = await response.text();
            console.error("Error details:", response.status, response.statusText, errorText);
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error("Fetch Error:", error);
        throw error;
    }
}

document.getElementById('questionForm').onsubmit = async function (e) {
    e.preventDefault();

    const question = document.getElementById('question').value;
    const answerContainer = document.getElementById('answerContainer');
    const answerText = document.getElementById('answerText');

    answerText.textContent = "Generating answer...";
    answerContainer.style.display = "block";

    try {
        const result = await getAnswer(question);
        answerText.textContent = result.answer || "No answer found.";
    } catch (error) {
        console.error(error);
        answerText.textContent = "An error occurred. Please try again.";
    }
};
