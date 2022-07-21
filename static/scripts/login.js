const loginForm = document.querySelector("#login-form-items")
const registerForm = document.querySelector("#register-form-items")

let toggled = false
const forms = [loginForm, registerForm]

function onToggleLoginClicked() {
    forms[toggled % 2].style.visibility = "hidden"
    forms[toggled % 2].style.height = "0px"
    forms[toggled % 2].style.width = "0px"
    forms[toggled % 2].style.display = "inline-block"
    forms[(toggled + 1) % 2].style.visibility = "visible"
    forms[(toggled + 1) % 2].style.height = "100%"
    forms[(toggled + 1) % 2].style.width = "100%"
    forms[(toggled + 1) % 2].style.display = "inline-block"
    toggled = !toggled
}