Feature: Looking For a Job

  Background: Set variables
    Given The path to ODS file is C:\my_jobs\log.ods
    And The path to HTML file folder is C:\my_jobs\ready_to_apply\
    And The label for emails in Gmail is label:_applied

  Scenario: Verify if I have never applied for this position before
    When Looking for company "Employer of Dream"
    Then Gmail API: Verify if "company" should not exist in emails
    And Docs API: Verify if "company" should not exist in ODS file

  Scenario: Find remote "Job of Dream" position on Indeed
    Given Indeed: Find "Job of Dream" in location "remote" within "any" miles for the last "3" days
    When Remove the positions that do not have "engineer" in the job title from the list of found on "Indeed"
    And Remove the positions that have "manager" in the job title from the list of found on "Indeed"
    And Gmail API: Remove the positions that have already been applied for from the list of found on "Indeed"
    And Docs API: Remove the positions that have been rejected from the list of found on "Indeed"
    Then Docs API: Create HTML file with the found positions on "Indeed"
    And Docs API: Open created HTML file in the browser