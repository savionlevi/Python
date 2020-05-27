# Created by slevi at 5/4/20
Feature: 6.1.1 Websites suite
  # We would like to validate client behavior with
  # a) navigation to IP, geolocation, and long url

  Scenario: Firefox navigation
    When Navigating to IP successfully
    Then browsing is successful

  Scenario: geo location verification
    When Navigating to geolocation checker
    Then country is as expected

  Scenario: navigation to long URL
    When navigating to long url
    Then page is shown as expected

  Scenario:
    When navigating to common web servers
    Then navigation is successful