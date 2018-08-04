


// trying to use as little jQuery as possible
$(document).ready(function () {

    var settings = {
        "async": true,
        "crossDomain": true,
        "url": "client/static/courses.json",
        "method": "GET",
    }

    $.ajax(settings)
    .done(function (response) {
        courses_json = JSON.parse(response)
        courses = courses_json["results"]
        console.log(courses);
    });

    new Awesomplete(".dashboard__profile__course-search", {
        list: ["aol.com", "att.net", "comcast.net", "facebook.com", "gmail.com", "gmx.com", "googlemail.com", "google.com", "hotmail.com", "hotmail.co.uk", "mac.com", "me.com", "mail.com", "msn.com", "live.com", "sbcglobal.net", "verizon.net", "yahoo.com", "yahoo.co.uk"],
        data: function (text, input) {
            return input.slice(0, input.indexOf("@")) + "@" + text;
        },
        filter: Awesomplete.FILTER_STARTSWITH
    });

    $('.awesomplete').addClass('form-group').css('display', 'block').parent().css('display');
    $('.form-group-addon').appendTo('.awesomplete');
   
})
