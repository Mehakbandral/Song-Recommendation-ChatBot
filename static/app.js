function scrollToSection(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        const offset = element.getBoundingClientRect().top + window.pageYOffset;
        window.scroll({
            top: offset,
            behavior: "smooth"
        });
    }
}

const menuItems = document.querySelectorAll(".menu-item");
menuItems.forEach(item => {
    item.addEventListener("click", () => {
        const sectionId = item.getAttribute("href").slice(1);
        scrollToSection(sectionId);
    });
});

function appendMessage(sender, message) {
    var chatDiv = document.getElementById("chat");
    var messageDiv = document.createElement("div");
    messageDiv.className = "chat-message " + sender + "-message";
    messageDiv.innerHTML = "<img src='" + (sender === 'bot' ? 'chatbot-icon.png' : 'human-icon.png') + "' alt='" + (sender === 'bot' ? 'Chatbot Icon' : 'Human Icon') + "' class='chat-icon'>" + "<p>" + message + "</p>";
    chatDiv.appendChild(messageDiv);
    chatDiv.scrollTop = chatDiv.scrollHeight;
}


function appendMessage(sender, message) {
    var chatDiv = document.getElementById("chat");
    var messageDiv = document.createElement("div");
    messageDiv.className = "chat-message " + sender + "-message";



    // Check if the message contains URLs and convert them to clickable links
    var regex = /(https?:\/\/[^\s]+)/g;
    var messageWithLinks = message.replace(regex, "<a href='$1' target='_blank'>$1</a>");

    messageDiv.innerHTML = "<img style='position:relative;float:"+(sender === 'bot' ? 'left' : 'right')+"' src='" + (sender === 'bot' ? 'static/chatbot-icon.png' : 'static/human-icon.png') + "' alt='" + (sender === 'bot' ? 'Chatbot Icon' : 'Human Icon') + "' class='chat-icon'>" + "<p>" + messageWithLinks + "</p>";

    //messageDiv.innerHTML = "<p>" + messageWithLinks + "</p>";
    chatDiv.appendChild(messageDiv);
    chatDiv.scrollTop = chatDiv.scrollHeight;
}
  
function appendEmotion(emotion){
    globalStoreEmothion = emotion
    var emo = document.getElementById("emotion_span");
    emo.innerHTML = emotion;
}

function appendSongsList(songslist){
    //globalStoreEmothion = emotion
    var emo = document.getElementById("listSongs");
    emo.innerHTML = songslist;
}


    function appendSongMessage(message, songUrl) {
        var chatDiv = document.getElementById("chat");
        var messageDiv = document.createElement("div");
        messageDiv.className = "chat-message bot-message";
        messageDiv.innerHTML = "<p>" + message + "</p><audio controls><source src='" + songUrl + "' type='audio/mpeg'></audio>";
        chatDiv.appendChild(messageDiv);
        chatDiv.scrollTop = chatDiv.scrollHeight;
    }

    function display_and_sendMessage() {
        var user_input = globalStoreEmothion;
        document.getElementById("user_input").value = '';
        //appendEmotion(user_input);

        fetch('/chat/searchsong', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 'message': user_input })
        })
        .then(response => response.json())
        .then(data => {
            var botResponse = data.message;
            if (botResponse.startsWith("I found a song for you:")) {
                //appendSongMessage(botResponse);
                //appendEmotion(data.emotion)
                appendSongsList(botResponse)
            } else {
                //appendMessage("bot", botResponse);
                appendSongsList(botResponse)

            }
        })
        .catch(error => console.error('Error:', error));
    }

    function sendMessage() {
        var user_input = document.getElementById("user_input").value;
        document.getElementById("user_input").value = '';
        appendMessage("user", user_input);
        console.log(user_input)
        fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 'message': user_input })
        })
        .then(response => response.json())
        .then(data => {
            appendEmotion(data.emotion);
            var botResponse = data.message;
            if (botResponse.startsWith("I found a song for you:")) {
                appendSongMessage("I found a ("+data.emotion+") song for you. Please click GET SONGS RECOMMENDATION button below.");
                appendSongsList(botResponse)
                
            } else {
                appendMessage("bot", botResponse);
                //appendSongsList(botResponse)

            }
        })
        .catch(error => console.error('Error:', error));
        
    }

    function handleKeyPress(event) {
        if (event.key === "Enter") {
            sendMessage();
        }
    }
