function showCommentArea() {
    var commentArea = document.getElementById("comment-area");
    commentArea.classList.remove("hide");
}

function showCommentReplyArea(id) {
    var replyArea = document.getElementById(id);
    replyArea.classList.remove("hide");
}