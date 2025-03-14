# Status Page
One Move Chess Status Page

# Status Page

## Abstract

This GitHub repository contains the codebase for the status page for the One Move Chess Game. 


### Contributors

| Name                  | 
| --------------        | 
| Khizar Qureshi        | 
| Ntense Obono          |
| Catherine Bregou      |  
| Bryan Yang            | 
| Sam Lengyel           | 
| Angel Ortiz Martinez  | 



## Contents

- [Description](#description)
- [Folders Organization](#folders)
- [Instructions](#instructions)
- [Credits](#credits)
- [Required Packages](#Required-Packages)
- [Additional Requirements](#Addtional-Requirements)
- [Contact](#Contact)



## Description

The One Move Chess Status Page provides real-time updates on the game's performance and availability. This project was developed as part of our Computer Science Senior Thesis at Carleton College - Chaos Monkeys: Software Engineering at Scale.

## Required Packages
To launch this status page, ensure the following packages are installed: 
Flask - Web framework for building the status page 
Selenium - Automates web interactions to simulate Human-Computer Interaction
Pandas - Handles data processing
Requests - Sends HTTP requests
Fake UserAgent - Generates random user-agent headers
Undetected Chromedriver - Helps bypass bot detection in Chrome

## Additional Requirements
Make sure you have the correct version of ChromeDriver installed. You can find the appropriate version and installation instructions here: https://sites.google.com/chromium.org/driver/.

You also need to create a VM-Key.pem that contains the SSH key required to monitor the virtual machine that holds the One Move Chess Service. If interested, reach out to khizar.qur@gmail.com. 

At a minimum, it is recommended to change the email address at /status_page/notify.py
## Instructions
Step 1:

To run this app locally, run python3 /status_page/status.py

Step 2: 

A link will show up in the terminal and will look simmilar to http://127.0.0.1:5000/. Copy the url of that link to your browser.

Step 3: 

The status page should show the availability and readiness of the One Move Chess Service.

Step 4:

You can click on the Fault-Injector button to run the /status_page/fault_injection/fault_injector.py script. Clicking the fault-fixer button will allow you to run the /status_page/fault_injection/fault_fixer.py script. 

Note, that the status page will automatically update every 2 minutes. 
## Folders
Our frontend HTML, CSS, and JS files can be found in our main folder under templates and static directories. 

Our API can be found within the main status folder. 

The fault-fixer and fault injector can be found in our main folder under fault_injection

The selenium bots can be found under our main folder under automation.

## Credits
We would like to thank our thesis advisor Professor Tanya Amert for their support throughout this project. 

## Contact
If you have any questions about this GitHub repository or are interested in reaching out, please contact khizar.qur@gmail.com
