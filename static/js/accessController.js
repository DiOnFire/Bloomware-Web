function auth() {
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
                if (data["detail"] === "Not authenticated") {
                    localStorage.clear();
                    document.location.replace("https://bloomware.org/login");
                }
            })
        })
}

document.addEventListener("DOMContentLoaded", function () {
    auth()
})