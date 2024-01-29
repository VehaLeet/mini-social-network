$(document).ready(function() {
    $(".like-button").on("click", function() {
        var post_id = $(this).data("post-id");
        var button = $(this);


        // Send an AJAX request to the toggle_like view
        $.ajax({
            type: "POST",
            url: `/post/like/${post_id}/`,
            success: function(data) {
                if (data.liked) {
                    // Post was liked, update button text and add 'liked' class
                    button.text("Unlike");
                    button.addClass("liked");
                } else {
                    // Post was unliked, update button text and remove 'liked' class
                    button.text("Like");
                    button.removeClass("liked");
                }
                // Update the like count
                $(".like-count-" + post_id).text("Likes: " + data.like_count);
            }
        });
    });

    $(".follow-button").on("click", function() {
        var follow_username = $(this).data("follow-username");
        var button = $(this);


            $.ajax({
                type: "POST",
                url: `/follow-unfollow/${follow_username}/`,
                success: function(data) {
                    if (data.followed) {
                        button.text("Unfollow");
                        button.addClass("followed");
                    } else {
                        button.text("Follow");
                        button.removeClass("followed");
                    }
                    $(".followers-count").text("Followers: " + data.followers_count);
                    }

            });
        });
});


