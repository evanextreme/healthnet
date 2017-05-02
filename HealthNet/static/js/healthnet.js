$(document).ready(function(){
      $('.parallax').parallax();
      $('.modal').modal({
           dismissible: false, // Modal can be dismissed by clicking outside of the modal
           opacity: .5, // Opacity of modal background
           inDuration: 300, // Transition in duration
           outDuration: 200, // Transition out duration
           startingTop: '4%', // Starting top style attribute
           endingTop: '10%', // Ending top style attribute
           ready: function(modal, trigger) { // Callback for Modal open. Modal and trigger parameters available.
           },
           complete: function() {
           } // Callback for Modal close
         }
       );
       $(".dropdown-button").dropdown({hover: false});
       $(".button-collapse").sideNav({hover: false});

    });

document.addEventListener("DOMContentLoaded", function(){
$('.preloader-background').delay(1000).fadeOut('slow');

$('.preloader-wrapper')
    .delay(1000)
    .fadeOut();
});

function newAppointment(){
  $.ajaxSetup({
    beforeSend: function(xhr, settings) {
        function getCookie(name) {
            var cookieValue = null;
            if (document.cookie && document.cookie != '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = jQuery.trim(cookies[i]);
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) == (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }
        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
            // Only send the token to relative URLs i.e. locally.
              xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    }
  });
  $.get("/appointments/new/",function(response){
      $('#apt-div').html(response);
  });
  $('#apt-modal').modal('open');
}

function newPrescription(){
  $.ajaxSetup({
    beforeSend: function(xhr, settings) {
        function getCookie(name) {
            var cookieValue = null;
            if (document.cookie && document.cookie != '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = jQuery.trim(cookies[i]);
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) == (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }
        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
            // Only send the token to relative URLs i.e. locally.
              xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    }
  });
  $.get("/prescriptions/new/",function(response){
      $('#apt-div').html(response);
  });
  $('#apt-modal').modal('open');
}

function getPrescriptions(patientid){
  var div = '#pat-div' + patientid;
  $.ajax({
      type: 'POST',
      url: '/prescriptions/',
      data: { get_patient_prescriptions: patientid },
      success: function(response) {
        $(div).html(response);
      }
  });
}

function getPrescriptionForm(prescriptionid){
  $.ajax({
      type: 'POST',
      url: '/prescriptions/update/',
      data: { update_prescription: prescriptionid },
      success: function(response) {
        $('#apt-div').html(response);

      }
  });
  $('#apt-modal').modal('open');
}

function returnToCard(patientid){
  var div = '#pat-div' + patientid;
  $.ajax({
      type: 'POST',
      url: '/card/',
      data: { patientid: patientid },
      success: function(response) {
        $(div).html(response);
      }
  });
}

function downloadAttachment(attachmenturl){
  var txt;
  var r = confirm("This doccument may contain sensitive information, by agreeing to view you will BLAH BLAH BLAH! By pressing OK you agree to these conditions");
  if (r == true) {
    window.open (attachmenturl,'_blank',false)
  } else {
      txt = "Welp we can't let you view the file then ¯\\_(ツ)_/¯";
      alert(txt)
  }


}
