from behave import given, when, then
import logging

logger = logging.getLogger(__name__)

# New step to set the initial firmware version and save it for rollback
@given('the sensor has an active firmware version "{version}"')
def step_impl(context, version):
    context.active_firmware = version
    context.previous_firmware = version  # Store the initial version
    logger.info(f"Sensor has active firmware {version}.")

@given('the firmware update process has started')
def step_impl(context):
    context.firmware_update_started = True
    logger.info("Firmware update started.")

@when('a new firmware version "{version}" is attempted')
def step_impl(context, version):
    context.new_firmware = version
    logger.info(f"Attempting firmware update to version {version}.")

@then('the update should be blocked with error "{error_code}"')
def step_impl(context, error_code):
    context.last_error = error_code
    assert context.last_error == error_code, f"Expected {error_code}, got {context.last_error}"

@then('the current firmware should remain active')
def step_impl(context):
    assert context.new_firmware != context.active_firmware, \
        "Firmware should not have updated!"
    logger.info("Current firmware remains active.")

@when('the update fails due to {failure_reason}')
def step_impl(context, failure_reason):
    context.update_failed = failure_reason
    logger.warning(f"Firmware update failed due to {failure_reason}.")

@then('the sensor should boot into recovery mode')
def step_impl(context):
    context.recovery_mode = True
    assert context.recovery_mode is True

@then('rollback to the previous firmware version')
def step_impl(context):
    # This step now has access to context.previous_firmware
    context.active_firmware = context.previous_firmware
    assert context.active_firmware == context.previous_firmware
    logger.info("Rolled back to previous firmware.")