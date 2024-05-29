# Case-Based-Reasoning-AI-system

For a given problem, a Case-Based Reasoning (CBR) AI system retrieves similar cases (corresponding to prior problems) stored in a database and adapts its solution according to the new circumstances. A Conversational Case-Based Reasoning (CCBR) AI system extends CBR when the full description of the problem statement is not available. CCBR interacts with the user to generate the problem description. It iteratively queries the user regarding features that are important to case retrieval. It also adapts the retrieved cases and generates explanation for the chosen cases. 

# Rent prediction CBR system

rent_prediction_CBR.py implements a Case-based Reasoning (CBR) AI system for apartment rent prediction. The rent_prediction_data.xlsx contains information extracted from an apartment rental site and describes apartments by city district, address, type of apartment (encoded as two digits, the number of bedrooms and the number of sitting rooms), the source of the listing, and the price.

The CBR system retrives similar cases using different features such as number of rooms, location, etc. It uses Euclidean distance (L2 norm) for calculating similar. The system also performs adaptation of retrieved cases before presenting it to the user. 

# Travel package prediction CCBR system

travel_package_prediction_CCBR.py implements a Conversational Case-based Reasoning (CCBR) AI system for travel package prediction. The CCBR system interacts with the user by posting queries to select the most similar travel package case stored in the database. It then adapts the retrieved cases before recommending them to the user. It also generates an explanation for presenting the recommended package.
