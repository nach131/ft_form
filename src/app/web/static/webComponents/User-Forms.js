class UserForms extends HTMLElement {
	constructor() {
	  super();
	  this.shadow = this.attachShadow({ mode: 'open' });
	  this._query = '';
	  this.container = document.createElement('div');
	  this.container.classList.add('container', 'mt-4');
	  this.container.innerHTML = `
		<div id="appendCardsHere" class="row g-3">
		
		</div>

	  `;
	  this.importStyles();

  
	  this.shadow.appendChild(this.container);
	}
  
	importStyles() {
	  const generalBootstrap = document.createElement('link');
	  generalBootstrap.setAttribute('rel', 'stylesheet');
	  generalBootstrap.setAttribute('href', window.djangoStaticUrls.bootstrapChanges);
  
	  const styleLink = document.createElement('link');
	  styleLink.setAttribute('rel', 'stylesheet');
	  styleLink.setAttribute('href', window.djangoStaticUrls.studentHomeStyles);
  
	  const bootstrap = document.createElement('link');
	  bootstrap.setAttribute('rel', 'stylesheet');
	  bootstrap.setAttribute('href', window.djangoStaticUrls.bootstrapCSS);
  
	  this.shadow.appendChild(styleLink);
	  this.shadow.appendChild(generalBootstrap);
	  this.shadow.appendChild(bootstrap);
	}
	
	addCard({ id, title, startDate, endDate, state, color, minutes, imageUrl }) {
		const GridOfCards = this.container.querySelector('#appendCardsHere');
	
		if (GridOfCards) {
			const card = document.createElement('section');
			card.classList.add('col-12', 'col-sm-6', 'col-md-4', 'col-lg-3');
			card.setAttribute('data-id', id);
			card.innerHTML = `
				   <div class="card" >
                <div id="header-${id}"class="card-header" style="height:150px " >
			
                </div>
                <div class="container" style="">
                    <!-- First Row -->
            <div class="row g-3 d-flex align-items-center justify-content-between mt-1 ms-2 me-2" >
                <!-- First column, aligned to the start -->
                <div class="col-2 d-flex align-items-center pe-1">
                    
                </div>

                <!-- Second column, aligned to the center -->
                <div  class="col-2 d-flex flex-column align-items-center justify-content-center pe-1 mb-5 position-relative ">
                    <!-- Stars stacked vertically -->
                     <div id="trophy-${id}"class="d-flex flex-column align-items-center justify-content-center star-container mb-5">
						
                        
                        <!-- Checkbox behind the stars -->
                     </div>
                </div>

                <!-- Third column, aligned to the end -->
                <div class="col-2 d-flex align-items-center pe-1">
                    <abbr title="${startDate} - ${endDate}">
                        <img class="mb-3" src="${window.djangoStaticUrls.calendarIcon}" width="30" height="30">
                    </abbr>
                </div>
            </div>
            </div>
                    <!-- Second Row -->
                    <div class="row ms-1 me-1">
                        <h3 class="card-title" >${title}</h2>
                    </div>

                    <!-- Third Row -->
                    <div class="row ms-2 me-2">
                        <!-- <div class="col-md-12"> -->
                            <div class="p-3 d-flex justify-content-start ">${minutes ? minutes :  '5'} min</div>
                        <!-- </div> -->
                    </div>
                    
                    <div class="row ms-2 me-2 mt-5">
                        <div class="col-md-12 d-flex justify-content-end align-items-end mt-3">
                          
                            <button onclick="window.location.href='https://example.com?formid=${id}';" type="button" class="btn " style="background-color: ${color}; border 0px; font-weight: bold; color: white;">Enter</button>
                        </div>
                    </div>
			`;
	
			const style = document.createElement('style');
			style.textContent = `
				.card-tall {
					height: 400px;
				}
				.card-header {
					
					background-size: cover;
					background-repeat: no-repeat;
					background-position: center;
				}
				.star-container {
					border-radius: 50%;
					background: #ededed;
					height: 50px;
					width: 50px;
				}
				
			`;
		
			let cardHeader = card.querySelector(`#header-${id}`);


			cardHeader.style.backgroundImage = `url('${imageUrl}')`;
			cardHeader.style.backgroundSize = 'cover';
			cardHeader.style.backgroundRepeat = 'no-repeat';
			cardHeader.style.backgroundPosition = 'center';
			
				

			card.appendChild(style);

			if (state === 'New')
			{
				let trophyParent = card.querySelector(`#trophy-${id}`); 
				if (trophyParent) {
					let completeTrophy = document.createElement('img');
					completeTrophy.src = window.djangoStaticUrls.trophyBlack
					completeTrophy.width = 30;
					completeTrophy.height = 30;
					
					trophyParent.appendChild(completeTrophy);
				}
				let newTitle = card.querySelector(`#header-${id}`); 
				if (newTitle) {
					let completeTrophy = document.createElement('h3');
					completeTrophy.textContent = 'New';
					completeTrophy.style.color = `${color}`;
					completeTrophy.style.fontSize = '24px'; 
					completeTrophy.style.fontWeight = 'bold'; 
			
					newTitle.appendChild(completeTrophy);
				}
	

			}
			else if (state == 'Complete')
			{
				let trophyParent = card.querySelector(`#trophy-${id}`); 
				let completeTrophy = document.createElement('img');
				completeTrophy.src = window.djangoStaticUrls.trophy;
				completeTrophy.width = 30;
				completeTrophy.height = 30;

				trophyParent.appendChild(completeTrophy);
			}
			else 
			{
				let trophyParent = card.querySelector(`#trophy-${id}`); 
				if (trophyParent) {

					let completeTrophy = document.createElement('img');
					completeTrophy.src = window.djangoStaticUrls.trophyBlack
					completeTrophy.width = 30;
					completeTrophy.height = 30;
					
					trophyParent.appendChild(completeTrophy);
				}
			} 
		
			
			
			GridOfCards.appendChild(card);
		}
	}

	
	connectedCallback() {
		const baseUrl = window.location.origin; 
		const userId = localStorage.getItem('id'); 


		const url = `${baseUrl}/api/user-forms/${userId}/`;

		// Make the GET request
		fetch(url, {
			method: 'GET',
		
		})
			.then(response => {
				if (!response.ok) {
					throw new Error('Network response was not ok');
				}
				return response.json();
			})
			.then(data => {
				data.forEach(element => {
					this.addCard({
						id: element.id,
						title: element.form_details.name,
						startDate: new Date(element.sended).toLocaleString(),
						endDate: "No End Date",
						state: element.is_new ? 'New' : 'Normal',
						color: localStorage.getItem('color'),
						imageUrl: 'https://developers.elementor.com/docs/assets/img/elementor-placeholder-image.png'
					})
				});
				
			})
			.catch(error => {
				console.error('There was a problem with the fetch operation:', error);
			});

		// this.addCard({
		// 	id: 1,
		// 	title: "Formulario Empleo Estudiantes",
		// 	startDate: "01/11/2024",
		// 	endDate: "15/11/2024",
		// 	badges: [{ text: "Info", }, { text: "Alert" }],
		// 	state: 'Complete',
		// 	color: '#3ED008',
		// 	imageUrl: 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT5GQARsHihVdu6u6zx-dPvQy9z42nlQXo8bg&s'
		//   });
	}
  }
  
  window.customElements.define('user-forms', UserForms);
  