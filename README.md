# DU_Human_Trafficking

The primary purpose of the directionality dataset is to track the movement across borders of trafficked persons. As such, statements contained within the TIP Report narratives are only considered codeable if they contain two directionality points (origin, transit, destination). Internal trafficking is not recorded in this data, but is collected in the primary dataset. Similarly, statements that only contain one directionality point (e.g., Afghanistan is a source country for boys trafficked for the purpose of forced labor) are not coded, but this information is collected in the primary dataset. If data pertaining to other coded countries or regions are provided with directionality in the narrative, these data are also collected.

# Main Objective
  - Interactive Data Visualization Graph
  - Below link is the map that envision it to look similar to: 
   http://www.digitalattackmap.com/#anim=1&color=0&country=ALL&list=1&time=17629&view=map
   
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
