# XACML-Puppetry of Drones

This repository supports the research paper titled  
**"Puppetry of Drones: A Case Study on Drone Fly-Over Policies Following FAA Regulations"**,  
submitted to CPS-Sec 2025.

## ✨ Overview

Modern Unmanned Aerial Vehicles (UAVs) operate in complex airspaces, requiring dynamic, policy-based access control. While the Federal Aviation Administration (FAA) issues regulations for drone usage, these are written for human interpretation and not readily machine-enforceable.

This project presents an XACML-based framework to automate FAA regulatory compliance checks, simulating access control decisions based on real-time drone attributes such as weight, kinetic energy, remote ID broadcast, purpose of operation, and more.

## 🛠️ Components

### 1. **XACML Policy Files**
- Define fine-grained, attribute-based rules aligned with FAA airspace and safety requirements.
- Structured using:
  - `<PolicySet>`, `<Policy>`, and `<Rule>` elements.
  - Contextual elements like `<Target>`, `<Condition>`, and `<Obligation>`.

### 2. **Request Generator**
- Written in Python.
- Accepts attributes like `weight`, `remote ID`, `commercial purpose`, etc.
- Generates XACML requests based on combinations of attributes (from Excel or manual input).

### 3. **PDP Engine Integration**
- Uses [AuthzForce PDP CLI](https://github.com/authzforce/core) to evaluate requests.
- Executes command-line evaluation using the configured `pdp-config.xml` file.

### 4. **Decision Logging**
- Evaluated results are parsed and logged in a structured CSV format.
- Enables post-analysis and decision auditing.

## 🧪 Use Case Simulation

We simulate scenarios where a drone attempts to fly over restricted zones. The PDP returns `Permit` or `Deny` decisions based on:
- Presence or absence of remote ID.
- Night Operations
- Kinetic energy and exposed rotating parts.
- Whether individuals have been informed.
- Purpose (recreational/commercial) and operational certifications.

## 💡 Research Contribution

- ✅ Translated FAA drone regulations into machine-readable XACML policies.
- ✅ Using the existing system and Developed a modular framework for real-time authorization decision simulation.
- ✅ Demonstrated potential for integrating policy-driven safety in UAV operations.

## 🔗 Folder Structure

```
📁 XACML-Puppetry_of_Drones/
├── policies/                # XACML policy and policy set files
├── requests/                # Sample XACML request files
├── scripts/
│   ├── request_generator.py # Python script for generating requests from Excel
│   └── run_pdp.xsd           # Script for PDP evaluation and logging
├── pdp-config.xml           # AuthzForce configuration
├── input_data.xlsx          # Excel with scenario data
└── README.md
```

## 📦 Requirements

- Python 3.7+
- Java 11 or above
- pandas
- AuthzForce PDP CLI (included or linked)

## 🚀 How to Run

1. **Install dependencies**:
   ```bash
   pip install pandas
   ```

2. **Prepare data**:  
   Fill `input_data.xlsx` with scenario attributes.( which is already in the repo)

3. **Run the evaluation**:
   ```bash
 ________________________________________
1. Clone the Repository
•	Command:
Use Git to clone the repository from GitHub: 
•	git clone https://github.com/authzforce/core.git
•	What it does:
This downloads the entire AuthzForce core source code (including the PDP engine) to your local machine.
________________________________________
2. Navigate to the Project Directory
•	Command: 
•	cd core
•	What it does:
You change your working directory to the project’s root, where the main pom.xml file is located.
________________________________________
3. Run Maven Install
•	Command: 
•	mvn clean install
•	What it does: 
o	clean: Deletes the previous build’s output (usually in the target/ folder).
o	install: Compiles the code, runs tests, packages the artifacts (JAR files), and installs them into your local Maven repository (typically located in your ~/.m2/repository folder).
During this process:
o	Maven downloads all required dependencies from remote repositories.
o	It executes unit tests to ensure the code works as expected.
o	It packages the project into JARs (or other artifacts) as defined in the pom.xml files.
o	The final artifacts are installed in your local repository so they can be used as dependencies in other projects.
________________________________________
4. Handling Build Failures
•	If the build fails: 
o	Check the error messages in the console output. They may indicate issues like missing dependencies, test failures, or configuration errors.
o	You can re-run Maven with additional logging for debugging: 
o	mvn clean install -X
o	Sometimes, skipping tests can help you focus on packaging: 
o	mvn clean install -DskipTests
________________________________________
5. Outcome
After a successful mvn clean install:
•	The project’s JAR files (such as the PDP engine JAR) will be generated and placed in their respective target/ folders.
•	They are also installed in your local Maven repository, meaning other Maven projects on your system can use them as dependencies.
________________________________________
Why Maven Install is Important for AuthzForce PDP Engine
For the AuthzForce PDP engine:
•	Building the Project:
Maven compiles the Java source code and packages it into executable JAR files. This is essential before you can run the PDP engine.
•	Running Tests:
Maven runs unit and integration tests to verify that the PDP engine works as expected.
•	Local Repository:
Once installed, you can reference AuthzForce artifacts in other projects if you plan to integrate the PDP engine with other systems.
•	Consistency:
Maven ensures that every build uses the same versions of dependencies, making your build reproducible across different environments.
________________________________________
Commands Recap
1.	Clone the repository: 
2.	git clone https://github.com/SafeFlyDrones/puppetryofdrones.git
3.	Navigate to the project directory: 
4.	cd gk
5.	cd core
8.	Build and install the project: 
9.	mvn clean install
10.	(Optional) Skip tests if necessary: 
11.	mvn clean install -DskipTests
12.	(Optional) Re-run with debug output for troubleshooting: 
13.	mvn clean install -X
This Maven process ensures your AuthzForce PDP engine and its components are built correctly, tested, and ready for integration or further use.

________________________________________
1. Overview of the Project
Objective:
You must write XACML policies that enforce FAA drone rules (like “Operation at night,” “Operations over human beings,” etc.) using XACML 3.0 combining algorithms. You are to use the AuthzForce PDP engine (available on GitHub) to evaluate these policies, and you can use a Python script to generate one or more policy files.
Components:
•	Policy Files:
These are the XACML XML documents that define your rules. In our example, we have:
o	Night-Operation.xml – a policy allowing operations at night.
o	Operations-Over-Humans.xml – a policy denying operations over human beings.
o	(Optionally, you could add a new policy like Remote-ID.xml if you have a rule for that.)
•	PDP Configuration (pdp-config.xml):
This file configures AuthzForce to load your policies (from the policies folder) and, if needed, specifies a root policy reference.
•	Sample Request Files:
These XACML request files (e.g., sample-request.xml, request_permit.xml, etc.) simulate various conditions (like different current times) to test your policies.
•	Python Script (generate_policies.py):
This script can be used to auto-generate one or more policy XML files based on parameters. It’s useful when you need to generate several policies programmatically or change parameters quickly.
•	AuthzForce PDP CLI:
The AuthzForce PDP engine (packaged as a JAR file) is used to load the PDP configuration and policies, evaluate incoming XACML requests, and output an XML response (e.g., Permit, Deny).
________________________________________
2. Directory Structure
Your project directory (inside the target folder) should look like this:
target/
├── authzforce-ce-core-pdp-cli-21.0.2-SNAPSHOT.jar
├── pdp.xsd                  <-- The XSD schema for PDP configuration
├── pdp-config.xml           <-- PDP configuration file
├── sample-request.xml       <-- A sample XACML request file
├── generate_policies.py     <-- Python script to generate policies
├── policies/                <-- Folder for XACML policy files
│    ├── Night-Operation.xml
│    └── Operations-Over-Humans.xml
└── requests/                <-- (Optional) Folder for request files
     └── sample-request.xml  <-- You can also store your request files here
________________________________________
3. File Details and Their Purposes
3.1 Policy Files
Night-Operation.xml
This policy defines rules for permitting drone operations at night (based on the current time).
Key points:
•	It uses the XACML 3.0 combining algorithm for permit overrides.
•	It has a <Target> element (required even if empty).
•	The <Condition> uses the functions time-greater-than-or-equal and time-less-than-or-equal wrapped by time-one-and-only to ensure a single time value is compared.
•	A default deny rule is included to ensure that if the conditions aren’t met, access is denied.
Example file content: (See the file provided earlier.)
Operations-Over-Humans.xml
This policy denies drone operations over human beings.
Key points:
•	Uses a deny-overrides combining algorithm.
•	Contains a <Target> element.
•	Its condition uses the string-equal function together with string-one-and-only to compare an attribute value.
•	A default deny rule is also provided.
Example file content: (See the file provided earlier.)
Remote-ID.xml (Optional New Policy)
If you have a rule that mandates drones broadcast a Remote ID, you can write a policy like this.
Key points:
•	It defines a rule to check that a specific attribute (e.g., drone:remote-id) equals “present.”
•	A default deny rule is also included.
Example file content: (Provided in an earlier answer if needed.)
________________________________________
3.2 PDP Configuration (pdp-config.xml)
This file configures the AuthzForce PDP engine.
Key points:
•	It specifies the static policy provider and points to your policies folder.
•	It includes a <rootPolicyRef> element so that the PDP knows which policy to use as the default for evaluation.
•	Use absolute hierarchical URIs for file paths on Windows.
Example file content:
<pdp xmlns="http://authzforce.github.io/core/xmlns/pdp/8"
     xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
     xsi:schemaLocation="http://authzforce.github.io/core/xmlns/pdp/8 file:///C:/Users/17372/Desktop/gk/core/pdp-cli/target/pdp.xsd"
     version="8.1">

    <policyProvider id="staticPolicyProvider" xsi:type="StaticPolicyProvider">
        <policyLocation>file:///C:/Users/17372/Desktop/gk/core/pdp-cli/target/policies/*.xml</policyLocation>
    </policyProvider>

    <rootPolicyRef>Night-Operation-Policy</rootPolicyRef>
</pdp>
________________________________________
3.3 Sample Request File (sample-request.xml)
This file simulates an XACML request. For example, if the current time is 22:00:00 (10:00 PM), your Night-Operation policy should return "Permit."
Example file content:
<?xml version="1.0" encoding="UTF-8"?>
<Request xmlns="urn:oasis:names:tc:xacml:3.0:core:schema:wd-17"
         ReturnPolicyIdList="false"
         CombinedDecision="false">
    <Attributes Category="urn:oasis:names:tc:xacml:3.0:attribute-category:environment">
        <Attribute AttributeId="urn:oasis:names:tc:xacml:1.0:environment:current-time" IncludeInResult="false">
            <AttributeValue DataType="http://www.w3.org/2001/XMLSchema#time">22:00:00</AttributeValue>
        </Attribute>
    </Attributes>
</Request>
________________________________________
3.4 Python Script (generate_policies.py)
This script auto generates one or more policy XML files (in our case, all the FAA policies in the policies folder). It’s useful if you want to quickly update parameters or generate multiple policies programmatically.
Why run it initially?
•	It helps ensure that your policies follow a consistent structure and format.
•	It saves time if you have many similar policies or need to update values dynamically.

________________________________________
4. Running the Project Step by Step
Step 1: Build and Set Up Puppetry of drones Engine
•	Clone and build the PDP engine from GitHub. https://github.com/SafeFlyDrones/puppetryofdrones.git
•	Ensure you have the authzforce-ce-core-pdp-cli-21.0.2-SNAPSHOT.jar in your target directory.
•	Make sure the schema file pdp.xsd,target is also present.
Step 2:check for  Generate Policies
•	Open a command prompt in the target directory.
•	Run the Python script: 
•	python generate_policies.py
This updates) the .xml files in the policies folder.
Step 3: Place Policy Files
•	Ensure your policies folder contains: 
o	All the policyxml. files
o	Operations-Over-Humans.xml (manually created or provided)
o	(Optional) Additional policy files such as Remote-ID.xml
Step 4: Create and/or Update the PDP Configuration
•	In pdp-config.xml, set the policy provider’s location and optionally a root policy reference. (See above for content.)
Step 5: check Request Files
•	Check all the XACML request file(s) (e.g., sample-request.xml) with different test cases. which is already present

Step 6: Run the PDP Engine
•	In the command prompt (in the target folder), run: 
•	java -jar authzforce-ce-core-pdp-cli-21.0.2-SNAPSHOT.jar -t XACML_XML pdp-config.xml sample-request.xml and then run  generate_policies.py using python command

•	This is just to make the PDP engine load your configuration and policies,Once done now run the python file with command: python generate_policies.py 
  This evaluates the request and returns a decision.
Step 7: Test Different Scenarios
•	Modify your request file(s) to simulate different conditions (e.g., change the current time or add/remove attributes) and re-run the PDP engine command: 
•	java -jar authzforce-ce-core-pdp-cli-21.0.2-SNAPSHOT.jar -t XACML_XML pdp-config.xml requests/your_modified_request.xml
•	Observe how the decision (Permit, Deny) changes.
________________________________________
5. Summary
•	AuthzForce PDP Engine uses your XACML policies (written in XML) to evaluate access requests.
•	Policies are defined in files (e.g., FAA ,Operation-Over Humans Night-Operation.xml) and combined using XACML 3.0 algorithms (like permit-overrides and deny- 
  overrides).
•	pdp-config.xml tells the engine where to load policies from and which policy to use as the root.
•	Python Script (generate_policies.py) is used to generate or update policy files automatically.
•	Request Files simulate various conditions; running the PDP engine with these requests shows the decision output.
   

4. **View output**:  
   Results will be visible in console.
   sample output :
   
Scenario 1:
Input: {'weight': 0.5, 'exposed_parts': 'absent', 'kinetic_energy': 10, 'remote_id': 'broadcasting', 'area_controlled': 'not-controlled', 'individuals_informed': 'informed', 'commercial_purpose': 'yes', 'bvlos_certification': 'approved'}
Decision: Permit

Scenario 2:
Input: {'weight': 0.6, 'exposed_parts': 'absent', 'kinetic_energy': 9, 'remote_id': 'broadcasting', 'area_controlled': 'not-controlled', 'individuals_informed': 'informed', 'commercial_purpose': 'yes', 'bvlos_certification': 'approved'}
Decision: Deny

Scenario 3:
Input: {'weight': 0.4, 'exposed_parts': 'present', 'kinetic_energy': 11, 'remote_id': 'broadcasting', 'area_controlled': 'controlled', 'individuals_informed': 'not-informed', 'commercial_purpose': 'no', 'bvlos_certification': 'approved'}
Decision: Deny

Scenario 4:
Input: {'weight': 0.7, 'exposed_parts': 'present', 'kinetic_energy': 10, 'remote_id': 'broadcasting', 'area_controlled': 'not-controlled', 'individuals_informed': 'not-informed', 'commercial_purpose': 'no', 'bvlos_certification': 'not-approved'}
Decision: Deny

Scenario 5:
Input: {'weight': 0.8, 'exposed_parts': 'absent', 'kinetic_energy': 12, 'remote_id': 'broadcasting', 'area_controlled': 'controlled', 'individuals_informed': 'informed', 'commercial_purpose': 'yes', 'bvlos_certification': 'not-approved'}
Decision: Deny

Scenario 6:
Input: {'weight': 0.3, 'exposed_parts': 'absent', 'kinetic_energy': 9, 'remote_id': 'not-broadcasting', 'area_controlled': 'not-controlled', 'individuals_informed': 'not-informed', 'commercial_purpose': 'yes', 'bvlos_certification': 'not-approved'}
Decision: Deny

Scenario 7:
Input: {'weight': 0.56, 'exposed_parts': 'present', 'kinetic_energy': 9, 'remote_id': 'broadcasting', 'area_controlled': 'controlled', 'individuals_informed': 'informed', 'commercial_purpose': 'yes', 'bvlos_certification': 'approved'}
Decision: Deny
   

## 🧭 Future Work

- Extend support to NLP-driven policy extraction from raw FAA documents.
- Integrate a user interface for real-time access decision visualization.
- Explore drone-to-edge computing PDP communication for field use.

## 📜 License

This project is for academic and research purposes. Please cite our paper if you use or build on this work.
