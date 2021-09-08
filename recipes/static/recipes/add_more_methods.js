let addMethButton = document.querySelector("#add_more_methods")

/* Getting the number of the last form on the page. (index 0, so minus 1).
Only want new form to be added to the page when user clicks add more button.
Need to create a function that performs remaining steps and attach it to the 
button press with event listener. */
addMethButton.addEventListener('click', addMethForm)

function addMethForm(e) {
    e.preventDefault()

    // Increment the count of formset.
    methFormCount++

    // Selecting the formset element and incrementing it to allow saving of 
    // extra forms.
    let totalMethForms = document.getElementById("id_steps-TOTAL_FORMS")
    totalMethForms.setAttribute('value', methFormCount+1)

    // Selecting elements with the methodform id.
    let methodForm = document.querySelector("#methodform")

    // Creating a virtual div element called methContainer.
    let methContainer = document.createElement('div')
    // Giving the container the class methodinfo, which is already in HTML.
    methContainer.classList.add('methodinfo')

    // element.insertAdjacentHTML(position, text);
    // Parses specified text as HTML and inserts resulting nodes in to the DOM tree at specified position. 
    // Position is 'beforeend' to insert inside the the methContainer, after it's last child.
    methContainer.insertAdjacentHTML("beforeend", emptyMethForm.replace(/__prefix__/g, methFormCount))
    
    // Adds a node to the end of the list of children or a specified parent node.
    // Essentially, adding the methContainer to the end of methodform.
    methodForm.appendChild(methContainer)
}
