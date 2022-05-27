import requests
import json
# import related models here
from .models import CarDealer
from requests.auth import HTTPBasicAuth


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data




# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)


# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        #dealers = json_result["rows"]
        dealers = json_result["body"]#["rows"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results

# def get_dealer_by_id(url, **kwargs):
    
#     # Call get_request with a URL parameter
#     json_result = get_request(url, id=id)
#     dealers = json_result["entries"][0]
#     dealer_obj = CarDealer(address=dealer["address"], city=dealer["city"], full_name=dealer["full_name"],
#                                 id=dealer["id"], lat=dealer["lat"], long=dealer["long"],
#                                 short_name=dealer["short_name"],
#                                 st=dealer["st"], zip=dealer["zip"])
#     return dealer_obj





#test
def get_dealer_by_id(url, id):
    
    # Call get_request with a URL parameter
    json_result = get_request(url, id=id)
    dealers = json_result["entries"][0]
    dealer_obj = CarDealer(address=dealer["address"], city=dealer["city"], full_name=dealer["full_name"],
                                id=dealer["id"], lat=dealer["lat"], long=dealer["long"],
                                short_name=dealer["short_name"],
                                st=dealer["st"], zip=dealer["zip"])
    return dealer_obj

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
def get_dealers_by_state(url, state):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, state=state)
    dealers = json_result["body"]["docs"]
    # For each dealer in the response
    for dealer in dealers:
        # Create a CarDealer object with values in `doc` object
        dealer_obj = CarDealer(address=dealer["address"], city=dealer["city"], full_name=dealer["full_name"],
                               id=dealer["id"], lat=dealer["lat"], long=dealer["long"],
                               short_name=dealer["short_name"],
                               st=dealer["st"], state=dealer["state"], zip=dealer["zip"])
        results.append(dealer_obj)

    return results


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





# def get_dealer_reviews_from_cf(url, **kwargs):
def get_dealer_reviews_from_cf(url, id):
    results = []
    id = kwargs.get("id")
    if id:
        json_result = get_request(url, id=id)
    else:
        json_result = get_request(url)
    # print(json_result)
    if json_result:
        reviews = json_result["body"]["data"]["docs"]
        for dealer_review in reviews:
            review_obj = DealerReview(dealership=dealer_review["dealership"],
                                   name=dealer_review["name"],
                                   purchase=dealer_review["purchase"],
                                   review=dealer_review["review"])
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


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative



