// German Learning Platform - Main JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Initialize popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
    
    // Handle audio player
    const audioPlayers = document.querySelectorAll('audio');
    audioPlayers.forEach(player => {
        const playButton = player.parentElement.querySelector('button');
        if (playButton) {
            playButton.addEventListener('click', function() {
                if (player.paused) {
                    player.play();
                    this.innerHTML = '<i class="fas fa-pause"></i>';
                } else {
                    player.pause();
                    this.innerHTML = '<i class="fas fa-play"></i>';
                }
            });
            
            player.addEventListener('ended', function() {
                playButton.innerHTML = '<i class="fas fa-play"></i>';
            });
        }
    });
    
    // Handle vocabulary copy button
    const copyButtons = document.querySelectorAll('.btn-copy');
    copyButtons.forEach(button => {
        button.addEventListener('click', function() {
            const textToCopy = this.getAttribute('data-copy');
            if (textToCopy) {
                navigator.clipboard.writeText(textToCopy).then(() => {
                    const originalText = this.innerHTML;
                    this.innerHTML = '<i class="fas fa-check"></i> Copied!';
                    this.classList.remove('btn-outline-secondary');
                    this.classList.add('btn-success');
                    
                    setTimeout(() => {
                        this.innerHTML = originalText;
                        this.classList.remove('btn-success');
                        this.classList.add('btn-outline-secondary');
                    }, 2000);
                });
            }
        });
    });
    
    // Handle exercise form submission
    const exerciseForms = document.querySelectorAll('.exercise-form');
    exerciseForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            const formData = new FormData(this);
            const exerciseId = this.getAttribute('data-exercise-id');
            const submitButton = this.querySelector('button[type="submit"]');
            const feedbackDiv = this.querySelector('.exercise-feedback');
            
            // Disable submit button
            if (submitButton) {
                const originalText = submitButton.innerHTML;
                submitButton.disabled = true;
                submitButton.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Checking...';
            }
            
            // Simulate API call (replace with actual fetch)
            setTimeout(() => {
                // This is a mock response - in a real app, you would make an API call here
                const isCorrect = Math.random() > 0.3; // 70% chance of being correct for demo
                
                if (feedbackDiv) {
                    feedbackDiv.innerHTML = `
                        <div class="alert ${isCorrect ? 'alert-success' : 'alert-danger'} mt-3">
                            <i class="fas fa-${isCorrect ? 'check' : 'times'}-circle me-2"></i>
                            ${isCorrect ? 'Correct! Well done!' : 'Incorrect. Please try again.'}
                        </div>
                    `;
                    
                    // Scroll to feedback
                    feedbackDiv.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
                }
                
                // Re-enable submit button
                if (submitButton) {
                    submitButton.disabled = false;
                    submitButton.innerHTML = isCorrect ? 'Next Exercise <i class="fas fa-arrow-right ms-1"></i>' : 'Try Again';
                    
                    if (isCorrect) {
                        submitButton.classList.remove('btn-primary');
                        submitButton.classList.add('btn-success');
                        
                        // Change to next exercise after delay
                        setTimeout(() => {
                            // In a real app, you would navigate to the next exercise
                            console.log('Moving to next exercise...');
                        }, 1500);
                    }
                }
            }, 800);
        });
    });
    
    // Handle translation toggle
    const toggleTranslationButtons = document.querySelectorAll('.toggle-translation');
    toggleTranslationButtons.forEach(button => {
        button.addEventListener('click', function() {
            const targetId = this.getAttribute('data-target');
            const targetElement = document.getElementById(targetId);
            
            if (targetElement) {
                targetElement.classList.toggle('d-none');
                const isVisible = !targetElement.classList.contains('d-none');
                this.innerHTML = isVisible ? 
                    '<i class="fas fa-eye-slash me-1"></i> Hide Translation' : 
                    '<i class="fas fa-language me-1"></i> Show Translation';
            }
        });
    });
    
    // Handle vocabulary search
    const vocabSearch = document.getElementById('vocabSearch');
    if (vocabSearch) {
        vocabSearch.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            const vocabItems = document.querySelectorAll('.vocab-item');
            
            vocabItems.forEach(item => {
                const term = item.getAttribute('data-term').toLowerCase();
                const translation = item.getAttribute('data-translation').toLowerCase();
                
                if (term.includes(searchTerm) || translation.includes(searchTerm)) {
                    item.style.display = '';
                } else {
                    item.style.display = 'none';
                }
            });
        });
    }
    
    // Add fade-in animation to elements with the 'fade-in' class
    const fadeElements = document.querySelectorAll('.fade-in');
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, {
        threshold: 0.1
    });
    
    fadeElements.forEach(element => {
        observer.observe(element);
    });
    
    // Handle back to top button
    const backToTopButton = document.getElementById('backToTop');
    if (backToTopButton) {
        window.addEventListener('scroll', function() {
            if (window.pageYOffset > 300) {
                backToTopButton.classList.add('show');
            } else {
                backToTopButton.classList.remove('show');
            }
        });
        
        backToTopButton.addEventListener('click', function(e) {
            e.preventDefault();
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    }
});

// Function to format dates in a user-friendly way
function formatDate(dateString) {
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    return new Date(dateString).toLocaleDateString('de-DE', options);
}

// Function to handle exercise submission via AJAX
function submitExercise(formElement) {
    const formData = new FormData(formElement);
    const exerciseId = formElement.getAttribute('data-exercise-id');
    
    fetch(`/api/exercises/${exerciseId}/submit/`, {
        method: 'POST',
        headers: {
            'X-CSRFTTOKEN': getCookie('csrftoken'),
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(Object.fromEntries(formData)),
    })
    .then(response => response.json())
    .then(data => {
        // Handle response
        console.log('Exercise submitted:', data);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

// Helper function to get CSRF token
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

// Add smooth scrolling to all links with hashes
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        
        const targetId = this.getAttribute('href');
        if (targetId === '#') return;
        
        const targetElement = document.querySelector(targetId);
        if (targetElement) {
            targetElement.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
            
            // Update URL without jumping
            history.pushState(null, null, targetId);
        }
    });
});

// Handle lesson completion
function completeLesson(lessonId) {
    fetch(`/api/lessons/${lessonId}/complete/`, {
        method: 'POST',
        headers: {
            'X-CSRFTTOKEN': getCookie('csrftoken'),
            'Content-Type': 'application/json',
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Update UI to show lesson is completed
            const completeButton = document.querySelector(`[data-lesson-id="${lessonId}"]`);
            if (completeButton) {
                completeButton.innerHTML = '<i class="fas fa-check-circle me-1"></i> Completed';
                completeButton.classList.remove('btn-primary');
                completeButton.classList.add('btn-success');
                completeButton.disabled = true;
            }
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

// Initialize any audio players with custom controls
function initAudioPlayers() {
    document.querySelectorAll('.audio-player').forEach(player => {
        const audio = player.querySelector('audio');
        const playButton = player.querySelector('.play-button');
        const progress = player.querySelector('.progress');
        const progressBar = player.querySelector('.progress-bar');
        const timeElapsed = player.querySelector('.time-elapsed');
        const duration = player.querySelector('.duration');
        const speed = player.querySelector('.playback-speed');
        const volume = player.querySelector('.volume');
        
        if (audio && playButton) {
            // Play/Pause
            playButton.addEventListener('click', () => {
                if (audio.paused) {
                    audio.play();
                    playButton.innerHTML = '<i class="fas fa-pause"></i>';
                } else {
                    audio.pause();
                    playButton.innerHTML = '<i class="fas fa-play"></i>';
                }
            });
            
            // Update progress bar
            audio.addEventListener('timeupdate', () => {
                const percent = (audio.currentTime / audio.duration) * 100;
                progressBar.style.width = `${percent}%`;
                
                // Update time elapsed
                const minutes = Math.floor(audio.currentTime / 60);
                const seconds = Math.floor(audio.currentTime % 60);
                timeElapsed.textContent = `${minutes}:${seconds.toString().padStart(2, '0')}`;
            });
            
            // Update duration on load
            audio.addEventListener('loadedmetadata', () => {
                const minutes = Math.floor(audio.duration / 60);
                const seconds = Math.floor(audio.duration % 60);
                duration.textContent = `${minutes}:${seconds.toString().padStart(2, '0')}`;
            });
            
            // Seek on progress bar click
            progress.addEventListener('click', (e) => {
                const rect = progress.getBoundingClientRect();
                const pos = (e.clientX - rect.left) / rect.width;
                audio.currentTime = pos * audio.duration;
            });
            
            // Playback speed
            if (speed) {
                speed.addEventListener('change', (e) => {
                    audio.playbackRate = parseFloat(e.target.value);
                });
            }
            
            // Volume control
            if (volume) {
                volume.addEventListener('input', (e) => {
                    audio.volume = e.target.value;
                });
            }
            
            // Handle audio end
            audio.addEventListener('ended', () => {
                playButton.innerHTML = '<i class="fas fa-play"></i>';
                progressBar.style.width = '0%';
                timeElapsed.textContent = '0:00';
            });
        }
    });
}

// Initialize audio players when the page loads
document.addEventListener('DOMContentLoaded', initAudioPlayers);
