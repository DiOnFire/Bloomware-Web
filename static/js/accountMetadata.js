function getToken() {
    let vars = {};
    let parts = window.location.href.replace(/[?&]+([^=&]+)=([^&]*)/gi, function (m, key, value) {
        vars[key] = value;
    });
    return vars["token"]
}

function checkEmail(email) {
    let res = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
    return res.test(email);
}

function changeEmail() {
    let email = $("#email").value
    document.getElementById("error").innerText = ""
    if (checkEmail(email)) {
        const request = {
            method: "POST"
        }

        let url = new URL("https://bloomware.org/api/users/me/change_email")
        url.searchParams.append("email", email)
        url.searchParams.append("token", getToken())

        fetch(url.toString(), request)
            .then(res => document.location.replace("https://bloomware.org/account"))
    } else {
        document.getElementById("error").innerText = "Invalid email. Try again."
    }
}

function changePassword() {
    let password = document.getElementById("password")
    let password_confirm = document.getElementById("password_confirm")

    if (password.innerText === password_confirm.innerText && password_confirm.innerText.length >= 8) {
        const request = {
            method: "POST"
        }

        let url = new URL("https://bloomware.org/api/users/me/password_reset")
        url.searchParams.append("token", getToken())
        url.searchParams.append("password", password.innerText)

        fetch(url.toString(), request)
            .then(res => document.location.replace("some url"))
    } else {
        if (password.innerText.length < 8) {
            document.getElementById("error").innerText = "Password must contain 8 or more symbols"
        } else {
            document.getElementById("error").innerText = "Passwords doesn't match"
        }
    }
}