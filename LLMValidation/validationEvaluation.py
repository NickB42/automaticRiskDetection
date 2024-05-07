import requests, json, os, time, csv, io

URL = "http://localhost:3000/api/"

def make_request(data, endpoint):
    headers = {
        "user":  "user1",
        "Content-Type": "text/plain"
    }

    try:
        response = requests.post(URL + endpoint,
                            headers=headers,
                            json=data)
    except Exception as err:
        print(err)
        return None

    text = response.text.strip('"')
    
    return answerToJson(text)

def answerToJson(text):
    reader = csv.DictReader(io.StringIO(text))
    json_data = json.dumps(list(reader))
    return json.loads(json_data)

def writeToFile(resultss):
    filename = "resultsEval.json"

    try:
        with open(filename, "a") as file:
            json.dump(resultss, file)

    except FileExistsError:
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        new_filename = f"{os.path.splitext(filename)[0]}_{timestamp}{os.path.splitext(filename)[1]}"
        with open(new_filename, "x") as file:
            json.dump(resultss, file)
            print(f"The file '{new_filename}' was created successfully.")
    else:
        print(f"The file '{filename}' was created successfully.")


if __name__ == "__main__":
    required_keys = {"risk_title", "risk_description","risk_impact","risk_likeliness"}

    body = '''risk_title,risk_description
Budget Overrun,There could be a risk of exceeding the allocated budget for the project. The project involves software licensing, hardware upgrades, consultancy services, staff training, and post-deployment support that might end up requiring more financial resources than initially planned, despite the contingency fund.
Vendor Reliability,There's a dependency on SAP and the SAP-certified consulting firm for successful implementation. In case these vendors do not deliver as expected in terms of quality, timelines, or support, the project could face delays, poor implementation, and additional costs.
Insufficient User Training,This risk can occur if the users within the different departments of the company are not adequately trained to use the SAP S/4HANA system. It can lead to a decrease in productivity, errors, and system under-utilization. It is especially significant as the successful migration not only involves the correct setup and functioning of the system, but also the system adoption by its users.
Data Loss During Migration,During system migration, there is a risk of data loss, which can cripple the company's operations and decision-making capabilities. This is due to potential compatibility issues, unanticipated software behavior and other unforeseen circumstances during migration. Any loss of data could deprive the company of crucial information necessary for business operations and decision making.
Project Timeline Delays, There's a risk that the project might not be completed within the scheduled 11 months. This could be due to unforeseen technical issues, restructuring of business processes, or vendor-related problems. Any delay can lead to an increase in project costs and strain on resources and might affect the expected benefits of transition.
Technical incompatabilities, During the system preparation and customization phase, technical compatibility issues may arise between the new SAP S/4HANA system and the existing IT infrastructure or other connected systems. These issues could disrupt the migration process, delay the project timeline and even add unforeseen labor and costs to the project.
Resistance To Change,Employees may resist switching from the current system to the new SAP S/4HANA system. Resistance can occur due to a lack of understanding, fear of job loss, or increased workload. This could slow down the adoption of the new system and negatively impact operational efficiency.
Data Security,In the process of migration, if proper security measures are not implemented, the system could be susceptible to security breaches. Unauthorized access or attacks could lead to data leakages, violating privacy regulations and potentially leading to hefty financial penalties and damage to the company's reputation.
Post-Implementation Support,Once the system is live, there may be technical glitches or user issues that need resolving. If the post-implementation support fails to address these concerns promptly and effectively, it could disrupt business processes, decrease user satisfaction, and affect overall adoption and productivity.
Regulatory risks,Operating in multiple countries, the company must ensure its IT systems, including the SAP S/4HANA, comply with the jurisdictional regulations of each country. Non-compliance risks could lead to penalties, legal issues, and potential damage to reputation. It's crucial to assess the compliance requirements early in the project.
'''

    for j in range(15):
        result = []
        for i in range(5): 
            print(f"Run {j+1}.{i+1} started!")
            res = make_request(body, "RiskPrompt/evaluateRisks")

            if len(res) != 10: continue

            quit = False
            for d in res:
                if not required_keys.issubset(d.keys()) or len(d.keys()) != 4: 
                    print("Risks in wrong format!")
                    quit = True
                    break
            if quit: continue
                    
            result = result +[[r["risk_title"], r["risk_impact"], r["risk_likeliness"]] for r in res]
            print("Risks successfully evaluated!")
        
        writeToFile(result)