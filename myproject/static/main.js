$(document).ready(function() {
  $('#main-login').on('submit', function(event) {
    $.ajax({
      data: JSON.stringify({
        name: $('#login_user').val(),
        password: $('#login_passwd').val()
      }),
      contentType : 'application/json; charset=utf-8',
      dataType: 'json',
      type: 'POST',
      url: '/myproject/login'
    })
    .done(function(data) {
      if (data.success) {
        alert(data.success)
        window.location.href = '/myproject'
      }
      else {
        alert(data.error)
        window.location.href = '/myproject/login'
      }
    });
    event.preventDefault();
  });
});

$(document).ready(function() {
  $('#login-page-form').on('submit', function(event) {
    $.ajax({
      data: JSON.stringify({
        name: $('#login-user').val(),
        password: $('#login-passwd').val()
      }),
      contentType : 'application/json; charset=utf-8',
      dataType: 'json',
      type: 'POST',
      url: '/myproject/login'
    })
    .done(function(data) {
      if (data.success) {
        alert(data.success)
        window.location.href = '/myproject'
      }
      else {
        alert(data.error)
        window.location.href = '/myproject/login'
      }
    });
    event.preventDefault();
  });
});


$(document).ready(function() {
  $('#main-register').on('submit', function(event) {
    $.ajax({
      data: JSON.stringify({
        name: $('#username').val(),
        email: $('#email').val(),
        password: $('#password').val(),
        confirm: $('#confirm').val()
      }),
      contentType : 'application/json; charset=utf-8',
      dataType: 'json',
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
      data: JSON.stringify({
        name: $('#username-register').val(),
        email: $('#email-register').val(),
        password: $('#password-register').val(),
        confirm: $('#confirm-register').val()
      }),
      contentType : 'application/json; charset=utf-8',
      dataType: 'json',
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

var num_of_rows;
var bigip_vals = []
var release_vals = []
var project_vals = []

$(document).ready(function() {
  $('#add-results-page-form').submit(function(e) {
    e.preventDefault()
    var test_val = parseInt($('#number-of-tests').val())
    num_of_rows = test_val
    console.log(test_val)
    if(test_val > 0) {
        $('#add-results-container').hide()
        $('#results-details').show()
        $.get('/myproject/bigip', get_bigip_vals);
        $.get('/myproject/release', get_release_vals);
        $.get('/myproject/project', get_project_vals);
        createTable(test_val, e)
      }
    else {
      //alert(document.getElementById('#number-of-tests').value)
      $("#add-result-err").text("Enter a value of atleast 1")
      $("#add-result-err").css({'color': 'red'})
    }
  });
});

function get_bigip_vals(reply, status) {
  $.merge(bigip_vals, reply['success'])
  var bigip_opts = ''
  for( var i=0; i<bigip_vals.length; i++) {
    bigip_opts += '<option value="' + bigip_vals[i] + '">' + bigip_vals[i] + '</option>'
  }
  document.getElementById('bigiplist').innerHTML = bigip_opts
}

function get_release_vals(reply, status) {
  $.merge(release_vals, reply['success'])
  var release_opts = ''
  for( var i=0; i<release_vals.length; i++) {
    release_opts += '<option value="' + release_vals[i] + '">' + release_vals[i] + '</option>'
  }
  document.getElementById('releaselist').innerHTML = release_opts
}

function get_project_vals(reply, status) {
  $.merge(project_vals, reply['success'])
  var project_opts = ''
  for( var i=0; i<project_vals.length; i++) {
    project_opts += '<option value="' + project_vals[i] + '">' + project_vals[i] + '</option>'
  }
  document.getElementById('projectlist').innerHTML = project_opts
}

function createTable(num_rows, e) {
  var num_of_rows = num_rows
  var num_of_cols = 4
  var theader = '<table id="add-results-table"><thead><tr><th>TestName</th><th style="width: 10%">TPS</th><th style="width: 10%">CPU</th><th>Comments</th></tr></thead>'
  var tbody = ''

  for( var i=0; i<num_of_rows;i++)
    {
        tbody += '<tr>';
        for( var j=0; j<num_of_cols;j++)
        {
            tbody += '<td><input type="text"  name= r' + i + 'c' + j + ' id= r' + i + 'c' + j + ' />';
            //tbody += 'Cell ' + i + ',' + j;
            tbody += '</td>'
        }
        tbody += '</tr>\n';
    }
    var tfooter = '</table>';

  document.getElementById('divTable').innerHTML = theader + tbody + tfooter;
  //console.log(theader + tbody + tfooter)
  return 1
}

$(document).ready(function() {
  $('#add-result-details-form').submit(function(e) {
    //var array = $('#add-result-details-form').serialize()
    var array = {}
    for(var i=0; i<num_of_rows; i++) {
      var temp_row_arr = []
      for(var j=0; j<4; j++) {
        td_val = $('#r' + i + 'c' + j).val()
        console.log(td_val)
        temp_row_arr.push(td_val)
        //temp_row_arr['c' + j] = td_val
      }
      array['r' + i] = temp_row_arr
    }
    console.log(array)
    console.log(document.getElementById("bigip-input").value)
    $.ajax({
      data: JSON.stringify({
        description: $('#description').val(),
        bigip: document.getElementById("bigip-input").value,
        release: document.getElementById("release-input").value,
        project: document.getElementById("project-input").value,
        tabledata: array
      }),
      contentType : 'application/json; charset=utf-8',
      dataType: 'json',
      type: 'POST',
      url: '/myproject/addresult'
    })
    .done(function(data) {
      if (data.success) {
        alert(data.success)
        window.location.href = '/myproject'
      }
      else {
        console.log("got here")
        alert(data.error)
        window.location.href = '/myproject/addresult'
      }
    });
    e.preventDefault()
  })
})


$(document).ready(function() {
  var data = { labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'], series: [[5, 2, 4, 2, 7]] }
  var options = { width: 2000, height: 800, low: 0, showArea: true, plugins: [ Chartist.plugins.ctPointLabels({textAnchor: 'middle'})] };
  var plugins = { plugins: [ Chartist.plugins.ctPointLabels({textAnchor: 'middle'})] }
  new Chartist.Line('.ct-chart', data, options)
});
