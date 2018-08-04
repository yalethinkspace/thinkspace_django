// trying to use as little jQuery as possible
$(document).ready(function () {

    $("#sign-up-form").submit(function (event) {
        // prevent regular form submission
        event.preventDefault()

        // get the form content and project to make a comment for
        let first_name = $("#sign-up-first-name").val()
        let last_name = $("#sign-up-last-name").val()
        let username = $("#sign-up-username").val()
        let email = $("#sign-up-email").val()
        let password = $("#sign-up-password").val()
        let confirm_password = $("#sign-up-confirm-password").val()

        // remove existing errors
        $("#sign-up-first-name").removeClass("is-invalid")
        $("#sign-up-last-name").removeClass("is-invalid")
        $("#sign-up-email").removeClass("is-invalid")
        $("#sign-up-username").removeClass("is-invalid")
        $("#sign-up-password").removeClass("is-invalid")
        $("#sign-up-confirm-password").removeClass("is-invalid")
        $(".sign-up__right-panel__form__general-errors").text()
        
        // client side validation
        let client_side_pass = true

        if (confirm_password != password) {
            client_side_pass = false
            $("#sign-up-confirm-password").addClass("is-invalid")
            $(".sign-up__right-panel__form__confirm-password__feedback").text("Passwords do not match.")
        }
       
        if (client_side_pass) {

            // prepare payload
            let form = new FormData()
            form.append("first_name", first_name)
            form.append("last_name", last_name)
            form.append("email", email)
            form.append("username", username)
            form.append("password", password)

            // settings to POST
            let settings = {
                "async": true,
                "crossDomain": true,
                "url": "/sign-up",
                "method": "POST",
                "processData": false,
                "contentType": false,
                "mimeType": "multipart/form-data",
                "data": form
            }

            // change button to loading
            $(".sign-up__right-panel__form__submit").html("<i class='fas fa-circle-notch fa-spin'></i>")

            // send
            $.ajax(settings)
            .always(function ()
            {

            })
            .done(function (data, textStatus, jqXHR)
            {
                console.log("Registered!")
                window.location.replace("/login");
            })
            .fail(function (jqXHR, textStatus, errorThrown)
            {
                // reset register button
                $(".sign-up__right-panel__form__submit").html("Sign up")

                let response_errors = JSON.parse(jqXHR.responseText)
                console.log(response_errors)
                
                if ("username" in response_errors) {
                    $("#sign-up-username").addClass("is-invalid")
                    $(".sign-up__right-panel__form__username__feedback").text(response_errors["username"])
                }
                else if ("password" in response_errors) {
                    $("#sign-up__right-password").addClass("is-invalid")
                    $(".sign-up__right-panel__form__password__feedback").text(response_errors["password"])
                }
                else if ("email" in response_errors) {
                    $("#sign-up__email").addClass("is-invalid")
                    $(".sign-up__right-panel__form__email__feedback").text(response_errors["email"])
                }
                else {
                    for(key in response_errors)
                    {
                        $(".sign-up__right-panel__form__general-errors").text(response_errors[key])
                    }
                }
            })
        }

        // prevent regular form submission
        return false
    })
})