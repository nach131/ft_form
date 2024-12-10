class TextComponent extends HTMLElement{
    constructor(){
        super();
        let shadow = this.attachShadow({mode: 'open'});
        let estilo = document.createElement('style');
        estilo.textContent = /*css*/`
        :host{
            color: #fff;
            width: 100vw;
            height: 100vh;
            font-family: 'Source Sans 3';
            display: block;
        }
        .form-card{
            border: 1px solid black;
                height: 40vh;
                width: 55vw;
                background: transparent;
                color: #fff;
                text-align: center;
                display:grid;
                grid-template-rows: 1fr 1fr 1fr 1fr;
                grid-template-columns: 1fr 1fr 1fr ; 
        }
        #question{
                top: 50%;
                left: 45%;
                transform: translate(-50%, -50%);
                position: absolute;
        }
        .num-question{
                text-align: left;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 1.5rem;
        }
        #next-btn{
            background-color: #FC0;
            border: 0px solid #000;
            color: #fff;
            font-size: 0.9rem;
            font-weight: 500;
            font-family: 'Source Sans 3';
            text-align: center;
            grid-row-start: 3;
            grid-row-end: 4;
            grid-column-start: 3;
            grid-column-end: 4;
            justify-self: flex-start;
            align-self: flex-start;
            border-radius: 15px;
            width: 64px;
			height: 25px;
        }
        #prev-btn{
            background-color: #00B8F0;
            color: #fff;
            border: 0px solid #000;
            font-size: 0.9rem;
            font-weight: 500;
            font-family: 'Source Sans 3';
            text-align: center;
            grid-row-start: 3;
            grid-row-end: 4;
            grid-column-start: 2;
            grid-column-end: 3;
            justify-self: center;
            align-self: flex-start;
            border-radius: 15px;
            width: 64px;
			height: 25px;
        }
        .question-title{
                display: flex;
				font-family: 'Source Sans 3';
                justify-content:flex-start;
                align-items: center;
                grid-column-start: 2;
                grid-column-end: 5;
                grid-row-start: 1;
                grid-row-end: 2;
                justify-self: stretch;
        }
        .input-container{
                grid-row-start: 2;
                grid-row-end: 5;
                grid-column-start: 2;
                grid-column-end: 4;
                display: grid;
                grid-template-rows: 1fr 1fr 1fr;
                grid-template-columns: 1fr 1fr 1fr;
                align-items: center;
            }
            svg{
                margin: 5px;
            }
            p{
                font-size: 1.5em;
            }
            input[type="text"] {
                height: 8.2em;
                width: 35em;
                border-radius: 15px;
                box-shadow: 0px 4px 4px 2px rgba(0, 0, 0, 0.25) inset;
                border: 1px solid #000;
                grid-column-start: span 3;
            }
            input[type="text"]::placeholder{
                color: rgba(0, 0, 0, 0.5);
                font-size: 1em;
                font-weight: 400;
                text-align: justify;
            }
			h1{
				font-weight: 400;
				font-size: 2.5em;
			}
        `;
        shadow.appendChild(estilo);
        let content = document.createElement('div');
		content.id = 'question';
        shadow.appendChild(content);
		
    }
    render(){
		let element = this.shadowRoot.getElementById('question');
		element.innerHTML = /*html*/`
            <div class="form-card">
                <div class="num-question">
                    <p>${this.numQuestion}</p>
                    <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="#fff">
                        <g clip-path="url(#clip0_171_262)">
                            <path d="M17.7806 15.031L11.0306 21.781C10.8899 21.9218 10.699 22.0008 10.5 22.0008C10.301 22.0008 10.1101 21.9218 9.96937 21.781C9.82864 21.6403 9.74958 21.4494 9.74958 21.2504C9.74958 21.0514 9.82864 20.8605 9.96937 20.7198L15.4397 15.2504H0.75C0.551088 15.2504 0.360322 15.1714 0.21967 15.0307C0.0790178 14.8901 0 14.6993 0 14.5004C0 14.3015 0.0790178 14.1107 0.21967 13.9701C0.360322 13.8294 0.551088 13.7504 0.75 13.7504H15.4397L9.96937 8.28104C9.82864 8.14031 9.74958 7.94944 9.74958 7.75042C9.74958 7.55139 9.82864 7.36052 9.96937 7.21979C10.1101 7.07906 10.301 7 10.5 7C10.699 7 10.8899 7.07906 11.0306 7.21979L17.7806 13.9698C17.8504 14.0394 17.9057 14.1222 17.9434 14.2132C17.9812 14.3043 18.0006 14.4019 18.0006 14.5004C18.0006 14.599 17.9812 14.6966 17.9434 14.7876C17.9057 14.8787 17.8504 14.9614 17.7806 15.031Z" fill="white"/>
                        </g>
                        <defs>
                            <clipPath id="clip0_171_262">
                                <rect width="24" height="24" fill="white"/>
                            </clipPath>
                        </defs>
                    </svg>   
                </div>
                <div class="question-title">
                    <h1 id="binary-question" for="binary">${this.question}</h1>
                </div>
                <form action="" class="input-container">
                    <input type="text" placeholder="Responde aqui" minlength="${this.getAttribute('minlength')}" maxlength="${this.getAttribute('maxlength')}"></input>
                    <button type="" id="next-btn">Next</button>
                </form>
            </div>
        `;
	}

    connectedCallback(){
		this.question = this.getAttribute('question');
        this.numQuestion = this.getAttribute('numQuestion');
		this.render();
        if (this.numQuestion != '1'){
            let inputContainer = this.shadowRoot.querySelector('.input-container');
            let prevBtn =  document.createElement('button');
            prevBtn.id = 'prev-btn';
            prevBtn.textContent = 'Previous';
            inputContainer.appendChild(prevBtn);
			
        }
    }
    
    disconnectedCallback(){
        let prevBtn = this.shadowRoot.querySelector('#prev-btn');
        if (prevBtn) {
            prevBtn.removeEventListener('click', this.prevBtnClickHandler);
        }
    }
}


window.customElements.define('text-tag', TextComponent);
