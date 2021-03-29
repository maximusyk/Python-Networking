!(function ($) {
    "use strict";

    $.fn.serializeObject = function () {

        var result = {};
        var extend = function (i, element) {
            var node = result[element.name];

            // If node with same name exists already, need to convert it to an array as it
            // is a multi-value field (i.e., checkboxes)

            if ('undefined' !== typeof node && node !== null) {
                if ($.isArray(node)) {
                    node.push(element.value);
                } else {
                    result[element.name] = [node, element.value];
                }
            } else {
                result[element.name] = element.value;
            }
        };

        $.each(this.serializeArray(), extend);
        return result;
    };

    var csrftoken = $('meta[name=csrf-token]').attr('content')

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type)) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    })

    // Preloader
    $(window).on('load', function () {
        if ($('#preloader').length) {
            $('#preloader').delay(100).fadeOut('slow', function () {
                $(this).remove();
            });
        }
    });

    // Hero typed
    if ($('.typed').length) {
        var typed_strings = $(".typed").data('typed-items');
        typed_strings = typed_strings.split(',');
        new Typed('.typed', {
            strings: typed_strings,
            loop: true,
            typeSpeed: 100,
            backSpeed: 50,
            backDelay: 2000
        });
    }

    // Activate smooth scroll on page load with hash links in the url
    $(document).ready(function () {
        if (window.location.hash) {
            var initial_nav = window.location.hash;
            if ($(initial_nav).length) {
                var scrollto = $(initial_nav).offset().top;
                $('html, body').animate({
                    scrollTop: scrollto
                }, 1500, 'easeInOutExpo');
            }
        }
    });

    $(document).on('click', '.mobile-nav-toggle', function (e) {
        $('body').toggleClass('mobile-nav-active');
        $('.mobile-nav-toggle i').toggleClass('icofont-navigation-menu icofont-close');
    });

    $(document).click(function (e) {
        var container = $(".mobile-nav-toggle");
        if (!container.is(e.target) && container.has(e.target).length === 0) {
            if ($('body').hasClass('mobile-nav-active')) {
                $('body').removeClass('mobile-nav-active');
                $('.mobile-nav-toggle i').toggleClass('icofont-navigation-menu icofont-close');
            }
        }
    });

    // Back to top button
    $(window).scroll(function () {
        if ($(this).scrollTop() > 100) {
            $('.back-to-top').fadeIn('slow');
        } else {
            $('.back-to-top').fadeOut('slow');
        }
    });

    $('.back-to-top').click(function () {
        $('html, body').animate({
            scrollTop: 0
        }, 1500, 'easeInOutExpo');
        return false;
    });

    // jQuery counterUp
    $('[data-toggle="counter-up"]').counterUp({
        delay: 10,
        time: 1000
    });

    // Skills section
    $('.skills-content').waypoint(function () {
        $('.progress .progress-bar').each(function () {
            $(this).css("width", $(this).attr("aria-valuenow") + '%');
        });
    }, {
        offset: '80%'
    });

    // Init AOS
    function aos_init() {
        AOS.init({
            duration: 1000,
            once: true
        });
    }

    // Porfolio isotope and filter
    $(window).on('load', function () {
        var portfolioIsotope = $('.portfolio-container').isotope({
            itemSelector: '.portfolio-item'
        });

        $('#portfolio-flters li').on('click', function () {
            $("#portfolio-flters li").removeClass('filter-active');
            $(this).addClass('filter-active');

            portfolioIsotope.isotope({
                filter: $(this).data('filter')
            });
            aos_init();
        });

        // Initiate venobox (lightbox feature used in portofilo)
        $('.venobox').venobox({
            'share': false
        });

        // Initiate aos_init() function
        aos_init();

        $('[data-toggle="tooltip"]').tooltip();

    });

    // Portfolio details carousel
    $(".portfolio-details-carousel").owlCarousel({
        autoplay: true,
        dots: true,
        loop: true,
        items: 1
    });

    $(document).ready(function () {

        $('#createForm[data-toggle="collapse"]').click(function () {
            $(this).toggleClass("active");
            if ($(this).hasClass("active")) {
                $(this).text("Cancel");
            } else {
                $(this).text("Add new...");
            }
        });

    });

    $(function () {
        $('#datepick').daterangepicker({
            timePicker: true,
            startDate: moment().startOf('hour'),
            endDate: moment().startOf('hour').add(32, 'hour'),
            locale: {
                format: 'M/DD hh:mm A'
            }
        });
    });

    $('#formModal').appendTo('body');


    $(function () {
        $("#msg").hide();
        $("#doneBlock").hide();
        $("#add-task-btn").hide();
        $("#edit-task-btn").hide();
        $("#delete-task-btn").hide();
        $("#update-task-btn").hide();
        $("#createForm").on("click", function (event) {
            $("#task-form").trigger('reset');
            dateRange();
            $("#view-task").hide();
            $("#task-form").show();
            $("#update-task-btn").hide();
            $("#add-task-btn").show();
            $("#doneBlock").hide();
            $("#task-form").attr('action', '/todo/create');
            $("#formModalLabel").html("Add new task to ToDo list");
        });
        $("#add-task-btn").on("click", function (event) {
            sendAjaxForm("#task-form", "#msg");
            event.preventDefault();
        });
        $("#update-task-btn").on("click", function (event) {
            sendAjaxForm("#task-form", "#msg");
            event.preventDefault();
        });
    });

    function sendAjaxForm(form_ajax, msg) {
        var form = $(form_ajax);
        console.log(`\nADDING/UPDATING TASK WAS STARTED.`);
        $.ajax({
            type: form.attr('method'),
            url: form.attr('action'),
            data: form.serialize(),
            success: function (response) {
                var json = JSON.parse(response);
                console.log(json);
                if (json.success == 'true') {
                    console.log(`\nADDING/UPDATING TASK COMPLETE.`);
                    $("#formModal").modal('hide');
                    $("#ToDos").html(json.data);
                } else {
                    console.log(`\nADDING/UPDATING TASK FAILED.\nVALIDATION FAILED`);
                    $(msg).show().html(json.msg).removeClass('alert-success').addClass('alert-danger');
                    for (const key in json.errors) {
                        $("#" + key).removeClass('is-valid').addClass('is-invalid');
                        $("#" + key + "-validation").html(json.errors[key][0]).removeClass('valid-feedback').addClass('invalid-feedback');
                    }
                    for (const key in json.data) {
                        if (!json.errors.hasOwnProperty(key)) {
                            console.log(json.errors[key]);
                            $("#" + key).removeClass('is-invalid').addClass('is-valid');
                            $("#" + key + "-validation").html('Looks good!').removeClass('invalid-feedback').addClass('valid-feedback');
                        }
                    }
                }
            }, error: function (error) {
                console.log(`\nADDING/UPDATING TASK FAILED.\n${error}`);
            }
        });
    }





    // $('#test-range').on('click', function() {
    //     console.log($('#date-range').val().split(" - "));
    // });



})(jQuery);

function Edit(elm) {
    elm = Number(elm);
    $("#add-task-btn").hide();
    $("#view-task").hide();
    $("#edit-task-btn").hide();
    $("#delete-task-btn").hide();
    $("#doneBlock").show();
    $("#update-task-btn").show();
    $("#closeModal").show();
    $("#task-form").show();
    $("#task-form").attr('action', `/todo/${elm}/update`);
    $("#formModalLabel").html("Update task data");
    $.ajax({
        url: `/todo/${elm}/getById`,
        type: "POST",
        success: function (res) {
            var json = JSON.parse(res);
            $("#title").val(json.title);
            $("#priority").val(json.priority);
            $("#timeline").val(json.timeline);
            $("#description").val(json.description);
            $("#is_done").prop('checked', json.is_done);
        },
        error: function (error) {
            console.log("ERRORS", error);
        }
    });

}

function Delete(elm) {
    elm = Number(elm);
    console.log(`\nDELETING TASK '${elm}' WAS STARTED.`);
    $.ajax({
        type: "POST",
        url: `/todo/${elm}/delete`,
        success: function (res) {
            console.log(`\nDELETING TASK '${elm}' COMPLETE.`);
            var json = JSON.parse(res);
            $("#ToDos").html(json.data);
            $("#formModal").modal('hide');
        },
        error: function (error) {
            console.log(`\nDELETING TASK '${elm}' FAILED.`);
            console.log("ERRORS", error);
        }
    });
}

function doneChange(elm) {
    elm = Number(elm);
    console.log(`\nMARK/UNMARK TASK '${elm}' AS TODO.`);
    $.ajax({
        type: "POST",
        url: `/todo/${elm}/markTodo`,
        contentType: "application/json",
        dataType: "json",
        data: JSON.stringify({
            check: $(`#check-${elm}`).prop("checked")
        }),
        success: function (res) {
            console.log(`\nMOVING TASK '${elm}' COMPLETE.`);
            $("#ToDos").html(res.data);
        },
        error: function (error) {
            console.log(`\nMOVING TASK '${elm}' FAILED.`);
            console.log("ERRORS", error);
        }
    });
}
function viewTask(elm) {
    elm = Number(elm);
    $("#task-form").hide();
    $("#view-task").show();
    $("#edit-task-btn").show();
    $("#add-task-btn").hide();
    $("#update-task-btn").hide();
    $("#closeModal").hide();
    $("#delete-task-btn").show();
    $("#formModalLabel").html(`Task-${elm} data`);
    $("#delete-task-btn").on("click", () => {
        Delete(elm);
    });
    $("#edit-task-btn").on("click", () => {
        Edit(elm);
    });
    console.log(`\nVIEW TASK '${elm}'.`);
    $.ajax({
        type: "POST",
        url: `/todo/${elm}`,
        success: function (res) {
            var json = JSON.parse(res);
            console.log(`\nVIEWING TASK '${elm}' COMPLETE.`);
            console.table(json);
            $("#view-task").empty();

            for (const item in json) {
                if (Object.hasOwnProperty.call(json, item)) {
                    var row = document.createElement("h5");
                    if (item === 'Status') {
                        if (json[item] === false) {
                            row.appendChild(document.createTextNode(item + ": Ongoing"));
                        } else {
                            row.appendChild(document.createTextNode(item + ": Done"));
                        }
                    } else {
                        row.appendChild(document.createTextNode(item + ": " + json[item]));
                    }
                    $("#view-task").append(row);
                }
            }
        },
        error: function (error) {
            console.log(`\nVIEWING TASK '${elm}' FAILED.`);
            console.log("ERRORS", error);
        }
    });
}

function dateRange() {
    var start = moment();
    var end = moment().endOf('day');

    function setInput(start, end) {
        $('#timeline').val(start.format('MMM-D HH:mm') + ' - ' + end.format('MMM-D HH:mm'));
    }

    $('#date-range-open').daterangepicker({
        timePicker: true,
        timePicker24Hour: true,
        startDate: start,
        endDate: end,
        ranges: {
            'Today': [moment(), moment().endOf('day')],
            'Tomorrow': [moment(), moment().add(1, 'd').endOf('day')],
            'This week': [moment(), moment().endOf('week')],
            'This mounth': [moment(), moment().endOf('month')]
        }
    }, setInput);

    setInput(start, end);

}