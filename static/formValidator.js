/* 
    Form Validator 2.1.1 by Gix075
    ===================================================================
    This is an useful class that you can use to validate any forms.
*/

function formValidator(globOpts) {
    
    var defaults = {
        bootstrap: true,
        mail: {
            format: true,
            confirm: true
        },
        password: {
            format: true,
            formatRegEx: /\b([A-Z0-9])([a-z0-9]+)?\b/gm,
            confirm: true
        },
    	telephone: {
    		numbersOnly: false
    	},
            showErrors: true
    },
    opts = $.extend( true, defaults, globOpts ),
    validator = this;

    this.opts = opts,
	this.formValidation = true,
	this.validInput = false,
	this.validTextarea = false,
	this.validPassword = false,
	this.validEmail = false,
	this.validSelect = false,
	this.validRadio = false,
	this.validCheckbox = false,
	this.validPhone = false,
	
	// validation method
	this.validate = function(element, button, callbacks) {
	    $(button).on('click', function(e) {
	
	        e.preventDefault();
	
	        var form = $('form' + element),
	            input = form.find('input.validate').not('input[type="radio"]').not('input[type="checkbox"]'),
	            password = form.find('input[type="password"].validate'),
	            phone = form.find('input[type="tel"].validate'),
	            textarea = form.find('textarea.validate'),
	            select = form.find('select.validate'),
	            email = form.find('input[type="email"].validate'),
	            radio = form.find('.radio-group.validate'),
	            checkbox = form.find('.checkbox-group.validate'),
	            loopError = 0;
	            
	            
	
	        // text, tel and all commons inputs
	        // ****************************************************
	        $(input).each(function() {
	            if ($(this).val() == "") {
	                if (opts.showErrors === true) validator.showError(this, 'input', 'empty');
	                loopError = loopError + 1;
	            } else {
	                if (opts.showErrors === true) validator.hideError(this, 'input');
	            }
	        });
	        validator.validInput = (loopError > 0) ? false : true;
	        loopError = 0;
	        // end input
	
	        // telephone input
	        // ****************************************************
	        if (opts.telephone.numbersOnly === true) {
	            $(phone).each(function() {
	                var telValue = $(this).val();
	                if (telValue != "") {
	                    var reg = /^\d+$/;
	                    if (reg.test(telValue) === false) {
	                        if (opts.showErrors === true) validator.showError(this, 'input', 'wrong');
	                        loopError = loopError + 1;
	                    } else {
	                        if (opts.showErrors === true) validator.hideError(this, 'input');
	                    }
	                }
	            });
	        }
	        validator.validPhone = (loopError > 0) ? false : true;
	        loopError = 0; 
	        // end telephone
	
	        // textarea
	        // ****************************************************
	        $(textarea).each(function() {
	            if ($(this).val() == "") {
	                if (opts.showErrors === true) validator.showError(this, 'textarea', 'empty');
	                loopError = loopError + 1;
	            } else {
	                if (opts.showErrors === true) validator.hideError(this, 'textarea');
	            }
	        });
	        validator.validTextarea = (loopError > 0) ? false : true;
	        loopError = 0;
	        // end textarea
	
	        // select
	        // ****************************************************
	        $(select).each(function() {
	            if (!$("option:selected", this).not('.not-option').length) {
	                if (opts.showErrors === true) validator.showError(this, 'select', 'empty');
	                loopError = loopError + 1;
	            } else {
	                if (opts.showErrors === true) validator.hideError(this, 'select');
	            }
	        });
	        validator.validSelect = (loopError > 0) ? false : true;
	        loopError = 0;
	        // end select
	
	        // email
	        // ****************************************************
	        $(email).not('.email-confirm').each(function() {
	            if ($(this).val() != "" && opts.mail.format === true) {
	                var re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
	                if (re.test($(this).val()) === false) {
	                    if (opts.showErrors === true) validator.showError(this, 'email', 'wrong');
	                    loopError = loopError + 1;
	                } else {
	                    if (opts.showErrors === true) validator.hideError(this, 'email');
	                }
	            }
	
	            if ($(this).val() != "" && opts.mail.confirm === true && loopError == 0) {
	                console.log($(this).attr('id'));
	                var confirmElement = $('.email-confirm[data-confirm="#' + $(this).attr('id') + '"]');
	                if ($(this).val() != $(confirmElement).val()) {
	                    if (opts.showErrors === true) validator.showError(confirmElement, 'email', 'wrong');
	                    loopError = loopError + 1;
	                } else {
	                    if (opts.showErrors === true) validator.hideError(confirmElement, 'email');
	                }
	            }
	
	        });
	        validator.validEmail = (loopError > 0) ? false : true;
	        loopError = 0;
	        // end email
	
	        // password 
	        // ****************************************************
	        //password format
	        if (opts.password.format === true) {
	            $(password).not('.pswd-confirm').each(function() {
	                if ($(this).val() != "") {
	                    var string = $(this).val(),
	                        regex = opts.password.formatRegEx;
	                    if (string.match(regex)) {
	                        if (opts.showErrors === true) validator.hideError(this, 'password');
	                    } else {
	                        if (opts.showErrors === true) validator.showError(this, 'password', 'wrong');
	                        loopError = loopError + 1;
	                    }
	                }
	            });
	        }
	
	        // password confirm 
	        if (opts.password.confirm === true) {
	            $('.pswd-confirm').each(function() {
	                if ($(this).val() != "") {
	                    var confirmPswdElement = $(this).data('confirm');
	                    if ($(this).val() != $(confirmPswdElement).val()) {
	                        if (opts.showErrors === true) validator.showError(this, 'password', 'wrong');
	                        loopError = loopError + 1;
	                    } else {
	                        if (opts.showErrors === true) validator.hideError(this, 'password');
	                    }
	                }
	            });
	        }
	        validator.validPassword = (loopError > 0) ? false : true;
	        loopError = 0;
	        // end password
	
	        // radio
	        // ****************************************************
	        $(radio).each(function() {
	            var checkedbox = false;
	            $(this).find('input[type="radio"]').each(function() {
	                if ($(this).is(':checked')) checkedbox = true;
	            })
	
	            if (checkedbox === false) {
	                if (opts.showErrors === true) validator.showError(this, 'radio', 'empty');
	                loopError = loopError + 1;
	            } else {
	                if (opts.showErrors === true) validator.hideError(this, 'radio');
	            }
	
	        });
	        validator.validRadio = (loopError > 0) ? false : true;
	        loopError = 0;
	        // end radio
	
	        // checkbox
	        // ****************************************************
	        $(checkbox).each(function() {
	            var checkedbox = false;
	            $(this).find('input[type="checkbox"]').each(function() {
	                if ($(this).is(':checked')) checkedbox = true;
	            })
	
	            if (checkedbox === false) {
	                if (opts.showErrors === true) validator.showError(this, 'checkbox', 'empty');
	                loopError = loopError + 1;
	            } else {
	                if (opts.showErrors === true) validator.hideError(this, 'checkbox');
	            }
	
	        });
	        validator.validCheckbox = (loopError > 0) ? false : true;
	        loopError = 0;
	        // end checkbox
	
	        // Callback Functions
	        // ****************************************************
	        if (validator.validInput === true && validator.validPassword === true && validator.validPhone === true && validator.validTextarea === true && validator.validEmail === true && validator.validSelect === true && validator.validRadio === true && validator.validCheckbox === true) {
	            callbacks.success();
	        } else {
	            callbacks.fail();
	        }
	
	
	    }); //end click
	
	
	}, // end validate()
	
	this.showError = function(inputElement, inputType, errorType) {
	    if (inputType == 'radio' || inputType == 'checkbox') {
	        // checkbox and radio error message
	        (opts.bootstrap === true) ? $(inputElement).closest('.' + inputType + '-group').addClass('has-error'): $(inputElement).addClass('error');
	        $(inputElement).closest('.' + inputType + '-group').find('.form-input-error-msg').addClass('show-error');
	    } else {
	        // common inputs error message
	        (opts.bootstrap === true) ? $(inputElement).closest('.form-group').addClass('has-error'): $(inputElement).addClass('error');
	        $(inputElement).prev('.form-input-error-msg').addClass('show-error');
	        switch (errorType) {
	            case 'empty':
	                $(inputElement).prev('.form-input-error-msg').find('.error-wrong').removeClass('show-error');
	                $(inputElement).prev('.form-input-error-msg').find('.error-empty').addClass('show-error');
	                break;
	            case 'wrong':
	                $(inputElement).prev('.form-input-error-msg').find('.error-empty').removeClass('show-error');
	                $(inputElement).prev('.form-input-error-msg').find('.error-wrong').addClass('show-error');
	                break;
	        } //end switch
	
	    }
	
	},
	this.hideError = function(inputElement, inputType) {
	    if (inputType == 'radio' || inputType == 'checkbox') {
	        (opts.bootstrap === true) ? $(inputElement).closest('.' + inputType + '-group').removeClass('has-error'): $(inputElement).removeClass('error');
	        $(inputElement).closest('.' + inputType + '-group').find('.form-input-error-msg').removeClass('show-error');
	    } else {
	        (opts.bootstrap === true) ? $(inputElement).closest('.form-group').removeClass('has-error'): $(inputElement).removeClass('error');
	        $(inputElement).prev('.form-input-error-msg').removeClass('show-error');
	        $(inputElement).prev('.form-input-error-msg').find('.error-empty,.error-wrong').removeClass('show-error');
	    }
	
	},
	this.clearError = function(formElement) {
	    $(formElement).find('*').removeClass('error');
	    $(formElement).find('*').removeClass('has-error');
	    $(formElement).find('*').removeClass('show-error');
	}

}