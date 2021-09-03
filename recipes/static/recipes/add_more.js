let addButton = document.querySelector("#add_more")

/* Getting the number of the last form on the page. (index 0, so minus 1).
Only want new form to be added to the page when user clicks add more button.
Need to create a function that performs remaining steps and attach it to the 
button press with event listener. */
addButton.addEventListener('click', addForm)

// e is event.
function addForm(e) {
    // Prevent default action of button click so only addForm is executed.
    e.preventDefault()

    // incrementing form count as it is static in html
    formCount++
    
    // Update the management form to use the correct value of TOTAL_FORMS
    // to allow extra forms to be saved. 
    let totalForms = document.getElementById("id_ingredients-TOTAL_FORMS")
    totalForms.setAttribute('value', formCount+1)
    // selecting anything with id ingredientform
    let ingredientForm = document.querySelector("#ingredientform")
    // browser parses html sent from server in to DOM. 
    /* creating a virtual div element that isn't rendered on the page 
    but you can do stuff with it and you can manually add it to the html. */
    let container = document.createElement('div');
    // giving container the class ingredientinfo
    container.classList.add('ingredientinfo');
    /* insert HTML string created by django in to the container. parses 
    HTML generated by django, which generates a DOM tree, which can be inserted
    in to the DOM */
    container.insertAdjacentHTML("beforeend", emptyForm.replace(/__prefix__/g, formCount))
    // adding the virtual DOM container to the actual DOM element included in the 
    // HTML and rendered on the page.
    ingredientForm.appendChild(container)

} 