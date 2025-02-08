function changeAvatar() {
    const avatarPreview = document.getElementById('avatarPreview');
    const colors = ['#ffcc00', '#ff6666', '#66ccff', '#cc66ff'];
    const randomColor = colors[Math.floor(Math.random() * colors.length)];
    avatarPreview.style.backgroundColor = randomColor;
}

function selectKeyword(keyword) {
    alert(keyword + " selected!");
}
