import random

def match_users_to_circles(waiting_users, circle_size=4):
    """
    Simple matching: Group users by grief_type first, then by time_frame
    Returns list of circles (each circle is a list of user IDs)
    """
    # Group by grief type
    grief_groups = {}
    for user in waiting_users:
        user_id, session_id, grief_type, time_frame, need, circle_id, created_at = user
        if grief_type not in grief_groups:
            grief_groups[grief_type] = []
        grief_groups[grief_type].append(user)
    
    # Create circles
    circles = []
    circle_id_counter = 1
    
    for grief_type, users in grief_groups.items():
        # Shuffle for variety
        random.shuffle(users)
        
        # Group into circles of circle_size
        for i in range(0, len(users), circle_size):
            circle_users = users[i:i + circle_size]
            if len(circle_users) >= 2:  # Need at least 2 people for a circle
                user_ids = [u[0] for u in circle_users]
                circles.append((circle_id_counter, user_ids))
                circle_id_counter += 1
    
    return circles