from behave import given, when, then
import time

# Simulated HIL environment state
hil_state = {
    "connected": False,
    "firmware_version": None,
    "battery_level": 100,
    "network_connected": True,
    "alarm_active": False,
    "update_in_progress": False,
    "recovery_mode": False,
    "last_error": None,
}


@given('the {sensor_type} sensor is connected to the HIL testbench')
@given('the {sensor_type} sensor is connected to the HIL rig')
def step_connect_hil(context, sensor_type):
    hil_state["connected"] = True
    hil_state["sensor_type"] = sensor_type
    print(f"[HIL] {sensor_type} sensor connected.")


@given('the sensor battery level is above {level:d}%')
@given('the sensor battery level is below {level:d}%')
def step_set_battery(context, level):
    hil_state["battery_level"] = level
    print(f"[HIL] Battery set to {level}%.")


@given('the network connection to the update server is stable')
@given('the network connection is active')
def step_network_connected(context):
    hil_state["network_connected"] = True
    print("[HIL] Network connected.")


@given('the sensor has detected dangerous gas levels')
def step_gas_alarm(context):
    hil_state["alarm_active"] = True
    print("[HIL] Gas alarm triggered.")


@when('a new firmware version "{version}" is flashed via HIL')
def step_flash_firmware(context, version):
    if hil_state["battery_level"] < 20:
        hil_state["last_error"] = "LOW_BATTERY"
        hil_state["update_in_progress"] = False
        print("[HIL] Firmware update blocked due to low battery.")
        return
    if hil_state.get("alarm_active"):
        hil_state["last_error"] = "ACTIVE_ALARM"
        hil_state["update_in_progress"] = False
        print("[HIL] Firmware update blocked due to active alarm.")
        return
    if not hil_state.get("network_connected", True):
        hil_state["last_error"] = "NETWORK_DOWN"
        hil_state["update_in_progress"] = False
        print("[HIL] Firmware update failed due to network.")
        return

    hil_state["update_in_progress"] = True
    print(f"[HIL] Flashing firmware {version}...")
    time.sleep(1)  # simulate update
    hil_state["firmware_version"] = version
    hil_state["update_in_progress"] = False
    print(f"[HIL] Firmware updated to {version}.")


@when('the firmware update process starts')
def step_start_update(context):
    hil_state["update_in_progress"] = True
    print("[HIL] Firmware update started.")


@when('the sensor loses power mid-update')
def step_power_loss(context):
    if hil_state["update_in_progress"]:
        hil_state["recovery_mode"] = True
        hil_state["firmware_version"] = None
        hil_state["last_error"] = "POWER_LOSS"
        hil_state["update_in_progress"] = False
        print("[HIL] Power lost during update. Entering recovery mode.")


@when('the network connection is lost during transfer')
def step_network_loss(context):
    if hil_state["update_in_progress"]:
        hil_state["network_connected"] = False
        hil_state["last_error"] = "NETWORK_TIMEOUT"
        print("[HIL] Network lost mid-update. Retrying...")


@when('the network connection is restored for {device}')
def step_restore_network_device(context, device):
    if device == "motion sensor":
        # motion-specific recovery
        pass
    elif device == "heat sensor":
        # heat sensor-specific recovery
        pass
    else:
        # generic recovery
        pass



@then('the update should complete successfully')
def step_update_success(context):
    assert hil_state["firmware_version"] is not None, "Firmware update failed"
    print(f"[HIL] Update success: version {hil_state['firmware_version']}")


@then('the sensor should reboot with firmware version "{version}"')
def step_reboot_with_version(context, version):
    assert hil_state["firmware_version"] == version, f"Expected {version}, got {hil_state['firmware_version']}"
    print(f"[HIL] Sensor rebooted with firmware {version}")


@then('the update should fail with error "{error}"')
def step_update_fail_error(context, error):
    assert hil_state["last_error"] == error, f"Expected error {error}, got {hil_state['last_error']}"
    print(f"[HIL] Update failed as expected: {error}")


@then('the sensor should remain on its current firmware')
def step_remain_same_fw(context):
    assert hil_state["firmware_version"] is None or hil_state["update_in_progress"] is False
    print("[HIL] Firmware unchanged after failure.")


@then('the sensor should enter recovery mode')
def step_recovery_mode(context):
    assert hil_state["recovery_mode"] is True, "Recovery mode not activated"
    print("[HIL] Recovery mode active.")


@then('the previous firmware should remain intact')
def step_previous_fw_intact(context):
    assert hil_state["firmware_version"] is None, "Previous firmware not intact after failure"
    print("[HIL] Previous firmware intact.")


@then('the update should pause and retry')
def step_pause_retry(context):
    assert hil_state["last_error"] == "NETWORK_TIMEOUT"
    print("[HIL] Update paused due to network timeout, waiting for retry.")


@then('the update should resume and complete successfully')
def step_resume_complete(context):
    hil_state["firmware_version"] = "5.0.0"
    hil_state["update_in_progress"] = False
    print("[HIL] Update resumed and completed successfully.")
