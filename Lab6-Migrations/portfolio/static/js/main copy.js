!(function ($) {
  "use strict";

  var csrftoken = $("meta[name=csrf-token]").attr("content");

  $.ajaxSetup({
    beforeSend: function (xhr, settings) {
      if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type)) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
      }
    },
  });

  // Preloader
  $(window).on("load", function () {
    if ($("#preloader").length) {
      $("#preloader")
        .delay(100)
        .fadeOut("slow", function () {
          $(this).remove();
        });
    }
  });

  // Hero typed
  if ($(".typed").length) {
    var typed_strings = $(".typed").data("typed-items");
    typed_strings = typed_strings.split(",");
    new Typed(".typed", {
      strings: typed_strings,
      loop: true,
      typeSpeed: 100,
      backSpeed: 50,
      backDelay: 2000,
    });
  }

  // Activate smooth scroll on page load with hash links in the url
  $(document).ready(function () {
    if (window.location.hash) {
      var initial_nav = window.location.hash;
      if ($(initial_nav).length) {
        var scrollto = $(initial_nav).offset().top;
        $("html, body").animate(
          {
            scrollTop: scrollto,
          },
          1500,
          "easeInOutExpo"
        );
      }
    }
  });

  $(document).on("click", ".mobile-nav-toggle", function (e) {
    $("body").toggleClass("mobile-nav-active");
    $(".mobile-nav-toggle i").toggleClass(
      "icofont-navigation-menu icofont-close"
    );
  });

  $(document).click(function (e) {
    var container = $(".mobile-nav-toggle");
    if (!container.is(e.target) && container.has(e.target).length === 0) {
      if ($("body").hasClass("mobile-nav-active")) {
        $("body").removeClass("mobile-nav-active");
        $(".mobile-nav-toggle i").toggleClass(
          "icofont-navigation-menu icofont-close"
        );
      }
    }
  });

  // Back to top button
  $(window).scroll(function () {
    if ($(this).scrollTop() > 100) {
      $(".back-to-top").fadeIn("slow");
    } else {
      $(".back-to-top").fadeOut("slow");
    }
  });

  $(".back-to-top").click(function () {
    $("html, body").animate(
      {
        scrollTop: 0,
      },
      1500,
      "easeInOutExpo"
    );
    return false;
  });

  // jQuery counterUp
  $('[data-toggle="counter-up"]').counterUp({
    delay: 10,
    time: 1000,
  });

  // Skills section
  $(".progress .progress-bar").each(function () {
    $(this).css("width", $(this).attr("aria-valuenow") + "%");
  });

  // Init AOS
  function aos_init() {
    AOS.init({
      duration: 1000,
      once: true,
    });
  }

  // Porfolio isotope and filter
  $(window).on("load", function () {
    var portfolioIsotope = $(".portfolio-container").isotope({
      itemSelector: ".portfolio-item",
    });

    $("#portfolio-flters li").on("click", function () {
      $("#portfolio-flters li").removeClass("filter-active");
      $(this).addClass("filter-active");

      portfolioIsotope.isotope({
        filter: $(this).data("filter"),
      });
      aos_init();
    });

    // Initiate venobox (lightbox feature used in portofilo)
    $(".venobox").venobox({
      share: false,
    });

    // Initiate aos_init() function
    aos_init();

    $("body").tooltip({
      selector: '[data-toggle="tooltip"]',
      trigger: "hover",
    });
  });

  // Portfolio details carousel
  $(".portfolio-details-carousel").owlCarousel({
    autoplay: true,
    dots: true,
    loop: true,
    items: 1,
  });

  $(function () {
    $("#datepick").daterangepicker({
      timePicker: true,
      startDate: moment().startOf("hour"),
      endDate: moment().startOf("hour").add(32, "hour"),
      locale: {
        format: "M/DD hh:mm A",
      },
    });
  });

  $("#formModal").appendTo("body");
  $(function () {
    $("#msg").hide();

    $("#todo-form").hide();
    $("#cat-form").hide();
    $("#task-form").hide();
    $("#empl-form").hide();

    $("#create-btn").hide();
    $("#add-btn").hide();
    $("#edit-btn").hide();
    $("#delete-btn").hide();
    $("#update-btn").hide();

    $("#doneBlock").hide();
    $("#cat-list").hide();
    $("#empl-list").hide();
    $("#task-list").hide();

    //#region CREATE BTNS
    $("#create-task-form").on("click", function (event) {
      AddTask();
    });
    $("#create-cat-form").on("click", () => {
      AddCategory();
    });
    $("#create-empl-form").on("click", () => {
      AddEmployee();
    });
    //#endregion
  });
})(jQuery);

// #region TASK CRUD
function AddTask() {
  $("#msg").hide();
  $(".modal-dialog").removeClass("modal-xl");
  $("#todo-form").trigger("reset");
  $("#cat-form").hide();
  $("#empl-form").hide();
  $("#task-list").hide();
  $("#cat-list").hide();
  $("#empl-list").hide();

  $("#edit-btn").hide();
  $("#delete-btn").hide();
  $("#update-btn").hide();

  $("#todo-form").show();
  $("#task-form").show();
  dateRange();
  $("#closeModal").show();
  $("#create-btn").show();
  $("#create-btn").html("Add");
  $("#create-btn").on("click", function (event) {
    createUpdateTask();
    event.preventDefault();
  });
  $("#doneBlock").hide();
  $("#todo-form").attr("action", "/todo/create");
  $("#formModalLabel").html("Add new Task");
}
function createUpdateTask() {
  var form = $("#todo-form");
  console.log(`\nADDING/UPDATING TASK WAS STARTED.`);
  $.ajax({
    type: form.attr("method"),
    url: form.attr("action"),
    data: form.serialize(),
    success: function (response) {
      var json = JSON.parse(response);
      console.log(json);
      if (json.success == "true") {
        console.log(`\nADDING/UPDATING TASK COMPLETE.`);
        $("#formModal").modal("hide");
        $("#ToDos").html(json.data);
      } else {
        console.log(`\nADDING/UPDATING TASK FAILED.\nVALIDATION FAILED`);
        $("#msg")
          .show()
          .html(json.msg)
          .removeClass("alert-success")
          .addClass("alert-danger");
        for (const key in json.errors) {
          $("#" + key)
            .removeClass("is-valid")
            .addClass("is-invalid");
          $("#" + key + "-validation")
            .html(json.errors[key][0])
            .removeClass("valid-feedback")
            .addClass("invalid-feedback");
        }
        for (const key in json.data) {
          if (!json.errors.hasOwnProperty(key)) {
            $("#" + key)
              .removeClass("is-invalid")
              .addClass("is-valid");
            $("#" + key + "-validation")
              .html("Looks good!")
              .removeClass("invalid-feedback")
              .addClass("valid-feedback");
          }
        }
      }
    },
    error: function (error) {
      console.log(`\nADDING/UPDATING TASK FAILED.\n${error}`);
    },
  });
}
function EditTask(elm) {
  elm = Number(elm);
  $("#todo-form").trigger("reset");
  $(".modal-dialog").removeClass("modal-xl");
  $("#task-list").hide();
  $("#cat-list").hide();
  $("#empl-list").hide();
  $("#category-form").hide();
  $("#empl-form").hide();
  $("#cat-form").hide();
  dateRange();

  $("#edit-btn").hide();
  $("#add-btn").hide();
  $("#delete-btn").hide();

  $("#todo-form").show();
  $("#task-form").show();
  $("#doneBlock").show();

  $("#closeModal").show();
  $("#update-btn").show();
  $("#formModalLabel").html("Update task data");
  $("#todo-form").attr("action", `/todo/${elm}/update`);
  $("#update-btn").on("click", function (event) {
    createUpdateTask();
    event.preventDefault();
  });
  $.ajax({
    url: `/todo/${elm}/get_by_id`,
    type: "POST",
    success: function (res) {
      var json = JSON.parse(res);
      $("#title").val(json.title);
      $("#priority").val(json.priority);
      $("#timeline").val(json.timeline);
      $("#category").val(json.category);
      for (const item of json.employee) {
        $("#employee")
          .find("option[value=" + item + "]")
          .prop("selected", "selected");
      }
      $("#description").val(json.description);
      $("#is_done").prop("checked", json.is_done);
    },
    error: function (error) {
      console.log("ERRORS", error);
    },
  });
}
function DeleteTask(elm) {
  elm = Number(elm);
  console.log(`\nDELETING TASK '${elm}' WAS STARTED.`);
  $.ajax({
    type: "POST",
    url: `/todo/${elm}/delete`,
    success: function (res) {
      console.log(`\nDELETING TASK '${elm}' COMPLETE.`);
      var json = JSON.parse(res);
      $("#ToDos").html(json.data);
      $("#formModal").modal("hide");
    },
    error: function (error) {
      console.log(`\nDELETING TASK '${elm}' FAILED.`);
      console.log("ERRORS", error);
    },
  });
}
function doneChange(elm) {
  elm = Number(elm);
  console.log(`\nMARK/UNMARK TASK '${elm}' AS TODO.`);
  $.ajax({
    type: "POST",
    url: `/todo/${elm}/mark_todo`,
    contentType: "application/json",
    dataType: "json",
    data: JSON.stringify({
      check: $(`#check-${elm}`).prop("checked"),
    }),
    success: function (res) {
      console.log(`\nMOVING TASK '${elm}' COMPLETE.`);
      $("#ToDos").html(res.data);
    },
    error: function (error) {
      console.log(`\nMOVING TASK '${elm}' FAILED.`);
      console.log("ERRORS", error);
    },
  });
}
function viewTask(elm) {
  elm = Number(elm);
  $(".modal-dialog").removeClass("modal-xl");
  $(".modal-dialog").addClass("modal-xl");
  $("#cat-list").hide();
  $("#empl-list").hide();
  $("#empl-form").hide();
  $("#cat-form").hide();
  $("#task-form").hide();
  $("#todo-form").hide();

  $("#update-btn").hide();
  $("#closeModal").hide();

  $("#add-btn").show();
  $("#add-btn").html("Add new");
  $("#edit-btn").show();
  $("#delete-btn").show();

  $("#view-task-table").bootstrapTable("showColumn", "Category");
  $("#task-list").show();

  $("#formModalLabel").html(`Task-${elm} data`);
  $("#delete-btn").on("click", () => {
    DeleteTask(elm);
  });
  $("#edit-btn").on("click", () => {
    EditTask(elm);
  });
  $("#add-btn").on("click", () => {
    AddTask(elm);
  });
  console.log(`\nVIEW TASK '${elm}'.`);
  $.ajax({
    type: "POST",
    url: `/todo/${elm}`,
    success: function (res) {
      var json = JSON.parse(res);
      var $table = $("#view-task-table");
      console.log(`\nVIEWING TASK '${elm}' COMPLETE.`);
      console.table(json);
      $table.bootstrapTable("removeAll");
      $table.bootstrapTable("append", json);
    },
    error: function (error) {
      console.log(`\nVIEWING TASK '${elm}' FAILED.`);
      console.log("ERRORS", error);
    },
  });
}
// #endregion

// #region CATEGORY CRUD
function AddCategory() {
  $("#msg").hide();
  $(".modal-dialog").removeClass("modal-xl");
  $("#todo-form").trigger("reset");
  $("#empl-form").hide();
  $("#task-form").hide();
  $("#task-list").hide();
  $("#empl-list").hide();

  $("#edit-btn").hide();
  $("#delete-btn").hide();
  $("#update-btn").hide();

  $("#cat-list").show();
  $("#todo-form").show();
  $("#cat-form").show();
  $("#closeModal").show();
  $("#create-btn").show();
  $("#create-btn").html("Add");
  $("#doneBlock").hide();
  $("#todo-form").attr("action", "/todo/category/create");
  $("#formModalLabel").html("Add new Category");
  $.ajax({
    type: "GET",
    url: `/todo/category/view`,
    success: function (res) {
      var json = JSON.parse(res);
      var $table = $("#view-cat-table");
      console.log(`\nVIEWING CATEGORIES COMPLETE.`);
      console.log(`\n${res}`);
      $table.bootstrapTable("load", json);
    },
    error: function (error) {
      console.log(`\nVIEWING CATEGORIES FAILED.`);
      console.log("ERRORS", error);
    },
  });

  $("#view-cat-table").on(
    "click-row.bs.table",
    function (field, value, row, $el) {
      viewCat(value.Name);
    }
  );
  $("#create-btn").on("click", function (event) {
    createUpdateCategory();
    event.preventDefault();
  });
}
function createUpdateCategory() {
  var form = $("#todo-form");
  console.log(`\nADDING/UPDATING CATEGORY WAS STARTED.`);
  $.ajax({
    type: form.attr("method"),
    url: form.attr("action"),
    data: form.serialize(),
    success: function (response) {
      var json = JSON.parse(response);
      console.log(json);
      if (json.success == "true") {
        console.log(`\nADDING/UPDATING CATEGORY COMPLETE.`);
        $("#formModal").modal("hide");
        $("#ToDos").html(json.data);
      } else {
        console.log(`\nADDING/UPDATING CATEGORY FAILED.\nVALIDATION FAILED`);
        $("#msg")
          .show()
          .html(json.msg)
          .removeClass("alert-success")
          .addClass("alert-danger");
        for (const key in json.errors) {
          $("#" + key)
            .removeClass("is-valid")
            .addClass("is-invalid");
          $("#" + key + "-validation")
            .html(json.errors[key][0])
            .removeClass("valid-feedback")
            .addClass("invalid-feedback");
        }
        for (const key in json.data) {
          if (!json.errors.hasOwnProperty(key)) {
            console.log(json.errors[key]);
            $("#" + key)
              .removeClass("is-invalid")
              .addClass("is-valid");
            $("#" + key + "-validation")
              .html("Looks good!")
              .removeClass("invalid-feedback")
              .addClass("valid-feedback");
          }
        }
      }
    },
    error: function (error) {
      console.log(`\nADDING/UPDATING CATEGORY FAILED.\n${error}`);
    },
  });
}
function EditCategory(elm) {
  $(".modal-dialog").removeClass("modal-xl");

  $("#task-form").hide();
  $("#add-btn").hide();
  $("#task-list").hide();
  $("#edit-btn").hide();
  $("#delete-btn").hide();

  $("#category-form").show();
  $("#cat-list").show();
  $("#doneBlock").show();
  $("#update-btn").show();
  $("#closeModal").show();
  $("#todo-form").show();
  $("#formModalLabel").html(`Update category '${elm}' data`);
  $("#todo-form").attr("action", `/todo/category/${elm}/update`);

  $.ajax({
    type: "GET",
    url: `/todo/category/view`,
    success: function (res) {
      var json = JSON.parse(res);
      var $table = $("#view-cat-table");
      console.log(`\nGETTING DATA COMPLETED.`);
      $("#cat_name").val(elm);
      $table.bootstrapTable("load", json);
    },
    error: function (error) {
      console.log(`\nVIEWING TASK '${elm}' FAILED.`);
      console.log("ERRORS", error);
    },
  });

  $("#view-cat-table").on(
    "click-row.bs.table",
    function (field, value, row, $el) {
      viewCat(value.Name);
    }
  );
  $("#update-btn").on("click", function (event) {
    createUpdateCategory();
    event.preventDefault();
  });
}
function DeleteCategory(elm) {
  console.log(`\nDELETING TASK '${elm}' WAS STARTED.`);
  $.ajax({
    type: "POST",
    url: `/todo/category/${elm}/delete`,
    success: function (res) {
      console.log(`\nDELETING TASK '${elm}' COMPLETE.`);
      var json = JSON.parse(res);
      $("#ToDos").html(json.data);
      $("#formModal").modal("hide");
    },
    error: function (error) {
      console.log(`\nDELETING TASK '${elm}' FAILED.`);
      console.log("ERRORS", error);
    },
  });
}
function viewCat(elm) {
  $(".modal-dialog").removeClass("modal-xl");
  $(".modal-dialog").addClass("modal-xl");

  $("#todo-form").hide();

  $("#update-btn").hide();
  $("#closeModal").hide();

  $("#cat-list").hide();
  $("#empl-list").hide();

  $("#view-task-table").bootstrapTable("hideColumn", "Category");
  $("#task-list").show();

  $("#add-btn").show();
  $("#add-btn").html("Add new");
  $("#edit-btn").show();
  $("#delete-btn").show();

  $("#formModalLabel").html(`Category-${elm} data`);
  $("#delete-btn").on("click", () => {
    if (elm === "Others") {
      alert("You cannot delete default Category!");
    } else {
      DeleteCategory(elm);
    }
  });
  $("#edit-btn").on("click", () => {
    EditCategory(elm);
  });
  $("#create-btn").on("click", () => {
    AddCategory();
  });
  console.log(`\nVIEW CATEGORY '${elm}'.`);
  $.ajax({
    type: "POST",
    url: `/todo/category/${elm}/view`,
    success: function (res) {
      var json = JSON.parse(res);
      var $table = $("#view-task-table");
      console.log(`\nVIEWING CATEGORY '${elm}' COMPLETE.`);
      console.table(json);
      $table.bootstrapTable("removeAll");
      $table.bootstrapTable("append", json);
    },
    error: function (error) {
      console.log(`\nVIEWING CATEGORY '${elm}' FAILED.`);
      console.log("ERRORS", error);
    },
  });
}
// #endregion

// #region EMPLOYEE CRUD
function AddEmployee() {
  $("#msg").hide();
  $(".modal-dialog").removeClass("modal-xl");
  $("#todo-form").trigger("reset");
  $("#task-form").hide();
  $("#task-list").hide();
  $("#cat-list").hide();
  $("#cat-form").hide();

  $("#edit-btn").hide();
  $("#delete-btn").hide();
  $("#update-btn").hide();

  $("#empl-form").show();
  $("#empl-list").show();
  $("#todo-form").show();
  $("#closeModal").show();
  $("#create-btn").show();
  $("#create-btn").html("Add");
  $("#doneBlock").hide();
  $("#todo-form").attr("action", "/todo/employee/create");
  $("#formModalLabel").html("Add new Employee");
  $.ajax({
    type: "GET",
    url: `/todo/employee/view`,
    success: function (res) {
      var json = JSON.parse(res);
      var $table = $("#view-empl-table");
      console.log(`\nVIEWING EMPLOYEES COMPLETE.`);
      $table.bootstrapTable("load", json);
    },
    error: function (error) {
      console.log(`\nVIEWING EMPLOYEES FAILED.`);
      console.log("ERRORS", error);
    },
  });

  $("#view-empl-table").on(
    "click-cell.bs.table",
    function (field, value, row, $el) {
      console.log(value);
      // viewEmployee(value.Name);
    }
  );
  $("#create-btn").on("click", function (event) {
    createUpdateEmployee();
    event.preventDefault();
  });
}
function createUpdateEmployee() {
  var form = $("#todo-form");
  console.log(`\nADDING/UPDATING EMPLOYEE WAS STARTED.`);
  $.ajax({
    type: form.attr("method"),
    url: form.attr("action"),
    data: form.serialize(),
    success: function (response) {
      var json = JSON.parse(response);
      console.log(json);
      if (json.success == "true") {
        console.log(`\nADDING/UPDATING EMPLOYEE COMPLETE.`);
        $("#formModal").modal("hide");
        $("#ToDos").html(json.data);
      } else {
        console.log(`\nADDING/UPDATING EMPLOYEE FAILED.\nVALIDATION FAILED`);
        $("#msg")
          .show()
          .html(json.msg)
          .removeClass("alert-success")
          .addClass("alert-danger");
        for (const key in json.errors) {
          $("#" + key)
            .removeClass("is-valid")
            .addClass("is-invalid");
          $("#" + key + "-validation")
            .html(json.errors[key][0])
            .removeClass("valid-feedback")
            .addClass("invalid-feedback");
        }
        for (const key in json.data) {
          if (!json.errors.hasOwnProperty(key)) {
            console.log(json.errors[key]);
            $("#" + key)
              .removeClass("is-invalid")
              .addClass("is-valid");
            $("#" + key + "-validation")
              .html("Looks good!")
              .removeClass("invalid-feedback")
              .addClass("valid-feedback");
          }
        }
      }
    },
    error: function (error) {
      console.log(`\nADDING/UPDATING EMPLOYEE FAILED.\n${error}`);
    },
  });
}
function EditEmployee(elm) {
  elm = Number(elm);
  $(".modal-dialog").removeClass("modal-xl");
  $("#task-form").show();
  $("#category-form").hide();
  $("#add-btn").hide();
  $("#task-list").hide();
  $("#edit-btn").hide();
  $("#delete-btn").hide();
  $("#doneBlock").show();
  $("#update-btn").show();
  $("#closeModal").show();
  $("#todo-form").show();
  $("#todo-form").attr("action", `/todo/${elm}/update`);
  $("#formModalLabel").html("Update task data");
  $.ajax({
    url: `/todo/${elm}/get_by_id`,
    type: "POST",
    success: function (res) {
      var json = JSON.parse(res);
      $("#title").val(json.title);
      $("#priority").val(json.priority);
      $("#timeline").val(json.timeline);
      $("#description").val(json.description);
      $("#is_done").prop("checked", json.is_done);
    },
    error: function (error) {
      console.log("ERRORS", error);
    },
  });
}
function DeleteEmployee(elm) {
  elm = Number(elm);
  console.log(`\nDELETING TASK '${elm}' WAS STARTED.`);
  $.ajax({
    type: "POST",
    url: `/todo/${elm}/delete`,
    success: function (res) {
      console.log(`\nDELETING TASK '${elm}' COMPLETE.`);
      var json = JSON.parse(res);
      $("#ToDos").html(json.data);
      $("#formModal").modal("hide");
    },
    error: function (error) {
      console.log(`\nDELETING TASK '${elm}' FAILED.`);
      console.log("ERRORS", error);
    },
  });
}
function viewEmployee(elm) {
  $("#todo-form").hide();
  $("#task-list").show();
  $(".modal-dialog").removeClass("modal-xl");
  $(".modal-dialog").addClass("modal-xl");

  $("#add-btn").show();
  $("#add-btn").html("Add new");
  $("#edit-btn").show();
  $("#delete-btn").show();

  $("#update-btn").hide();
  $("#closeModal").hide();

  $("#formModalLabel").html(`Category-${elm} data`);
  $("#delete-btn").on("click", () => {
    DeleteCategory(elm);
    console.log("DELETE BUTTON");
  });
  $("#edit-btn").on("click", () => {
    Edit(elm);
    console.log("EDIT BUTTON");
  });
  console.log(`\nVIEW CATEGORY '${elm}'.`);
  $.ajax({
    type: "POST",
    url: `/todo/category/${elm}/view`,
    success: function (res) {
      var json = JSON.parse(res);
      var $table = $("#view-task-table");
      console.log(`\nVIEWING CATEGORY '${elm}' COMPLETE.`);
      $table.bootstrapTable("load", json);
    },
    error: function (error) {
      console.log(`\nVIEWING TASK '${elm}' FAILED.`);
      console.log("ERRORS", error);
    },
  });
}
// #endregion

function dateRange() {
  var start = moment();
  var end = moment().endOf("day");

  function setInput(start, end) {
    $("#timeline").val(
      start.format("MMM-D HH:mm") + " - " + end.format("MMM-D HH:mm")
    );
  }

  $("#date-range-open").daterangepicker(
    {
      timePicker: true,
      timePicker24Hour: true,
      startDate: start,
      endDate: end,
      ranges: {
        Today: [moment(), moment().endOf("day")],
        Tomorrow: [moment(), moment().add(1, "d").endOf("day")],
        "This week": [moment(), moment().endOf("week")],
        "This mounth": [moment(), moment().endOf("month")],
      },
    },
    setInput
  );

  setInput(start, end);
}
