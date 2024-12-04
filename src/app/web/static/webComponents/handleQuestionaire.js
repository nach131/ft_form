
const urlparams = new URLSearchParams(window.location.search);
let formId = urlparams.get('formId');

if (formId){
    
    try{
        let response = await fetch(`http://localhost:8000/api/sent-form/${userId}/${formId}`);
        if (!response.ok){
            throw new Error('Error: failed to fetch form');
        }
        let data = await response.json();
        renderQuestionaire(data);
    }catch(error){
        console.log(error);
    }
}


function renderQuestionaire(data){
   let content =  document.getElementsByTagName('body');
   let estile = document.createElement('style');
   estile.textContent = `
        body{
            color: #000;
        }
        .question-container {
            display: none;
        }
        .question-container.active {
            display: block;
        }
   `;
    content.appendChild(estile);

    let container = document.createElement('div');
    container.id = 'questionaire-container';
    body.appendChild(container);

    let questionElements = [];

    data.forEach((question,index ) => {
        let questionElement;
        let fieldType = question.type;

        if (fieldType === 'Text question'){
            questionElement = document.createElement('text-tag');
            questionElement.setAttribute('minlength', question.min_chars);
            questionElement.setAttribute('maxlength', question.max_chars);
            questionElement.setAttribute('question', question.text);
            questionElement.setAttribute('numQuestion', question.order);
        }else if (fieldType === 'Boolean question'){
            questionElement = document.createElement('binary-tag');
            questionElement.setAttribute('question', question.text);
            questionElement.setAttribute('numQuestion', question.order);
        }else if (fieldType === 'Option question'){
            questionElement = document.createElement('multiple-option-tag');
            questionElement.setAttribute('question', question.text);
            questionElement.setAttribute('numQuestion', question.order);
            questionElement.setAttribute('options', question.options);
        }else{
            console.log('Invalid or yet not suported question type');
        }
        if (questionElement){
            let questionContainer = document.createElement('div');
            questionContainer.className = 'question-container';
            if (index === 0) {
                questionContainer.classList.add('active');
            }
            questionContainer.appendChild(questionElement);
            container.appendChild(questionContainer);
            questionElements.push(questionContainer);

            let nextButton = questionElement.querySelector('#next-btn');
            let prevButton = questionElement.querySelector('#prev-btn');

            if (nextButton) {
                nextButton.addEventListener('click', () => {
                    if (index < questionElements.length - 1) {
                        showQuestion(index + 1);
                    }
                });
            }

            if (prevButton) {
                prevButton.addEventListener('click', () => {
                    if (index > 0) {
                        showQuestion(index - 1);
                    }
                });
            }
        }
    });
    let currentIndex = 0;

    function showQuestion(index) {
        questionElements[currentIndex].classList.remove('active');
        questionElements[index].classList.add('active');
        currentIndex = index;
    }

}