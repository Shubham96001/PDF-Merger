const toolCards = document.querySelectorAll('.tool-card');
const toolTitle = document.getElementById('tool-title');
const uploadArea = document.getElementById('upload-area');
const fileInput = document.getElementById('file-input');
const fileList = document.getElementById('file-list');
const processBtn = document.getElementById('process-btn');
const optionsArea = document.getElementById('options-area');
const loading = document.getElementById('loading');
const errorMessage = document.getElementById('error-message');

let currentTool = 'merge';
let files = [];

const toolConfig = {
    merge: { title: 'Merge PDF', multiple: true, accept: '.pdf' },
    rotate: { title: 'Rotate PDF', multiple: false, accept: '.pdf', optionsHtml: '<label>Rotation degree:</label><select id="rotation-input"><option value="90">90° Clockwise</option><option value="180">180°</option><option value="270">90° Counter-Clockwise</option></select>' },
    password: { title: 'Add Password', multiple: false, accept: '.pdf', optionsHtml: '<label>Password:</label><input type="password" id="password-input" placeholder="Enter password">' }
};

toolCards.forEach(card => {
    card.addEventListener('click', () => {
        toolCards.forEach(c => c.classList.remove('active'));
        card.classList.add('active');
        currentTool = card.dataset.tool;
        toolTitle.textContent = toolConfig[currentTool].title;
        fileInput.multiple = toolConfig[currentTool].multiple;
        
        if (toolConfig[currentTool].optionsHtml) {
            optionsArea.innerHTML = toolConfig[currentTool].optionsHtml;
            optionsArea.classList.remove('hidden');
        } else {
            optionsArea.innerHTML = '';
            optionsArea.classList.add('hidden');
        }
        
        files = [];
        updateFileList();
        errorMessage.classList.add('hidden');
    });
});

fileInput.addEventListener('change', (e) => {
    handleFiles(e.target.files);
});

uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadArea.classList.add('dragover');
});

uploadArea.addEventListener('dragleave', () => {
    uploadArea.classList.remove('dragover');
});

uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadArea.classList.remove('dragover');
    handleFiles(e.dataTransfer.files);
});

function handleFiles(newFiles) {
    errorMessage.classList.add('hidden');
    const validFiles = Array.from(newFiles).filter(f => f.type === 'application/pdf');
    
    if (validFiles.length === 0) {
        showError('Please upload valid PDF files.');
        return;
    }

    if (!toolConfig[currentTool].multiple) {
        files = [validFiles[0]];
    } else {
        files = [...files, ...validFiles];
    }
    
    // Check size limit for Vercel Free Tier (approx 4MB total payload)
    // We keep it slightly lower to account for boundary boundaries
    const totalSize = files.reduce((acc, f) => acc + f.size, 0);
    if (totalSize > 4 * 1024 * 1024) {
        showError('Total file size exceeds 4MB. The free Vercel Python serverless tier has a 4.5MB limit. Please use smaller files.');
        files = [];
    }

    updateFileList();
}

function updateFileList() {
    fileList.innerHTML = '';
    files.forEach((file, index) => {
        const div = document.createElement('div');
        div.className = 'file-item';
        div.innerHTML = `
            <span>${file.name} (${(file.size / 1024 / 1024).toFixed(2)} MB)</span>
            <button onclick="removeFile(${index})" style="background:none; border:none; color:#ef4444; cursor:pointer;">✕</button>
        `;
        fileList.appendChild(div);
    });

    if (files.length > 0) {
        processBtn.classList.remove('hidden');
    } else {
        processBtn.classList.add('hidden');
    }
}

window.removeFile = (index) => {
    files.splice(index, 1);
    updateFileList();
};

function showError(msg) {
    errorMessage.textContent = msg;
    errorMessage.classList.remove('hidden');
}

processBtn.addEventListener('click', async () => {
    if (files.length === 0) return;

    const formData = new FormData();
    formData.append('tool', currentTool);
    
    files.forEach(f => formData.append('files', f));

    if (currentTool === 'rotate') {
        formData.append('rotation', document.getElementById('rotation-input').value);
    } else if (currentTool === 'password') {
        const pwd = document.getElementById('password-input').value;
        if (!pwd) return showError('Please enter a password.');
        formData.append('password', pwd);
    }

    processBtn.classList.add('hidden');
    loading.classList.remove('hidden');
    errorMessage.classList.add('hidden');

    try {
        const response = await fetch('/api/process', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            let errMsg = 'Failed to process PDF.';
            try {
                const errData = await response.json();
                errMsg = errData.error || errMsg;
            } catch {
                errMsg = await response.text() || errMsg;
            }
            throw new Error(errMsg);
        }

        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `processed_${currentTool}.pdf`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);

    } catch (err) {
        showError(err.message);
    } finally {
        loading.classList.add('hidden');
        processBtn.classList.remove('hidden');
    }
});
