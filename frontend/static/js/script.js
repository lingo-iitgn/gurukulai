

// Get elements
const queryInput = document.getElementById("query");
const sendButton = document.getElementById("send");
const chatContent = document.getElementById("chat-content");
const classSelect = document.getElementById("class-select");
const subjectSelect = document.getElementById("subject-select");
const typingIndicator = document.getElementById("typing-indicator");

// Add loading state management
let isLoading = false;

function handleTemplateButtonClick(event) {
    const button = event.currentTarget;
    const question = button.dataset.question;
    
    if (question) {
        // Set the question in the textarea
        queryInput.value = question;
        
        // Get current class and subject selections
        const selectedClass = classSelect.value;
        const selectedSubject = subjectSelect.value;
        
        // Create and dispatch a synthetic event for sendQuery
        const syntheticEvent = new Event('synthetic');
        syntheticEvent.preventDefault = () => {}; // Add preventDefault method
        
        // Call sendQuery with our synthetic event
        sendQuery(syntheticEvent);
    }
}
const templateHTML = `
    <div class="template-questions">
        <div class="template-title">Quick Questions</div>
        <div class="template-buttons">
            <button class="template-btn" data-question="Can you explain the concept of photosynthesis?">
                <i data-lucide="leaf"></i>
                Explain Photosynthesis
            </button>
            <button class="template-btn" data-question="What are Newton's three laws of motion?">
                <i data-lucide="move"></i>
                Newton's Laws
            </button>
            <button class="template-btn" data-question="How do chemical reactions work?">
                <i data-lucide="flask-conical"></i>
                Chemical Reactions
            </button>
            <button class="template-btn" data-question="Can you help me solve quadratic equations?">
                <i data-lucide="square-equal"></i>
                Quadratic Equations
            </button>
        </div>
    </div>
`;

function showTypingIndicator() {
    if (typingIndicator) {
        typingIndicator.style.display = 'block';
        chatContent.scrollTop = chatContent.scrollHeight;
    }
}

function hideTypingIndicator() {
    if (typingIndicator) {
        typingIndicator.style.display = 'none';
    }
}

function validateInput(query, selectedClass, selectedSubject) {
    if (!query.trim()) {
        appendMessageLeft("Please enter your question.");
        return false;
    }
    
    if (selectedClass === "" || selectedSubject === "") {
        appendMessageLeft("Please select both class and subject before sending your query.");
        return false;
    }
    
    return true;
}

async function sendQuery(event) {
    event.preventDefault();
    
    if (!queryInput || !chatContent || !classSelect || !subjectSelect) {
        console.error("Required DOM elements not found");
        return;
    }

    // Prevent multiple submissions while loading
    if (isLoading) {
        return;
    }

    const query = queryInput.value.trim();
    const selectedClass = classSelect.value;
    const selectedSubject = subjectSelect.value;
    
    if (!validateInput(query, selectedClass, selectedSubject)) {
        return;
    }

    try {
        isLoading = true;
        queryInput.value = "";
        appendMessageRight(query);
        showTypingIndicator();
        
        const response = await fetch("/gurukulai/upload_query", {
            method: "POST",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ 
                query: query,
                class: selectedClass,
                subject: selectedSubject,
                isTemplate: query === document.querySelector(`[data-question="${query}"]`)?.dataset.question
            
            })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        hideTypingIndicator();
        
        if (data.error) {
            appendMessageLeft(`Error: ${data.error}`);
            return;
        }

        const answer = data.answer || "I apologize, but I couldn't generate a response. Please try rephrasing your question.";
        appendMessageLeft(answer);

    } catch (error) {
        console.error("Error:", error);
        hideTypingIndicator();
        appendMessageLeft("I apologize, but there was an error processing your request. Please try again in a moment.");
    } finally {
        isLoading = false;
        queryInput.focus();
        queryInput.value = "";
    }
}

function appendMessageRight(text) {
    const messageDiv = document.createElement("div");
    messageDiv.classList.add("message", "user-message");
    messageDiv.innerHTML = `
        <div class="message-content">
            ${formatMessage(text)}
        </div>`;
    chatContent.appendChild(messageDiv);
    scrollToBottom();
}

function scrollTemplateButtonIntoView(button) {
    button.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}


// function appendMessageLeft(text) {
//     const messageDiv = document.createElement("div");
//     messageDiv.classList.add("message", "bot-message");
//     messageDiv.innerHTML = `
//         <div class="message-content">
//             ${formatMessage(text)}
//         </div>`;
//     chatContent.appendChild(messageDiv);
//     scrollToBottom();
// }

async function sendFeedbackToServer(feedbackType, messageContent) {
    try {
        const response = await fetch("/submit_feedback", {
            method: "POST",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                feedbackType,
                messageContent,
                timestamp: new Date().toISOString()
            })
        });
        
        if (!response.ok) {
            console.error('Failed to submit feedback');
        }
    } catch (error) {
        console.error('Error submitting feedback:', error);
    }
}

function handleFeedback(event) {
    const button = event.currentTarget;
    const feedbackType = button.dataset.feedback;
    const buttonsContainer = button.closest('.feedback-buttons');
    const allButtons = buttonsContainer.querySelectorAll('.feedback-btn-small');
    
    // Remove previous feedback
    allButtons.forEach(btn => {
        btn.classList.remove('liked', 'disliked');
    });
    
    // Add new feedback
    if (feedbackType === 'like') {
        button.classList.add('liked');
    } else {
        button.classList.add('disliked');
    }
    
    // Update count (you can integrate this with your backend)
    const countSpan = button.querySelector('.feedback-count');
    const currentCount = parseInt(countSpan.textContent);
    countSpan.textContent = currentCount + 1;
    
    // You can send the feedback to your backend here
    sendFeedbackToServer(feedbackType, button.closest('.message').textContent);
}

// function appendMessageLeft(text) {
//     const messageDiv = document.createElement("div");
//     messageDiv.classList.add("message", "bot-message");
//     messageDiv.innerHTML = `
//         <div class="message-content">
//             ${formatMessage(text)}
//         </div>
//         <div class="message-footer">
//             <div class="feedback-buttons">
//                 <button class="feedback-btn-small" data-feedback="like" aria-label="Like response">
//                     <i data-lucide="thumbs-up"></i>
                    
//                 </button>
//                 <button class="feedback-btn-small" data-feedback="dislike" aria-label="Dislike response">
//                     <i data-lucide="thumbs-down"></i>
                    
//                 </button>
//             </div>
            
//         </div>`;
    
//     chatContent.appendChild(messageDiv);
//     scrollToBottom();
    
//     // Initialize Lucide icons for the new message
//     lucide.createIcons({
//         target: messageDiv
//     });
    
//     // Add feedback button listeners
//     const feedbackButtons = messageDiv.querySelectorAll('.feedback-btn-small');
//     feedbackButtons.forEach(button => {
//         button.addEventListener('click', handleFeedback);
//     });
// }

function appendMessageLeft(text) {
    const messageDiv = document.createElement("div");
    messageDiv.classList.add("message", "bot-message");
    messageDiv.innerHTML = `
        <div class="message-content">
            ${formatMessage(text)}
        </div>
        <div class="message-footer">
            <div class="feedback-buttons">
                <button class="feedback-btn-small" data-feedback="like" aria-label="Like response">
                    <i data-lucide="thumbs-up"></i>
                </button>
                <button class="feedback-btn-small" data-feedback="dislike" aria-label="Dislike response">
                    <i data-lucide="thumbs-down"></i>
                </button>
            </div>
        </div>`;
    
    chatContent.appendChild(messageDiv);
    scrollToBottom();
    
    // Initialize Lucide icons for the new message
    lucide.createIcons({
        target: messageDiv
    });
    
    // Add feedback button listeners
    const feedbackButtons = messageDiv.querySelectorAll('.feedback-btn-small');
    feedbackButtons.forEach(button => {
        button.addEventListener('click', handleFeedback);
    });
}



// function formatMessage(text) {
//     // Convert URLs to clickable links
//     const urlRegex = /(https?:\/\/[^\s]+)/g;
//     const escapedText = escapeHtml(text);
//     return escapedText.replace(urlRegex, '<a href="$1" target="_blank" rel="noopener noreferrer">$1</a>');
// }

function cleanHtmlContent(text) {
    // Remove all paragraph tags while preserving line breaks
    return text
        .replace(/<p>/g, '')
        .replace(/<\/p>/g, '\n\n')
        .trim()
        .replace(/\n\s*\n/g, '\n\n'); // Normalize multiple line breaks
}

function formatMessage(text) {
    // First clean the HTML content
    let cleanedText = cleanHtmlContent(text);
    
    // Escape HTML to prevent XSS
    const escapedText = escapeHtml(cleanedText);
    
    // Convert URLs to clickable links
    const urlRegex = /(https?:\/\/[^\s]+)/g;
    const textWithLinks = escapedText.replace(urlRegex, '<a href="$1" target="_blank" rel="noopener noreferrer">$1</a>');
    
    // Convert line breaks to paragraphs for proper formatting
    const paragraphs = textWithLinks.split('\n\n').filter(p => p.trim());
    return paragraphs.map(p => `<p>${p}</p>`).join('');
}

function scrollToBottom() {
    chatContent.scrollTop = chatContent.scrollHeight;
}

function escapeHtml(unsafe) {
    return unsafe
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

function addInitialMessage() {
    if (chatContent) {
        appendMessageLeft("Hi! I'm your AI tutor. How can I help you with your studies today?");
    }
}

// Handle disabled options
function updateDisabledState() {
    document.querySelectorAll('.select-wrapper').forEach(wrapper => {
        const select = wrapper.querySelector('select');
        const selectedOption = select.options[select.selectedIndex];
        
        if (selectedOption.disabled) {
            wrapper.classList.add('disabled');
        } else {
            wrapper.classList.remove('disabled');
        }
    });
}

// Add event listeners
if (sendButton) {
    sendButton.addEventListener("click", sendQuery);
}

if (queryInput) {
    queryInput.addEventListener("keypress", (event) => {
        if (event.key === "Enter" && !event.shiftKey) {
            event.preventDefault();
            sendQuery(event);
        }
    });
}

[classSelect, subjectSelect].forEach(select => {
    if (select) {
        select.addEventListener('change', updateDisabledState);
    }
});

// Initialize the page
// document.addEventListener("DOMContentLoaded", () => {
//     addInitialMessage();
//     updateDisabledState();
// });

document.addEventListener('DOMContentLoaded', () => {
    // Add template questions after welcome message
    const welcomeMessage = document.getElementById('welcome-message');
    if (welcomeMessage) {
        welcomeMessage.insertAdjacentHTML('afterend', templateHTML);
        
        // Initialize Lucide icons for template buttons
        lucide.createIcons();
        
        // Add click handlers for template buttons
        document.querySelectorAll('.template-btn').forEach(button => {
            button.addEventListener('click', handleTemplateButtonClick);
            });
       
    }
    // Initialize tooltips for template buttons
    document.querySelectorAll('.template-btn').forEach(button => {
        button.addEventListener('mouseenter', () => {
            if (button.offsetWidth < button.scrollWidth) {
                button.setAttribute('title', button.dataset.question);
            }
        });
    });
    
    // Add initial message
    addInitialMessage();
    updateDisabledState();
});

document.querySelectorAll('.template-btn').forEach(button => {
    button.addEventListener('mouseenter', () => {
        if (button.offsetWidth < button.scrollWidth) {
            button.setAttribute('title', button.dataset.question);
        }
    });
});