document.addEventListener("DOMContentLoaded", function () {
    const options = {
        method: "GET",
        credentials: 'include',
        headers: {
            'Authorization': "Bearer " + localStorage.getItem("access_token")
        }
    }
    
    document.getElementById("unlink_discord_btn").style.visibility = "hidden"

    fetch("https://bloomware.org/api/users/me", options)
        .then(res => {
            res.json().then(data => {
                document.getElementById("account_text").innerText = data["login"];
                document.getElementById("email_text").innerText = "Email: " + data["email"];
                document.getElementById("account_name_up").innerText = "Welcome, " + data["login"];
                applyDiscord(data);
            })
        })
})

function applyDiscord(data) {
    if (!data["discord_linked"]) {
        document.getElementById("discord_name").innerText = "Discord not linked!"
    } else {
        const request = {
            method: "GET",
            headers: {
                "Authorization": "Bearer " + data["discord_oauth"]
            }
        }

        fetch("https://discord.com/api/users/@me", request)
            .then(res => res.json())
            .then(res => {
                if (res["username"] === null) {
                    const request = {
                        method: "POST",
                        credentials: "include",
                        headers: {
                            'Authorization': "Bearer " + localStorage.getItem("access_token")
                        }
                    }

                    fetch("https://bloomware.org/api/users/me/discord/unlink", request)
                        .then(res => document.getElementById("discord_name").innerText = "Discord not linked! (Relink is required due invalid credentials)")
                } else {
                    document.getElementById("discord_name").innerText = "Logged in as: " + res["username"] + "#" + res["discriminator"]
                    document.getElementById("link_discord_btn").innerHTML = "Relink Discord"
                    document.getElementById("unlink_discord_btn").style.visibility = "visible"
                }
            })
    }
    if (data["email_verified"]) {
        document.getElementById("verify_email_btn").style.visibility = "hidden"
    }
}

function logout() {
    localStorage.clear();
}

function linkDiscord() {
    document.location.replace("https://discord.com/api/oauth2/authorize?client_id=964644356755709992&redirect_uri=https%3A%2F%2Fbloomware.org%2Faccount%2Fdiscord_link&response_type=code&scope=identify%20email")
}

function unlinkDiscord() {
    const request = {
        method: "POST",
        credentials: "include",
        headers: {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + localStorage.getItem("access_token")
        }
    }
    
    fetch("https://bloomware.org/api/users/me/discord/unlink", request)
        .then(res => window.location.reload())
}

function verifyEmail() {
    const request = {
        method: "GET",
        credentials: "include",
        headers: {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + localStorage.getItem("access_token")
        }
    }

    fetch("https://bloomware.org/api/users/me/mail_link", request)
        .then(res => document.location.replace("http://127.0.0.1:8000/account/email_verify"))
}

document.getElementById("link_discord_btn").addEventListener("click", event => {
    linkDiscord()
})
document.getElementById("unlink_discord_btn").addEventListener("click", event => {
    unlinkDiscord()
})
document.getElementById("verify_email_btn").addEventListener("click", event => {
    verifyEmail()
})