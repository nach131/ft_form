
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
        .inactive {
            display: none;
        }
        .active {
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
		let questionContainer = document.createElement('div');
		questionContainer.appendChild(questionElement);
		questionElements.push({ element: questionContainer, order: question.order });
	  });
	  
	  data.boolean_questions.forEach((question) => {
		let questionElement = createQuestionElement(question, 'boolean');
		let questionContainer = document.createElement('div');
		questionContainer.appendChild(questionElement);
		questionElements.push({ element: questionContainer, order: question.order });
	  });
	  
	  data.option_questions.forEach((question) => {
		let questionElement = createQuestionElement(question, 'option');
		let questionContainer = document.createElement('div');
		questionContainer.appendChild(questionElement);
		questionElements.push({ element: questionContainer, order: question.order });
	  });

	  questionElements.sort((a, b) => a.order - b.order);

	  questionElements.forEach((item, index) => {
		if(index === 0){
			item.element.classList.add('active');
		}
		else{
			item.element.classList.add('inactive');
		}
		container.appendChild(item.element);
		
		let customElement = item.element.firstElementChild;
		let shadow = customElement.shadowRoot;

		let nextButton = shadow.querySelector('#next-btn');
		let prevButton = shadow.querySelector('#prev-btn');


		if (nextButton) {
		  nextButton.addEventListener('click', (event) => {
			event.preventDefault();
			if (index < questionElements.length - 1) {
			  showQuestion(index + 1);
			}
		  });
		}
	  
		if (prevButton) {
		  prevButton.addEventListener('click', (event) => {
			event.preventDefault();
			if (index > 0) {
			  showQuestion(index - 1);
			}
		  });
		}
});
	 
    let currentIndex = 0;
	

    function showQuestion(index) {
		if (questionElements[currentIndex]) {
			console.log(questionElements[currentIndex]);
			questionElements[currentIndex].element.classList.remove('active');
			questionElements[currentIndex].element.classList.add('inactive');
		  }
		  if (questionElements[index]) {
			console.log(questionElements[index]);
			questionElements[index].element.classList.remove('inactive');
			questionElements[index].element.classList.add('active');
			currentIndex = index;
		  } else {
			console.error('Invalid index:', index);
		  }
		}
}