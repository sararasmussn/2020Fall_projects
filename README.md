# Computer use at the public library

Sara Rasmussen (saralr2)  
IS 597PR FA 2020 

## Project summary

Using a Monte Carlo simulation, I investigate the use of free public computers at a large public library. The closure of public libraries in response to the COVID-19 pandemic cast a bright spotlight on digital inequality in the United States. Since the late 1990s, public libraries have provided computers for the community to use for activities from writing and printing documents, online shopping, completing schoolwork, job seeking and applying for social services. There are many people in the United States without reliable access to either a device or broadband internet, for whom this is an essential service. As libraries reopen, enabling access to the computers is a top priority. 

At the same time, libraries face growing constraints to their budgets and regular calls for accountability and transparency in their spending. Policy-makers often presume that “everyone has a smartphone these days,” rendering such services as free computer terminals unnecessary. There is a real tension between service quality and cost. Libraries must strive to be as cost-effective as possible with their technology investments.   

Striking a balance between these two, this project simulates public library computer utilization to determine the optimal number of computers to make available at one library branch, relative to demand.

I use open data from Chicago Public Library and Seattle Public Library to help determine the business rules and inform the probability distributions for my simulation. One, from Chicago Public Library, provides the number of computer sessions at each of its branch location by month, for the last few years. Another, from the City of Chicago, provides the number of computers currently at each branch. Lastly, Seattle Public Library provides a history table of materials checked out, with their timestamp, across all locations. This table includes devices such as laptops and tablets.

## Fixed business rules
- Simulation scale: n days at one library branch
- Library operating hours 
- IT asset acquisition and maintenance costs

## Probabilistic variables
- Number of computers functioning and available per day
- Number of patrons per day and distribution of patrons per hour
- Computer use policy: Patrons can reserve a computer for 15 or 60 minutes
- Patron willingness to wait for an open computer: If there are more people than computers, each patron has a randomized length of time they are willing to wait

## Hypothesis
The fewer public computers a library offers, the lower the service cost -- and quality. The more public computers a library offers, the more sessions patrons will log and the higher the cost of the service, but eventually, the number of computers would exceed demand, decreasing utilization rates. Somewhere along this spectrum, there is an optimal computer “fleet” size for public libraries, which balances service quality and cost.

Cost measures:
- Device acquisition and maintenance 
- Device utilization rates

Service quality measures:
- Number of people who waited for a computer 
- How long patrons waited for a computer
- Number of people who departed because the wait was too long

## Findings
Please see sample_output/ for examples of the program's output. 

[Download presentation deck](https://github.com/sararasmussn/saralr2_2020Fall_project/blob/main/saralr2_IS597PR_presentation.pdf)

## Bibliography
Please see bibliography.md for citations and project data sources.

## Requirements
- python 3.7.3  
- numpy 1.16.4  
- matplotlib 3.1.0  
- pandas 0.24.2  
