/**
 * Retrieves the value of a specified cookie by name.
 *
 * @param {string} name - The name of the cookie to retrieve.
 * @returns {string|null} The value of the cookie if found, otherwise null.
 */
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

/**
 * Retrieves the user's input from the message input field.
 *  
 * @returns {string} The user's input.
 */
function getUserInput() {
    return document.getElementById('message-input').value.trim();
}

/**
 * Clears the user input field by setting its value to an empty string.
 * This function targets the HTML element with the ID 'message-input'.
 */
function clearUserInput() {
    document.getElementById('message-input').value = '';
}

/**
 * Sends a chat message to the server and returns the server's response.
 *
 * @param {string} content - The content of the chat message to be sent.
 * @returns {Promise<string|null>} - A promise that resolves to the server's response output if successful, or null if the message sending failed.
 */
async function chat(content) {
    const chat = document.getElementById('chat').dataset.chat;
    const csrftoken = getCookie('csrftoken');
    const response = await fetch(`/chats/chat/${chat}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': csrftoken
        },
        body: `content=${content}`
    });

    if (response.ok) {
        const data = await response.json();
        return data.output;
    } else {
        console.error('Message sending failed');
        return null;
    }
}

/**
 * Adds a loading indicator to the chat messages.
 * This function creates a new div element with the id "loading" and the class "agent message",
 * and appends it to the element with the id "messages".
 */
function addLoading() {
    const messages = document.getElementById('messages');
    const loading = document.createElement('div');
    loading.id = "loading";
    loading.className = "agent message";
    messages.appendChild(loading);
}

/**
 * Removes the loading element from the DOM if it exists.
 * This function looks for an element with the ID 'loading' and removes it.
 */
function removeLoading() {
    const loading = document.getElementById('loading');
    if (loading) {
        loading.remove();
    }
}

/**
 * Formats the given content by replacing newline characters with <br> tags,
 * unless the content contains HTML tags.
 *
 * @param {string} content - The content to format.
 * @returns {string} - The formatted content.
 */
function formatContent(content) {
    const regex = /<[^>]+>/;
    if (regex.test(content)) {
        return content;
    }
    return content.replace(/\n/g, "<br>");
}

/**
 * Adds a message to the chat interface.
 *
 * @param {string} sender - The sender of the message.
 * @param {string} content - The content of the message.
 */
function addMessage(sender, content) {
    const messages = document.getElementById('messages');
    const message = document.createElement('div');
    message.className = `${sender} message`;
    message.innerHTML = formatContent(content);
    messages.appendChild(message);
}

/**
 * Scrolls the messages container to the bottom.
 *
 * @param {boolean} [smooth=false] - If true, scrolls smoothly; otherwise, scrolls instantly.
 */
function scrollToBottom(smooth = false) {
    const messages = document.getElementById('messages');
    messages.scrollTo({
        top: messages.scrollHeight,
        behavior: smooth ? 'smooth' : 'auto'
    });
};

/**
 * Handles the submission of user input in the chat interface.
 * 
 * @async
 * @function submit
 * @returns {Promise<void>} A promise that resolves when the chat response has been processed.
 */
async function submit() {
    const input = getUserInput();

    if (input) {
        addMessage('user', input);
        clearUserInput();
        addLoading();
        scrollToBottom(true);

        const output = await chat(input);

        removeLoading();
        scrollToBottom(true);
        if (output) {
            addMessage('agent', output);
            scrollToBottom(true);
        }
    }
}

document.addEventListener('DOMContentLoaded', () => scrollToBottom(false));
document.getElementById('send-button').onclick = submit;
document.getElementById('message-input').addEventListener('keydown', (e) => {
    if (e.key === 'Enter') {
        if (e.shiftKey) {
            return;
        }
        e.preventDefault();
        submit();
    }
});