@all @firmware @hil
Feature: HIL-based recovery validation for firmware updates
  To ensure devices can recover from failed firmware updates
  Using Hardware-in-the-Loop (HIL) testing

  @recovery
  Scenario Outline: <REQ_FW_14> Sensor recovers after failed firmware update
    Given a <sensor_type> sensor is connected to the HIL bench
    And the firmware update process has started
    When the update fails due to <failure_cause>
    Then the sensor should boot into recovery mode
    And rollback to the previous firmware version

    Examples:
      | sensor_type | failure_cause    |
      | heat        | power_loss       |
      | heat        | corrupted_image  |
      | gas         | network_timeout  |
      | gas         | flash_error      |