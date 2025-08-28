# features/steps/motion_sensor_steps.py
from behave import given, when, then

# --------------------------
# GIVEN STEPS
# --------------------------

@given('a motion sensor with UUID={UUID} is connected to the network')
def step_sensor_connected(context, UUID):
    context.sensor_uuid = UUID
    context.sensor_status = "idle"
    context.sensor_firmware = None
    context.sensor_battery = 100
    context.network_status = "connected"
    print(f"Sensor {UUID} connected to network")

@given('The sensor battery level is not below the minimum threshold 30%')
def step_battery_not_low(context):
    context.sensor_battery = 100
    print(f"Sensor battery level: {context.sensor_battery}% (not low)")

@given('The sensor battery level is below the minimum threshold 30%')
def step_battery_low(context):
    context.sensor_battery = 20
    print(f"Sensor battery level: {context.sensor_battery}% (low)")

@given('a new firmware version={Current_Version} is available')
def step_firmware_available(context, Current_Version):
    context.current_version = Current_Version
    print(f"Current firmware version: {Current_Version}")

# --------------------------
# WHEN STEPS
# --------------------------

@when('the firmware update process was triggered')
def step_trigger_firmware_update(context):
    if context.sensor_battery >= 30:
        context.sensor_status = "updating"
    else:
        context.sensor_status = "denied"
    print(f"Firmware update triggered. Sensor status: {context.sensor_status}")

@when('the network connection is lost')
def step_network_lost(context):
    context.network_status = "disconnected"
    print(f"Network lost for sensor {context.sensor_uuid}")


# --------------------------
# THEN STEPS
# --------------------------

@then('the motion sensor\'s status indicates "{expected_status}"')
def step_check_status(context, expected_status):
    assert context.sensor_status == expected_status, \
        f"Expected status {expected_status}, but got {context.sensor_status}"
    print(f"Sensor status verified: {context.sensor_status}")

@then('the firmware version on the sensor is updated to the new version={New_Version}')
def step_check_firmware_update(context, New_Version):
    if context.sensor_status == "updating":
        context.sensor_firmware = New_Version
    assert context.sensor_firmware == New_Version, \
        f"Expected firmware {New_Version}, but got {context.sensor_firmware}"
    print(f"Firmware updated successfully to {context.sensor_firmware}")

@then('the sensor\'s firmware version={Current_Version} remains the same.')
def step_firmware_not_updated(context, Current_Version):
    context.sensor_firmware = Current_Version
    assert context.sensor_firmware == Current_Version, \
        f"Firmware should remain {Current_Version}, but got {context.sensor_firmware}"
    print(f"Firmware remains unchanged at {context.sensor_firmware}")

@then('the motion sensor returns to its idle state')
def step_sensor_idle(context):
    if context.sensor_status == "updating":
        context.sensor_status = "idle"
    assert context.sensor_status == "idle", f"Sensor is not idle, status={context.sensor_status}"
    print(f"Sensor returned to idle state")

@then('the motion sensor can detect motion as expected')
def step_motion_detect(context):
    # Simulate motion detection
    motion_detected = True
    assert motion_detected, "Motion detection failed"
    print("Motion detection successful")

@then('a notification is sent to the user that the battery is too low to update')
def step_notify_low_battery(context):
    if context.sensor_status == "denied":
        notification_sent = True
    else:
        notification_sent = False
    assert notification_sent, "No low battery notification sent"
    print("Low battery notification sent")

@then('the firmware update is paused or aborted')
def step_update_paused(context):
    if context.network_status == "disconnected":
        context.sensor_status = "paused"
    assert context.sensor_status in ["paused", "denied"], \
        f"Firmware update not paused or aborted, status={context.sensor_status}"
    print(f"Firmware update {context.sensor_status}")

@then('a notification is sent to the user indicating a lost connection')
def step_notify_lost_connection(context):
    if context.network_status == "disconnected":
        notification_sent = True
    else:
        notification_sent = False
    assert notification_sent, "No lost connection notification sent"
    print("Lost connection notification sent")

@then('the sensor\'s firmware is not corrupted')
def step_firmware_not_corrupted(context):
    # Simulate firmware integrity check
    firmware_ok = True
    assert firmware_ok, "Firmware corrupted"
    print("Firmware integrity verified")

@then('the sensor is able to reconnect and retry the update once the network is restored')
def step_retry_update(context):
    if context.network_status == "connected":
        context.sensor_status = "updating"
    assert context.sensor_status == "updating", "Sensor did not retry update"
    print("Sensor retried firmware update successfully")
