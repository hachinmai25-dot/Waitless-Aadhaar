from math import radians, cos, sin, sqrt, atan2

def haversine_distance(lat1, lon1, lat2, lon2):
    """Calculate distance in km between two coordinates."""
    R = 6371
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    return R * 2 * atan2(sqrt(a), sqrt(1-a))

def find_nearest_center(applicant_lat, applicant_lon, centers):
    """
    Given applicant coordinates and a list of center dicts,
    return top 3 nearest centers with available capacity.
    """
    available = [c for c in centers if c['current_load'] < c['capacity_per_day'] and c['is_active']]
    
    for center in available:
        center['distance_km'] = round(
            haversine_distance(applicant_lat, applicant_lon,
                               center['latitude'], center['longitude']), 2
        )
    
    sorted_centers = sorted(available, key=lambda x: x['distance_km'])
    return sorted_centers[:3]  # Return top 3 nearest
