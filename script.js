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
                "Authorization": `Bearer ${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}`
            },
            body: JSON.stringify({ question }),
        });

        if (!response.ok) {
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
