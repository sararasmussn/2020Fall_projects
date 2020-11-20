# 2020Fall_project

Sara Rasmussen (saralr2)  
IS 594PR 

Project proposal:

Using a Monte Carlo simulation, I would like to investigate the use of free public computers at a large public library. The closure of public libraries in response to the COVID-19 pandemic cast a bright spotlight on digital inequality in the United States. Since the late 1990s, public libraries have provided computers for the community to use for activities from writing and printing documents, online shopping, completing schoolwork, job seeking and applying for social services. There are many people in the United States without reliable access to either a device or broadband internet, for whom this is an essential service. As libraries plan or begin to reopen, enabling access to the computers is a top priority. 

At the same time, libraries face growing constraints to their budgets and regular calls for accountability and transparency in their spending. Policy-makers often presume that “everyone has a smartphone these days,” rendering such services as free computer terminals unnecessary. There is a real tension between service quality and cost. Libraries must strive to be as cost-effective as possible with their technology investments.   

Striking a balance between these two, I propose a tool to simulate public library computer utilization and determine the optimal number of computers to make available at a library, relative to demand. (1) 

I intend to use three datasets, linked below, to help determine the business rules and inform the probability distributions for my simulation. One, from Chicago Public Library, provides the number of computer sessions at each location by month, for the last few years. Another, from the City of Chicago, provides the number of computers currently at each location. Lastly, Seattle Public Library provides a history table of materials checked out, with their timestamp, across all locations. This table includes devices such as computers and tablets.

Together, this information can help me determine what the demand for computers might look like by time of day, day of the week, and month of the year. 

Fixed business rules (a work in progress): 

- Open hours at the library. 
- Cost per device and annual maintenance cost of the fleet.
- Computer use policy: 
    - You can use a computer for either 15 minutes or 1 hour. 
    - After each computer use, there will be a 15-minute delay (where the computer is unavailable to be used) so that staff can sanitize the area per the library’s COVID-19 cleaning procedures.
- If there are more people than computers, and a patron has to wait for more than 30 minutes to use a computer, they’ll leave.

Variables (also a work in progress):

- Number of patrons who want to use the computer at a given time/day/month.
- Length of use selected by the patrons. 
- Number of computers that are out of service at any given moment. 

Hypothesis: The more computers you have in one location, the more people will use those computers, and the higher the overall cost of the service. However, there will be a tipping point where computers would exceed demand, decreasing utilization rates. I am interested in finding the “point of convergence” for the most cost-effective number of computers to maintain.

Data sources:

https://data.cityofchicago.org/browse?q=library%20computer&sortBy=relevance 
https://data.cityofchicago.org/Education/Connect-Chicago-Locations/bmus-hp7e/data
https://data.seattle.gov/Community/Checkouts-By-Title-Physical-Items-/5src-czff/data  

(1) Why simulate this, rather than conduct an analysis of historical trends? There is not enough open data available on this topic to do so. The data is patchy, and possibly not even collected, by some libraries. However, I hope the little data available can help enrich this simulation.





