import frappe
 

def get_context(context):
 context.full_width = True
 return context

@frappe.whitelist()
def get_announcements(channel=None, page=1, limit=5):
    """
    Function to fetch announcements based on filters such as channel, pagination (page and limit), 
    and additional details like reactions, attachments, and user images.

    Parameters:
    - channel (str): Optional filter for announcement type/category.
    - page (int): Page number for pagination.
    - limit (int): Number of announcements to fetch per page.

    Returns:
    - dict: A dictionary containing announcements, total count, and pagination info.
    """
    filters = {"published": 1}
    if channel:
        filters["type_of_announcement"] = channel
 
    try:
        start = (int(page) - 1) * int(limit)
 
        announcements = frappe.get_all(
            "Announcements",
            fields=["name", "announcement_name", "description", "created_by", "creation"],
            filters=filters,
            order_by="creation desc",
            start=start,
            page_length=int(limit)
        )
 
        total_count = frappe.db.count("Announcements", filters=filters)
 
        for announcement in announcements:
            reactions = frappe.get_all(
                "Announcement Reactions",
                filters={"parent": announcement["name"]},
                fields=["user", "reaction"]
            )
            announcement["reactions"] = reactions
 
            attachments = frappe.get_all(
                "File",
                filters={
                    "attached_to_doctype": "Announcements",
                    "attached_to_name": announcement["name"]
                },
                fields=["file_url", "file_name"]
            )
            announcement["attachments"] = [
                {"url": a.file_url, "name": a.file_name} for a in attachments
            ]
 
            email = frappe.get_value("User", {"username": announcement["created_by"]}, "name")
            user_image = frappe.db.get_value("User", email, "user_image") if email else None
            announcement["user_image"] = user_image or "/assets/sarvadhi_it_hrms/images/default_user.png"
 
            if announcement.get("creation"):
                announcement["creation"] = announcement["creation"].isoformat()
 
        return {
            "message": announcements,
            "total_count": total_count,
            "page": int(page),
            "limit": int(limit)
        }
 
    except Exception as e:
        frappe.log_error(messgae=frappe.get_traceback(), title="Error in get_announcements")
        return {"error": "Failed to fetch announcements."}
 
 
@frappe.whitelist()
def get_discussion_channels():
    """
    Function to fetch the discussion channels available to a user.

    This function retrieves the channels that the current user is a member of by querying the 
    'Discussion Channel' doctype and filtering it based on the user's membership in the 
    'Discussion Members' table.

    Returns:
    - list: A list of dictionaries, each representing a discussion channel with fields:
      - "name": The unique identifier of the channel.
      - "channel_name": The name of the channel.
    - dict: In case of an error, a dictionary with an error message.
    """
    try:
        user = frappe.session.user
        return frappe.get_all(
            "Discussion Channel",
            fields=["name", "channel_name"],
            filters=[["Discussion Members", "user", "=", user]],
            distinct=True
        )
    except Exception:
        frappe.log_error(message=frappe.get_traceback(), title="Error in fetch_channels")
        return {"error": "An error occurred while fetching channels."}
 
 
@frappe.whitelist()
def update_reaction(post_id=None, emoji=None):
    """
    Updates the reaction of a user on a specific post (announcement).
    
    Args:
        post_id (str): The ID of the post (announcement) being reacted to.
        emoji (str): The emoji representing the user's reaction.
    
    Returns:
        dict: A dictionary containing the status of the update, 
              or an error message if the update fails.
    
    Raises:
        frappe.exceptions.ValidationError: If the post_id is not provided.
    """
    data = frappe.form_dict
    post_id = data.get("post_id") or post_id
    emoji = data.get("emoji") or emoji
 
    if not post_id:
        frappe.throw("Post ID is required")
 
    try:
        user = frappe.session.user
        announcement = frappe.get_doc("Announcements", post_id)
 
        existing_reaction = next(
            (r for r in announcement.reactions if r.user == user), None
        )
 
        if existing_reaction:
            existing_reaction.reaction = emoji
        else:
            announcement.append("reactions", {"user": user, "reaction": emoji})
 
        announcement.save()
        frappe.db.commit()
        return {"status": "success"}
 
    except Exception:
        frappe.log_error(message=frappe.get_traceback(),title= "Error in update_reaction")
        return {"error": "Failed to update reaction."}
    
    
    
    
    