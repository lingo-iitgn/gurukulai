document.head.insertAdjacentHTML('beforeend', `
    <style>
/* Enhanced Send Button disabled state */
.send-button.disabled {
    opacity: 0.6;
    cursor: not-allowed;
    background-color: #e0e0e0;
    box-shadow: none;
}

/* Enhanced OCR Notification */
.ocr-notification {
    display: flex;
    align-items: center;
    padding: 10px 14px;
    margin: 0 0 12px; /* Changed from 8px 0 12px to ensure proper spacing above input */
    width: 100%;
    background-image: linear-gradient(to right, #e3f2fd, #bbdefb);
    border-left: 4px solid #2196f3;
    border-radius: 8px;
    font-size: 14px;
    font-weight: 500;
    color: #0277bd;
    box-shadow: 0 2px 5px rgba(0,0,0,0.08);
    transition: all 0.3s ease;
    animation: fadeIn 0.5s ease-out;
}

.ocr-notification:hover {
    box-shadow: 0 4px 8px rgba(0,0,0,0.12);
    transform: translateY(-1px);
}

.ocr-notification i {
    margin: 0 0 12px; 
    width: 100%;
    color: #00c853;
    font-size: 18px;
    animation: pulse 1.5s infinite;
}

/* Animation for notification appearance */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

/* Pulse animation for the checkmark icon */
@keyframes pulse {
    0% { transform: scale(1); }
    50% { transform: scale(1.1); }
    100% { transform: scale(1); }
}

/* Make sure text is readable - not too small */
.ocr-notification span {
    font-size: 14px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    max-width: 90%;
}

/* Add a close button if desired */
.ocr-notification .close-btn {
    margin-left: auto;
    cursor: pointer;
    opacity: 0.7;
    transition: opacity 0.2s;
}

.ocr-notification .close-btn:hover {
    opacity: 1;
}
    </style>
    `);



// Get elements
const queryInput = document.getElementById("query");
const sendButton = document.getElementById("send");
const chatContent = document.getElementById("chat-content");
const classSelect = document.getElementById("class-select");
const subjectSelect = document.getElementById("subject-select");
const typingIndicator = document.getElementById("typing-indicator");
const templateQuestionsSection = document.getElementById("template-questions-section");

// OCR related elements
const fileInput = document.getElementById("file-input");
const imageUploadButton = document.getElementById("image-upload-btn");
const ocrProgress = document.getElementById("ocr-progress");
const ocrPreview = document.getElementById("ocr-preview");
    
// Add loading state management
let isLoading = false;
let isProcessingOcr = false;
let extractedOcrText = "";

if (imageUploadButton) {
    imageUploadButton.addEventListener("click", function() {
        fileInput.click();
    });
}

if (fileInput) {
    fileInput.addEventListener("change", processSelectedImage);
}



async function processSelectedImage(event) {
    const file = event.target.files[0];
    if (!file) return;
    
    // Check if file is an image
    if (!file.type.startsWith('image/')) {
        alert('Please upload an image file');
        return;
    }
    
    try {
        // Disable send button while processing
        if (sendButton) {
            sendButton.disabled = true;
            sendButton.classList.add('disabled');
        }
        
        // Show processing indicator
        isProcessingOcr = true;
        ocrProgress.style.display = 'block';
        
        // Show image preview
        const reader = new FileReader();
        reader.onload = function(e) {
            ocrPreview.src = e.target.result;
            ocrPreview.style.display = 'block';
        };
        reader.readAsDataURL(file);
        
        // Use Tesseract.js for OCR
        const worker = await Tesseract.createWorker({
            logger: m => {
                console.log(m);
                // Update progress message if desired
                if (m.status === 'recognizing text') {
                    ocrProgress.textContent = `Processing: ${Math.round(m.progress * 100)}%`;
                }
            }
        });
        
        // Load language data - both English and Hindi
        await worker.loadLanguage('eng+hin');
        await worker.initialize('eng+hin');
        
        // Recognize text in the image
        const { data } = await worker.recognize(file);
        console.log('OCR Result:', data.text);
        
        // Store the extracted text but don't send it yet
        extractedOcrText = data.text;
        
        // Show a notification that image is ready
        const notification = document.createElement('div');
        notification.className = 'ocr-notification';
        notification.innerHTML = `
            <i data-lucide="check-circle"></i>
            <span>Image processed - text extracted (${extractedOcrText.length} characters)</span>
            <div class="close-btn" title="Dismiss">
                <i data-lucide="x" size="16"></i>
            </div>
        `;

        // If there's already a notification, replace it
        const existingNotification = document.querySelector('.ocr-notification');
        if (existingNotification) {
            existingNotification.replaceWith(notification);
        } else {
            // Insert above the entire input container instead of before the query input
            const inputContainer = queryInput.closest('.input-container');
            inputContainer.parentElement.insertBefore(notification, inputContainer);
        }
        
        // Initialize the icon
        lucide.createIcons({
            target: notification
        });
        
        // Add click handler for close button
        const closeBtn = notification.querySelector('.close-btn');
        if (closeBtn) {
            closeBtn.addEventListener('click', (e) => {
                e.stopPropagation();
                notification.remove();
            });
        }
        // Terminate the worker to free up resources
        await worker.terminate();
        
    } catch (error) {
        console.error("OCR error:", error);
        alert(`OCR failed: ${error.message || 'Unknown error'}`);
    } finally {
        // Re-enable send button after processing completes
        if (sendButton) {
            sendButton.disabled = false;
            sendButton.classList.remove('disabled');
        }
        
        // Hide processing indicator
        isProcessingOcr = false;
        ocrProgress.style.display = 'none';
    }
}

function generateSessionId() {
    return 'session_' + Math.random().toString(36).substring(2, 15);
}

let sessionId = localStorage.getItem('gurukulai_session_id');
if (!sessionId) {
sessionId = generateSessionId();
localStorage.setItem('gurukulai_session_id', sessionId);
}

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
        syntheticEvent.preventDefault = () => { }; // Add preventDefault method
        syntheticEvent.fromTemplate = true; // Add a flag to indicate template question

        // Call sendQuery with our synthetic event
        sendQuery(syntheticEvent);

        setTimeout(() => {
            queryInput.value = "";
        }, 10);
    }
}
const templateHTML = `
    <div class="template-questions">
        <div class="template-title">Quick Questions</div>
        <div class="template-buttons">
            <button class="template-btn" data-question="Can you explain the concept of photosynthesis?">
                <i data-lucide="leaf" size="16"></i>
                Explain Photosynthesis
            </button>
            <button class="template-btn" data-question="What are Newton's three laws of motion?">
                <i data-lucide="orbit" size="16"></i>
                Newton's Laws
            </button>
            <button class="template-btn" data-question="How do chemical reactions work?">
                <i data-lucide="flask-conical" size="16"></i>
                Chemical Reactions
            </button>
            <button class="template-btn" data-question="Can you help me solve quadratic equations?">
                <i data-lucide="square-equal" size="16"></i>
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

async function generateSuggestedQuestions(question, answer) {
    try {
        const response = await fetch('/gurukulai/generate_suggestions', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                question: question,
                answer: answer,
                class: document.getElementById('class-select').value,
                subject: document.getElementById('subject-select').value
            })
        });
        
        if (!response.ok) {
            throw new Error('Failed to generate suggestions');
        }
        
        const data = await response.json();
        return data.suggestions || [];
    } catch (error) {
        console.error('Error generating suggestions:', error);
        return [];
    }
}
    // Add this function to start a new conversation
function startNewConversation() {
// Generate a new session ID
sessionId = generateSessionId();
localStorage.setItem('gurukulai_session_id', sessionId);

// Clear the chat content
chatContent.innerHTML = '';

// Add initial welcome message
addInitialMessage();

// Show template questions again
if (templateQuestionsSection) {
    templateQuestionsSection.style.display = 'block';
}

// Notify the server to reset the conversation history for this session
fetch(`/gurukulai/conversation_history?session_id=${sessionId}`, {
    method: 'POST',
})
.then(response => response.json())
.then(data => {
    console.log("New conversation started", data);
})
.catch(error => console.error('Error creating new session:', error));
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
    const hasOcrText = extractedOcrText.length > 0;
    
    // Special validation for the combined case
    if (!query && !hasOcrText) {
        appendMessageLeft("Please enter a question or upload an image with text.");
        return;
    }
    
    if (!selectedClass || !selectedSubject) {
        appendMessageLeft("Please select both class and subject before sending your query.");
        return;
    }

    try {
        isLoading = true;

        if (imageUploadButton) {
            imageUploadButton.disabled = true;
        }
        const originalQuery = query;
        queryInput.value = "";
        
        // Create the message to display to the user
        let displayMessage = originalQuery;
        if (hasOcrText) {
            // If we have both query and OCR text
            if (originalQuery) {
                displayMessage = `${originalQuery}\n\n[Attached image with text: ${extractedOcrText.substring(0, 50)}${extractedOcrText.length > 50 ? '...' : ''}]`;
            } else {
                // If we only have OCR text
                displayMessage = `Image uploaded with text: ${extractedOcrText.substring(0, 100)}${extractedOcrText.length > 100 ? '...' : ''}`;
            }
        }
        
        // IMPORTANT: Clear OCR elements immediately after preparing the display message
        // Remove the notification if it exists
        const notification = document.querySelector('.ocr-notification');
        if (notification) {
            notification.remove();
        }
        
        // Also hide the preview after sending
        if (ocrPreview) {
            ocrPreview.style.display = 'none';
            ocrPreview.src = '';
        }
        
        appendMessageRight(displayMessage);
        showTypingIndicator();
        
        // Prepare data for the backend
        const requestData = {
            query: query,
            class: selectedClass,
            subject: selectedSubject,
            isTemplate: event.fromTemplate === true,
            session_id: sessionId
        };
        
        // Add OCR text if available
        if (hasOcrText) {
            requestData.ocrText = extractedOcrText;
            requestData.isOcr = true;
        }

        const response = await fetch("/gurukulai/upload_query", {
            method: "POST",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestData)
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

        // If the server returns a new session ID, update it
        if (data.session_id) {
            sessionId = data.session_id;
            localStorage.setItem('gurukulai_session_id', sessionId);
        }

        const answer = data.answer || "I apologize, but I couldn't generate a response. Please try rephrasing your question.";
        
        // Pass the combined query for generating suggested questions
        const combinedQuery = query + (hasOcrText ? "\n" + extractedOcrText : "");
        appendMessageLeft(answer, combinedQuery, data.pdf_link);
        
        // Clear the OCR text now that it's been sent
        extractedOcrText = "";
        
        // Clear the file input so a new file can be selected
        if (fileInput) {
            fileInput.value = '';
        }

    } catch (error) {
        console.error("Error:", error);
        hideTypingIndicator();
        appendMessageLeft("I apologize, but there was an error processing your request. Please try again in a moment.");
    } finally {
        isLoading = false;
        if (imageUploadButton) {
            imageUploadButton.disabled = false;
        }
        queryInput.focus();

        // Hide template questions after any query is sent
        if (templateQuestionsSection) {
            templateQuestionsSection.style.display = 'none';
        }
    }
}

function setupTemplateButtons() {
    document.querySelectorAll('.template-btn').forEach(button => {
        button.addEventListener('click', function() {
            const question = this.getAttribute('data-question') || this.dataset.question;
            if (!question) return;
            
            // Set the question in the input
            queryInput.value = question;
            
            // Simply trigger the send button click
            // This will use the native event handling which should work as expected
            sendButton.click();
        });
    });
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
        const messageContent = button.closest('.message').querySelector('.message-content').textContent.trim();

        // Remove previous feedback
        allButtons.forEach(btn => {
            btn.classList.remove('liked', 'disliked');
        });

        // Add new feedback
        if (feedbackType === 'like') {
            button.classList.add('liked');
            // Send feedback to server
            sendFeedbackToServer('like', messageContent);
        } else {
            button.classList.add('disliked');
            // Send feedback to server
            sendFeedbackToServer('dislike', messageContent);
        }
    }
    // <a href="${pdfLink}" target="_blank">
    //                     📄 View Source PDF
    //                 </a>
    
    async function appendMessageLeft(text, originalQuery = "", pdfLink = null) {
        const messageDiv = document.createElement("div");
        messageDiv.classList.add("message", "bot-message");
        let sourceHtml = "";
        
        if (pdfLink) {
            // Extract the filename from the PDF link
            const filename = pdfLink.split('/').pop(); // Gets the last part of the URL path
            const decodedFilename = decodeURIComponent(filename); // Handle URL encoded characters
            
            // Extract useful information from the filename
            let displayName = decodedFilename;
            
            // Handle specific patterns like "class9/science/science_08.pdf"
            const matches = pdfLink.match(/class(\d+)\/(\w+)\/(\w+)_(\d+)\.pdf/i);
            if (matches) {
                const [, classNum, subject, topicPrefix, chapterNum] = matches;
                // Format as "Science Class 9 - Chapter 8" 
                displayName = `${subject.charAt(0).toUpperCase() + subject.slice(1)} Class ${classNum} - Chapter ${parseInt(chapterNum)}`;
            } else {
                // General cleanup if specific pattern isn't found
                displayName = decodedFilename
                    .replace(/\.pdf$/i, '') // Remove .pdf extension
                    .replace(/_/g, ' ') // Replace underscores with spaces
                    .replace(/([a-z])([0-9])/gi, '$1 $2') // Add space between letters and numbers
                    .split(' ')
                    .map(word => word.charAt(0).toUpperCase() + word.slice(1)) // Capitalize first letter of each word
                    .join(' ');
            }
            
            sourceHtml = `
                <div class="source-link">
                    <a href="${pdfLink}" class="pdf-link" target="_blank" rel="noopener noreferrer">
                        <div class="pdf-button">
                            <i data-lucide="file-text" size="16"></i>
                            <span class="pdf-filename">${displayName}</span>
                        </div>
                    </a>
                </div>`;
        }
    
        // Create the main content div for the answer
        const contentHtml = `
            <div class="message-content">
                ${convertMarkdownToHtml(text)}
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
            </div>` + sourceHtml;
        
        messageDiv.innerHTML = contentHtml;
        chatContent.appendChild(messageDiv);
        
        // Initialize Lucide icons for the message
        lucide.createIcons({
            target: messageDiv
        });
        
        // Make sure the PDF icon is initialized properly
        if (pdfLink) {
            const pdfIconElement = messageDiv.querySelector('.pdf-button i');
            if (pdfIconElement) {
                lucide.createIcons({
                    target: pdfIconElement.parentElement
                });
            }
        }
        
        // Add feedback button listeners
        const feedbackButtons = messageDiv.querySelectorAll('.feedback-btn-small');
        feedbackButtons.forEach(button => {
            button.addEventListener('click', handleFeedback);
        });
        
        // If we have an original query, generate and add suggested questions
        if (originalQuery) {
            try {
                // Show a temporary loading state for suggestions
                const suggestionLoaderDiv = document.createElement("div");
                suggestionLoaderDiv.className = "suggested-questions-loading";
                suggestionLoaderDiv.innerHTML = '<div class="suggestion-loader"></div>';
                messageDiv.appendChild(suggestionLoaderDiv);
                
                // Generate suggestions
                const suggestions = await generateSuggestedQuestions(originalQuery, text);
                
                // Remove the loading indicator
                messageDiv.removeChild(suggestionLoaderDiv);
                
                // Only add suggestions if we got some
                if (suggestions && suggestions.length > 0) {
                    // Create suggested questions container
                    const suggestedQuestionsDiv = document.createElement("div");
                    suggestedQuestionsDiv.className = "suggested-questions";
                    
                    // Add title
                    const titleDiv = document.createElement("div");
                    titleDiv.className = "suggested-questions-title";
                    titleDiv.textContent = "Follow-up Questions:";
                    suggestedQuestionsDiv.appendChild(titleDiv);
                    
                    // Add question buttons
                    suggestions.forEach(question => {
                        const button = document.createElement("button");
                        button.className = "suggested-question-btn";
                        button.innerHTML = `
                            <i data-lucide="help-circle" size="14"></i>
                            <span>${question}</span>
                        `;
                        
                        // Add click handler to submit this question
                        button.addEventListener("click", function() {
                            queryInput.value = question;
                            sendButton.click();
                        });
                        
                        suggestedQuestionsDiv.appendChild(button);
                    });
                    
                    // Add the suggestions to the message
                    messageDiv.appendChild(suggestedQuestionsDiv);
                    
                    // Initialize Lucide icons in the new elements
                    lucide.createIcons({
                        target: suggestedQuestionsDiv
                    });
                }
            } catch (error) {
                console.error("Error generating suggested questions:", error);
            }
        }
        
        scrollToBottom();
    }

    // Initialize the Showdown converter
    const converter = new showdown.Converter({
        tables: true,
        strikethrough: true,
        tasklists: true
    });

    function convertMarkdownToHtml(markdownText) {
        return converter.makeHtml(markdownText);
    }



function cleanHTML(html) {   
return html
.replace(/<\/?strong>/g, "**")  // Convert <strong> to Markdown-style bold (**bold**)
.replace(/<\/?em>/g, "*")       // Convert <em> to *italic*
.replace(/<li>/g, "- ")         // Convert list items to plain text lists
.replace(/<\/li>/g, "\n")       // Add newline after list items
.replace(/<\/?ol>/g, "\n")      // Remove ordered list tags
.replace(/<\/?ul>/g, "\n")      // Remove unordered list tags
.replace(/<br\s*\/?>/g, "\n")   // Convert <br> to newline
.replace(/<\/?p>/g, "\n\n")     // Convert <p> to double newlines for spacing
.replace(/<\/?[^>]+(>|$)/g, ""); // Remove all other remaining HTML tags
}



function cleanHtmlContent(html) {
// Remove HTML tags and convert to Markdown-like format
let cleanedText = html
    .replace(/<ol>/g, '') // Remove <ol> start tag
    .replace(/<\/ol>/g, '') // Remove <ol> end tag
    .replace(/<li>/g, '- ') // Replace <li> with a bullet point
    .replace(/<\/li>/g, '\n') // Add a newline after each </li>
    .replace(/<strong>(.*?)<\/strong>/g, '**$1**') // Convert <strong> to Markdown bold
    .replace(/<em>(.*?)<\/em>/g, '*$1*') // Convert <em> to Markdown italic
    .replace(/<br\s*[\/]?>/gi, '\n') // Convert <br> to newline
    .replace(/<p>/g, '') // Remove <p> start tag
    .replace(/<\/p>/g, '\n\n') // Replace </p> with double newline for paragraph spacing
    .replace(/&nbsp;/g, ' ') // Replace &nbsp; with a space
    .replace(/<\/?[^>]+(>|$)/g, '') // Remove any remaining HTML tags
    .trim();

// Remove extra line breaks
console.log(cleanedText)
cleanedText = cleanedText.replace(/\n{3,}/g, '\n\n');

return cleanedText;
}
function formatMessage(text) {
// Clean the HTML content first
let cleanedText = cleanHtmlContent(text);

// Escape HTML entities to prevent XSS
let escapedText = escapeHtml(cleanedText);

// Convert URLs to clickable links
const urlRegex = /(https?:\/\/[^\s]+)/g;
let linkedText = escapedText.replace(urlRegex, '<a href="$1" target="_blank" rel="noopener noreferrer">$1</a>');

// Replace newlines with <br> for display in HTML
let formattedText = linkedText.replace(/\n/g, '<br>');

return formattedText;
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
        // JavaScript function to handle sending the query
function askTemplateQuestion(question) {
queryInput.value = question;  // Set the question in the textarea

    // Create a synthetic event to simulate a button click
    const syntheticEvent = new Event('click', {
        bubbles: true,
        cancelable: true
    });

    // Dispatch the synthetic event on the send button
    sendButton.dispatchEvent(syntheticEvent);
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

document.addEventListener('DOMContentLoaded', () => {
    // Add click listeners to template buttons
    lucide.createIcons();
    setupTemplateButtons();
    const templateButtons = document.querySelectorAll('.template-btn');
    templateButtons.forEach(button => {
        button.addEventListener('click', (event) => {
            event.preventDefault();  // Prevent the default form submission
            const question = button.dataset.question;
            //queryInput.value = question;  // Set the question in the textarea

            // Create a synthetic event to simulate a button click
            const syntheticEvent = new Event('click', {
                bubbles: true,
                cancelable: true
            });
            syntheticEvent.fromTemplate = true; // Add a flag to indicate template question

            // Dispatch the synthetic event on the send button
            sendButton.dispatchEvent(syntheticEvent);
        });
    });

    function updateSubjectOptions(selectedClass) {
        const subjectSelect = document.getElementById('subject-select');
        subjectSelect.innerHTML = ""; // Clear all options
    
        const subjects9_10 = [
            { value: "science", label: "Science" },
            { value: "maths", label: "Mathematics" },
            { value: "english", label: "English" },
            { value: "hindi", label: "Hindi" },
            { value: "social-science", label: "Social Science" }
        ];
    
        const subjects11_12 = [
            { value: "physics", label: "Physics" },
            { value: "chemistry", label: "Chemistry" },
            { value: "biology", label: "Biology" },
            { value: "maths", label: "Mathematics" },
            { value: "english", label: "English" },
            { value: "pe", label: "Physical Education" },
            { value: "hindi", label: "Hindi" }
        ];
    
        const isSeniorClass = selectedClass === "class-11" || selectedClass === "class-12";
        const subjects = isSeniorClass ? subjects11_12 : subjects9_10;
    
        subjects.forEach(subject => {
            const option = document.createElement("option");
            option.value = subject.value;
            option.textContent = subject.label;
            subjectSelect.appendChild(option);
        });
    }
    
    // Attach listener
    document.getElementById('class-select').addEventListener('change', function () {
        updateSubjectOptions(this.value);
        updateDisabledState();
    });
    
    // Initialize subjects on load
    updateSubjectOptions(document.getElementById('class-select').value);
    
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
const newConversationBtn = document.getElementById('new-conversation-btn');
    if (newConversationBtn) {
        newConversationBtn.addEventListener('click', startNewConversation);
    }
});

// Add initial message
addInitialMessage();
updateDisabledState();
});

// Add this code to your existing home.js file

// Function to scroll to input on page load for mobile devices
function scrollToInputOnMobile() {
    if (window.innerWidth <= 768) {
        // Small delay to ensure DOM is fully loaded
        setTimeout(() => {
            const inputSection = document.querySelector('.input-section');
            if (inputSection) {
                window.scrollTo({
                    top: document.body.scrollHeight,
                    behavior: 'smooth'
                });
            }
        }, 300);
    }
}

// Call this function when page loads
document.addEventListener('DOMContentLoaded', function() {
    scrollToInputOnMobile();
    
    // Also call when orientation changes
    window.addEventListener('orientationchange', function() {
        setTimeout(scrollToInputOnMobile, 300);
    });
    
    // Initialize template questions horizontal scrolling for small screens
    if (window.innerWidth <= 480) {
        const templateButtons = document.querySelector('.template-buttons');
        if (templateButtons) {
            // Add momentum scrolling for iOS
            templateButtons.style.webkitOverflowScrolling = 'touch';
        }
    }
    
    // Auto-resize textarea as user types
    const textarea = document.getElementById('query');
    if (textarea) {
        textarea.addEventListener('input', function() {
            this.style.height = 'auto';
            const newHeight = Math.min(this.scrollHeight, 150);
            this.style.height = newHeight + 'px';
        });
    }
    
    // Make new conversation button more accessible
    const newConversationBtn = document.getElementById('new-conversation-btn');
    if (newConversationBtn) {
        newConversationBtn.addEventListener('click', function() {
            // After starting new conversation, focus the input
            setTimeout(() => {
                const textarea = document.getElementById('query');
                if (textarea) textarea.focus();
            }, 100);
        });
    }
});

// Make the input section visible without scrolling when keyboard appears (Android)
if (/Android/.test(navigator.userAgent)) {
    window.addEventListener('resize', function() {
        if (document.activeElement.tagName === 'TEXTAREA') {
            window.scrollTo(0, document.body.scrollHeight);
        }
    });
}

// For iOS keyboard issues
document.addEventListener('focusin', function(e) {
    if (e.target.tagName === 'TEXTAREA' || e.target.tagName === 'INPUT') {
        // Small delay to account for keyboard animation
        setTimeout(() => {
            e.target.scrollIntoView({behavior: 'smooth', block: 'center'});
        }, 300);
    }
});

// document.querySelectorAll('.template-btn').forEach(button => {
//     button.addEventListener('click', function() {
//         const question = this.getAttribute('data-question');
//         document.getElementById('query').value = question;
//         document.getElementById('send').click();
//     });

//     setTimeout(() => {
//         document.getElementById('query').value = "";
//     }, 10);
// });

// Add this to your home.js file to ensure consistent message styling

// Function to standardize message formatting
function standardizeMessageFormatting() {
    // Get all messages
    const messages = document.querySelectorAll('.message');
    
    messages.forEach(message => {
        // Apply consistent styling
        message.style.fontSize = '1rem';
        message.style.lineHeight = '1.6';
        
        // Ensure consistent paragraph spacing if messages contain paragraphs
        const paragraphs = message.querySelectorAll('p');
        if (paragraphs.length > 0) {
            paragraphs.forEach(p => {
                p.style.margin = '0 0 0.75rem 0';
                p.style.fontSize = '1rem';
            });
            // Remove margin from last paragraph
            if (paragraphs.length > 0) {
                paragraphs[paragraphs.length-1].style.marginBottom = '0';
            }
        }
    });
}

// Call this function when new messages are added and on page load
document.addEventListener('DOMContentLoaded', function() {
    // Initial run on page load
    standardizeMessageFormatting();
    
    // Set up a mutation observer to detect when new messages are added
    const chatContent = document.getElementById('chat-content');
    if (chatContent) {
        const observer = new MutationObserver(function(mutations) {
            mutations.forEach(function(mutation) {
                if (mutation.type === 'childList' && mutation.addedNodes.length > 0) {
                    standardizeMessageFormatting();
                }
            });
        });
        
        observer.observe(chatContent, { childList: true });
    }
});

// Enhance the message creation function if you have one
// If you have a function that creates messages, modify it to include:
function createMessage(content, isBot = true) {
    const messageDiv = document.createElement('div');
    messageDiv.className = isBot ? 'message bot-message' : 'message user-message';
    messageDiv.innerHTML = content;
    messageDiv.style.fontSize = '1rem'; // Set consistent font size
    
    // Add to chat
    document.getElementById('chat-content').appendChild(messageDiv);
    
    return messageDiv;
}