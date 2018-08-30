# DU_Human_Trafficking

The primary purpose of the directionality dataset is to track the movement across borders of trafficked persons. As such, statements contained within the TIP Report narratives are only considered codeable if they contain two directionality points (origin, transit, destination). Internal trafficking is not recorded in this data, but is collected in the primary dataset. Similarly, statements that only contain one directionality point (e.g., Afghanistan is a source country for boys trafficked for the purpose of forced labor) are not coded, but this information is collected in the primary dataset. If data pertaining to other coded countries or regions are provided with directionality in the narrative, these data are also collected.


# Introduction

Human trafficking is defined as "the recruitment, harboring, transportation, provision, or obtaining of a person for labor or services, through the use of force, fraud, or coercion for the purpose of subjection to involuntary servitude, peonage, debt bondage, or slavery".

The most challenging aspect of addressing human trafficking is identifying the victims, which is problematic for several reasons. Victims may not perceive themselves as trafficked individuals. They may fear retaliation by the trafficker; lack knowledge of resources to help themselves; and face many cultural, social, and language barriers.

As a part of this project we are determined to make a interative data visualtion dashboard showing the inlfow an outflow of different type of human trafficking between source and destination.

To increase awareness of human trafficking, the HTC has created the Human Trafficking Flow Map, an online dashboard that displays some of the data from the Center's Human Trafficking Index (HTI) project. The dashboard is a tool that visualizes source and destination countries of trafficking victims as well as a profile and trafficking type, when known. The project aims to help policymakers, researchers, advocates, students, and the general public easily and interactively map and explore human trafficking flows between countries.

# Main Objective
The main objective of this Project are

- To create an Interactive data visualization Dashboard to show the inflow and outflow of different type of human trafficking from source to the destination over the countries.

- Graph/ Plot to show the overall statistic of different type of trafficking from the Year 2008 to 2016.

- Try to cluster the data using Kmean.

- Below link is the map that envision it to look similar to: 
   http://www.digitalattackmap.com/#anim=1&color=0&country=ALL&list=1&time=17629&view=map

- Final graph looks something like this

  ![alt text](https://github.com/rose0037/DU-Human-Trafficking/blob/master/new_pic.PNG)
 
# Information about uploaded notebooks and excel sheets.
  - Data_Cleaning.ipynb is the python notebook containing the code for cleaning Directionality Coding 2008-2016.xlsx and         creating source and destinations latitidues and longitudes columns.
  - Human_Traffic_data.csv is the excel sheet created after cleaning the data(created in Data_Cleaning.ipynb notebook)
  - Human Trafficking Bokeh.ipynb is the main file containg the graphs and interactive widgets.Data used from                   Human_Traffic_data.csv file
 
 # Table for tentative milestones:

<table>
<tr>
  <th>Weeks</th><th>Milestones</th><th>Status</th>
</tr>
<tr>
  <td>2nd week</td><td>Loading and cleaning of data</td><td>Completed</td>
</tr>
<tr>
<td>3rd week</td><td>Graph plots using source and destination nodes</td><td>Completed</td>
</tr>
<tr>
<td>4th week</td><td>Adding Years drop down</td><td>Completed</td>
</tr>
<tr>
<td>5th week</td><td>Adding interactive parameters</td><td>Completed/td>
</tr>
<tr>
<td>6th week</td><td>Adding tier Information</td><td>Completed</td>
</tr>
<tr>
<td>7th week</td><td>Merging all information</td><td> Completed</td>
</tr>
</table>
