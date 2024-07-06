from core.models import Review, Profile
import math

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great-circle distance between two points 
    on the Earth's surface given their longitude and latitude in decimal degrees.
    """
    lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])
    
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a)) 
    r = 6371 
    return c * r

def get_recommended_reviews(user):
    if not user.profile.latitude or not user.profile.longitude:
        return []

    # Get user's location
    user_lat = float(user.profile.latitude)
    user_lon = float(user.profile.longitude)
    
    # Get all reviews
    reviews = Review.objects.all()
    
    # Calculate the distance and followers score for each review
    recommended_reviews = []
    for review in reviews:
        restaurant = review.restaurant
        distance = haversine(user_lon, user_lat, float(restaurant.longitude), float(restaurant.latitude))
        followers_count = review.user.profile.followed_by.count()
        score = followers_count - distance  # you can adjust this formula as needed
        recommended_reviews.append((review, score))
    
    # Sort reviews by score
    recommended_reviews.sort(key=lambda x: x[1], reverse=True)
    
    # Return the sorted reviews, just return the review part
    return [review for review, score in recommended_reviews]
