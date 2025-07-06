const BASE_PATH = window.location.href.includes('/gurukulai/') 
    ? '/gurukulai' 
    : '';

let currentStep = 1;
let selectedClass = null;
let selectedSubject = null;
let selectedClassText = '';
let selectedSubjectText = '';

let loadedQuestionCount = 0;
let currentChapterId = null;
let preloadedQuestions = [];
let isPreloading = false;
let questionHistory = new Set(); 


const BACKEND_URL = window.location.protocol === 'https:'
    ? 'https://lingo.iitgn.ac.in/gurukulai'
    : 'http://lingo.iitgn.ac.in/gurukulai';

document.addEventListener('DOMContentLoaded', () => {
    lucide.createIcons();

    // Main event delegation setup for the questions container
    const questionsContainer = document.getElementById('questionsContainer');
    if (questionsContainer) {
        questionsContainer.addEventListener('click', function(event) {
            // Handle Check Answer button clicks
            const checkButton = event.target.closest('.check-answer');
            if (checkButton) {
                handleCheckAnswer(checkButton);
                return;
            }
            
            // Handle Try Again button clicks
            const tryAgainButton = event.target.closest('.try-again-button');
            if (tryAgainButton) {
                handleTryAgain(tryAgainButton);
                return;
            }
        });
    }

    // Class card selection
    document.querySelectorAll('.class-card').forEach(card => {
        card.addEventListener('click', async (e) => {
            document.querySelectorAll('.class-card').forEach(c => c.classList.remove('selected'));
            e.currentTarget.classList.add('selected');
            
            selectedClass = e.currentTarget.dataset.classId;
            selectedClassText = e.currentTarget.querySelector('h3').innerText;
            
            if (e.currentTarget) {
                e.currentTarget.style.animation = 'pulse 0.5s ease-out';
                setTimeout(() => {
                    if (e.currentTarget) {
                        e.currentTarget.style.animation = '';
                    }
                }, 500);
            }
            
            await loadSubjects(selectedClass);
            advanceStep(2);
        });
    });

    // Subject selection
    document.querySelector('#subjectContainer').addEventListener('click', async (e) => {
        const subjectCard = e.target.closest('.subject-card');
        if(subjectCard) {
            document.querySelectorAll('.subject-card').forEach(c => c.classList.remove('selected'));
            subjectCard.classList.add('selected');
            
            selectedSubject = subjectCard.dataset.subjectId;
            selectedSubjectText = subjectCard.querySelector('h3').innerText;
            
            subjectCard.style.animation = 'pulse 0.5s ease-out';
            setTimeout(() => subjectCard.style.animation = '', 500);
            
            await loadChapters(selectedSubject);
            advanceStep(3);
        }
    });
    
    // Chapter selection
    document.querySelector('#chapterContainer').addEventListener('click', async (e) => {
        const chapterItem = e.target.closest('.chapter-item');
        
        if(chapterItem) {
            const chapterId = chapterItem.dataset.chapterId;
            window.selectedChapterId = chapterId;

            const modal = document.getElementById("practiceTypeModal");
            if (modal) {
                modal.style.display = "flex";
                // Scroll to the modal after it is displayed
                modal.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }
        }
    });

    // Practice type selection
    document.getElementById("mcqMode").addEventListener("click", () => {
        document.getElementById("practiceTypeModal").style.display = "none";
        clearSubjectList(); // Clear the subject list before loading MCQ questions
        if (window.selectedChapterId) {
            loadQuestions(window.selectedChapterId);
        }
    });
      
    document.getElementById("theoryMode").addEventListener("click", () => {
        document.getElementById("practiceTypeModal").style.display = "none";
        clearSubjectList(); // Clear the subject list before loading theoretical questions
        if (window.selectedChapterId) {
            loadTheoreticalPractice(window.selectedChapterId);
        }
    });

    document.getElementById("practiceTypeModal")?.querySelector(".modal-close-btn")?.addEventListener("click", () => {
        document.getElementById("practiceTypeModal").style.display = "none";
    });
});


function clearSubjectList() {
    const subjectContainer = document.getElementById('subjectContainer');
    if (subjectContainer) {
        subjectContainer.innerHTML = '';
    }
}
function handleTryAgain(tryAgainButton) {
    const questionId = tryAgainButton.dataset.questionId;
    const questionCard = document.getElementById(`question-${questionId}`);
    const feedbackContainer = document.getElementById(`feedback-${questionId}`);
    const checkButton = questionCard.querySelector('.check-answer');
    
    // Reset the option styling
    questionCard.querySelectorAll('.option').forEach(opt => {
        opt.classList.remove('correct-option', 'wrong-option');
    });
    
    // Reset the check button
    checkButton.classList.remove('answered');
    checkButton.innerHTML = '<i data-lucide="check-circle"></i> Check Answer';
    
    // Clear the feedback
    feedbackContainer.innerHTML = '';
    
    // Re-create icons
    lucide.createIcons();
}

function handleCheckAnswer(checkButton) {
    if (checkButton.classList.contains('answered')) return;
    
    const questionId = checkButton.dataset.questionId;
    const correctAnswerIndex = parseInt(checkButton.dataset.correct);
    const questionCard = document.getElementById(`question-${questionId}`);
    const selectedOption = questionCard.querySelector('input[type="radio"]:checked');
    const feedbackContainer = document.getElementById(`feedback-${questionId}`);

    if (!selectedOption) {
        feedbackContainer.innerHTML = `
            <div class="mcq-answer-result mcq-wrong-answer">
                <i data-lucide="alert-triangle" class="mcq-result-icon"></i>
                <div>Please select an answer first.</div>
            </div>`;
        lucide.createIcons();
        return;
    }

    const selectedIndex = parseInt(selectedOption.value);
    const selectedOptionText = questionCard.querySelectorAll('.option')[selectedIndex]
        ?.querySelector('label span:nth-child(3)').innerText || "Unknown option";
    const isCorrect = selectedIndex === correctAnswerIndex;
    
    const correctOptionText = questionCard.querySelectorAll('.option')[correctAnswerIndex]
        ?.querySelector('label span:nth-child(3)').innerText || "Option not found";

    if (isCorrect) {
        feedbackContainer.innerHTML = `
            <div class="mcq-answer-result mcq-correct-answer">
                <i data-lucide="check-circle" class="mcq-result-icon"></i>
                <div><strong>Correct!</strong> Well done!</div>
            </div>`;
    } else {
        feedbackContainer.innerHTML = `
            <div class="mcq-answer-result mcq-wrong-answer">
                <i data-lucide="x-circle" class="mcq-result-icon"></i>
                <div>
                    <strong>Incorrect</strong><br/>
                    Correct answer: <strong>${correctOptionText}</strong>
                </div>
            </div>`;
    }

    lucide.createIcons();
    checkButton.classList.add('answered');
    checkButton.innerHTML = isCorrect
        ? '<i data-lucide="check"></i> Correct!'
        : '<i data-lucide="x"></i> Incorrect';

    // Don't disable the radio buttons anymore
    // Instead, add a try again button
    if (!isCorrect) {
        feedbackContainer.innerHTML += `
            <button class="try-again-button" data-question-id="${questionId}">
                <i data-lucide="refresh-cw"></i> Try Again
            </button>`;
        lucide.createIcons();
    }

    questionCard.querySelectorAll('.option').forEach((opt, idx) => {
        if (idx === correctAnswerIndex) {
            opt.classList.add('correct-option');
        } else if (idx === selectedIndex && !isCorrect) {
            opt.classList.add('wrong-option');
        }
    });
    
    submitMCQAnswer(questionId, selectedOptionText, isCorrect);
}


function advanceStep(step) {
    const currentStepElement = document.querySelector(`.selector-card[data-step="${currentStep}"]`);
    const nextStepElement = document.querySelector(`.selector-card[data-step="${step}"]`);

    if (currentStepElement) {
        currentStepElement.classList.remove('active');
    }
    
    if (nextStepElement) {
        nextStepElement.classList.add('active');
    }
    
    document.querySelectorAll('.step').forEach(s => s.classList.remove('active'));
    for (let i = 1; i <= step; i++) {
        const stepIndicator = document.querySelector(`.step[data-step="${i}"]`);
        if (stepIndicator) {
            stepIndicator.classList.add('active');
        }
    }
    
    const progressBar = document.getElementById('progressBar');
    if (progressBar) {
        if (step === 1) progressBar.style.width = '33.33%';
        if (step === 2) progressBar.style.width = '66.66%';
        if (step === 3) progressBar.style.width = '100%';
    }
    
    currentStep = step;
    
    const container = document.querySelector('.practice-container');
    if (container) {
        container.scrollIntoView({ behavior: 'smooth' });
    }
}


async function loadSubjects(classId) {
    try {
        const subjectContainer = document.getElementById('subjectContainer');
        if (subjectContainer) {
            subjectContainer.innerHTML = 
                `<div class="loading">
                    <div class="general-loading-spinner"></div>
                    <p>Loading subjects...</p>
                </div>`;
        }
        
        const fetchUrl = `${BASE_PATH}/practice/get_subjects/${classId}`;
        console.log(`Fetching subjects from: ${fetchUrl}`);
        
        const response = await fetch(fetchUrl);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const subjects = await response.json();
        console.log('Subjects received:', subjects);
        
        if (!subjectContainer) {
            throw new Error('Subject container element not found');
        }
        
        if (subjects.length === 0) {
            subjectContainer.innerHTML = 
                `<div class="empty-state">
                    <i data-lucide="folder" style="width: 48px; height: 48px; color: #cbd5e1;"></i>
                    <p>No subjects available for this class yet.</p>
                </div>`;
            lucide.createIcons();
            return;
        }
        
        const subjectIcons = {
            'Mathematics': 'calculator',
            'Science': 'flask-conical', 
            'English': 'book-open',
            'History': 'landmark',
            'Geography': 'globe',
            'Physics': 'atom',
            'Chemistry': 'flask-round',
            'Biology': 'heart-pulse',
            'Computer спробіScience': 'code'
        };
        
        let subjectCardsHTML = '';
        subjects.forEach(s => {
            const icon = subjectIcons[s.name] || 'book';
            subjectCardsHTML += `
                <div class="subject-card" data-subject-id="${s.id}">
                    <div class="subject-icon">
                        <i data-lucide="${icon}"></i>
                    </div>
                    <h3>${s.name}</h3>
                </div>`;
        });
        
        subjectContainer.innerHTML = subjectCardsHTML;
        lucide.createIcons();
    } catch (error) {
        console.error('Error loading subjects:', error);
        const subjectContainer = document.getElementById('subjectContainer');
        if (subjectContainer) {
            subjectContainer.innerHTML = `
                <div class="general-error">
                    <i data-lucide="alert-circle"></i>
                    Failed to load subjects. Please try again.
                    <p class="error-details">${error.message}</p>
                </div>`;
            lucide.createIcons();
        }
    }
}


function submitMCQAnswer(questionId, selectedOption, isCorrect) {
    const user = USER_NAME || 'isha'; // Fallback to 'isha' if USER_NAME is undefined
    console.log('Submitting MCQ answer:', { user, questionId, selectedOption, isCorrect });

    fetch(`${BASE_PATH}/practice/submit_answer`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            user: user,
            question_id: questionId,
            selected: selectedOption,
            is_correct: isCorrect
        })
    })
    .then(response => {
        console.log('Response status:', response.status);
        return response.json();
    })
    .then(data => {
        if (data.status === 'success') {
            console.log('MCQ answer submitted successfully:', data);
        } else {
            console.error('Error submitting MCQ answer:', data.error, data.received);
            console.warn('Continuing despite error - this won\'t affect the user experience');
        }
    })
    .catch(error => {
        console.error('Network error submitting MCQ answer:', error);
        console.warn('Continuing despite error - this won\'t affect the user experience');
    });
}


async function loadChapters(subjectId) {
    try {
        const chapterContainer = document.getElementById('chapterContainer');
        if (chapterContainer) {
            chapterContainer.innerHTML = 
                `<div class="loading">
                    <div class="general-loading-spinner"></div>
                    <p>Loading chapters...</p>
                </div>`;
        }
        
        const fetchUrl = `${BASE_PATH}/practice/get_chapters/${subjectId}`;
        console.log(`Fetching chapters from: ${fetchUrl}`);
        
        const response = await fetch(fetchUrl);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const chapters = await response.json();
        console.log('Chapters received:', chapters);
        
        if (!chapterContainer) {
            throw new Error('Chapter container element not found');
        }
        
        if (chapters.length === 0) {
            chapterContainer.innerHTML = 
                `<div class="empty-state">
                    <i data-lucide="file-x" style="width: 48px; height: 48px; color: #cbd5e1;"></i>
                    <p>No chapters available for this subject yet.</p>
                </div>`;
            lucide.createIcons();
            return;
        }
        
        chapterContainer.innerHTML = chapters.map(c => 
            `<div class="chapter-item" data-chapter-id="${c.id}">
                <i data-lucide="file-text" class="chapter-icon"></i>
                <span class="chapter-title">${c.name}</span>
            </div>`).join('');
        
        lucide.createIcons();
    } catch (error) {
        console.error('Error loading chapters:', error);
        const chapterContainer = document.getElementById('chapterContainer');
        if (chapterContainer) {
            chapterContainer.innerHTML = 
                `<div class="general-error">
                    <i data-lucide="alert-circle"></i>
                    Failed to load chapters. Please try again.
                </div>`;
            lucide.createIcons();
        }
    }
}

async function loadTheoreticalPractice(chapterId) {
    try {
        const questionsContainer = document.getElementById('questionsContainer');
        if (questionsContainer) {
            questionsContainer.innerHTML = `
                <div class="loading">
                    <div class="general-loading-spinner"></div>
                    <p>Loading theoretical questions...</p>
                </div>`;
        }

        currentChapterId = chapterId;
        const cleanClass = selectedClassText.replace(/\s+/g, '').toLowerCase();
        const cleanSubject = selectedSubjectText.toLowerCase();

        const fetchUrl = `${BASE_PATH}/practice/get_theory_questions/${chapterId}?user=${USER_NAME}&class=${cleanClass}&subject=${cleanSubject}`;
        console.log(`Fetching theoretical questions from: ${fetchUrl}`);

        const response = await fetch(fetchUrl);
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);

        const questions = await response.json();
        console.log('Theoretical questions received:', questions);

        if (!questionsContainer) throw new Error('Questions container element not found');

        if (!Array.isArray(questions) || questions.length === 0) {
            questionsContainer.innerHTML = `
                <div class="empty-state">
                    <i data-lucide="file-x" style="width: 48px; height: 48px; color: #cbd5e1;"></i>
                    <p>No theoretical questions available for this chapter yet.</p>
                    <button class="styled-button" onclick="goBackToStep(3)">
                        <i data-lucide="arrow-left-circle"></i> Choose Another Chapter
                    </button>
                </div>`;
            lucide.createIcons();
            return;
        }

        const breadcrumbTrail = `
            <div class="breadcrumb question-breadcrumb">
                <span class="breadcrumb-item clickable" onclick="goBackToStep(1)">${selectedClassText}</span>
                <i data-lucide="chevron-right" class="breadcrumb-separator"></i>
                <span class="breadcrumb-item clickable" onclick="goBackToStep(2)">${selectedSubjectText}</span>
                <i data-lucide="chevron-right" class="breadcrumb-separator"></i>
                <span class="breadcrumb-item current">Theoretical Questions</span>
            </div>`;

        const changeChapterBtn = `
            <div class="change-chapter-wrapper">
                <button class="change-chapter-btn" onclick="goBackToStep(3)">
                    <i data-lucide="arrow-left"></i> Change Chapter
                </button>
            </div>`;

        questionsContainer.innerHTML = `
            ${changeChapterBtn}
            ${breadcrumbTrail}
            <h2 class="questions-heading">Theoretical Practice</h2>
            <div class="questions-list">
                ${questions.map((q, i) => `
                    <div class="question-card theory-question" id="theory-${q.id}">
                        <div class="question-header">
                            <div class="theory-question-number">${i + 1}</div>
                            <div class="theory-question-text">${q.question}</div>
                        </div>
                        <textarea rows="6" class="theory-input" data-question-id="${q.id}" placeholder="Type your answer here..." style="width: 100%; padding: 0.75rem; border: 1px solid #d1d5db; border-radius: 0.5rem; resize: vertical;"></textarea>
                        <button class="submit-theory styled-button" data-question-id="${q.id}" data-answer="${encodeURIComponent(q.answer)}" style="margin-top: 0.75rem;">
                            <i data-lucide="send"></i> Submit Answer
                        </button>
                        <div class="answer-feedback" id="feedback-${q.id}" style="margin-top: 0.75rem;"></div>
                    </div>
                `).join('')}
            </div>
        `;

        document.querySelectorAll('.submit-theory').forEach(btn => {
            btn.addEventListener('click', async () => {
                const qid = btn.dataset.questionId;
                const actual = decodeURIComponent(btn.dataset.answer);
                const textarea = btn.previousElementSibling;
                const userAnswer = textarea.value.trim();
                const feedbackDiv = document.getElementById(`feedback-${qid}`);
                const questionText = btn.closest('.question-card').querySelector('.theory-question-text').innerText;

                if (!userAnswer) {
                    feedbackDiv.innerHTML = `
                        <div class="theory-answer-result theory-wrong-answer">
                            <i data-lucide="alert-triangle" class="theory-result-icon"></i>
                            <div>Please provide an answer before submitting.</div>
                        </div>`;
                    lucide.createIcons();
                    return;
                }

                feedbackDiv.innerHTML = `
                    <div class="theory-answer-result">
                        <i data-lucide="loader-circle" class="theory-result-icon spin"></i>
                        <div>Evaluating your answer...</div>
                    </div>`;
                lucide.createIcons();

                try {
                    const res = await fetch(`${BASE_PATH}/practice/submit_theory_answer`, {
                        method: "POST",
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            user: USER_NAME,
                            question_id: qid,
                            user_answer: userAnswer,
                            expected_answer: actual,
                            question_text: questionText,
                            class: cleanClass,
                            subject: cleanSubject
                        })
                    });

                    const data = await res.json();
                    if (data.success) {
                        feedbackDiv.innerHTML = `
                            <div class="theory-answer-result theory-correct-answer">
                                <i data-lucide="check-circle" class="theory-result-icon"></i>
                                <div>
                                    ${data.rating ? `<strong>Rating: ${data.rating}/10</strong><br>` : ''}
                                    ${data.feedback}
                                </div>
                            </div>`;
                        btn.disabled = true;
                        btn.innerHTML = '<i data-lucide="check"></i> Submitted';
                        textarea.disabled = true;
                    } else {
                        feedbackDiv.innerHTML = `
                            <div class="theory-answer-result theory-wrong-answer">
                                <i data-lucide="alert-circle" class="theory-result-icon"></i>
                                <div>Error: ${data.error || 'Failed to evaluate answer.'}</div>
                            </div>`;
                    }
                } catch (err) {
                    console.error('Error submitting theory answer:', err);
                    feedbackDiv.innerHTML = `
                        <div class="theory-answer-result theory-wrong-answer">
                            <i data-lucide="alert-circle" class="theory-result-icon"></i>
                            <div>Failed to submit answer. Please try again.</div>
                        </div>`;
                }
                lucide.createIcons();
            });
        });

        lucide.createIcons();

    } catch (error) {
        console.error('Error loading theoretical questions:', error);
        const questionsContainer = document.getElementById('questionsContainer');
        if (questionsContainer) {
            questionsContainer.innerHTML = `
                <div class="general-error">
                    <i data-lucide="alert-circle" style="width: 48px; height: 48px; color: #f87171;"></i>
                    <h3>Chapter is being updated!</h3>
                    <p>We're currently adding theoretical questions for this chapter. Please check back soon.</p>
                    <button class="styled-button" onclick="goBackToStep(3)">
                        <i data-lucide="arrow-left-circle"></i> Choose Another Chapter
                    </button>
                </div>`;
            lucide.createIcons();
        }
    }
}

async function loadQuestions(chapterId) {
    try {
        const questionsContainer = document.getElementById('questionsContainer');
        if (questionsContainer) {
            questionsContainer.innerHTML = `
                <div class="loading">
                    <div class="general-loading-spinner"></div>
                    <p>Loading questions...</p>
                </div>`;
        }

        currentChapterId = chapterId;
        loadedQuestionCount = 0;
        preloadedQuestions = [];
        questionHistory = new Set(); // Keep track of loaded question IDs

        const cleanClass = selectedClassText.replace(/\s+/g, '').toLowerCase();
        const cleanSubject = selectedSubjectText.toLowerCase();

        // Add random seed to avoid caching issues and ensure new questions
        const timestamp = new Date().getTime();
        const fetchUrl = `${BASE_PATH}/practice/get_questions/${chapterId}?user=${USER_NAME}&class=${cleanClass}&subject=${cleanSubject}&seed=${timestamp}`;

        console.log(`Fetching questions from: ${fetchUrl}`);
        const response = await fetch(fetchUrl);
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);

        const questions = await response.json();
        console.log('Questions received:', questions);

        if (!questionsContainer) throw new Error('Questions container element not found');

        if (!Array.isArray(questions) || questions.length === 0) {
            questionsContainer.innerHTML = `<div class="empty-state">
                <i data-lucide="help-circle" style="width: 48px; height: 48px; color: #cbd5e1;"></i>
                <p>No questions available for this chapter yet.</p>
            </div>`;
            lucide.createIcons();
            return;
        }

        // Keep track of loaded questions to avoid duplicates
        questions.forEach(q => questionHistory.add(q.id));
        
        const initialQuestions = questions.slice(0, 5);
        loadedQuestionCount = initialQuestions.length;

        const breadcrumbTrail = `
            <div class="breadcrumb question-breadcrumb">
                <span class="breadcrumb-item clickable" onclick="goBackToStep(1)">${selectedClassText}</span>
                <i data-lucide="chevron-right" class="breadcrumb-separator"></i>
                <span class="breadcrumb-item clickable" onclick="goBackToStep(2)">${selectedSubjectText}</span>
                <i data-lucide="chevron-right" class="breadcrumb-separator"></i>
                <span class="breadcrumb-item current">Questions</span>
            </div>`;

        const changeChapterBtn = `
            <div class="change-chapter-wrapper">
                <button class="change-chapter-btn" onclick="goBackToStep(3)">
                    <i data-lucide="arrow-left"></i> Change Chapter
                </button>
            </div>`;
        
        questionsContainer.innerHTML = `
            ${changeChapterBtn}
            ${breadcrumbTrail}
            <h2 class="questions-heading">Practice Questions</h2>
            <div class="questions-list">
                ${renderQuestionsHTML(initialQuestions)}
            </div>
            <div class="questions-footer">
                <button class="next-questions-btn">Next Questions</button>
            </div>`;

        document.querySelector('.next-questions-btn')?.addEventListener('click', showNextQuestions);

        document.querySelector('.change-chapter-btn')?.addEventListener('click', async () => {
            if (questionsContainer) {
                questionsContainer.innerHTML = '';
            }
        
            const chapterSection = document.querySelector('.selector-card[data-step="3"]');
            if (chapterSection) {
                chapterSection.style.display = '';
            }
        
            await loadChapters(selectedSubject);
            advanceStep(3);
        });

        lucide.createIcons();
        preloadNextQuestions();

    } catch (error) {
        console.error('Error loading questions:', error);
        const questionsContainer = document.getElementById('questionsContainer');
        if (questionsContainer) {
            questionsContainer.innerHTML = `
                <div class="general-error">
                    <i data-lucide="alert-circle" style="width: 48px; height: 48px; color: #f87171;"></i>
                    <h3>Chapter is being updated!</h3>
                    <p>We're currently adding questions for this chapter. Please check back soon.</p>
                    <button class="styled-button">
                        <i data-lucide="arrow-left-circle"></i> Choose Another Chapter
                    </button>
                </div>`;
    
            lucide.createIcons();
    
            const chooseAnotherBtn = document.querySelector('.styled-button');
            chooseAnotherBtn?.addEventListener('click', async () => {
                if (questionsContainer) {
                    questionsContainer.innerHTML = '';
                }
    
                const chapterSection = document.querySelector('.selector-card[data-step="3"]');
                if (chapterSection) {
                    chapterSection.style.display = '';
                }
    
                await loadChapters(selectedSubject);
                advanceStep(3);
            });
        }
    }
}


function showNextQuestions() {
    const nextBtn = document.querySelector('.next-questions-btn');
    const questionsList = document.querySelector('.questions-list');
    
    if (!questionsList) {
        console.error('Questions list not found');
        return;
    }
    
    if (preloadedQuestions.length === 0) {
        loadNextQuestions();
        return;
    }
    
    if (nextBtn) {
        nextBtn.classList.add('button-loading');
        nextBtn.disabled = true;
        nextBtn.innerHTML = 'Loading...';
    }
    
    questionsList.insertAdjacentHTML('beforeend', renderQuestionsHTML(preloadedQuestions));
    loadedQuestionCount += preloadedQuestions.length;
    
    const questionCount = preloadedQuestions.length;
    preloadedQuestions = [];
    
    if (nextBtn) {
        nextBtn.classList.remove('button-loading');
        nextBtn.disabled = false;
        nextBtn.innerHTML = '<i data-lucide="arrow-right-circle"></i> Next Questions';
    }
    
    lucide.createIcons();
    preloadNextQuestions();
    
    const newQuestions = document.querySelectorAll('.question-card');
    if (newQuestions.length > 0) {
        const firstNewQuestion = newQuestions[newQuestions.length - questionCount];
        if (firstNewQuestion) {
            firstNewQuestion.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    }
}


async function loadNextQuestions() {
    try {
        const nextBtn = document.querySelector('.next-questions-btn');
        if (nextBtn) {
            nextBtn.classList.add('button-loading');
            nextBtn.disabled = true;
            nextBtn.innerHTML = 'Loading...';
        }

        const questionsList = document.querySelector('.questions-list');
        if (!questionsList) throw new Error('Questions list not found');

        const cleanClass = selectedClassText.replace(/\s+/g, '').toLowerCase();
        const cleanSubject = selectedSubjectText.toLowerCase();

        // Add timestamp to ensure fresh questions and avoid duplicates
        const timestamp = new Date().getTime();
        const fetchUrl = `${BASE_PATH}/practice/get_questions/${currentChapterId}?user=${USER_NAME}&class=${cleanClass}&subject=${cleanSubject}&skip=${loadedQuestionCount}&seed=${timestamp}`;

        console.log(`Fetching next questions from: ${fetchUrl}`);
        const response = await fetch(fetchUrl);
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);

        const allNewQuestions = await response.json();
        console.log('Next questions received:', allNewQuestions);

        // Filter out any questions that were already shown
        const newQuestions = Array.isArray(allNewQuestions) 
            ? allNewQuestions.filter(q => !questionHistory.has(q.id))
            : [];
            
        // Add the new questions to our history tracker
        newQuestions.forEach(q => questionHistory.add(q.id));

        if (newQuestions.length === 0) {
            alert('No more questions available!');
            nextBtn?.remove();
            return;
        }

        questionsList.insertAdjacentHTML('beforeend', renderQuestionsHTML(newQuestions));
        loadedQuestionCount += newQuestions.length;

        lucide.createIcons();
        preloadNextQuestions();
    } catch (error) {
        console.error('Error loading next questions:', error);
        alert('Could not load more questions. Please try again.');
    } finally {
        const nextBtn = document.querySelector('.next-questions-btn');
        if (nextBtn) {
            nextBtn.classList.remove('button-loading');
            nextBtn.disabled = false;
            nextBtn.innerHTML = '<i data-lucide="arrow-right-circle"></i> Next Questions';
            lucide.createIcons();
        }
    }
}


async function preloadNextQuestions() {
    if (isPreloading) return;
    
    try {
        isPreloading = true;
        
        const cleanClass = selectedClassText.replace(/\s+/g, '').toLowerCase();
        const cleanSubject = selectedSubjectText.toLowerCase();

        // Add timestamp for fresh questions
        const timestamp = new Date().getTime();
        const fetchUrl = `${BASE_PATH}/practice/get_questions/${currentChapterId}?user=${USER_NAME}&class=${cleanClass}&subject=${cleanSubject}&skip=${loadedQuestionCount}&seed=${timestamp}`;

        console.log(`Preloading next questions from: ${fetchUrl}`);
        const response = await fetch(fetchUrl);
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);

        const allNewQuestions = await response.json();
        console.log('All preloaded questions:', allNewQuestions);

        // Filter out any questions that were already shown
        const newQuestions = Array.isArray(allNewQuestions) 
            ? allNewQuestions.filter(q => !questionHistory.has(q.id))
            : [];

        console.log('Filtered preloaded questions:', newQuestions);

        if (newQuestions.length > 0) {
            preloadedQuestions = newQuestions;
            const nextBtn = document.querySelector('.next-questions-btn');
            if (nextBtn) {
                nextBtn.innerHTML = `<i data-lucide="arrow-right-circle"></i> Next Questions (${newQuestions.length})`;
                lucide.createIcons();
            }
        } else {
            const nextBtn = document.querySelector('.next-questions-btn');
            if (nextBtn) {
                nextBtn.innerHTML = 'No More Questions';
                nextBtn.disabled = true;
            }
        }
    } catch (error) {
        console.error('Error preloading questions:', error);
    } finally {
        isPreloading = false;
    }
}


function setupEventDelegation() {
    const questionsContainer = document.getElementById('questionsContainer');
    if (!questionsContainer) return;
}

function renderQuestionsHTML(questions) {
    return questions.map((q, index) => `
        <div class="question-card fade-in" id="question-${q.id}">
            <div class="question-header">
                <div class="mcq-question-number">${document.querySelectorAll('.question-card').length + index + 1}</div>
                <div class="mcq-question-text">${q.question || q.text}</div>
            </div>
            <div class="question-options">
                ${q.options.map((opt, i) => `
                    <div class="option">
                        <label>
                            <input type="radio" id="q${q.id}_opt${i}" name="q${q.id}" value="${i}">
                            <span class="radio-custom"></span>
                            <span>${opt}</span>
                        </label>
                    </div>`).join('')}
            </div>
            <button class="check-answer" data-question-id="${q.id}" data-correct="${q.correct}">
                <i data-lucide="check-circle"></i> Check Answer
            </button>
            <div class="answer-feedback" id="feedback-${q.id}"></div>
        </div>`).join('');
}