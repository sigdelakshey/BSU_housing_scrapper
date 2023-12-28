import time
import json
import smtplib
import requests
from bs4 import BeautifulSoup
from email.mime.text import MIMEText

email_sender = "xxxxxx@xxx.xxx"  # Sender's email address
email_password = "xxxxxxxxxx"  # Email 'App password'
email_recipient = "yyyyyyyyy@yyyyy.yyy"  # Recipient's email

# URL of the webpage
url = "https://www.boisestate.edu/housing-apartments/apartments-availability/"

# Function to scrape the table data
def scrape_table_data():
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find("table", class_="tablepress tablepress-id-14")
    
    # Extract data from each row
    data = []
    for row in table.find_all("tr"):
        cells = row.find_all("td")
        if len(cells) == 4:
            data.append({
                "community": cells[0].text.strip(),
                "apartment_type": cells[1].text.strip(),
                "date_available": cells[2].text.strip(),
                "status": cells[3].text.strip(),
            })
    return data

def send_email_notification(new_apartments):
    # Customize email content
    message_body = ""
    for apartment in new_apartments:
        message_body += f"["
        message_body += f"**Community:** {apartment['community']}\n"
        message_body += f"**Apartment Type:** {apartment['apartment_type']}\n"
        message_body += f"**Date Available:** {apartment['date_available']}\n"
        message_body += f"**Status:** {apartment['status']}\n"
        message_body += f"]\n"        
    message_body += f"\n"
    message_body += "**I am interested in leasing one of these apartments. Please let me know what steps I need to take to apply.**"

    message = MIMEText(message_body, "plain")

    # Set message parameters
    message["Subject"] = "Regarding Leasing Available Apartment at BSU Hosuing"
    message["From"] = email_sender
    message["To"] = email_recipient

    # Send email using SMTP
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(email_sender, email_password)
        server.sendmail(email_sender, email_recipient, message.as_string())

    print(f"Email notification sent for new apartments.")

def main():
    # Initial run: scrape data and save
    #current_data = scrape_table_data()
    current_data = [{"community": "Available", "apartment_type": " Available", "date_available": " Available", "status": "Available"}]
    try:
        with open("apartment_data.json", "r") as f:
            previous_data = json.load(f)
    except FileNotFoundError:
        previous_data = None

    with open("apartment_data.json", "w") as f:
        json.dump(current_data, f)

    # Check for changes and notify
    if previous_data and current_data != previous_data:
        new_apartments = [apartment for apartment in current_data if apartment not in previous_data]
        if new_apartments:
            send_email_notification(new_apartments)
    # Wait for a certain interval before checking again
    time.sleep(60 * 0.2)  # adjust as needed


if __name__ == "__main__":
    while True:
        try:
            main()
        except Exception as e:
            print(f"Error occurred: {e}")  # Log the error
            time.sleep(60 * 0.35)





