document.getElementById("activate_btn").addEventListener("click", event => {
    const options = {
        method: "PUT",
        credentials: "include",
        headers: {
            'Authorization': "Bearer " + localStorage.getItem("access_token")
        }
    }

    fetch("https://bloomware.org/api/key/activate?key_raw=" + $("#key").value, options)
        .then(res => {
            res.json().then(data => {
                if (data["message"] === "successful activation") {
                    document.getElementById("error").innerText = "Successful activation!";
                } else {
                    document.getElementById("error").innerText = "Invalid key!";
                }
            })
        })
})
