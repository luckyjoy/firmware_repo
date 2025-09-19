@all @firmware @hil @gas_sensor 
Feature: Gas sensor firmware update with Hardware-in-the-Loop (HIL)
  As a QA engineer
  I want to validate the firmware update process on the gas sensor
  Using Hardware-in-the-Loop (HIL) testing
  So that I can ensure safety-critical updates behave correctly
	
  @acceptance  @smoke
  Scenario: <REQ_FW_05> <REQ_FW_06> <REQ_FW_07> Successful gas sensor firmware update
    Given the gas sensor is connected to the HIL rig
    And the network connection to the update server is stable
    When a new firmware version "1.0.2.2" is flashed via HIL
    Then the update should complete successfully
    And the sensor should reboot with firmware version "1.0.2.2"

  @network 
  Scenario: <REQ_FW_08> <REQ_FW_09> <REQ_FW_10> <REQ_FW_11> Gas sensor loses network during firmware update
    Given the gas sensor is connected to the HIL rig
    And the network connection is active
    When the firmware update process starts
    And the network connection is lost during transfer
    Then the update should pause and retry
    When the network connection is restored for gas sensor
    Then the update should resume and complete successfully

  @safety @smoke
  Scenario: <REQ_FW_12> Firmware update blocked due to active gas alarm
    Given the gas sensor is connected to the HIL rig
    And the sensor has detected dangerous gas levels
    And the sensor has an active firmware version "1.0.2.1"
    When a new firmware version "1.0.2.2" is attempted
    Then the update should be blocked with error "ACTIVE_ALARM"
    And the current firmware should remain active
