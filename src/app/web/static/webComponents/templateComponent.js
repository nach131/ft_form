/* Reemplazar el nombre TemplateComponent por el de la clase que deseamos crear*/
class TemplateComponent extends HTMLElement{
    constructor(){
        super();
        let shadow = this.attachShadow({mode: 'open'});
        let estilo = document.createElement('style');
        estilo.textContent = /*css*/``;
        shadow.appendChild(estilo);
        let content = document.createElement('div');
        content.innerHTML = /*html*/``;
        shadow.appendChild(content);
    }
    connectedCallback(){
        
    }
    disconnectedCallback(){
    }
}
window.customElements.define('template-component', TemplateComponent);
