const Validation = {
    isNumeric(value) {
        if (value === null || value === undefined || value === '') return false;
        return !isNaN(parseFloat(value)) && isFinite(value);
    },

    validatePredictionForm(formData) {
        const errors = {};
        let isValid = true;

        if (!this.isNumeric(formData.time) || parseFloat(formData.time) < 0) {
            errors.time = "Time must be a positive number.";
            isValid = false;
        }

        if (!this.isNumeric(formData.amount) || parseFloat(formData.amount) < 0) {
            errors.amount = "Amount must be a positive number.";
            isValid = false;
        }

        for (let i = 1; i <= 28; i++) {
            const key = `V${i}`;
            if (!this.isNumeric(formData.v_features[key])) {
                errors[key] = "Must be numeric.";
                isValid = false;
            }
        }

        return { isValid, errors };
    },

    showError(inputId, message) {
        const input = document.getElementById(inputId);
        const errorSpan = document.getElementById(`${inputId}-error`);
        if (input) input.classList.add('invalid');
        if (errorSpan) errorSpan.textContent = message;
    },

    clearErrors() {
        document.querySelectorAll('.invalid').forEach(el => el.classList.remove('invalid'));
        document.querySelectorAll('.error-message').forEach(el => el.textContent = '');
        const globalError = document.getElementById('form-global-error');
        if(globalError) {
            globalError.style.display = 'none';
            globalError.textContent = '';
        }
    }
};
