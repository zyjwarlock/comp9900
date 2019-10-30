INTERVAL_TIME = 500
// @param: url
// @param: args
// @param: callback
// Wrapped AJAX method, send args data to url in HTTP POST method
jQuery.postJSON = function (url, args, callback) {
    $.ajax({
        url: url, data: $.param(args), dataType: "text", type: "POST",
        success: function (response) {
            if (callback) callback(eval("(" + response + ")"));
        }, error: function (response) {
            console.log("ERROR:", response);
        }
    });
};

// change to josn
function formatToMessage(val) {
    var json = {};
    json['question'] = val;
    return json;
};

//update ScrollBar
function updateScrollBar() {
    var $messages_w = $('.pvr_chat_wrapper .chat-messages');
    $messages_w.scrollTop($messages_w.prop("scrollHeight"));
    $messages_w.perfectScrollbar('update');
}

// implement feedback loop
// put questions ID, questions and answers into arrays
// use <a title=””> to give user choice and get feedback
function showHints(hints, userQuestion) {
    // var i = 0;
    var hint_chooser = [];
    var html_questions = "The related questions indicate below.<br>";
    var none_choice = '<a href="#" class="none_choice" >None of these above. Could you ask again?</a><br>'
    var answers = [];
    var questions = [];
    var question_ids = [];
    for (var question in hints) {
        var answer = hints[question];
        // random hint_ID a-z0-9
        var hint_id = '_' + Math.random().toString(36).substr(2, 9);
        var hint = '<a href="#" id="' + hint_id + '" >' + question + '</a><br>'
        html_questions += hint
        answers.push(answer);
        questions.push(question);
        question_ids.push(hint_id);
    }
    html_questions += none_choice;
    html_questions += '</div></div>'
    
    printBotMsg(html_questions);
    updateScrollBar();

    for (var i = 0; i < question_ids.length; ++i) {
        (function(index) {
            setTimeout(function(){
                question_id = question_ids[index];
                question_selector = '#' + question_id;
                $(question_selector).on('click', function () {
                    ans_id = 'ans_' + question_ids[index];
                    reply_ans = answers[index] + "<br/><a href='#' id='" + ans_id + "'>Click here, if you think this is an acceptable response.</a>";
                    
                    printBotMsg(reply_ans);
                    
                    setTimeout(function () {
                        dict = {'question': userQuestion, 'ques':question[index], 'answer': answers[index]};
                        // send request to backend
                        // change url here
                        apiUrl = "/message/record";
                        answer_chooser = "#" + ans_id;
                        $(answer_chooser).on('click', function () {
                            $.postJSON(apiUrl, dict, function (response) {
                                printBotMsg(response.msg)
                            });
                        });
                    }, INTERVAL_TIME + 100)

                    return false;
                });
            }, INTERVAL_TIME + 200);
        }(i));
    }
    
    setTimeout(function () {
        $('.none_choice').on('click', function () {
            $('.message-input').focus();
            return false;
        });
    }, INTERVAL_TIME + 200);
}

function printBotMsg(content) {
    setTimeout(function () {
        $('.chat-messages').append('<div class="message"><div class="message-content">' + content + '</div></div>');
        updateScrollBar();
    }, INTERVAL_TIME - 100)
    updateScrollBar();
}

/* handle user input */
function handle_message() {
    var content = $('.message-input').val();
    if (content == '') {
        return false;
    }

    /* display message */
    $('.chat-messages').append('<div class="message self"><div class="message-content">' + content + '</div></div>');

    /* clear input box */
    $('.message-input').val('');

    /* send postJSON to backend and receive reply message,
    then render it in the front end */
    message = formatToMessage(content);
    $.postJSON("/message/new", message, function (response) {
        // display reply message
        if (response.show_hints == "yes") {
            showHints(response.reply_other, content);
            
        } else {
            printBotMsg(response.reply_msg);
        }
    });

    return false;
}

$(function () {
    $.backstretch("/static/img/bg.jpg");
    
    /* Helper button: Show message window */
    $('.pvr_chat_wrapper').toggleClass('active');

    $('.pvr_chat_button, .pvr_chat_wrapper .close_chat').on('click', function () {
        $('.pvr_chat_wrapper').toggleClass('active');
        return false;
    });

    // render scroll bar
    $('.pvr_chat_wrapper .chat-messages').perfectScrollbar();

    /* Four buttons: basic questions and answers for the course */
    $('#class_time').on('click', function () {
        printBotMsg("This is class time: Thu 18:00 - 20:00 (Weeks:1-9)");
        return false;
    });

    $('#class_loc').on('click', function () {
        printBotMsg("<iframe src='https://www.google.com/maps/embed?pb=!1m14!1m8!1m3!1d13243.455528077853!2d151.2311988!3d-33.9189027!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x0%3A0xae9b690cb686f09f!2sUNSW+School+of+Computer+Science+and+Engineering!5e0!3m2!1sen!2sus!4v1553919231295!5m2!1sen!2sus' width='300' height='225' frameborder='0' style='border:0' allowfullscreen></iframe>");
        return false;
    });

    $('#lab_time').on('click', function () {
        printBotMsg("This is lab time：Thu 14:30 - 16:00 (Weeks:2-4)");
        return false;
    });

    $('#exam_info').on('click', function () {
        printBotMsg("This is exam info：17-MAR-2019 in CSE lab");
        return false;
    });

    $(function () {
        /* user send message event */
        $('.message-input').on('keypress', function (e) {
            if (e.which == 13) {
                handle_message();
            }
        });

        $(".send_chat").on('click', function () {
            // call message handle function 
            handle_message();
        });

        // $(".send_voice").on('click', function () {
        //     handle_record();
        // });
    });
});


// voice input but fail to recognize 
// const recordAudio = () =>
//   new Promise(async resolve => {
//     const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
//     const mediaRecorder = new MediaRecorder(stream);
//     const audioChunks = [];

//     mediaRecorder.addEventListener("dataavailable", event => {
//       audioChunks.push(event.data);
//     });

//     const start = () => mediaRecorder.start();

//     const stop = () =>
//       new Promise(resolve => {
//         mediaRecorder.addEventListener("stop", () => {
//           const audioBlob = new Blob(audioChunks);
//           const audioUrl = URL.createObjectURL(audioBlob);
//           const audio = new Audio(audioUrl);
//           const play = () => audio.play();
//           // downloadLink = document.getElementById('download');
//           // downloadLink.href = audioUrl;
//           // downloadLink.download = 'acetest.webm';
//           // downloadRecordedAudio(audioUrl);
//           resolve({ audioBlob, audioUrl, play });
//         });

//         mediaRecorder.stop();
//       });

//     resolve({ start, stop });
//   });


// const sleep = time => new Promise(resolve => setTimeout(resolve, time));

// const handle_record = async () => {
//     const recorder = await recordAudio();
//     const actionButton = document.getElementById('record');
//     actionButton.disabled = true;
//     recorder.start();
//     await sleep(3000);
//     const audio = await recorder.stop();
//     audio.play();
//     await sleep(3000);
//     actionButton.disabled = false;

//     voice_content = 'sent voice message';
//     $('.chat-messages').append('<div class="message self"><div class="message-content">' + voice_content + '</div></div>');

//     audioBlob = "/message/audio";
//     $.postJSON(audioBlob, audioUrl, function (response) {
//         printBotMsg(response.msg)
//     });

//     return false;
// }
