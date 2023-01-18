document.addEventListener("DOMContentLoaded", function () {

    const institutionList = document.querySelector('#institution-list')
    if (institutionList) {
        const buttonOne = document.querySelector('#button-step-1')
        let userCategories
        // Transition step1 > step2:
        buttonOne.addEventListener('click', function (e) {

            const categoryList = document.querySelector('#category-list')
            const categories = [...categoryList.querySelectorAll('input')]
            userCategories = []
            categories.forEach(category => {
                if (category.checked) {
                    userCategories.push(category.value)
                }
            })
            const emptyCategory = categoryList.querySelector('.empty-category')
            if (userCategories.length === 0) {
                e.stopImmediatePropagation()
                emptyCategory.style.display = 'flex'
            } else {
                emptyCategory.style.display = 'none'
            }

        })


        //     Transition step2 > step3:
        const buttonTwo = document.querySelector("#button-step-2")
        buttonTwo.addEventListener('click', function (e) {
            let filtredInstitutions = []
            const institutions = [...institutionList.querySelectorAll('label')]
            institutions.forEach(institution => {
                let instCategories = []
                instCategories += institution.querySelector('.hidden-info').textContent.split(', ')
                if (userCategories.every(cat => instCategories.includes(cat))) {
                    institution.style.display = "flex"
                    filtredInstitutions.push(institution)
                } else {
                    institution.style.display = "none"
                }
            })

            const bagsInput = e.target.parentElement.parentElement.querySelector("input");
            const emptyBags = document.querySelector('#empty-bags')
            console.log(bagsInput.value)
            if (bagsInput.value) {
                emptyBags.style.display = 'none'
            } else {
                e.stopImmediatePropagation()
                emptyBags.style.display = 'flex'
            }

            const emptyMessage = institutionList.querySelector('.empty-list')
            if (filtredInstitutions.length) {
                emptyMessage.style.display = 'none'
            } else {
                emptyMessage.style.display = 'flex'

            }
            //     Add amount of bags to donation summary:
            const bagsSummary = document.querySelector('.bags-summary')
            const newSpanBags = document.createElement('span')
            newSpanBags.setAttribute('class', "summary--text")
            newSpanBags.innerText = `Liczba worków: ${bagsInput.value}.`
            bagsSummary.appendChild(newSpanBags)
        })

        //     Transition step3 > step4 ( user won't be able to continue if no institution is selected ):
        const buttonThree = document.querySelector("#button-step-3")
        buttonThree.addEventListener('click', function (e) {
            const institutionInput = [...institutionList.querySelectorAll('input')]
            let userInstitutions = []

            console.log(userInstitutions)
            institutionInput.forEach(institution => {
                console.log(institution)
                if (institution.checked) {
                    userInstitutions.push(institution.id)
                }
            })
            const emptyInstitution = document.querySelector('#empty-institution')
            if (userInstitutions.length === 0) {
                e.stopImmediatePropagation()
                emptyInstitution.style.display = 'flex'
            } else {
                emptyInstitution.style.display = 'none'
            }
            // Add institution name to donation summary:
            const institutionSummary = document.querySelector('.institution-summary')
            const newSpanInstitution = document.createElement('span')
            newSpanInstitution.setAttribute('class', "summary--text")
            newSpanInstitution.innerText = `Dla ${userInstitutions[0]}.`
            institutionSummary.appendChild(newSpanInstitution)

        })
        // Transition step 4 > 5
        const buttonFour = document.querySelector('#button-step-4')
        buttonFour.addEventListener('click', function (e) {

            const donationDetails = document.querySelector('#pick-up-details')
            const donationInput = [...donationDetails.querySelectorAll('input')]
            const dateDetails = document.querySelector('#pick-up-date')
            const dateInput = [...dateDetails.querySelectorAll('input')]

            let userDates = []
            console.log(userDates)
            dateInput.forEach(date => {
                userDates.push(date.value)
            })

            let userDonation = []
            donationInput.forEach(donation => {
                userDonation.push(donation.value)
            })

            function getTomorrow() {
                let today = new Date();
                let tomorrow = new Date(today);
                tomorrow.setHours(0);
                tomorrow.setMinutes(0);
                tomorrow.setSeconds(0);
                tomorrow.setDate(tomorrow.getDate() + 1);
                return tomorrow;
            }

            function validateDate(date_data) {
                let inputDate = new Date(date_data);
                return inputDate >= getTomorrow();
            }


            let numberValidation = /[a-zA-Z]/g
            const emptyDetails = document.querySelector('#empty-details')
            const wrongPhoneNumber = document.querySelector('#wrong-data')
            const wrongZipCode = document.querySelector('#wrong-zip-code')
            const wrongDate = document.querySelector('#wrong-date')
            if (userDonation[0].length <= 2) {
                e.stopImmediatePropagation()
                emptyDetails.style.display = 'flex'
            } else if (userDonation[1].length <= 2) {
                e.stopImmediatePropagation()
                emptyDetails.style.display = 'flex'
            } else if (userDonation[2].length <= 4) {
                e.stopImmediatePropagation()
                wrongZipCode.style.display = 'flex'
            } else if (numberValidation.test(userDonation[2])) {
                e.stopImmediatePropagation()
                wrongZipCode.style.display = 'flex'
            } else if (userDonation[3].length <= 8 || userDonation[3].length >= 20) {
                e.stopImmediatePropagation()
                wrongPhoneNumber.style.display = 'flex'
            } else if (numberValidation.test(userDonation[3])) {
                e.stopImmediatePropagation()
                wrongPhoneNumber.style.display = 'flex'
            } else if (!validateDate(userDates[0])) {
                e.stopImmediatePropagation()
                wrongDate.style.display = 'flex'

            } else {
                emptyDetails.style.display = 'none'
                wrongPhoneNumber.style.display = 'none'
                wrongZipCode.style.display = 'none'
            }
            // Filling up donation summary with user inputs:
            const addressSummary = document.querySelector('.address-list')
            const newLiAddress = document.createElement('li')
            const newLiCity = document.createElement('li')
            const newLiZipCode = document.createElement('li')
            const newLiPhoneNumber = document.createElement('li')
            const dateSummary = document.querySelector('.pick-up-date')
            const newLiDate = document.createElement('li')
            const newLiTime = document.createElement('li')

            newLiAddress.classList.add('addressSummary')
            newLiAddress.innerText = userDonation[0]
            addressSummary.appendChild(newLiAddress)

            newLiCity.classList.add('addressSummary')
            newLiCity.innerText = userDonation[1]
            addressSummary.appendChild(newLiCity)

            newLiZipCode.classList.add('addressSummary')
            newLiZipCode.innerText = userDonation[2]
            addressSummary.appendChild(newLiZipCode)

            newLiPhoneNumber.classList.add('addressSummary')
            newLiPhoneNumber.innerText = userDonation[3]
            addressSummary.appendChild(newLiPhoneNumber)

            newLiDate.classList.add('dateSummary')
            newLiDate.innerText = `Dnia: ${userDates[0]}`
            dateSummary.appendChild(newLiDate)

            newLiTime.classList.add('dateSummary')
            newLiTime.innerText = `O godzinie: ${userDates[1]}`
            dateSummary.appendChild(newLiTime)

        })


    }

    /**
     * HomePage - Help section
     */
    class Help {
        constructor($el) {
            this.$el = $el;
            this.$buttonsContainer = $el.querySelector(".help--buttons");
            this.$slidesContainers = $el.querySelectorAll(".help--slides");
            this.currentSlide = this.$buttonsContainer.querySelector(".active").parentElement.dataset.id;
            this.init();
        }

        init() {
            this.events();
        }

        events() {
            /**
             * Slide buttons
             */
            this.$buttonsContainer.addEventListener("click", e => {
                if (e.target.classList.contains("btn")) {
                    this.changeSlide(e);
                }
            });

            /**
             * Pagination buttons
             */
            this.$el.addEventListener("click", e => {
                if (e.target.classList.contains("btn") && e.target.parentElement.parentElement.classList.contains("help--slides-pagination")) {
                    this.changePage(e);
                }
            });
        }

        changeSlide(e) {
            e.preventDefault();
            const $btn = e.target;

            // Buttons Active class change
            [...this.$buttonsContainer.children].forEach(btn => btn.firstElementChild.classList.remove("active"));
            $btn.classList.add("active");

            // Current slide
            this.currentSlide = $btn.parentElement.dataset.id;

            // Slides active class change
            this.$slidesContainers.forEach(el => {
                el.classList.remove("active");

                if (el.dataset.id === this.currentSlide) {
                    el.classList.add("active");
                }
            });
        }

        /**
         * TODO: callback to page change event
         */
        changePage(e) {
            e.preventDefault();
            const page = e.target.dataset.page;

            // console.log(page);
        }
    }

    const helpSection = document.querySelector(".help");
    if (helpSection !== null) {
        new Help(helpSection);
    }

    /**
     * Form Select
     */
    class FormSelect {
        constructor($el) {
            this.$el = $el;
            this.options = [...$el.children];
            this.init();
        }

        init() {
            this.createElements();
            this.addEvents();
            this.$el.parentElement.removeChild(this.$el);
        }

        createElements() {
            // Input for value
            this.valueInput = document.createElement("input");
            this.valueInput.type = "text";
            this.valueInput.name = this.$el.name;

            // Dropdown container
            this.dropdown = document.createElement("div");
            this.dropdown.classList.add("dropdown");

            // List container
            this.ul = document.createElement("ul");

            // All list options
            this.options.forEach((el, i) => {
                const li = document.createElement("li");
                li.dataset.value = el.value;
                li.innerText = el.innerText;

                if (i === 0) {
                    // First clickable option
                    this.current = document.createElement("div");
                    this.current.innerText = el.innerText;
                    this.dropdown.appendChild(this.current);
                    this.valueInput.value = el.value;
                    li.classList.add("selected");
                }

                this.ul.appendChild(li);
            });

            this.dropdown.appendChild(this.ul);
            this.dropdown.appendChild(this.valueInput);
            this.$el.parentElement.appendChild(this.dropdown);
        }

        addEvents() {
            this.dropdown.addEventListener("click", e => {
                const target = e.target;
                this.dropdown.classList.toggle("selecting");

                // Save new value only when clicked on li
                if (target.tagName === "LI") {
                    this.valueInput.value = target.dataset.value;
                    this.current.innerText = target.innerText;
                }
            });
        }
    }

    document.querySelectorAll(".form-group--dropdown select").forEach(el => {
        new FormSelect(el);
    });

    /**
     * Hide elements when clicked on document
     */
    document.addEventListener("click", function (e) {
        const target = e.target;
        const tagName = target.tagName;

        if (target.classList.contains("dropdown")) return false;

        if (tagName === "LI" && target.parentElement.parentElement.classList.contains("dropdown")) {
            return false;
        }

        if (tagName === "DIV" && target.parentElement.classList.contains("dropdown")) {
            return false;
        }

        document.querySelectorAll(".form-group--dropdown .dropdown").forEach(el => {
            el.classList.remove("selecting");
        });
    });

    /**
     * Switching between form steps
     */
    class FormSteps {
        constructor(form) {
            this.$form = form;
            this.$next = form.querySelectorAll(".next-step");
            this.$prev = form.querySelectorAll(".prev-step");
            this.$step = form.querySelector(".form--steps-counter span");
            this.currentStep = 1;

            this.$stepInstructions = form.querySelectorAll(".form--steps-instructions p");
            const $stepForms = form.querySelectorAll("form > div");
            this.slides = [...this.$stepInstructions, ...$stepForms];

            this.init();
        }

        /**
         * Init all methods
         */
        init() {
            this.events();
            this.updateForm();
        }

        /**
         * All events that are happening in form
         */
        events() {
            // Next step
            this.$next.forEach(btn => {
                btn.addEventListener("click", e => {
                    e.preventDefault();
                    this.currentStep++;
                    this.updateForm();
                });
            });

            // Previous step
            this.$prev.forEach(btn => {
                btn.addEventListener("click", e => {
                    e.preventDefault();
                    this.currentStep--;
                    this.updateForm();
                });
            });

            // Form submit
            this.$form.querySelector("form").addEventListener("submit", e => this.submit(e));
        }

        /**
         * Update form front-end
         * Show next or previous section etc.
         */
        updateForm() {
            this.$step.innerText = this.currentStep;

            // TODO: Validation

            this.slides.forEach(slide => {
                slide.classList.remove("active");

                if (slide.dataset.step == this.currentStep) {
                    slide.classList.add("active");
                }
            });

            this.$stepInstructions[0].parentElement.parentElement.hidden = this.currentStep >= 6;
            this.$step.parentElement.hidden = this.currentStep >= 6;

            // TODO: get data from inputs and show them in summary
        }

        /**
         * Submit form
         *
         * TODO: validation, send data to server
         */
        // submit(e) {
        //     e.preventDefault();
        //     this.currentStep++;
        //     this.updateForm();
        // }
    }

    const form = document.querySelector(".form--steps");
    if (form !== null) {
        new FormSteps(form);
    }
});

