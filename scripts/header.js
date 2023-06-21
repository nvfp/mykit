


// select all buttons in the header
const BTNS = document.querySelectorAll("header button");

// add click listener to each button
BTNS.forEach((btn) => {
    btn.addEventListener("click", () => {

        let id = btn.id;
        let text = btn.textContent;
        // console.log(`DEBUG: id: ${id}`)

        // the div
        let div = document.querySelector(`header #${id}-div`);

        if (text.startsWith("v")) {  // when expanded
            div.style.display = 'none';
            btn.textContent = ">" + text.slice(1);
        } else {  // closed
            div.style.display = 'flex';
            btn.textContent = "v" + text.slice(1);
        }
    });
});