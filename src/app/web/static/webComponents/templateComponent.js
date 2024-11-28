/* Reemplazar el nombre TemplateComponent por el de la clase que deseamos crear*/
class TemplateComponent extends HTMLElement{
    constructor(){
        super();
        let shadow = this.attachShadow({mode: 'open'});
        let estilo = document.createElement('style');
        /* insertar el estilo(css) que queramos darle al componente dentro del text content de la variable estilo*/
        estilo.textContent = /*css*/``;
        shadow.appendChild(estilo);
        let content = document.createElement('div');
        /* insertar los elementos html que queramos darle al componente dentro del text content de la variable content*/
        content.innerHTML = /*html*/``;
        shadow.appendChild(content);
    }
    /*Metodos del ciclo de vida del componente aqui van todos los event listeners
     , y fetchs que necesite hacer el componente para su funcionamiento, asi como funciones que necesite para su uso */
    connectedCallback(){
        
    }
    /*aqui nos encargamos de eliminar todos los event listener que creamos en la connected callback,
     para que no queden huerfanos*/ 
    disconnectedCallback(){
    }
}

/*Reemplazar los campos por template-component por el nombre que queramos darle a la etiqueta en cuestion y TemplateComponent por el nombre de la clase creada*/
window.customElements.define('template-component', TemplateComponent);
