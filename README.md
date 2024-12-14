The report must effectively communicate what you did for your project in a way that lets a technical bystander reproduce your work. Include:
Software and hardware requirements
Links to any data sources
Motivation for your project
Explanation of what you accomplished
How you measured your success (or failure)


Software and hardware requirements
We used Python 3 through VSCode and Github 
Data Source
https://www.kaggle.com/datasets/dilwong/flightprices
The data we chose was a CSV file where each row is a purchasable ticket found on Expedia between 2022-04-16 and 2022-10-05, to/from the following airports: ATL, DFW, DEN, ORD, LAX, CLT, MIA, JFK, EWR, SFO, DTW, BOS, PHL, LGA, IAD, OAK. There were 27 columns of data but we cleaned the data to only contain the following: route (start and end destination), search date, flight date, and total fare. 
Libraries 
pandas → analyzing the data 
random →  to simulate price changes
datetime → for dates
json → for q-table loading/saving
os → to check path
References: 
We used the following pseudocode from the textbook to write the Q-Learning model: 

Motivation 
Our group all love to travel and explore different countries and states. In fact, all of us have gone or are currently on a study abroad program. While it is great, it can get pricey and we know algorithms for companies are meant to make them the most profit, meaning prices typically change. We wanted to create and implement an algorithm that tells the user if they should buy the flight or wait and hopefully save them money. 
Explanation of what you accomplished
1) Problem Setup
Found and cleaned data. This step required researching different datasets to find one that best fit our needs. We debated using a dataset that only included Indian routes as well as one from the U.S. government before landing on the kaggle dataset linked above. Once we had determined the right dataset to use, we had to clean the data of unnecessary columns such as if the route had multiple stops. It should be noted that cleaning this dataset for our uses has the potential to make our predictions less accurate.  The data is only from April to October, so that also had an impact on how we went abou this. 
As I said above, this algortihm’s goal is to minimize the total fare by deciding whether to "buy" or "wait." We carried this out by implementing a reinforcement learning problem. The user (agent) would learn from the environment (tickets over time). For reinforcement learning you need a clearly defined state, action and reward. This is how we defined it:
State: flight details such as 
Action: Buy - purchase plane tickets now ; Wait - postpone purchasing to be closer to the flight date
Reward: +10 if the historical data is cheaper in future, -10 if it would’ve been cheaper to buy earlier 
Parameters were defined (learning rate, discount factor, exploration rate, # of episodes
Trained agent 
Ran multiple training episodes to update the Q-Table so that the agent can learn the best strategies over time by using the Q-Learning pseudocode above.
Saved and Loaded Model
Insted of retraining everytime, we saved the Q-Table to allow for quick decision making and to enable the algorithm to learn from its past computations. 
Result 
User will input flight details (route and date) and will receive advice on whether to buy or wait
How you measured your success (or failure)
 We believe we hit the main points of what we proposed: using Q Learning to train an agent for sequential decision-making regarding flight buying. We were able to apply Q-Learning based on a simulated dynamic price environment, with randomness. I will say we fell short of the original hoping to incorporate holidays, economic factors, and availability. The model tends to fall towards waiting, so it could mean the model is not being trained properly. The simulating prices does oversimplify the problem a little, but it is hard when demand and competition play a big factor. There is also potential failure for missing data (like a missing fare for that day). This could make the model prone to hallucinations, especially because our “simulate_price_change” function returns a random fare change which is not based on the training data. Additional failures in refining the most optimal policy include the lack of logic to compare previous search days (we believe that our model only looks to the future without learning from the past (in the training data). The absence of holiday modeling and more realistic pricing data indicates room for future improvement, but we measured our success by having made a model that given data helps the user make a decision. 
Training data approaches:
We have trained the data using different approaches. Originally, there have been 82milion rows. We played around with different values for max_times in flight_project.py. We used values between 1000 and 10000, with then different values for sampling percentage which covers a certain percentage of the 82 million rows. The code would run between one to a few hours depending on the values. In the submission we have used the following values: max_times = 10000 and 10% sample which ended up covering and sampling 8.2 million rows out of 82 million. 

Testing and producing the output:
We created a execution file in which if a user gives a certain input (e.g., source, destination, fare, and dates), we estimate similar preferences (if not the same), from the given Q table that allow the user to find a flight that best matches their preferred flight preferences. This is done by using a threshold (in this test case 20%) to provide states that are within it, thus minimizing the available flights to just those that are most preferred by the user.
If the confidence score is below 40 then we recommend to wait, otherwise buy.
Input values: Any price. Any previously mentioned airports.



