import requests
import json
# import related models here
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import Features,SentimentOptions
import time
####################################################################################################################################################

#upadate 28/5
# def get_request(url, api_key=False, **kwargs):
#     print(f"GET from {url}")
#     if api_key:
#         # Basic authentication GET
#         try:
#             response = requests.get(url, headers={'Content-Type': 'application/json'},
#                                     params=kwargs, auth=HTTPBasicAuth('apikey', api_key))
#         except:
#             print("An error occurred while GET request. ")
#     else:
#         # No authentication GET
#         try:
#             response = requests.get(url, headers={'Content-Type': 'application/json'},
#                                     params=kwargs)
#         except:
#             print("An error occurred while GET request. ")

#     status_code = response.status_code
#     print(f"Status {status_code}")
#     json_data = json.loads(response.text)

#     return json_data

#update 31/5###############################################################################################
def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        if "api_key" in kwargs:
            response = requests.get(url, params=kwargs, headers={'Content-Type': 'application/json'},
                                    auth=HTTPBasicAuth('apikey', kwargs['api_key']))
        else:            
            response = requests.get(url, params=kwargs, headers={'Content-Type': 'application/json'})
    except:
        print("An error occurred while GET request.")
    status_code = response.status_code
    print("Status {} ".format(status_code))
    json_data = json.loads(response.text)

    return json_data
#############################################################################################################



#working up to 28/5
# def get_request(url, **kwargs):    
#     # If argument contain API KEY
#     api_key = kwargs.get("api_key")
#     print("GET from {} ".format(url))
#     try:
#         if api_key:
#             params = dict()
#             params["text"] = kwargs["text"]
#             params["version"] = kwargs["version"]
#             params["features"] = kwargs["features"]
#             params["return_analyzed_text"] = kwargs["return_analyzed_text"]
#             response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
#         else:
#             # Call get method of requests library with URL and parameters
#             response = requests.get(url, headers={'Content-Type': 'application/json'},
#                                     params=kwargs)
#     except:
#         # If any error occurs
#         print("Network exception occurred")

#     status_code = response.status_code
#     print("With status {} ".format(status_code))
#     json_data = json.loads(response.text)
#     return json_data

####################################################################################################################################################################

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
#from the forum
# def post_request(url, payload, **kwargs):
#     print(kwargs)
#     print("POST to {} ".format(url))
#     print(payload)
#     response = requests.post(url, params=kwargs, json=payload)
#     status_code = response.status_code
#     print("With status {} ".format(status_code))
#     json_data = json.loads(response.text)
#     return json_data


# also from forum####################################################################################################################################################
def post_request(url, json_payload, **kwargs):
    json_data = json.dumps(json_payload, indent=4)
    print(f"{json_data}")
    try:
        # Call get method of requests library with URL and parameters
        response = requests.post(url, params=kwargs, json=json_data)
    except Exception as e:
        # If any error occurs
        print("Network exception occurred")
        print(f"Exception: {e}")
    print(f"With status {response.status_code}")
    print(f"Response: {response.text}")

######################################################################################################################################################################

# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
# def get_dealers_from_cf(url, **kwargs):
#     results = []
#     # Call get_request with a URL parameter
#     json_result = get_request(url)
#     if json_result:
#         # Get the row list in JSON as dealers
#         #dealers = json_result["rows"]
#         dealers = json_result["body"]#["rows"]
#         # For each dealer object
#         for dealer in dealers:
#             # Get its content in `doc` object
#             dealer_doc = dealer["doc"]
#             # Create a CarDealer object with values in `doc` object
#             dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
#                                    id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
#                                    short_name=dealer_doc["short_name"],
#                                    st=dealer_doc["st"], zip=dealer_doc["zip"])
#             results.append(dealer_obj)

#     return results

def get_dealers_from_cf(url, **kwargs):
    results = []
    state = kwargs.get("state")
    if state:
        json_result = get_request(url, state=state)
    else:
        json_result = get_request(url)
    # print(json_result)    
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["body"]#["rows"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer["doc"]
            # print(dealer_doc)
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)
    return results

#############################################################################################################################################################################




def get_dealer_by_id_from_cf(url, id):
    json_result = get_request(url, id=id)    
    if json_result:
        dealers = json_result["body"]            
        dealer_doc = dealers["docs"][0]
        dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"],
                                id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],                                
                                st=dealer_doc["st"], zip=dealer_doc["zip"])
    return dealer_obj

#test###################################################################
# def get_dealer_by_id(url, **kwargs):   
#     # Call get_request with a URL parameter
#     json_result = get_request(url, id=id)
#     dealers = json_result["entries"][0]
#     dealer_obj = CarDealer(address=dealer["address"], city=dealer["city"], full_name=dealer["full_name"],
#                                 id=dealer["id"], lat=dealer["lat"], long=dealer["long"],
#                                 short_name=dealer["short_name"],
#                                 st=dealer["st"], zip=dealer["zip"])
#     return dealer_obj


# def get_dealer_by_id(url, id):
    
#     # Call get_request with a URL parameter
#     json_result = get_request(url, id=id)
#     dealers = json_result["entries"][0]
#     dealer_obj = CarDealer(address=dealer["address"], city=dealer["city"], full_name=dealer["full_name"],
#                                 id=dealer["id"], lat=dealer["lat"], long=dealer["long"],
#                                 short_name=dealer["short_name"],
#                                 st=dealer["st"], zip=dealer["zip"])
#     return dealer_obj










#tests###############################################################################
# def get_dealers_by_state(url, **kwargs):
#     results = []
#     # Call get_request with a URL parameter
#     json_result = get_request(url, state=state)
#     if json_result:
#         # Get the row list in JSON as dealers
#         #dealers = json_result["rows"]
#         dealers = json_result["body"]#["rows"]
#         # For each dealer object
#         for dealer in dealers:
#             # Get its content in `doc` object
#             dealer_doc = dealer["doc"]
#             # Create a CarDealer object with values in `doc` object
#             dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
#                                    id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
#                                    short_name=dealer_doc["short_name"],
#                                    st=dealer_doc["st"], zip=dealer_doc["zip"])
#             results.append(dealer_obj)
#     return results

#test
# def get_dealers_by_state(url, state):
#     results = []
#     # Call get_request with a URL parameter
#     json_result = get_request(url, state=state)
#     dealers = json_result["body"]["docs"]
#     # For each dealer in the response
#     for dealer in dealers:
#         # Create a CarDealer object with values in `doc` object
#         dealer_obj = CarDealer(address=dealer["address"], city=dealer["city"], full_name=dealer["full_name"],
#                                id=dealer["id"], lat=dealer["lat"], long=dealer["long"],
#                                short_name=dealer["short_name"],
#                                st=dealer["st"], state=dealer["state"], zip=dealer["zip"])
#         results.append(dealer_obj)
#     return results


#####################################################################################################################################################################
def get_dealer_reviews_from_cf(url, **kwargs):
    results = []
    id = kwargs.get("id")
    if id:
        json_result = get_request(url, id=id)
    else:
        json_result = get_request(url)
    if json_result:
        reviews = json_result["body"]["data"]["docs"]
        for dealer_review in reviews:
            #dealer_review = reviews[0]           
            review_obj = DealerReview(dealership=dealer_review["dealership"],
                                   name=dealer_review["name"],
                                   purchase=dealer_review["purchase"],
                                   review=dealer_review["review"], 
                                   id=dealer_review["id"])
            if "id" in dealer_review:
                review_obj.id = dealer_review["id"]
            if "purchase_date" in dealer_review:
                review_obj.purchase_date = dealer_review["purchase_date"]
            if "car_make" in dealer_review:
                review_obj.car_make = dealer_review["car_make"]
            if "car_model" in dealer_review:
                review_obj.car_model = dealer_review["car_model"]
            if "car_year" in dealer_review:
                review_obj.car_year = dealer_review["car_year"]
            
            sentiment = analyze_review_sentiments(review_obj.review)
            print(sentiment)
            review_obj.sentiment = sentiment
            results.append(review_obj)

    return results

########################################################################################################################################################################


# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
# def get_dealer_reviews_from_cf(url, dealer_id):
#     results = []
#     # Perform a GET request with the specified dealer id
#     json_result = get_request(url, dealerId=dealer_id)

#     if json_result:
#         # Get all review data from the response
#         #reviews = json_result["body"]["data"]["docs"]
#         reviews = json_result["body"]["data"]["docs"]
#         # For every review in the response
#         for review in reviews:
#             # Create a DealerReview object from the data
#             # These values must be present
#             review_content = review["review"]
#             id = review["_id"]
#             name = review["name"]
#             purchase = review["purchase"]
#             dealership = review["dealership"]

#             try:
#                 # These values may be missing
#                 car_make = review["car_make"]
#                 car_model = review["car_model"]
#                 car_year = review["car_year"]
#                 purchase_date = review["purchase_date"]

#                 # Creating a review object
#                 review_obj = DealerReview(dealership=dealership, id=id, name=name, 
#                                           purchase=purchase, review=review_content, car_make=car_make, 
#                                           car_model=car_model, car_year=car_year, purchase_date=purchase_date
#                                           )

#             except KeyError:
#                 print("Something is missing from this review. Using default values.")
#                 # Creating a review object with some default values
#                 review_obj = DealerReview(
#                     dealership=dealership, id=id, name=name, purchase=purchase, review=review_content)

#             # Analysing the sentiment of the review object's review text and saving it to the object attribute "sentiment"
#             review_obj.sentiment = analyze_review_sentiments(review_obj.review)
#             print(f"sentiment: {review_obj.sentiment}")

#             # Saving the review object to the list of results
#             results.append(review_obj)

#     return results



####################################################################################################################################################################

# def get_dealer_reviews_from_cf(url, **kwargs):
# def get_dealer_reviews_from_cf(url, id):
#     results = []
#     id = kwargs.get("id")
#     if id:
#         json_result = get_request(url, id=id)
#     else:
#         json_result = get_request(url)
#     # print(json_result)
#     if json_result:
#         reviews = json_result["body"]["data"]["docs"]
#         for dealer_review in reviews:
#             review_obj = DealerReview(dealership=dealer_review["dealership"],
#                                    name=dealer_review["name"],
#                                    purchase=dealer_review["purchase"],
#                                    review=dealer_review["review"])
#             if "id" in dealer_review:
#                 review_obj.id = dealer_review["id"]
#             if "purchase_date" in dealer_review:
#                 review_obj.purchase_date = dealer_review["purchase_date"]
#             if "car_make" in dealer_review:
#                 review_obj.car_make = dealer_review["car_make"]
#             if "car_model" in dealer_review:
#                 review_obj.car_model = dealer_review["car_model"]
#             if "car_year" in dealer_review:
#                 review_obj.car_year = dealer_review["car_year"]
            
#             sentiment = analyze_review_sentiments(review_obj.review)
#             print(sentiment)
#             review_obj.sentiment = sentiment
#             results.append(review_obj)

#     return results


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative



####################################################
#FROM THE FORUM

 

def analyze_review_sentiments(text):
    url = "https://api.eu-gb.natural-language-understanding.watson.cloud.ibm.com/instances/237c022e-b459-4451-95a0-2565c33b3e1c"
    api_key = ""
    # api_key = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    authenticator = IAMAuthenticator(api_key)
    natural_language_understanding = NaturalLanguageUnderstandingV1(version='2021-08-01',authenticator=authenticator)
    natural_language_understanding.set_service_url(url)
    response = natural_language_understanding.analyze( text=text,features=Features(sentiment=SentimentOptions(targets=[text]))).get_result()
    label=json.dumps(response, indent=2)
    label = response['sentiment']['document']['label']
    return(label)


#update 31/05###########################################################################################################################################
# def analyze_review_sentiments(dealerreview, **kwargs):
#     url = "https://api.eu-gb.natural-language-understanding.watson.cloud.ibm.com/instances/237c022e-b459-4451-95a0-2565c33b3e1c"
#     api_key = ""
#     # api_key = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
#     authenticator = IAMAuthenticator(apikey)
#     natural_language_understanding = NaturalLanguageUnderstandingV1(version='2021-08-01', authenticator=authenticator)
#     natural_language_understanding.set_service_url(url)
#     response = natural_language_understanding.analyze(text=dealerreview,features=Features(sentiment=SentimentOptions())).get_result()
    
#     # - Get the returned sentiment label such as Positive or Negative
#     #print(json.dumps(response, indent=2))
#     print("setiment of review: ", response["sentiment"]["document"]["label"])
#     sentiment = response["sentiment"]["document"]["label"]
#     return sentiment
####################################################################################################################################



# def analyze_review_sentiments(review_text):
#     # Watson NLU configuration
#     try:
#         if os.environ['env_type'] == 'PRODUCTION':
#             url = os.environ['WATSON_NLU_URL']
#             api_key = os.environ["WATSON_NLU_API_KEY"]
#     except KeyError:
    #     url = config('WATSON_NLU_URL')
    #     api_key = config('WATSON_NLU_API_KEY')

    # version = '2021-08-01'
    # authenticator = IAMAuthenticator(api_key)
    # nlu = NaturalLanguageUnderstandingV1(
    #     version=version, authenticator=authenticator)
    # nlu.set_service_url(url)

    # # get sentiment of the review
    # try:
    #     response = nlu.analyze(text=review_text, features=Features(
    #         sentiment=SentimentOptions())).get_result()
    #     print(json.dumps(response))
    #     # sentiment_score = str(response["sentiment"]["document"]["score"])
    #     sentiment_label = response["sentiment"]["document"]["label"]
    # except:
    #     print("Review is too short for sentiment analysis. Assigning default sentiment value 'neutral' instead")
    #     sentiment_label = "neutral"

    # # print(sentiment_score)
    # print(sentiment_label)

    # return sentiment_label


####################################################################################################################################################################


#############################from the forum 
# import requests
# import json
# from .models import CarDealer, DealerReview
# from requests.auth import HTTPBasicAuth
# from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
# from ibm_watson import NaturalLanguageUnderstandingV1
# from ibm_watson.natural_language_understanding_v1 import Features,SentimentOptions
# import time
 

# def analyze_review_sentiments(text):
#     url = "https://api.eu-gb.natural-language-understanding.watson.cloud.ibm.com/instances/c8b0f019-31d6-41ac-b003-a2a31608839e"
#     api_key = "X2W_XG21E2BqmQ57cKeaX1rI9N43ZflG2KuaUmPJ_7wq"
#     authenticator = IAMAuthenticator(api_key)
#     natural_language_understanding = NaturalLanguageUnderstandingV1(version='2021-08-01',authenticator=authenticator)
#     natural_language_understanding.set_service_url(url)
#     response = natural_language_understanding.analyze( text=text+"hello hello hello",features=Features(sentiment=SentimentOptions(targets=[text+"hello hello hello"]))).get_result()
#     label=json.dumps(response, indent=2)
#     label = response['sentiment']['document']['label']
        
#     return(label)


#############################################################################################################################################################

# def get_dealers_from_cf(url, **kwargs):
#     results = []
#     state = kwargs.get("state")
#     if state:
#         json_result = get_request(url, state=state)
#     else:
#         json_result = get_request(url)
#     # print(json_result)    

#     if json_result:
#         # Get the row list in JSON as dealers
#         dealers = json_result["body"]["rows"]
#         # For each dealer object
#         for dealer in dealers:
#             # Get its content in `doc` object
#             dealer_doc = dealer["doc"]
#             # print(dealer_doc)
#             # Create a CarDealer object with values in `doc` object
#             dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"],
#                                    id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                
#                                    st=dealer_doc["st"], zip=dealer_doc["zip"])
#             results.append(dealer_obj)

#     return results


# def get_dealer_by_id_from_cf(url, id):
#     json_result = get_request(url, id=id)
    
#     if json_result:
#         dealers = json_result["body"]
        
    
#         dealer_doc = dealers["docs"][0]
#         dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"],
#                                 id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                
#                                 st=dealer_doc["st"], zip=dealer_doc["zip"])
#     return dealer_obj




##############################################################################################################################################################

# def get_dealer_reviews_from_cf(url, **kwargs):
#     results = []
#     id = kwargs.get("id")
#     if id:
#         json_result = get_request(url, id=id)
#     else:
#         json_result = get_request(url)

#     if json_result:
#         reviews = json_result["body"]["data"]

#         for dealer_review in reviews:
#             dealer_review = reviews["docs"][0]
            
#             review_obj = DealerReview(dealership=dealer_review["dealership"],
#                                    name=dealer_review["name"],
#                                    purchase=dealer_review["purchase"],
#                                    review=dealer_review["review"])
#             if "id" in dealer_review:
#                 review_obj.id = dealer_review["id"]
#             if "purchase_date" in dealer_review:
#                 review_obj.purchase_date = dealer_review["purchase_date"]
#             if "car_make" in dealer_review:
#                 review_obj.car_make = dealer_review["car_make"]
#             if "car_model" in dealer_review:
#                 review_obj.car_model = dealer_review["car_model"]
#             if "car_year" in dealer_review:
#                 review_obj.car_year = dealer_review["car_year"]
            
#             sentiment = analyze_review_sentiments(review_obj.review)
#             print(sentiment)
#             review_obj.sentiment = sentiment
#             results.append(review_obj)

#     return results



###############################################################################################################################################################

# def get_request(url, **kwargs):
    
#     # If argument contain API KEY
#     api_key = kwargs.get("api_key")
#     print("GET from {} ".format(url))
#     try:
#         if api_key:
#             params = dict()
#             params["text"] = kwargs["text"]
#             params["version"] = kwargs["version"]
#             params["features"] = kwargs["features"]
#             params["return_analyzed_text"] = kwargs["return_analyzed_text"]
#             response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
#         else:
#             # Call get method of requests library with URL and parameters
#             response = requests.get(url, headers={'Content-Type': 'application/json'},
#                                     params=kwargs)
#     except:
#         # If any error occurs
#         print("Network exception occurred")

#     status_code = response.status_code
#     print("With status {} ".format(status_code))
#     json_data = json.loads(response.text)
#     return json_data


#############################################################################################################################################################


# def post_request(url, payload, **kwargs):
#     print(kwargs)
#     print("POST to {} ".format(url))
#     print(payload)
#     response = requests.post(url, params=kwargs, json=payload)
#     status_code = response.status_code
#     print("With status {} ".format(status_code))
#     json_data = json.loads(response.text)
#     return json_data


#########ΠΡΟΣΟΧΗ ΣΤΟ dealerId##################################################################################################
def get_dealer_details_from_cf(url, dealerId):
    results = []
    json_result = get_request(url+dealerId)
    details = json_result["dealership"]
    for doc in details:
        results = CarDealer(
            address=doc["address"], city=doc["city"], full_name=doc["full_name"],
                                id=doc["id"], lat=doc["lat"], long=doc["long"],
                                short_name=doc["short_name"],
                                st=doc["st"], zip=doc["zip"])

    return results
#####################################################################################################################################





