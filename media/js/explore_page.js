/*var $container = $('.video-thumb-container');
$container.masonry({
    columnWidth: '.c-s-6',
    itemSelector: ".c-s-6"
});
*/
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
var csrftoken = getCookie('csrftoken');
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    crossDomain: false, // obviates need for sameOrigin test
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type)) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

function getVideoContainer(domObj) {
    return $(domObj).closest('.widget-video');
}

$(".video-thumb-container").delegate(".btn-create-comment", "click", function(e){
    var $videoContainer = getVideoContainer(this);
    var videoId = $videoContainer.data("video-id");
    $.ajax({
        url: "/comment/create/" + videoId + "/",
        data: {
            'content': $videoContainer.find(".txt-create-comment").val()
        },
        method: "post",
        success: function(result) {
            console.log(arguments);
            if(result.success == true) {
                $("#recent_comments_"+videoId).html(result.recent);
                $("#top_comments_"+videoId).html(result.top);

                var commentDiv = $videoContainer.find(".thumb-comment-tab");
                var commentCount = parseInt(commentDiv.data("count"));
                commentDiv.data("count", commentCount + 1);
                $videoContainer.find(".thumb-comment-tab").collapse('show');
            }
        },
        failed: function() {
            console.log(arguments);
        }
    });
});

$(".thumb-comment-tab").delegate("a.like", "click", function(e){
    var evt = e ? e: window.event;
    evt.preventDefault();
    var commentId = $(this).attr('href');
    $.ajax({
        url: "/comment/vote/" + commentId + "/",
        data: {
            'mode': "like"
        },
        method: "post",
        success: function(result) {
            console.log(arguments);
            if(result.success == true) {
                $(".c_recommend_"+commentId).html(result.recommend);
            }
        },
        failed: function() {
            console.log(arguments);
        }
    });
    return false;
});
$(".thumb-comment-tab").delegate("a.unlike", "click", function(e){
    var evt = e ? e: window.event;
    evt.preventDefault();
    var commentId = $(this).attr('href');
    $.ajax({
        url: "/comment/vote/" + commentId + "/",
        data: {
            'mode': "unlike"
        },
        method: "post",
        success: function(result) {
            console.log(arguments);
            if(result.success == true) {
                $(".c_recommend_"+commentId).html(result.recommend);
            }
        },
        failed: function() {
            console.log(arguments);
        }
    });
    return false;
});

$(".video-thumb-container").delegate(".thumb-comment-tab", "hidden", function(){
    getVideoContainer(this).find('.btn-toggle-comment').text('Show Comments('+$(this).data('count')+')');
});

$(".video-thumb-container").delegate(".thumb-comment-tab", "shown", function(){
    getVideoContainer(this).find('.btn-toggle-comment').text('Hide Comments');
});

$(".video-thumb-container").delegate(".btn-video-bookmark", "click", function(e){
    var self = this;
    var evt = e ? e: window.event;
    evt.preventDefault();
    var $videoContainer = getVideoContainer(this);
    var videoId = $videoContainer.data('video-id');
    var mode = $(this).data("fav");
    $.ajax({
        url: "/video/"+videoId+"/fav",
        data: {'mode': mode},
        method: "post",
        success: function(result) {
            console.log(arguments);
            if (result.success) {
                $(self).data("fav", result.status);
                if(result.status == "fav") {
                    $(self).find("i").removeClass('e-icon-star').addClass('e-icon-star3');
                } else {
                    $(self).find("i").removeClass('e-icon-star3').addClass('e-icon-star');
                }
            }
        },
        failed: function() {
            console.log(arguments);
        }
    });
    return false;
});

$(".video-thumb-container").delegate(".btn-video-bookmark-remove", "click", function(e){
    var evt = e ? e: window.event;
    evt.preventDefault();
    var $videoContainer = getVideoContainer(this);
    var videoId = $videoContainer.data('video-id');
    $.ajax({
        url: "/video/"+videoId+"/fav",
        data: {'mode': 'unfav'},
        method: "post",
        success: function(result) {
            console.log(arguments);
        },
        failed: function() {
            console.log(arguments);
        }
    });
    return false;
});

$(".video-thumb-container").delegate(".btn-video-like", "click", function(e){
    var evt = e ? e: window.event;
    evt.preventDefault();
    var $videoContainer = getVideoContainer(this);
    var videoId = $videoContainer.data('video-id');
    $.ajax({
        url: "/video/"+videoId+"/like",
        method: "post",
        success: function(result) {
            console.log(arguments);
            if(result.success) {
                $videoContainer.find(".video-label-recommend").text(result.recommend);
            }
        },
        failed: function() {
            console.log(arguments);
        }
    });
    return false;
});

$(".video-thumb-container").delegate(".btn-video-unlike", "click", function(e){
    var evt = e ? e: window.event;
    evt.preventDefault();
    var $videoContainer = getVideoContainer(this);
    var videoId = $videoContainer.data('video-id');
    $.ajax({
        url: "/video/"+videoId+"/unlike",
        method: "post",
        success: function(result) {
            console.log(arguments);
            if(result.success) {
                $videoContainer.find(".video-label-recommend").text(result.recommend);
            }
        },
        failed: function() {
            console.log(arguments);
        }
    });
    return false;
});

$(".need_auth").click(function(e){
    var evt = e ? e: window.event;
    evt.preventDefault();
    $("#modal_login").modal('show');
    return false;
});

$(".video-thumb-container").delegate(".share-video", "click", function(e){
    var evt = e ? e: window.event;
    evt.preventDefault();
    var $videoContainer = getVideoContainer(this);
    var videoId = $videoContainer.data('video-id');
    var self = this;
    bootbox.confirm("Are you sure to change this video's share mode?", function(result) {
        if (result) {
            $.ajax({
                url: "/user/video/"+videoId+"/share",
                method: "post",
                success: function(result) {
                    console.log(arguments);
                    if(result.success) {
                        if (result.shared) {
                            $(self).find("i").attr('class','icon-stop');
                        } else {
                            $(self).find("i").attr('class', 'icon-share');
                        }
                    }
                },
                failed: function() {
                    console.log(arguments);
                }
            });
        }
    });
    return false;
});
if ( MOREVIDEOSEXIST ) {
    $(".video-thumb-container").jscroll({
        nextSelector: 'a.next_link'
    });
}
