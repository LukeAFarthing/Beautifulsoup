import requests
from bs4 import BeautifulSoup
from flask import Flask
from flask import render_template
import json

app = Flask(__name__)
@app.route("/")
def displayJobDetails():
    
    response = requests.get('https://raw.githubusercontent.com/Nehalk145/pythonBeautifulSoup/main/jobDetails.json')
    #responseJSON = response.json()
    responseJSON = json.loads(response.text)
    return render_template('index.html',responseJSON = 
    responseJSON
)

#def displayJobDetails():
#    print("Display job details")

#function to get job list from url 'https://www.indeed.com/jobs?q={role}&l={location}'
def getJobList(role,location): 
    url = 'https://www.indeed.com/jobs?q={role}&l={location}'
    url = url.replace("{role}", role)
    url = url.replace("{location}", location)

    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    soup2 = soup.find_all('div',class_='job_seen_beacon')

    myArray = []
    
    for i in soup2:
        title = i.find('h2',class_='jobTitle').text
        name = i.find('span',class_='companyName').text
        description = i.find('div',class_='job-snippet').text.replace('\n', '')
        try:
            salary = i.find('div',class_='salary-snippet-container').text
        except:
            salary = 'NA'
        
        myJson = {
            "Title" : title,
            "CompanyName" : name,
            "Description" : description,
            "Salary" : salary
        }

        myArray.append(myJson)
    
    return myArray

#save data in JSON file
def saveDataInJSON(jobDetails):
    with open("jobDetails.json", "w") as outfile:
        json.dump(jobDetails, outfile)
    print("Saving data to JSON")


#main function
def main():
    print("Enter role you want to search")
    role = input()
    print("Enter the location you want to search")
    location = input()
    print("Role: " + role)
    print("Location: " + location)
    print(getJobList(role, location))
    job_details = getJobList(role, location)
    saveDataInJSON(job_details)
    
if __name__ == '__main__':
    main()
