if (localStorage.getItem("access_token") !== null) {
    document.location.replace("https://bloomware.org/account")
} else {
    $("#form").addEventListener("submit", event => {
        event.preventDefault()

        const user_data = {
            username: $("#email").value,
            password: $("#password").value
        }

        if (user_data["username"].length < 3) {
            document.getElementById("error").innerText = "Nickname too short!"
            return
        }

        if (user_data["password"] < 8) {
            document.getElementById("error").innerText = "Your password should contain 8 or more symbols!"
            return
        }

        const options = {
            method: "POST",
            body: JSON.stringify(user_data),
            headers: {
                'Content-Type': 'application/json'
            }
        }

        fetch("https://bloomware.org/api/users/auth", options)
            .then(res => res.json())
            .then(res => {
                if (res["error"] !== "invalid credentials") {
                    localStorage.setItem("access_token", res["access_token"]);
                    document.location.replace("https://bloomware.org/account");
                } else {
                    document.getElementById("error").innerText = "Invalid credentials!";
                }
            } );
    })
}