var ingredients = [];
$(function() {
    function submit_message(message) {
        if(message.toLowerCase().startsWith("remove"))
        {
          ingredient = message.toLowerCase().split(/ (.+)/)[1]
          index = ingredients.indexOf(ingredient)
          if(index == -1)
          {
            msg = "Couldn't find " + ingredient + ". Please type the ingredient exactly."
          }
          else
          {
              ingredients.splice(index)
              ingredientString = ingredients.toString()
              msg = "Removed " + ingredient + "."
          }
          $('.chat-container').append(`
              <div class="chat-message col-md-5 offset-md-7 bot-message">
                  ${msg}
              </div
          `)
          // remove the loading indicator
          $( "#loading" ).remove();
        }else if(message.toLowerCase() == "show")
        {
          $.post( "/get_titles", {
              message: ingredientString
          }, handle_show_response);
        }
        else if(!isNaN(message))
        {
          if(message < 1)
          {
            $('.chat-container').append(`
                <div class="chat-message col-md-5 offset-md-7 bot-message">
                    ${"Please enter a valid number."}
                </div
            `)
            // remove the loading indicator
            $( "#loading" ).remove();
          }
          else
          {
            ingredients.push(message);
            ingredientString = ingredients.toString()
            $.post( "/get_full", {
                message: ingredientString
            }, handle_full_response);
          }
          ingredients.pop()
          ingredientString = ingredients.toString()
        }
        else
        {
          ingredients.push(message);
          ingredientString = ingredients.toString()
          $.post( "/get_number", {
              message: ingredientString
          }, handle_number_response);
        }
        function handle_show_response(data)
        {
          $('.chat-container').append(`
              <div class="chat-message col-md-5 offset-md-7 bot-message">
                  ${data.message}
              </div>
          `)
          // remove the loading indicator
          $( "#loading" ).remove();
        }

        function handle_full_response(data)
        {
          $('.chat-container').append(`
              <div class="chat-message col-md-5 offset-md-7 bot-message">
                  ${data.message}
              </div>
          `)
          // remove the loading indicator
          $( "#loading" ).remove();
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