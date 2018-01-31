$(document).ready(function() {
  $('#main-register').on('submit', function(event) {
    $.ajax({
      data: {
        name: $('#username').val(),
        email: $('#email').val(),
        password: $('#password').val(),
        confirm: $('#confirm').val()
      },
      type: 'POST',
      url: '/myproject/register'
    })
    .done(function(data) {
      if (data.success) {
        alert(data.success)
        window.location.href = '/myproject/login'
      }
      else {
        alert(data.error)
        window.location.href = '/myproject/register'
      }
    });
    event.preventDefault();

  });
});

$(document).ready(function() {
  $('#register-page-form').on('submit', function(event) {
    $.ajax({
      data: {
        name: $('#username-register').val(),
        email: $('#email-register').val(),
        password: $('#password-register').val(),
        confirm: $('#confirm-register').val()
      },
      type: 'POST',
      url: '/myproject/register'
    })
    .done(function(data) {
      if (data.success) {
        alert(data.success)
        window.location.href = '/myproject/login'
      }
      else {
        alert(data.error)
        window.location.href = '/myproject/register'
      }
    });
    event.preventDefault();

  });
});
