E-waste modelling tool for Dss+. 
Tool accepts a number of user provided info. 
Enered data is posted to the Flask backend via an Ajax POST request. 
Data is retrieved and processed under the 'product_modelling' route. 
'Final_values' is computed and stored in a database session. 
A redirect is called to redirect to the route 'matrix_page'. 
final_values' is accessed and retrieved under the matrix page route for further processing.

