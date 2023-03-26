// Handle different steps to create an account

let nextBtn = document.getElementById("next")
let prevBtn = document.getElementById("prev")
let step1 = document.getElementById("private-data")
let step2 = document.getElementById("body-data")

nextBtn.addEventListener('click', function () {
    step1.classList.replace("d-block", "d-none")
    step2.classList.replace("d-none", "d-block")
    window.scrollTo(0, 0);
})

prevBtn.addEventListener('click', function () {
    step2.classList.replace("d-block", "d-none")
    step1.classList.replace("d-none", "d-block")
    window.scrollTo(0, 0);
})

let form = document.querySelector("form")
let birthdate = document.getElementById("birthdate")
birthdate.max = new Date().toLocaleDateString('fr-FR')

// Validation eventListeners to validate fields in real time

form.firstname.addEventListener('change', function () {
    validate_firstname()
})

form.lastname.addEventListener('change', function () {
    validate_lastname()
})

form.birthdate.addEventListener('change', function () {
    validate_birthdate()
})

form.username.addEventListener('change', function () {
    validate_username()
})

form.email.addEventListener('change', function () {
    validate_email()
})

form.password.addEventListener('change', function () {
    validate_password() 
})

form.confirm_password.addEventListener('change', function () {
    validate_password() 
})

// Validation functions

function validate_firstname() {
    let firstname = document.getElementById("firstname")
    let regex = new RegExp("^(?=.{1,40}$)[a-zA-Z]+(?:[-'\s][a-zA-Z]+)*$");
    
    if (firstname.value == "" || regex.test(firstname.value) == false) {
        if (firstname.classList.contains("is-valid"))
            firstname.classList.replace("is-valid", "is-invalid")
        else
            firstname.classList.add("is-invalid")
        return false;
    }
    if (firstname.classList.contains("is-invalid"))
        firstname.classList.replace("is-invalid", "is-valid")
    else
        firstname.classList.add("is-valid")
    return true;
}

function validate_lastname() {
    let lastname = document.getElementById("lastname");
    let regex = new RegExp("^(?=.{1,40}$)[a-zA-Z]+(?:[-'\s][a-zA-Z]+)*$");
    
    if (lastname.value == "" || regex.test(lastname.value) == false) {
        if (lastname.classList.contains("is-valid"))
            lastname.classList.replace("is-valid", "is-invalid")
        else
            lastname.classList.add("is-invalid")
        return false;
    }
    if (lastname.classList.contains("is-invalid"))
        lastname.classList.replace("is-invalid", "is-valid")
    else
        lastname.classList.add("is-valid")
    return true;
}

function validate_birthdate() {
    let birthdate = document.getElementById("birthdate");
    let date = new Date(birthdate.value);
    let now = new Date();
    
    if (birthdate.value == "" || date == "Invalid Date" || date > now) {
        if (birthdate.classList.contains("is-valid"))
            birthdate.classList.replace("is-valid", "is-invalid")
        else
            birthdate.classList.add("is-invalid")
        return false;
    }
    if (birthdate.classList.contains("is-invalid"))
        birthdate.classList.replace("is-invalid", "is-valid")
    else
        birthdate.classList.add("is-valid")
    return true;
}

function validate_username() {
    let username = document.getElementById("username");
    let regex = new RegExp("^(?=.{1,40}$)[a-zA-Z]+(?:[-'\s][a-zA-Z]+)*$");
    
    if (username.value == "" || regex.test(username.value) == false) {
        if (username.classList.contains("is-valid"))
            username.classList.replace("is-valid", "is-invalid")
        else
            username.classList.add("is-invalid")
        return false;
    }
    if (username.classList.contains("is-invalid"))
        username.classList.replace("is-invalid", "is-valid")
    else
        username.classList.add("is-valid")
    return true;
}

function validate_email() {
    let email = document.getElementById("email");
    // let regex = /^[A-Za-z0-9_!#$%&'*+\/=?`{|}~^.-]+@[A-Za-z0-9.-]+$/gm;
    let regex = new RegExp("([!#-'*+/-9=?A-Z^-~-]+(\.[!#-'*+/-9=?A-Z^-~-]+)*|\"\(\[\]!#-[^-~ \t]|(\\[\t -~]))+\")@([!#-'*+/-9=?A-Z^-~-]+(\.[!#-'*+/-9=?A-Z^-~-]+)*|\[[\t -Z^-~]*])");

    if (email.value == "" || regex.test(email.value) == false) {
        if (email.classList.contains("is-valid"))
            email.classList.replace("is-valid", "is-invalid")
        else
            email.classList.add("is-invalid")
        return false
    }
    if (email.classList.contains("is-invalid"))
        email.classList.replace("is-invalid", "is-valid")
    else
        email.classList.add("is-valid")
    return true;
}

function validate_password() {
    let password = document.getElementById("password");
    let confirm_password = document.getElementById("confirm_password");
    
    if ((password.value == "" && confirm_password.value == "") || (password.value != confirm_password.value)) {
        if (password.classList.contains("is-valid") && confirm_password.classList.contains("is-valid")) {
            password.classList.replace("is-valid", "is-invalid")
            confirm_password.classList.replace("is-valid", "is-invalid")
        }
        else {
            password.classList.add("is-invalid")
            confirm_password.classList.add("is-invalid")
        }
        return false;
    }
    if (password.classList.contains("is-invalid") && confirm_password.classList.contains("is-invalid")) {
        password.classList.replace("is-invalid", "is-valid")
        confirm_password.classList.replace("is-invalid", "is-valid")
    }
    else {
        password.classList.add("is-valid")
        confirm_password.classList.add("is-valid")
    }
    return true;
}

function validate_bodydata() {
    // TODO
}