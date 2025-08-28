# Specific heat sensor steps (can extend hil_common if needed)
from behave import given

@given('the heat sensor has baseline firmware "{version}"')
def step_heat_fw_baseline(context, version):
    context.heat_fw_version = version
    print(f"[HEAT] Baseline firmware: {version}")
