var ingredients = [];
$(function() {
    function submit_message(message) {
        if(message.toLowerCase().startsWith("remove"))
        {
          ingredient = message.toLowerCase().split(/ (.+)/)[1]
          $('.chat-container').append(`
              <div class="chat-message col-md-5 offset-md-7 bot-message">
                  ${"will attempt to remove " + ingredient}
              </div>
          `)
        }else
        {
          ingredients.push(message);
          ingredientString = ingredients.toString()
          $.post( "/get_number", {
              message: ingredientString
          }, handle_number_response);
        }
        function handle_number_response(data) {
            var response_string = "There are " + data.message + " recipes that include " + ingredients.toString().replace(/,/g, ", ") + ". Type \"show\" if you would like to see "
            if(data.message > 10)
            {
              response_string += "the first 10."
            }else if(data.message == 1)
            {
              response_string = "There is 1 recipe that includes " + ingredients.toString().replace(/,/g, ", ") + ". Type \"show\" if you would like to see it."
            }
            else if (data.message == "0")
            {
              response_string = "There are no recipes that include " + ingredients.toString().replace(/,/g, ", ") + ". You can type \"remove [ingedient]\" to remove an ingredient."
            }else
            {
              response_string += "them."
            }
            // append the bot repsonse to the div
            console.log(data.message)
            $('.chat-container').append(`
                <div class="chat-message col-md-5 offset-md-7 bot-message">
                    ${response_string}
                </div>
            `)
            // remove the loading indicator
            $( "#loading" ).remove();
        }
    }

    $('#target').on('submit', function(e){
        e.preventDefault();
        const input_message = $('#input_message').val()
        // return if the user does not enter any text
        if (!input_message) {
            return
        }

        $('.chat-container').append(`
            <div class="chat-message col-md-5 human-message">
                ${input_message}
            </div>
        `)

        // loading
        $('.chat-container').append(`
            <div class="chat-message text-center col-md-2 offset-md-10 bot-message" id="loading">
                <b>...</b>
            </div>
        `)

        // clear the text input
        $('#input_message').val('')

        // send the message
        submit_message(input_message)
    });
});