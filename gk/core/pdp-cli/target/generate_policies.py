import os
import subprocess
import xml.etree.ElementTree as ET
import pandas as pd

# Path to the AuthzForce PDP CLI JAR file
PDP_CLI_JAR = "authzforce-ce-core-pdp-cli-21.0.2-SNAPSHOT.jar"
# Path to the PDP configuration file
PDP_CONFIG_FILE = "pdp-config.xml"
# Path to the Excel file containing input data
EXCEL_FILE = "input_data.xlsx"

def generate_xacml_request(
    weight=None, exposed_parts=None, kinetic_energy=None, remote_id=None,
    area_controlled=None, individuals_informed=None,
    commercial_purpose=None, bvlos_certification=None
):
    """
    Generates an XACML request XML string based on input parameters.
    """
    # Validate inputs
    if exposed_parts and exposed_parts not in ["present", "absent"]:
        raise ValueError("Invalid value for 'exposed_parts'. Must be 'present' or 'absent'.")
    if remote_id and remote_id not in ["broadcasting", "not-broadcasting"]:
        raise ValueError("Invalid value for 'remote_id'. Must be 'broadcasting' or 'not-broadcasting'.")
    if area_controlled and area_controlled not in ["controlled", "not-controlled"]:
        raise ValueError("Invalid value for 'area_controlled'. Must be 'controlled' or 'not-controlled'.")
    if individuals_informed and individuals_informed not in ["informed", "not-informed"]:
        raise ValueError("Invalid value for 'individuals_informed'. Must be 'informed' or 'not-informed'.")
    if commercial_purpose and commercial_purpose not in ["yes", "no"]:
        raise ValueError("Invalid value for 'commercial_purpose'. Must be 'yes' or 'no'.")
    if bvlos_certification and bvlos_certification not in ["approved", "not-approved"]:
        raise ValueError("Invalid value for 'bvlos_certification'. Must be 'approved' or 'not-approved'.")

    # Create the root Request element
    request = ET.Element("Request", {
        "xmlns": "urn:oasis:names:tc:xacml:3.0:core:schema:wd-17",
        "ReturnPolicyIdList": "false",
        "CombinedDecision": "false"
    })

    # Add resource Attributes
    resource_attributes = ET.SubElement(request, "Attributes", {"Category": "urn:oasis:names:tc:xacml:3.0:attribute-category:resource"})

    if weight is not None:
        attribute = ET.SubElement(resource_attributes, "Attribute", {"AttributeId": "urn:oasis:names:tc:xacml:1.0:resource:suas-weight", "IncludeInResult": "false"})
        value = ET.SubElement(attribute, "AttributeValue", {"DataType": "http://www.w3.org/2001/XMLSchema#double"})
        value.text = str(weight)

    if exposed_parts is not None:
        attribute = ET.SubElement(resource_attributes, "Attribute", {"AttributeId": "urn:oasis:names:tc:xacml:1.0:resource:exposed-parts", "IncludeInResult": "false"})
        value = ET.SubElement(attribute, "AttributeValue", {"DataType": "http://www.w3.org/2001/XMLSchema#string"})
        value.text = exposed_parts

    if kinetic_energy is not None:
        attribute = ET.SubElement(resource_attributes, "Attribute", {"AttributeId": "urn:oasis:names:tc:xacml:1.0:resource:kinetic-energy", "IncludeInResult": "false"})
        value = ET.SubElement(attribute, "AttributeValue", {"DataType": "http://www.w3.org/2001/XMLSchema#double"})
        value.text = str(kinetic_energy)

    if remote_id is not None:
        attribute = ET.SubElement(resource_attributes, "Attribute", {"AttributeId": "urn:oasis:names:tc:xacml:1.0:resource:remote-id", "IncludeInResult": "false"})
        value = ET.SubElement(attribute, "AttributeValue", {"DataType": "http://www.w3.org/2001/XMLSchema#string"})
        value.text = remote_id

    if commercial_purpose is not None:
        attribute = ET.SubElement(resource_attributes, "Attribute", {"AttributeId": "urn:oasis:names:tc:xacml:1.0:resource:commercial-purpose", "IncludeInResult": "false"})
        value = ET.SubElement(attribute, "AttributeValue", {"DataType": "http://www.w3.org/2001/XMLSchema#string"})
        value.text = commercial_purpose

    if bvlos_certification is not None:
        attribute = ET.SubElement(resource_attributes, "Attribute", {"AttributeId": "urn:oasis:names:tc:xacml:1.0:resource:bvlos-certification", "IncludeInResult": "false"})
        value = ET.SubElement(attribute, "AttributeValue", {"DataType": "http://www.w3.org/2001/XMLSchema#string"})
        value.text = bvlos_certification

    # Add environment Attributes
    environment_attributes = ET.SubElement(request, "Attributes", {"Category": "urn:oasis:names:tc:xacml:3.0:attribute-category:environment"})

    if area_controlled is not None:
        attribute = ET.SubElement(environment_attributes, "Attribute", {"AttributeId": "urn:oasis:names:tc:xacml:1.0:environment:area-controlled", "IncludeInResult": "false"})
        value = ET.SubElement(attribute, "AttributeValue", {"DataType": "http://www.w3.org/2001/XMLSchema#string"})
        value.text = area_controlled

    if individuals_informed is not None:
        attribute = ET.SubElement(environment_attributes, "Attribute", {"AttributeId": "urn:oasis:names:tc:xacml:1.0:environment:individuals-informed", "IncludeInResult": "false"})
        value = ET.SubElement(attribute, "AttributeValue", {"DataType": "http://www.w3.org/2001/XMLSchema#string"})
        value.text = individuals_informed

    return ET.tostring(request, encoding="unicode")

def evaluate_request(request_xml):
    """
    Evaluates the XACML request using the AuthzForce PDP engine.
    Returns the decision (Permit, Deny, Indeterminate).
    """
    # Save the request to a temporary file
    with open("temp-request.xml", "w", encoding="utf-8") as f:
        f.write(request_xml)
    
    # Run the AuthzForce PDP CLI command
    result = subprocess.run(
        ["java", "-jar", PDP_CLI_JAR, "-t", "XACML_XML", PDP_CONFIG_FILE, "temp-request.xml"],
        capture_output=True,
        text=True
    )
    
    # Parse the decision from the output
    try:
        response_xml = result.stdout
        root = ET.fromstring(response_xml)
        decision = root.find(".//{urn:oasis:names:tc:xacml:3.0:core:schema:wd-17}Decision").text
        return decision
    except Exception as e:
        print(f"Error parsing PDP response: {e}")
        return "Indeterminate"

def main():
    # Load input data from the Excel file
    try:
        df = pd.read_excel(EXCEL_FILE)
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        return

    # Iterate through each row in the Excel file
    for i, row in df.iterrows():
        scenario = {
            "weight": row.get("weight"),
            "exposed_parts": row.get("exposed_parts"),
            "kinetic_energy": row.get("kinetic_energy"),
            "remote_id": row.get("remote_id"),
            "area_controlled": row.get("area_controlled"),
            "individuals_informed": row.get("individuals_informed"),
            "commercial_purpose": row.get("commercial_purpose"),
            "bvlos_certification": row.get("bvlos_certification")
        }
        print(f"\nScenario {i + 1}:")
        print(f"Input: {scenario}")
        
        try:
            # Generate the XACML request
            request_xml = generate_xacml_request(**scenario)
            
            # Evaluate the request
            decision = evaluate_request(request_xml)
            print(f"Decision: {decision}")
        except ValueError as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()