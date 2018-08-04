// trying to use as little jQuery as possible
$(document).ready(function () {

    $("#login-form").submit(function (event) {
        // prevent regular form submission
        event.preventDefault()

        // get the form content and project to make a comment for
        let username = $("#login-username").val()
        let password = $("#login-password").val()

        // prepare payload
        let form = new FormData()
        form.append("username", username)
        form.append("password", password)

        // settings to POST
        let settings = {
            "async": true,
            "crossDomain": true,
            "url": "/login",
            "method": "POST",
            "processData": false,
            "contentType": false,
            "mimeType": "multipart/form-data",
            "data": form
        }

        // change login button to loading
        $(".login__right-panel__form__submit").html("<i class='fas fa-circle-notch fa-spin'></i>")
        // remove existing errors, if any
        $("#login-username").removeClass("is-invalid")
        $("#login-password").removeClass("is-invalid")
        $(".login__right-panel__form__general-errors").text()

        // send
        $.ajax(settings)
        .always(function ()
        {
            
        })
        .done(function (data, textStatus, jqXHR)
        {
            // redirect to the user's dashboard
            window.location.replace("/dashboard");
        })
        .fail(function (jqXHR, textStatus, errorThrown)
        {
            // reset login button
            $(".login__right-panel__form__submit").html("Login")
            // parse the response
            let response_json = JSON.parse(jqXHR.responseText)
            // gather the errors
            // render username errors, if any
            if ("username" in response_json) {
                $("#login-username").addClass("is-invalid")
                $(".login__right-panel__form__username__feedback").text(response_json["username"]) 
            }
            // render password errors, if any
            else if ("password" in response_json) {
                $("#login-password").addClass("is-invalid")
                $(".login__right-panel__form__password__feedback").text(response_json["password"])
            }
            // render all other errors
            else {
                $(".login__right-panel__form__general-errors").text(response_json["non_field_errors"])
            }
        })
        // prevent regular form submission
        return false
    })
})
