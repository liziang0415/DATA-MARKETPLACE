function showWishlist() {
    document.getElementById('wishlist').style.display = 'block';
    document.getElementById('displayReview2').style.display = 'none';
    document.getElementById('soldThreads').style.display = 'none';
}

function showReviews() {
    document.getElementById('wishlist').style.display = 'none';
    document.getElementById('displayReview2').style.display = 'block';
    document.getElementById('soldThreads').style.display = 'none';
}

function showSoldThreads() {
    document.getElementById('wishlist').style.display = 'none';
    document.getElementById('displayReview2').style.display = 'none';
    document.getElementById('soldThreads').style.display = 'block';
}

console.log("User profile JavaScript loaded.");
