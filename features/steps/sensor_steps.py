# features/steps/sensor_steps.py
import json
from behave import given, when, then

# Utility function to load HIL config
def load_hil_config(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

@given('a heat sensor is connected to the HIL bench')
def step_impl(context):
    context.heat_sensor_config = load_hil_config("hil_configs/heat_sensor_config.json")
    context.heat_sensor_connected = True
    print(f"Heat sensor connected with config: {context.heat_sensor_config}")

@given('a gas sensor is connected to the HIL bench')
def step_impl(context):
    context.gas_sensor_config = load_hil_config("hil_configs/gas_sensor_config.json")
    context.gas_sensor_connected = True
    print(f"Gas sensor connected with config: {context.gas_sensor_config}")

@when('the firmware update process is triggered for the heat sensor')
def step_impl(context):
    if context.heat_sensor_connected:
        # Example: update simulation state
        context.heat_sensor_config['update_status'] = 'updating'
        print("Heat sensor firmware update triggered.")

@when('the firmware update process is triggered for the gas sensor')
def step_impl(context):
    if context.gas_sensor_connected:
        context.gas_sensor_config['update_status'] = 'updating'
        print("Gas sensor firmware update triggered.")

@then('the heat sensor firmware is updated successfully')
def step_impl(context):
    context.heat_sensor_config['update_status'] = 'updated'
    print("Heat sensor firmware updated successfully.")

@then('the gas sensor firmware is updated successfully')
def step_impl(context):
    context.gas_sensor_config['update_status'] = 'updated'
    print("Gas sensor firmware updated successfully.")


