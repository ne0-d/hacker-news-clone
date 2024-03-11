document.addEventListener('DOMContentLoaded', function() {
    var commentsList = document.getElementById('user-comments-list');
    var toggleButton = document.getElementById('toggle-comments-btn');

    toggleButton.addEventListener('click', function() {
        console.log("hello")
        if (commentsList.style.display === 'none' || commentsList.style.display === '') {
            commentsList.style.display = 'block';
        } else {
            commentsList.style.display = 'none';
        }
    });
});
