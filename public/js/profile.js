export const tempData = {
    username: 'JohnDoe',
    bio: 'Welcome to my profile!',
    elo: 1500,
    rank: 'Gold',
};


function injectProfileHeaderData(params) {
    const profileHeader = document.querySelector('.profileheader');
    const buttonHeaderProfile = document.createElement('button');
    buttonHeaderProfile.className = 'button-header-profile';
    // Inject profile data into the header
    buttonHeaderProfile.innerHTML = `
        <h1>${params.username}</h1>
        <p>${params.bio}</p>
        <p>Elo: ${params.elo}</p>
        <p>Rank: ${params.rank}</p>
    `;
    profileHeader.appendChild(buttonHeaderProfile);
}

window.addEventListener('DOMContentLoaded', () => {
    // Inject the profile header data
    injectProfileHeaderData(tempData);
});