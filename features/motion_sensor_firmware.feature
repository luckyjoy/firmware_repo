#motion_sensor_firmware.feature
@all @firmware @hil @motion_sensor
Feature: Motion Sensor Firmware Update with Hardware-in-the-Loop (HIL)
  As a user
  I want to validate the firmware update process
  So that I know my device is reliable

  @full_battery
  Scenario Outline: <REQ_FW_01> <REQ_FW_02> <REQ_FW_03> <REQ_FW_04> A new firmware update is successfully installed when sensor battery is not low.
    Given a motion sensor with UUID=<UUID> is connected to the network
    And The sensor battery level is not below the minimum threshold 30%
    And a new firmware version=<Current_Version> is available
    When the firmware update process was triggered
    Then the motion sensor's status indicates "updating"
    And the firmware version on the sensor is updated to the new version=<New_Version>
    And the motion sensor returns to its idle state
    And the motion sensor can detect motion as expected
    Examples:
      | UUID                                   | Current_Version | New_Version |
      | "b87fdc67-a78b-a56c-e4de-ba088bd94a1c" | "1.0.2.1"       | "1.1.0.0"   |
      | "b87fdc67-a78b-a56c-e4de-ba088bd94a1c" | "1.0.2.2"       | "1.1.0.0"   |
      | "378da358-0bab-1e5f-f6e5-ca06bd575da0" | "1.0.2.0"       | "1.1.0.0"   |
      | "378da358-0bab-1e5f-f6e5-ca06bd575da0" | "1.0.2.1"       | "1.1.0.0"   |


  @low_battery
  Scenario Outline: <REQ_FW_05> <REQ_FW_06> <REQ_FW_07> A new firmware update is not installed when sensor battery is low.
    Given a motion sensor with UUID=<UUID> is connected to the network
    And The sensor battery level is below the minimum threshold 30%
    And a new firmware version=<Current_Version> is available
    When the firmware update process was triggered
    Then the motion sensor's status indicates "denied"
    And a notification is sent to the user that the battery is too low to update
    And the sensor's firmware version=<Current_Version> remains the same.
    Examples:
      | UUID                                   | Current_Version | New_Version |
      | "b87fdc67-a78b-a56c-e4de-ba088bd94a1c" | "1.0.2.1"       | "1.1.0.0"   |
      | "b87fdc67-a78b-a56c-e4de-ba088bd94a1c" | "1.0.2.2"       | "1.1.0.0"   |
      | "378da358-0bab-1e5f-f6e5-ca06bd575da0" | "1.0.2.0"       | "1.1.0.0"   |
      | "378da358-0bab-1e5f-f6e5-ca06bd575da0" | "1.0.2.1"       | "1.1.0.0"   |


  @lost_connection
  Scenario Outline: <REQ_FW_08> <REQ_FW_09> <REQ_FW_10> <REQ_FW_11> The sensor loses connection during the firmware update
    Given a motion sensor with UUID=<UUID> is connected to the network
    And The sensor battery level is below the minimum threshold 30%
    And a new firmware version=<Current_Version> is available
    When the firmware update process was triggered
    And the network connection is lost
    And the network connection is restored for motion sensor
    Then the firmware update is paused or aborted
    And a notification is sent to the user indicating a lost connection
    And the sensor's firmware is not corrupted
    And the sensor is able to reconnect and retry the update once the network is restored
    Examples:
      | UUID                                   | Current_Version | New_Version |
      | "b87fdc67-a78b-a56c-e4de-ba088bd94a1c" | "1.0.2.1"       | "1.1.0.0"   |
      | "b87fdc67-a78b-a56c-e4de-ba088bd94a1c" | "1.0.2.2"       | "1.1.0.0"   |
      | "378da358-0bab-1e5f-f6e5-ca06bd575da0" | "1.0.2.0"       | "1.1.0.0"   |
      | "378da358-0bab-1e5f-f6e5-ca06bd575da0" | "1.0.2.1"       | "1.1.0.0"   |