// app/static/js/cipher.js

let currentInputType = 'text';
let processingStartTime;

// Main initialization when document is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Add event listeners for encrypt/decrypt buttons
    document.getElementById('encrypt-btn').addEventListener('click', () => process('encrypt'));
    document.getElementById('decrypt-btn').addEventListener('click', () => process('decrypt'));

    // Check if elements exist
    console.log('Input text element:', document.getElementById('input-text'));
    console.log('Key input element:', document.getElementById('key'));
    console.log('Text counter element:', document.getElementById('text-counter'));
    console.log('Key strength element:', document.getElementById('key-strength'));
    
    // Initialize other event listeners
    initializeEventListeners();
    updateCipherDescription();
    checkDarkMode();
    updateCharacterCounters();
});

// Initialize all event listeners
function initializeEventListeners() {
    // Cipher type change
    document.getElementById('cipher-type').addEventListener('change', function() {
        updateCipherInfo(this.value);
    });
    
    // Text input changes
    const inputText = document.getElementById('input-text');
    if (inputText) {
        inputText.addEventListener('input', function() {
            const count = this.value.length;
            document.getElementById('text-counter').textContent = `${count} characters`;
            console.log('Input text changed:', count);
        });
    }
    
    // Key input changes
    const keyInput = document.getElementById('key');
    if (keyInput) {
        keyInput.addEventListener('input', function() {
            updateKeyStrength();
            console.log('Key changed:', this.value.length);
        });
    }
    
    // Buttons
    document.getElementById('encrypt-btn').addEventListener('click', () => process('encrypt'));
    document.getElementById('decrypt-btn').addEventListener('click', () => process('decrypt'));
    
    // Output related buttons
    document.querySelector('[onclick="copyOutput()"]').addEventListener('click', copyOutput);
    document.querySelector('[onclick="downloadOutput()"]').addEventListener('click', downloadOutput);
    document.querySelector('[onclick="clearOutput()"]').addEventListener('click', clearOutput);
    
    // Clear input button
    document.querySelector('[onclick="clearInput(\'input-text\')"]').addEventListener('click', () => clearInput('input-text'));
    
    // Generate key button
    document.querySelector('[onclick="generateKey()"]').addEventListener('click', generateKey);
    
    updateCharacterCounters();
}

function updateCipherInfo(type) {
    const info = {
        standard: "Uses 26 alphabet characters (A-Z). Non-alphabet characters are ignored.",
        autokey: "Uses plaintext as part of the key for stronger encryption using Vigenere Auto-Key method.",
        extended: "Uses all ASCII characters (256). Can encrypt special characters.",
        playfair: "Uses 5x5 matrix with combined I/J. Key determines matrix arrangement. Enter text without special characters.",
        affine: "Uses mathematical function (ax + b) mod 26. Key format: a,b (e.g., '5,8'). Only alphabetic characters."
    };
    document.getElementById('cipher-info').textContent = info[type];
    
    // Update key input placeholder and validation based on cipher type
    const keyInput = document.getElementById('key');
    const generateKeyBtn = document.getElementById('generate-key');
    
    if (type === 'affine') {
        keyInput.placeholder = "Enter key in format: a,b (e.g., '5,8')";
        keyInput.pattern = "\\d+,\\d+";
        generateKeyBtn.textContent = "Generate Valid Key Pair";
    } else if (type === 'playfair') {
        keyInput.placeholder = "Enter keyword for Playfair matrix";
        keyInput.pattern = "[A-Za-z]+";
        generateKeyBtn.textContent = "Generate Keyword";
    } else {
        keyInput.placeholder = "Enter encryption key";
        keyInput.pattern = ".*";
        generateKeyBtn.textContent = "Generate Random Key";
    }
}

// Function to clear input
function clearInput(inputId) {
    const element = document.getElementById(inputId);
    element.value = '';
    updateCharacterCounter(inputId, 'text-counter');
}

// Update the cipher description based on selected type
function updateCipherDescription() {
    const cipherType = document.getElementById('cipher-type').value;
    updateCipherInfo(cipherType);
}

// Update character counters
function updateCharacterCounters() {
    updateCharacterCounter('input-text', 'text-counter');
    updateCharacterCounter('output-text', 'output-counter');
}

// Update individual character counter
function updateCharacterCounter(inputId, counterId) {
    const input = document.getElementById(inputId);
    const counter = document.getElementById(counterId);
    const count = input.value.length;
    counter.textContent = `${count} character${count !== 1 ? 's' : ''}`;
}

// Update key strength indicator
function updateKeyStrength() {
    const keyInput = document.getElementById('key');
    const strengthEl = document.getElementById('key-strength');
    const cipherType = document.getElementById('cipher-type').value;
    
    if (!keyInput || !strengthEl) return;
    
    const key = keyInput.value;
    let strength = 'None';
    let colorClass = 'text-gray-500';
    
    if (key.length > 0) {
        if (cipherType === 'affine') {
            // Validate affine cipher key format
            if (/^\d+,\d+$/.test(key)) {
                const [a, b] = key.split(',').map(Number);
                const validA = [1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25];
                if (validA.includes(a) && b >= 0 && b < 26) {
                    strength = 'Valid';
                    colorClass = 'text-green-500';
                } else {
                    strength = 'Invalid';
                    colorClass = 'text-red-500';
                }
            } else {
                strength = 'Invalid Format';
                colorClass = 'text-red-500';
            }
        } else {
            // For other cipher types
            if (key.length < 4) {
                strength = 'Weak';
                colorClass = 'text-red-500';
            } else if (key.length < 8) {
                strength = 'Medium';
                colorClass = 'text-yellow-500';
            } else {
                strength = 'Strong';
                colorClass = 'text-green-500';
            }
        }
    }
    
    strengthEl.textContent = `Key strength: ${strength}`;
    strengthEl.className = `text-sm ${colorClass}`;
}

// Generate random key
function generateKey(length = 12) {
    const cipherType = document.getElementById('cipher-type').value;
    const keyInput = document.getElementById('key');
    
    if (cipherType === 'affine') {
        // Generate valid affine cipher keys
        const validA = [1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25];
        const a = validA[Math.floor(Math.random() * validA.length)];
        const b = Math.floor(Math.random() * 26);
        keyInput.value = `${a},${b}`;
    } else if (cipherType === 'playfair') {
        // Generate random keyword for Playfair
        const charset = 'ABCDEFGHIKLMNOPQRSTUVWXYZ'; // Note: I/J combined
        length = 8; // Shorter length for Playfair keyword
        let key = '';
        for (let i = 0; i < length; i++) {
            key += charset.charAt(Math.floor(Math.random() * charset.length));
        }
        keyInput.value = key;
    } else {
        // For other cipher types
        const charset = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
        let key = '';
        for (let i = 0; i < length; i++) {
            key += charset.charAt(Math.floor(Math.random() * charset.length));
        }
        keyInput.value = key;
    }
    
    updateKeyStrength();
}

// Main process function
async function process(operation) {
    console.log(`Processing ${operation}...`);
    
    const key = document.getElementById('key').value.toUpperCase();
    const text = document.getElementById('input-text').value;
    const cipherType = document.getElementById('cipher-type').value;

    // Validation
    if (!text) {
        Swal.fire({
            icon: 'error',
            title: 'Input Required',
            text: 'Please enter text to process'
        });
        return;
    }

    if (!key) {
        Swal.fire({
            icon: 'error',
            title: 'Key Required',
            text: 'Please enter an encryption key'
        });
        return;
    }

    // Additional validation for Affine cipher
    if (cipherType === 'affine') {
        if (!/^\d+,\d+$/.test(key)) {
            Swal.fire({
                icon: 'error',
                title: 'Invalid Key Format',
                text: 'Affine cipher key must be in format: a,b (e.g., "5,8")'
            });
            return;
        }
        const [a, b] = key.split(',').map(Number);
        const validA = [1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25];
        if (!validA.includes(a) || b < 0 || b >= 26) {
            Swal.fire({
                icon: 'error',
                title: 'Invalid Key Values',
                text: `'a' must be one of: ${validA.join(', ')}\n'b' must be between 0 and 25`
            });
            return;
        }
    }

    processingStartTime = performance.now();
    const loadingElement = document.querySelector('.container');
    loadingElement.classList.add('loading');

    try {
        const response = await fetch('/process', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: JSON.stringify({
                text: text,
                key: key,
                operation: operation,
                cipher_type: cipherType
            })
        });

        const data = await response.json();
        if (data.success) {
            document.getElementById('output-text').value = data.result;
            updateCharacterCounters();
        } else {
            throw new Error(data.error || 'Unknown error occurred');
        }
    } catch (error) {
        console.error('Error details:', error);
        Swal.fire({
            icon: 'error',
            title: 'Processing Error',
            text: error.message
        });
    } finally {
        loadingElement.classList.remove('loading');
        const processingTime = performance.now() - processingStartTime;
        document.getElementById('processing-time').textContent = 
            `Processing time: ${processingTime.toFixed(2)}ms`;
    }
}

// Dark mode functions
function toggleDarkMode() {
    document.documentElement.classList.toggle('dark');
    localStorage.setItem('darkMode', 
        document.documentElement.classList.contains('dark') ? 'true' : 'false'
    );
}

function checkDarkMode() {
    if (localStorage.getItem('darkMode') === 'true' ||
        window.matchMedia('(prefers-color-scheme: dark)').matches) {
        document.documentElement.classList.add('dark');
    }
}

function clearOutput() {
    document.getElementById('output-text').value = '';
    updateCharacterCounter('output-text', 'output-counter');
    document.getElementById('processing-time').textContent = '';
}

function copyOutput() {
    const output = document.getElementById('output-text').value;
    if (!output) {
        Swal.fire({
            icon: 'info',
            title: 'Nothing to Copy',
            text: 'No output text available'
        });
        return;
    }

    navigator.clipboard.writeText(output)
        .then(() => {
            Swal.fire({
                icon: 'success',
                title: 'Copied!',
                text: 'Output has been copied to clipboard',
                timer: 1500,
                showConfirmButton: false
            });
        })
        .catch(() => {
            Swal.fire({
                icon: 'error',
                title: 'Copy Failed',
                text: 'Failed to copy text to clipboard'
            });
        });
}

function downloadOutput() {
    const output = document.getElementById('output-text').value;
    if (!output) {
        Swal.fire({
            icon: 'info',
            title: 'Nothing to Download',
            text: 'No output text available'
        });
        return;
    }

    const blob = new Blob([output], { type: 'text/plain' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'cipher-output.txt';
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
    document.body.removeChild(a);
}