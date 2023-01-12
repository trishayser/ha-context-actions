import {
  LitElement,
  html,
  css
} from "https://unpkg.com/lit-element@2.0.1/lit-element.js?module";
import { until } from '/local/lit-html/directives/until.js';


class ContextActionsCard extends LitElement {
  static get properties() {
    return {
      hass: {},
      config: {},
      data: Array
    }
  }

  constructor() {
    super();
    this.data = [];
    this.activated = false;
    this.data_init = false;
  }

  connectedCallback() {
    super.connectedCallback();
    this.fetchData();
  }

  fetchData() {
    // fetch json file
    fetch('/local/json.json', {
      mode: 'same-origin',
      headers: { 'Content-Type': 'application/json', }
    })
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        };
        return response.json();
      })
      .then(data => {
        // init all data one time
        if (this.data_init == false) {
          this.data = data;
          this.data_init = true;
        }
        for (let i = 0; i < data.length; i++) {
          var found = false;
          for (let j = 0; j < this.data.length; j++) {
            if (this.data[j].action_id == data[i].action_id) {
              found = true;
            }
          }
          if (found == false) {
            this.data.push(data[i]);
          }
        }
        console.log('Success:', data);
      })
      .catch((error) => {
        console.error('Error:', error);
      });
  }

  // render card
  render() {
    // get data
    this.fetchData();
    var json_file = "http://homeassistant:8123/local/json.json";

    // call the context action service to update
    this.hass.callService("context_actions", "update_json");

    // loading message
    if (!this.data) {
      return html`
              <h4>Loading...</h4>
          `;
    }

    // render html
    return html`
          <ha-card class="ca-card"> ${console.log("rendered")}
            <h1 class="card-header">Context Actions</h1>
            <div class="card-content">
              ${this.data.map(ent => {
      ent.activated = false;
      var action_text;

      // get service name from json data
      var hass_service = ent.state_data.service.split('.')[1]

      // get service word in german
      if (hass_service == "turn_on") {
        action_text = "anmachen";
      } else if (hass_service == "turn_off") {
        action_text = "ausmachen";
      } else if (hass_service == "close_cover") {
        action_text = "zumachen"
      } else if (hass_service == "lock") {
        action_text = "schließen"
      } else if (hass_service == "unlock") {
        action_text = "aufschließen"
      }

      return html`
                <div class="ca-action">
                  <div class="ca-row">
                    <div class="ca-generic-row">
                      <div class="ca-name">${ent.friendly_name} ${action_text}</div>
                      <label class="switch ca-switch">
                        <input type="checkbox" @click="${() => this._handlebuttonclick(ent)}" onchange="document.getElementById('action-3').disabled = !this.checked;" id="action-${ent.action_id}">
                        <span class="slider round"></span>
                      </label>
                    </div>
                  </div>
                </div>
                `;


    })}
            </div>
          </ha-card>`;
  }

  // cal service, when a button is clicked
  _handlebuttonclick(entitiy) {
    var hass_domain = entitiy.state_data.service.split('.')[0]
    var hass_service = entitiy.state_data.service.split('.')[1]
    this.hass.callService(hass_domain, hass_service, {
      entity_id: entitiy.entitiy
    });
  }

  setConfig(config) {
    this.config = config;
  }

  getCardSize() {
    return 3;
  }

  // css style
  static get styles() {
    return css`

        .ca-generic-row {
          display: flex;
          align-items: center;
          flex-direction: row;
        }

        .ca-switch {
          float: right;
        }

        .ca-name {
          flex: 1 0 30%;
          font-size: 1.2em;
        }

        .ca-action {
          padding: 5px 0px;
        }

        .switch {
          position: relative;
          display: inline-block;
          width: 60px;
          height: 34px;
        }
        
        /* Hide default HTML checkbox */
        .switch input {
          opacity: 0;
          width: 0;
          height: 0;
        }
        
        /* The slider */
        .slider {
          position: absolute;
          cursor: pointer;
          top: 0;
          left: 0;
          right: 0;
          bottom: 0;
          background-color: #ccc;
          -webkit-transition: .4s;
          transition: .4s;
        }
        
        .slider:before {
          position: absolute;
          content: "";
          height: 26px;
          width: 26px;
          left: 4px;
          bottom: 4px;
          background-color: white;
          -webkit-transition: .4s;
          transition: .4s;
        }
        
        input:checked + .slider {
          background-color: #2196F3;
        }
        
        input:focus + .slider {
          box-shadow: 0 0 1px #2196F3;
        }
        
        input:checked + .slider:before {
          -webkit-transform: translateX(26px);
          -ms-transform: translateX(26px);
          transform: translateX(26px);
        }
        
        /* Rounded sliders */
        .slider.round {
          border-radius: 34px;
        }
        
        .slider.round:before {
          border-radius: 50%;
        }`;
  }
}

// define card for lovelace
customElements.define('context-actions-card', ContextActionsCard);