// When document loaded
(function () {
    'use strict';
    // run form validation rules when form submitted
    document.getElementById('registrationForm').onsubmit = function (e) {
        // prevent the default behavior
        e.preventDefault();
        var signUpForm = new Validation();
        signUpForm.render();
        if (signUpForm.emptyErrors())
            document.getElementById('successMessage').classList.add('active');
        else
            signUpForm.onBlurValidation();
    };
})();

/**
 * @constructor
 */
function Validation() {
    this.$errorMessages = [];
    this.fields = document.getElementsByClassName('inp-v');
}

/**
 * Append error message to the DOM
 * @param _element,  the input field
 * @param messages,  array of this element error message
 * @return void
 */
Validation.prototype.appendErrorMessages = function (_element, messages) {
    'use strict';
    // add error class
    _element.parentElement.classList.add('has-error');

    // append the first message error
    if (_element.type === 'checkbox')
        _element.nextElementSibling.nextElementSibling.firstElementChild.textContent = messages[0];
    else {
        _element.nextElementSibling.firstElementChild.textContent = messages[0];
    }
    // hide success message
    document.getElementById('successMessage').classList.remove('active');

};

/**
 * Remove error message from the element
 * @param _element,  the input field
 * @return void
 */
Validation.prototype.removeErrorMessages = function (_element) {
    'use strict';
    var _parent = _element.parentElement; // parent of input field
    // Check whether the parent has class {has-error}
    if (_parent.className.indexOf('has-error') > -1) {
        // remove error class from the parent element
        _parent.classList.remove('has-error');
        // remove error message element
        if (_element.type === 'checkbox')
            _element.nextElementSibling.nextElementSibling.firstElementChild.textContent = '';
        else
            _element.nextElementSibling.firstElementChild.textContent = '';
    }
};

/**
 * Check whether the error messages array is empty
 * return boolean
 * */
Validation.prototype.isEmptyErrors = function () {
    'use strict';
    return (this.$errorMessages.length === 0);
};

/**
 * Check whether the error messages array is empty
 * return boolean
 * */
Validation.prototype.emptyErrors = function () {
    'use strict';
    return (document.getElementsByClassName('has-error').length === 0);
};

/**
 * Render the validation for given form
 */
Validation.prototype.render = function () {
    'use strict';
    // loop throw each input field
    for (var i = 0; i < this.fields.length; i++) {
        // get validation rules for each field
        var rules = this.fields[i].getAttribute('data-rule'),
            inputVal = this.fields[i].value,
            _element = this.fields[i];

        // continue to the second field in case this field doesn't has validation rules
        if (rules.trim().length === 0) continue;

        // reset error messages array
        this.$errorMessages = [];

        // split rules into array
        rules = rules.split('|');

        // Loop throw rules array
        for (var j in rules) {
            // Case 1 -- First check for rule that have SINGLE value e.g('required')
            if (rules[j].indexOf(':') === -1) {
                switch (rules[j]) {
                    case 'required':
                        if (inputVal.length === 0)
                            this.$errorMessages.push('This field can\'t be empty');
                        break;
                    // Required Checkbox
                    case 'checkbox':
                        if (!_element.checked)
                            this.$errorMessages.push('Please indicate that you accept the Terms and Conditions');
                        break;
                    case 'string':
                        if (!(/^[A-Za-z -_]*$/.test(inputVal)))
                            this.$errorMessages.push('This field can only contain alphabet character and -_ special characters');
                        break;
                    case 'alpha':
                        if (!(/^[A-Za-z ]*$/.test(inputVal)))
                            this.$errorMessages.push('Please provide an Alphabet characters');
                        break;
                    case 'email':
                        if (!(/^(.+){3,}@(.+){2,}\.[a-z]{2,}$/.test(inputVal)))
                            this.$errorMessages.push('Please provide a valid email address');
                        break;
                    // At least (one capital varter, one small letter, one number 0-9 and one special symbol)
                    case 'password':
                        if (!(/^(?=.*[A-Z])(?=.*[!@#$%^&*+-_])(?=.*[0-9])(?=.*[a-z]).*$/.test(inputVal)))
                            this.$errorMessages.push('Please provide a valid password pattern');
                        break;
                }
            } // End case 1
            // Case 2 -- check Rule that have TWO value e.g('min:3')
            else if (rules[j].indexOf(':') > -1) {
                var ruleValue = rules[j].split(':');
                switch (ruleValue[0]) {
                    case 'min':
                        if (inputVal.length < ruleValue[1])
                            this.$errorMessages.push('The minimum value allowed is ' + ruleValue[1]);
                        break;
                    case 'max':
                        if (inputVal.length > ruleValue[1])
                            this.$errorMessages.push('The maximum value allowed is ' + ruleValue[1]);
                        break;
                    // Match the value of input field with the given value of element id
                    case 'match':
                        if (inputVal !== document.getElementById(ruleValue[1]).value)
                            this.$errorMessages.push('Passwords don\'t match');
                        break;
                }
            } // End case 2
        } // End for loop

        if (this.isEmptyErrors())
            this.removeErrorMessages(_element);
        else
            this.appendErrorMessages(_element, this.$errorMessages);
    }
};

Validation.prototype.onBlurValidation = function () {
    'use strict';
    var self = this;
    // loop throw each input field
    for (var i = 0; i < this.fields.length; i++) {
        this.fields[i].onblur = function () {
            self.render();
        };
    }
};

// LOGIN

window.onload = function(){$("#showPassword").hide();}

$("#txtPassword").on('change',function() {  
    if($("#txtPassword").val())
    {
      $("#showPassword").show();
    }
    else
    {
      $("#showPassword").hide();
    }
});

$(".reveal").on('click',function() {
    var $pwd = $("#txtPassword");
    if ($pwd.attr('type') === 'password') 
    {
        $pwd.attr('type', 'text');
    } 
    else 
    {
        $pwd.attr('type', 'password');
    }
});
