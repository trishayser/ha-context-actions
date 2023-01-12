# pp-context-actions


## Installation

1. Copy the `custom_component` folder and the `www` folder into the `configuration` folder of your Home Assistant installation and restart Home Assistant.
2. Configure your context actions for your needs like in the configuration section of this readme to your `configuration.yaml` and restart your Home Assistant System
3. Go to Settings -> Dashboard -> Resources and add `/local/context-actions-card.js` as JavaScript Module (You need to have to enabled the Advanced Mode in the User Settings)
4. Add `type: custom:context-actions-card` to your Lovelace dashboard
5. Disable the Cache from your Browser

## Configuration
Example:
``` yaml
context_actions:
    - rule:
        trigger:
            - type: light
              name: light.example_light
              state: 'off'
            - type: state
              name: example.state
              state: 'on'
        action:
              entity: example.example
              service: example.service
    - rule:
        trigger:
          - type: temperature
            name: example.heatpump
            min: 16.0
            max: 24.0
        action:
              entity: example.example
              service: example.service
```

| Type | Description |
| :-----: | :-: |
| light | Light States can trigger an action. Triggers needs `state` |
| temperature | Needs `min` or `max` or both to set a range, where it gets triggered |
| time | The Time can trigger an action. Needs `begin` and `end` to set a range of time for trigger an action. Time can be set as a string, like `'hh:mm'` |
| attr_if | Atrributes from an Entity can trigger an action. Needs `state` (state of the attribute) and `name_attribute` (name of the attribute).  |
| state_if | States from an Entity can trigger an action. Needs the name of the entity (`name`) and the `state`. |


## Testing

* For testing the Context Actions you can download Home Assistant here: https://www.home-assistant.io/installation/ (I recommend to install Home Assistant as a VM with VirtualBox)

* You can add demo devices to your Home Assistant System by adding `demo:` to the `configuration.yaml` and restart your Home Assistant System

* For copying the files into your Home Assistant System, you can use the Samba Add-On from the Add-On-Store. For editing the Configuration File, you can install the File Editor.

* Then you can install Context Actions, like in the Installation with the following configuration, which is based on the demo devices

``` yaml
# configuration.yaml
context_actions:
    - rule:
        trigger:
            - type: light
              name: light.kitchen_lights
              state: 'off'
            - type: light
              name: light.ceiling_lights
              state: 'off'
        action:
              entity: light.ceiling_lights
              service: light.turn_on
    - rule:
        trigger:
          - type: temperature
            name: climate.heatpump
            min: 16.0
        action:
              entity: cover.living_room_window
              service: cover.close_cover
    - rule:
        trigger:
          - type: state_if
            name: light.kitchen_lights
            state: 'off'
          - type: state_if
            name: lock.kitchen_door
            state: 'unlocked'
        action:
            entity: lock.kitchen_door
            service: lock.lock
```

* For testing you can change the state or the atrributes of the demo devices by using the developer tools in your Home Assistant
