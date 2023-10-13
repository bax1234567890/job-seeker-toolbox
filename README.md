# Job Seeker Toolbox



## Description

This project was created just for fun. We spend a lot of time each day in the routine of job hunting. The typical workflow involves manual tasks like searching for suitable job openings on various job boards, checking if we've applied for some of them previously, and ensuring none of the potential employers from these listings are on our 'do not apply/stop' list. So, all these boring tasks are automated by building a BDD framework from scratch.

## Prerequisites

- Gmail is mandatory.
- Set up a dedicated label in your Gmail account to organize confirmation emails received after applying to job boards.
- Generate a file named `gmail_credentials.json` by following the instructions provided in the guide at https://developers.google.com/gmail/api/quickstart/python. This file should be moved to the project root folder.
- Create an ODS spreadsheet file for maintaining and updating your 'do not apply/stop' list. The first column of this spreadsheet should be reserved for company names.

## Installation

1. Clone the project
2. Install Python and all requirements
3. Put `gmail_credentials.json` to the project root folder
4. Set up Gmail label name and paths to ODS and HTML files
5. Edit feature file as your need

## Usage example

```gherkin
Feature: Looking For a Job

  Background: Set variables
    Given The path to ODS file is C:\my_jobs\log.ods
    And The path to HTML file folder is C:\my_jobs\ready_to_apply\
    And The label for emails in Gmail is label:_applied

  Scenario: Find remote "Job of Dream" position on Indeed
    Given Indeed: Find "Job of Dream" in location "remote" within "any" miles for the last "3" days
    When Remove the positions that do not have "engineer" in the job title from the list of found on "Indeed"
    And Remove the positions that have "manager" in the job title from the list of found on "Indeed"
    And Gmail API: Remove the positions that have already been applied for from the list of found on "Indeed"
    And Docs API: Remove the positions that have been rejected from the list of found on "Indeed"
    Then Docs API: Create HTML file with the found positions on "Indeed"
    And Docs API: Open created HTML file in the browser
```



