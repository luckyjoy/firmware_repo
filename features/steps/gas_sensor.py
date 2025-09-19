# Specific gas sensor steps (can extend hil_common if needed)
from behave import given

@given('the gas sensor has baseline firmware "{version}"')
def step_gas_fw_baseline(context, version):
    context.gas_fw_version = version
    print(f"[GAS] Baseline firmware: {version}")
