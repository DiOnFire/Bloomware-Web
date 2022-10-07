if (localStorage.getItem("access_token") !== null) {
    document.location.replace("https://bloomware.org/account")
} else {
    $("#form").addEventListener("submit", event => {
        event.preventDefault()
        const user_data = {
            login: $("#nickname").value,
            password: $("#password").value,
            email: $("#email").value
        }

        const options = {
            method: "POST",
            body: JSON.stringify(user_data),
            headers: {
                'Content-Type': 'application/json'
            }
        }

        fetch("https://bloomware.org/api/users/create", options)
            .then(res => res.json())
            .then(res => {
                if (res["error"] !== undefined) {
                    document.getElementById("error").innerText = res["error"]
                } else {
                    document.location.replace("https://bloomware.org/account/register_verify")
                }
            })
    })
}