from .models import Review, Profile
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
    r = 6371 #in km
    return c * r

def get_recommended_reviews(user):
    if not (user.profile.latitude and user.profile.longitude):
        return []

    user_lat = float(user.profile.latitude)
    user_lon = float(user.profile.longitude)

    reviews = Review.objects.all().exclude(user=user)
    recommended_reviews = []

    for review in reviews:
        restaurant = review.restaurant
        reviewer_profile = review.user.profile

        if not (reviewer_profile.latitude and reviewer_profile.longitude):
            continue

        distance = haversine(user_lon, user_lat, float(restaurant.longitude), float(restaurant.latitude))
        followers_count = reviewer_profile.followed_by.count()
        
        #  scoring function
        score = (followers_count) * (6-review.rating) / (distance + 1)
        
        recommended_reviews.append((review, score))

    # Sort reviews by score in descending order
    recommended_reviews.sort(key=lambda x: x[1], reverse=True)

    top_10_reviews = [review for review, score in recommended_reviews[:10]]
    return top_10_reviews