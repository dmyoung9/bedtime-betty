/* wizard.js */

class Wizard {
    constructor(containerId, apiKey) {
        this.container = document.getElementById(containerId);
        this.pages = [];
        this.currentPageIndex = -1;
        this.apiKey = apiKey;
    }

    addPage(sourceUrl, formatFunc = null) {
        const page = new WizardPage(sourceUrl, this.apiKey, formatFunc);
        this.pages.push(page);
        this.container.appendChild(page.optionsContainer);
    }

    async loadPage(num = 13) {
        const currentPage = this.pages[this.currentPageIndex];
        if (currentPage) {
            currentPage.loadOptions(num);
        }
    }

    async goToPage(index) {
        if (index >= 0 && index < this.pages.length) {
            this.currentPageIndex = index;
            this.updatePages();
        }
    }

    updatePages() {
        for (let idx in this.pages) {
            var offset = this.currentPageIndex * -100;
            this.pages[idx].optionsContainer.style.transform = `translate(${offset}%)`;
        }
    }

    nextPage() {
        this.goToPage(this.currentPageIndex + 1);
        this.loadPage();
    }

    previousPage() {
        this.goToPage(this.currentPageIndex - 1);
    }

    start() {
        this.goToPage(0);
        this.loadPage();
    }
}

class WizardPage {
    constructor(sourceUrl, apiKey, formatFunc) {
        this.sourceUrl = sourceUrl;
        this.apiKey = apiKey
        this.options = [];
        this.formatFunc = formatFunc;
        this.selectedOption = null;

        this.optionsRow = document.createElement('div');
        this.optionsRow.classList.add('row', 'align-items-center', 'justify-content-center');
        this.optionsContainer = document.createElement('div')
        this.optionsContainer.classList.add('page-container');
        this.optionsContainer.appendChild(this.optionsRow)
    }

    async loadOptions(num) {
        return new Promise((resolve, reject) => {
            const socket = new WebSocket(this.sourceUrl);

            socket.addEventListener('open', () => {
                console.log('WebSocket connection opened.');
                var request_msg = { type: 'request', data: { api_key: this.apiKey, num: num } }
                socket.send(JSON.stringify(request_msg));
            });

            socket.addEventListener('message', (event) => {
                const data = JSON.parse(event.data);
                console.log(data)
                if (data.type === 'end') {
                    socket.close();
                    resolve();
                } else if (data.type === 'item') {
                    this.addOption(data.data);
                }
            });

            socket.addEventListener('close', () => {
                console.log('WebSocket connection closed.');
            });

            socket.addEventListener('error', (error) => {
                console.error('WebSocket error:', error);
                reject(error);
            });
        });
    }

    addOption(option) {
        this.options.push(option);
        const optionCol = document.createElement('div');
        optionCol.classList.add('col-xs-12', 'col-sm-6', 'col-md-4', 'col-lg-3', 'mb-3');

        let optionElement = document.createElement('button');
        optionElement.classList.add('btn', 'btn-primary', 'option-btn');

        optionElement = this.formatFunc(optionElement, option);

        optionElement.addEventListener('click', () => {
            this.setSelectedOption(option);
        });

        optionCol.appendChild(optionElement);
        this.optionsRow.appendChild(optionCol);

        setTimeout(() => {
            optionElement.classList.add("loaded")
        }, 100);
    }

    setSelectedOption(option) {
        this.selectedOption = option;
        // Handle user interactions, like going to the next page or submitting the form
    }

    getSelectedOption() {
        return this.selectedOption;
    }

    show() {
        // this.optionsContainer.classList.add('active');
    }

    hide() {
        // this.optionsContainer.classList.remove('active');
    }

    slideLeft() {
        this.optionsContainer.classList.add('slide-left');
        this.optionsContainer.classList.remove('slide-center', 'slide-right');
    }

    slideCenter() {
        this.optionsContainer.classList.add('slide-center');
        this.optionsContainer.classList.remove('slide-left', 'slide-right');
    }

    slideRight() {
        this.optionsContainer.classList.add('slide-right');
        this.optionsContainer.classList.remove('slide-left', 'slide-center');
    }
}