document.addEventListener('DOMContentLoaded', () => {
    Animations.init();
    
    const form = document.getElementById('predictionForm');
    const pcaGrid = document.getElementById('pcaFeaturesGrid');
    const pcaToggle = document.getElementById('pcaDropdownToggle');
    const resultCard = document.getElementById('resultCard');
    const resetBtn = document.getElementById('resetBtn');
    
    // Generate PCA Inputs
    for (let i = 1; i <= 28; i++) {
        // Generate random default values for demo
        const randomVal = (Math.random() * 2 - 1).toFixed(4);
        const html = `
            <div class="pca-input-group">
                <label for="V${i}">V${i}</label>
                <input type="number" id="V${i}" name="V${i}" value="${randomVal}" step="any" required>
            </div>
        `;
        pcaGrid.insertAdjacentHTML('beforeend', html);
    }
    
    // Toggle PCA dropdown
    pcaToggle.addEventListener('click', () => {
        pcaToggle.classList.toggle('active');
        pcaGrid.classList.toggle('active');
    });

    // Form Submit
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        Validation.clearErrors();
        
        // Collect Data
        const time = document.getElementById('time').value;
        const amount = document.getElementById('amount').value;
        const v_features = {};
        
        for (let i = 1; i <= 28; i++) {
            v_features[`V${i}`] = parseFloat(document.getElementById(`V${i}`).value);
        }
        
        const formData = {
            time: parseFloat(time),
            amount: parseFloat(amount),
            v_features: v_features
        };
        
        // Validate
        const { isValid, errors } = Validation.validatePredictionForm(formData);
        
        if (!isValid) {
            if (errors.time) Validation.showError('time', errors.time);
            if (errors.amount) Validation.showError('amount', errors.amount);
            
            let pcaError = false;
            for (let i = 1; i <= 28; i++) {
                if (errors[`V${i}`]) {
                    Validation.showError(`V${i}`, errors[`V${i}`]);
                    pcaError = true;
                }
            }
            if(pcaError && !pcaGrid.classList.contains('active')) {
                pcaToggle.click(); // Open grid to show errors
            }
            return;
        }
        
        // UI Loading State
        setLoadingState(true);
        
        try {
            const result = await API.predictFraud(formData);
            displayResult(result);
        } catch (error) {
            const globalError = document.getElementById('form-global-error');
            globalError.textContent = error.message || "Failed to connect to the backend.";
            globalError.style.display = 'block';
            setLoadingState(false);
        }
    });
    
    resetBtn.addEventListener('click', () => {
        resultCard.classList.remove('active');
        setLoadingState(false);
    });
    
    function setLoadingState(isLoading) {
        const btn = document.getElementById('predictBtn');
        const btnText = btn.querySelector('.btn-text');
        const loader = document.getElementById('predictLoader');
        const inputs = form.querySelectorAll('input');
        
        if (isLoading) {
            btn.disabled = true;
            btnText.textContent = 'Analyzing Transaction...';
            loader.classList.remove('hidden');
            inputs.forEach(input => input.disabled = true);
        } else {
            btn.disabled = false;
            btnText.textContent = 'Predict Fraud';
            loader.classList.add('hidden');
            inputs.forEach(input => input.disabled = false);
        }
    }
    
    function displayResult(result) {

    console.log("Backend Result:", result);

    console.log(document.getElementById('resultPrediction'));
    console.log(document.getElementById('resultProbability'));
    console.log(document.getElementById('resultRiskLevel'));
    console.log(document.getElementById('resultConfidence'));
    console.log(document.getElementById('resultModel'));
    console.log(document.getElementById('resultThreshold'));
    console.log(document.getElementById('resultExplanation'));
    console.log(document.getElementById('resultCard'));

    setLoadingState(false);

    const titleEl = document.getElementById('resultPrediction');
    const probEl = document.getElementById('resultProbability');
    const riskEl = document.getElementById('resultRiskLevel');
    const confEl = document.getElementById('resultConfidence');
    const modelEl = document.getElementById('resultModel');
    const threshEl = document.getElementById('resultThreshold');
    const expEl = document.getElementById('resultExplanation');

    titleEl.textContent = result.prediction;
    probEl.textContent = `${(result.probability * 100).toFixed(2)}%`;
    riskEl.textContent = result.risk_level;
    confEl.textContent = `${result.confidence}%`;
    modelEl.textContent = result.model;
    threshEl.textContent = result.threshold;
    expEl.textContent = result.explanation;

    // Unhide and activate the result card
    resultCard.classList.remove('hidden');
    resultCard.classList.add('active');
// Color styling based on prediction
if (result.prediction.toLowerCase() === 'fraudulent') {
    titleEl.parentElement.classList.remove('result-safe');
    titleEl.parentElement.classList.add('result-fraud');
    probEl.style.color = 'var(--accent-red)';
    riskEl.style.color = 'var(--accent-red)';
} else {
    titleEl.parentElement.classList.remove('result-fraud');
    titleEl.parentElement.classList.add('result-safe');
    probEl.style.color = 'var(--accent-green)';
    riskEl.style.color = 'var(--accent-green)';
}
}
});
