// Get modal elements
const modal = document.getElementById('userAgreementModal');
const openLink = document.getElementById('openAgreementLink');
const closeBtn = document.getElementsByClassName('close')[0];
const agreeCheckMain = document.getElementById('agreeCheckMain'); // Checkbox in the form
const agreeCheckModal = document.getElementById('agreeCheckModal'); // Checkbox in the modal
const agreeBtn = document.getElementById('agreeBtn');

// Function to check if the user has seen the agreement in the current session
function showAgreementIfFirstVisit() {
    // Check if 'hasSeenAgreement' is in sessionStorage
    if (!sessionStorage.getItem('hasSeenAgreement')) {
        // If not, show the modal
        modal.style.display = 'block';
    }
}

// Call the function on page load
window.onload = function() {
    showAgreementIfFirstVisit();
}

// Close the modal when the user clicks on the 'x'
closeBtn.onclick = function() {
    modal.style.display = 'none';
}

// Close the modal if the user clicks outside of it
window.onclick = function(event) {
    if (event.target === modal) {
        modal.style.display = 'none';
    }
}

// Enable or disable the "Agree and Submit" button in the modal
agreeCheckModal.onclick = function() {
    if (agreeCheckModal.checked) {
        agreeBtn.disabled = false;
        agreeBtn.classList.add('enabled');
    } else {
        agreeBtn.disabled = true;
        agreeBtn.classList.remove('enabled');
    }
}

// When the user clicks "Agree and Submit" in the modal
agreeBtn.onclick = function() {
    if (agreeCheckModal.checked) {
        modal.style.display = 'none';
        agreeCheckMain.checked = true; // Check the checkbox in the main form
        // Set 'hasSeenAgreement' to true in sessionStorage to track the current session
        sessionStorage.setItem('hasSeenAgreement', 'true');
    }
}

// Open the modal when the "Terms and Conditions" link is clicked
openLink.onclick = function(event) {
    event.preventDefault();
    modal.style.display = 'block';
}
