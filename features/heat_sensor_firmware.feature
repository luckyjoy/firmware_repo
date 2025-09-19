@all @firmware @hil @heat_sensor
Feature: Heat sensor firmware update with Hardware-in-the-Loop (HIL)
  As a QA engineer
  I want to validate the firmware update process on the heat sensor
  Using Hardware-in-the-Loop (HIL) testing
  So that I can ensure reliable upgrades under real hardware conditions

   @smoke
  Scenario: <REQ_FW_05> <REQ_FW_06> <REQ_FW_07> Successful firmware update on heat sensor with sufficient battery
    Given the heat sensor is connected to the HIL testbench
    And the sensor battery level is above 40%
    When a new firmware version "1.0.2.2" is flashed via HIL
    Then the update should complete successfully
    And the sensor should reboot with firmware version "1.0.2.2"

  @negative 
  Scenario: <REQ_FW_05> <REQ_FW_06> <REQ_FW_07> Heat sensor firmware update fails due to low battery
    Given the heat sensor is connected to the HIL testbench
    And the sensor battery level is below 15%
    When a new firmware version "1.0.2.2" is flashed via HIL
    Then the update should fail with error "LOW_BATTERY"
    And the sensor should remain on its current firmware

  @resilience  @smoke
  Scenario: <REQ_FW_13> <REQ_FW_14> Heat sensor loses power during firmware update
    Given the heat sensor is connected to the HIL testbench
    And the sensor battery level is above 50%
    When the firmware update process starts
    And the sensor loses power mid-update
    Then the sensor should enter recovery mode
    And the previous firmware should remain intact
