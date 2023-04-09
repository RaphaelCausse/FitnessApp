// Ajout de post

let btn_add_post = document.getElementById('btn-add-post')
let div_form = document.getElementById('form-add-post')

btn_add_post.addEventListener('click', function () {
    toggle_add_post()
})

function toggle_add_post() {
    // Toggle du bouton
    if (btn_add_post.classList.contains("d-block")) {
        btn_add_post.classList.replace("d-block", "d-none")
    }
    else if (btn_add_post.classList.contains("d-none")) {
        btn_add_post.classList.replace("d-none", "d-block")
    }
    // Toggle du formulaire
    if (div_form.classList.contains("d-none")) {
        div_form.classList.replace("d-none", "d-block")
    }
    else if (div_form.classList.contains("d-block")) {
        div_form.classList.replace("d-block", "d-none")
    }
}

// Formulaire

let cancel_btn = document.getElementById('cancel')
cancel_btn.addEventListener('click', function () {
    cancel_input()
})

let form = document.querySelector("form")
form.message.addEventListener('change', function () {
    validate_add_post
})

// Fonctions du formulaire

function validate_add_post() {
    let input = document.getElementById('message')
    if (input.value == "" || input.value.lenght > input.maxLength) {
        if (input.classList.contains("is-valid"))
            input.classList.replace("is-valid", "is-invalid")
        else
            input.classList.add("is-invalid")
        return false
    }
    if (input.classList.contains("is-invalid"))
        input.classList.replace("is-invalid", "is-valid")
    else
        input.classList.add("is-valid")
    return true
}

function cancel_input() {
    let input = document.getElementById('message')
    input.setAttribute('value', "")
    toggle_add_post()
}