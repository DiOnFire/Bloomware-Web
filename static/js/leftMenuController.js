document.getElementById("dashboard_menu").addEventListener("click", event => {
    document.location.replace("https://bloomware.org/dashboard")
})

document.getElementById("account_menu").addEventListener("click", event => {
    document.location.replace("https://bloomware.org/account")
})

document.getElementById("support_menu").addEventListener("click", event => {
    document.location.replace("https://bloomware.org/support")
})

document.getElementById("downloads_menu").addEventListener("click", event => {
    document.location.replace("https://bloomware.org/downloads")
})

document.getElementById("sign_out_menu").addEventListener("click", event => {
    localStorage.clear()
    document.location.replace("https://bloomware.org/")
})