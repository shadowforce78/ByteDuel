import { tempData } from "./profile.js";

function injectCombat(params) {
    const combatSection = document.querySelector('.combatsection');
    const buttonCombat = document.createElement('button');
    buttonCombat.className = 'button-combat';
    buttonCombat.innerHTML = `
        <h2>Combat</h2>
        <p>Elo: ${params.elo}</p>
        <p>Rank: ${params.rank}</p>
    `;
    combatSection.appendChild(buttonCombat);
}

window.addEventListener('DOMContentLoaded', () => {
    // Inject the combat section data
    injectCombat(tempData);
});