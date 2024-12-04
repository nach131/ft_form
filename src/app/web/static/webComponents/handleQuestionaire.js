
const urlparams = new URLSearchParams(window.location.search);
let formId = urlparams.get('formId');
let userId = urlparams.get('userId');

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
   let content =  document.getElementsByTagName('body')[0];
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
    content.appendChild(container);

    let questionElements = [];

	function createQuestionElement(question, type) {
		let questionElement;
		if (type === 'text') {
		  questionElement = document.createElement('text-tag');
		  questionElement.setAttribute('minlength', question.min_chars);
		  questionElement.setAttribute('maxlength', question.max_chars);
		} else if (type === 'boolean') {
		  questionElement = document.createElement('binary-tag');
		} else if (type === 'option') {
		  questionElement = document.createElement('multiple-option-tag');
		}
		questionElement.setAttribute('question', question.text);
		questionElement.setAttribute('numQuestion', question.order);
		return questionElement;
	  }
	  data.text_questions.forEach((question) => {
		let questionElement = createQuestionElement(question, 'text');
		questionElements.push({ element: questionElement, order: question.order });
	  });
	  
	  data.boolean_questions.forEach((question) => {
		let questionElement = createQuestionElement(question, 'boolean');
		questionElements.push({ element: questionElement, order: question.order });
	  });
	  
	  data.option_questions.forEach((question) => {
		let questionElement = createQuestionElement(question, 'option');
		questionElements.push({ element: questionElement, order: question.order });
	  });

	  questionElements.sort((a, b) => a.order - b.order);

	  questionElements.forEach((item, index) => {
		console.log("item: ",item);
		console.log("index: ",index);
		let questionContainer = document.createElement('div');
		questionContainer.appendChild(item.element);
		container.appendChild(questionContainer);
	  
		let nextButton = item.element.querySelector('#next-btn');
		let prevButton = item.element.querySelector('#prev-btn');
		console.log(nextButton);
		console.log(prevButton);


		if (nextButton) {
			console.log('nextButton');
		  nextButton.addEventListener('click', () => {
			if (index < questionElements.length - 1) {
			  showQuestion(index + 1);
			}
		  });
		}
	  
		if (prevButton) {
			console.log('prevButton');
		  prevButton.addEventListener('click', () => {
			if (index > 0) {
			  showQuestion(index - 1);
			}
		  });
		}
});
	 
    let currentIndex = 0;

    function showQuestion(index) {
        questionElements[currentIndex].classList.remove('active');
        questionElements[index].classList.add('active');
        currentIndex = index;
    }
}