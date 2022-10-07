document.addEventListener("DOMContentLoaded", function () {
    const options = {
        method: "GET",
        credentials: 'include',
        headers: {
            'Authorization': "Bearer " + localStorage.getItem("access_token")
        }
    }

    fetch("https://bloomware.org/api/users/me", options)
        .then(res => {
            res.json().then(data => {
                if (!data["email_verified"]) {

                }
            })
        })
}