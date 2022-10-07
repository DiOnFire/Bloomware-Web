function getCode() {
    let vars = {};
    let parts = window.location.href.replace(/[?&]+([^=&]+)=([^&]*)/gi, function (m, key, value) {
        vars[key] = value;
    });
    return vars["code"]
}

function getAccessToken() {
    const params = new URLSearchParams();
    params.append('client_id', "964644356755709992");
    params.append('client_secret', "Oe7IlYn4eA_x3vnViULB_UbWptFQoftV");
    params.append('grant_type', 'authorization_code');
    params.append('code', getCode());
    params.append('redirect_uri', "https://bloomware.org/account/discord_link");

    const request = {
        method: "POST",
        body: params,
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
            'Accept': 'application/json'
        }
    }

    fetch("https://discord.com/api/oauth2/token", request)
        .then(res => res.json())
        .then(res => { linkDatabase(res["access_token"]) });
}

function linkDatabase(token) {
    const request = {
        method: "POST",
        credentials: 'include',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': "Bearer " + localStorage.getItem("access_token")
        }
    }

    fetch("https://bloomware.org/api/users/me/discord/link?discord_oauth=" + token, request)
        .then(res => document.location.replace())
}

document.addEventListener("DOMContentLoaded", function () {
    getAccessToken()
})