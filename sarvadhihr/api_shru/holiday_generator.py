import frappe
import requests
from datetime import date, timedelta, datetime

API_KEY = "toPH57oQmCR7p9LFVJx5DJT21YvQ09vH"

def fetch_holidays_from_calendarific(year=2025, country_code="IN"):
    url = "https://calendarific.com/api/v2/holidays"
    
    params = {
        "api_key": API_KEY,
        "country": country_code,
        "year": year,
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        holidays = data.get("response", {}).get("holidays", [])
        
        return holidays
    except requests.exceptions.RequestException as e:
        frappe.log_error("Holiday Fetch Error", str(e))
        return []

def generate_weekends_and_holidays(year=2025, country_code="IN"):
    company = "Sarvadhi"  # Change to your actual company name
    holidays = fetch_holidays_from_calendarific(year, country_code)

    # Convert holiday list to a set for easy lookup
    holiday_dates = set()
    
    for holiday in holidays:
        holiday_date = holiday["date"]["iso"]
        formatted_date = datetime.fromisoformat(holiday_date).date().strftime("%Y-%m-%d")
        holiday_dates.add(formatted_date)

        # Save as public holiday
        existing_entry = frappe.db.exists("Weekend and Holiday List", {"date": formatted_date})
        if not existing_entry:
            frappe.get_doc({
                "doctype": "Weekend and Holiday List",
                "holiday_name": holiday.get("name", "Public Holiday"),
                "date": formatted_date,
                "is_public_holiday": 1,
                "company": company
            }).insert(ignore_permissions=True)

    # Generate weekends but avoid adding weekends that are already public holidays
    start_date = date(year, 1, 1)
    end_date = date(year, 12, 31)
    delta = timedelta(days=1)

    while start_date <= end_date:
        formatted_date = start_date.strftime("%Y-%m-%d")

        if start_date.weekday() == 5 and formatted_date not in holiday_dates:  # Saturday only if not a holiday
            existing_entry = frappe.db.exists("Weekend and Holiday List", {"date": formatted_date})
            if not existing_entry:
                frappe.get_doc({
                    "doctype": "Weekend and Holiday List",
                    "holiday_name": "Weekend",
                    "date": formatted_date,
                    "is_weekend": 1,
                    "company": company
                }).insert(ignore_permissions=True)

        start_date += delta

    frappe.db.commit()
    return "Weekends & Public Holidays updated successfully!"
