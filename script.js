function toggleTheme() {
    const html = document.documentElement;
    const currentTheme = html.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    html.setAttribute('data-theme', newTheme);
}

async function getAnswer(question) {
    try{
        const response = await fetch("https://huggingface.co/spaces/nxnccy/ask", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ question }),
        });

        if (!response.ok) {
            console.error("Error status:", response.status, response.statusText);
            throw new Error("Failed to fetch answer from the server.");
        }

        const result = await response.json();
        console.log("API Response:",result);
        return result;
    }
    catch (error){
        console.error("Fetch Eroor:",error);
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
