import os
import subprocess
import xml.etree.ElementTree as ET
import pandas as pd


# =========================================================
# FILE PATHS
# =========================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

PDP_CLI_JAR = os.path.join(BASE_DIR, "authzforce-ce-core-pdp-cli-21.0.2-SNAPSHOT.jar")
PDP_CONFIG_FILE = os.path.join(BASE_DIR, "pdp-config.xml")
EXCEL_FILE = os.path.join(BASE_DIR, "input_data.xlsx")
TEMP_REQUEST_FILE = os.path.join(BASE_DIR, "temp-request.xml")


# =========================================================
# HELPERS
# =========================================================
def normalize_value(value):
    """
    Convert Excel NaN to None so it does not get written as a bad request value.
    """
    if pd.isna(value):
        return None
    return value


def add_attribute(parent, attribute_id, data_type, value):
    """
    Add one XACML Attribute element with one AttributeValue.
    """
    attribute = ET.SubElement(
        parent,
        "Attribute",
        {
            "AttributeId": attribute_id,
            "IncludeInResult": "false"
        }
    )
    attr_value = ET.SubElement(
        attribute,
        "AttributeValue",
        {
            "DataType": data_type
        }
    )
    attr_value.text = str(value)


def extract_response_xml(stdout_text, stderr_text):
    """
    AuthzForce sometimes writes the XML response in stdout, and sometimes logs can
    appear around it. This safely extracts the <Response> XML block.
    """
    combined = ((stdout_text or "") + "\n" + (stderr_text or "")).strip()

    if not combined:
        return ""

    # Prefer XML declaration if present
    idx = combined.find("<?xml")
    if idx != -1:
        return combined[idx:].strip()

    # Otherwise start from Response tag
    idx = combined.find("<Response")
    if idx != -1:
        return combined[idx:].strip()

    return combined


# =========================================================
# REQUEST GENERATOR
# =========================================================
def generate_xacml_request(
    weight=None,
    exposed_parts=None,
    kinetic_energy=None,
    remote_id=None,
    area_controlled=None,
    individuals_informed=None,
    commercial_purpose=None,
    bvlos_certification=None,

    # Night-operation fields
    current_time=None,
    night_operation_knowledge_requirement=None,
    night_operation_lighting_requirement=None,
    civil_twilight_operation_lighting=None,
    civil_twilight_time_definition=None,
    lighting_safety_adjustment=None,
    certificate_waiver_expiration=None
):
    """
    Generates a complete XACML Request XML based on request attributes.
    """

    # -----------------------------
    # Validate standard attributes
    # -----------------------------
    if exposed_parts is not None and exposed_parts not in ["present", "absent"]:
        raise ValueError("Invalid exposed_parts. Must be 'present' or 'absent'.")

    if remote_id is not None and remote_id not in ["broadcasting", "not-broadcasting"]:
        raise ValueError("Invalid remote_id. Must be 'broadcasting' or 'not-broadcasting'.")

    if area_controlled is not None and area_controlled not in ["controlled", "not-controlled"]:
        raise ValueError("Invalid area_controlled. Must be 'controlled' or 'not-controlled'.")

    if individuals_informed is not None and individuals_informed not in ["informed", "not-informed"]:
        raise ValueError("Invalid individuals_informed. Must be 'informed' or 'not-informed'.")

    if commercial_purpose is not None and commercial_purpose not in ["yes", "no"]:
        raise ValueError("Invalid commercial_purpose. Must be 'yes' or 'no'.")

    if bvlos_certification is not None and bvlos_certification not in ["approved", "not-approved"]:
        raise ValueError("Invalid bvlos_certification. Must be 'approved' or 'not-approved'.")

    # -----------------------------
    # Validate night-operation fields
    # -----------------------------
    permit_deny_values = {"Permit", "Deny"}

    night_fields = {
        "night_operation_knowledge_requirement": night_operation_knowledge_requirement,
        "night_operation_lighting_requirement": night_operation_lighting_requirement,
        "civil_twilight_operation_lighting": civil_twilight_operation_lighting,
        "civil_twilight_time_definition": civil_twilight_time_definition,
        "lighting_safety_adjustment": lighting_safety_adjustment,
        "certificate_waiver_expiration": certificate_waiver_expiration,
    }

    for field_name, field_value in night_fields.items():
        if field_value is not None and field_value not in permit_deny_values:
            raise ValueError(f"Invalid {field_name}. Must be 'Permit' or 'Deny'.")

    # -----------------------------
    # Root Request
    # -----------------------------
    request = ET.Element(
        "Request",
        {
            "xmlns": "urn:oasis:names:tc:xacml:3.0:core:schema:wd-17",
            "ReturnPolicyIdList": "false",
            "CombinedDecision": "false"
        }
    )

    # -----------------------------
    # Resource Attributes
    # -----------------------------
    resource_attributes = ET.SubElement(
        request,
        "Attributes",
        {"Category": "urn:oasis:names:tc:xacml:3.0:attribute-category:resource"}
    )

    if weight is not None:
        add_attribute(
            resource_attributes,
            "urn:oasis:names:tc:xacml:1.0:resource:suas-weight",
            "http://www.w3.org/2001/XMLSchema#double",
            weight
        )

    if exposed_parts is not None:
        add_attribute(
            resource_attributes,
            "urn:oasis:names:tc:xacml:1.0:resource:exposed-parts",
            "http://www.w3.org/2001/XMLSchema#string",
            exposed_parts
        )

    if kinetic_energy is not None:
        add_attribute(
            resource_attributes,
            "urn:oasis:names:tc:xacml:1.0:resource:kinetic-energy",
            "http://www.w3.org/2001/XMLSchema#double",
            kinetic_energy
        )

    if remote_id is not None:
        add_attribute(
            resource_attributes,
            "urn:oasis:names:tc:xacml:1.0:resource:remote-id",
            "http://www.w3.org/2001/XMLSchema#string",
            remote_id
        )

    if commercial_purpose is not None:
        add_attribute(
            resource_attributes,
            "urn:oasis:names:tc:xacml:1.0:resource:commercial-purpose",
            "http://www.w3.org/2001/XMLSchema#string",
            commercial_purpose
        )

    if bvlos_certification is not None:
        add_attribute(
            resource_attributes,
            "urn:oasis:names:tc:xacml:1.0:resource:bvlos-certification",
            "http://www.w3.org/2001/XMLSchema#string",
            bvlos_certification
        )

    # Night-operation resource attributes matching your URN-style Night policy
    if night_operation_knowledge_requirement is not None:
        add_attribute(
            resource_attributes,
            "urn:drone-policy:resource:night-operation-knowledge-requirement",
            "http://www.w3.org/2001/XMLSchema#string",
            night_operation_knowledge_requirement
        )

    if night_operation_lighting_requirement is not None:
        add_attribute(
            resource_attributes,
            "urn:drone-policy:resource:night-operation-lighting-requirement",
            "http://www.w3.org/2001/XMLSchema#string",
            night_operation_lighting_requirement
        )

    if civil_twilight_operation_lighting is not None:
        add_attribute(
            resource_attributes,
            "urn:drone-policy:resource:civil-twilight-operation-lighting",
            "http://www.w3.org/2001/XMLSchema#string",
            civil_twilight_operation_lighting
        )

    if civil_twilight_time_definition is not None:
        add_attribute(
            resource_attributes,
            "urn:drone-policy:resource:civil-twilight-time-definition",
            "http://www.w3.org/2001/XMLSchema#string",
            civil_twilight_time_definition
        )

    if lighting_safety_adjustment is not None:
        add_attribute(
            resource_attributes,
            "urn:drone-policy:resource:lighting-safety-adjustment",
            "http://www.w3.org/2001/XMLSchema#string",
            lighting_safety_adjustment
        )

    if certificate_waiver_expiration is not None:
        add_attribute(
            resource_attributes,
            "urn:drone-policy:resource:certificate-waiver-expiration",
            "http://www.w3.org/2001/XMLSchema#string",
            certificate_waiver_expiration
        )

    # -----------------------------
    # Environment Attributes
    # -----------------------------
    environment_attributes = ET.SubElement(
        request,
        "Attributes",
        {"Category": "urn:oasis:names:tc:xacml:3.0:attribute-category:environment"}
    )

    if area_controlled is not None:
        add_attribute(
            environment_attributes,
            "urn:oasis:names:tc:xacml:1.0:environment:area-controlled",
            "http://www.w3.org/2001/XMLSchema#string",
            area_controlled
        )

    if individuals_informed is not None:
        add_attribute(
            environment_attributes,
            "urn:oasis:names:tc:xacml:1.0:environment:individuals-informed",
            "http://www.w3.org/2001/XMLSchema#string",
            individuals_informed
        )

    if current_time is not None:
        add_attribute(
            environment_attributes,
            "urn:oasis:names:tc:xacml:1.0:environment:current-time",
            "http://www.w3.org/2001/XMLSchema#time",
            current_time
        )

    return ET.tostring(request, encoding="unicode")


# =========================================================
# EVALUATION
# =========================================================
def evaluate_request(request_xml):
    """
    Save request XML, run AuthzForce CLI, and parse the decision.
    """
    with open(TEMP_REQUEST_FILE, "w", encoding="utf-8") as f:
        f.write(request_xml)

    result = subprocess.run(
        ["java", "-jar", PDP_CLI_JAR, "-t", "XACML_XML", PDP_CONFIG_FILE, TEMP_REQUEST_FILE],
        capture_output=True,
        text=True
    )

    response_xml = extract_response_xml(result.stdout, result.stderr)

    try:
        root = ET.fromstring(response_xml)

        decision = None
        for elem in root.iter():
            if elem.tag.endswith("Decision"):
                decision = (elem.text or "").strip()
                break

        if not decision:
            print("Could not find <Decision> in PDP response.")
            print("STDOUT:\n", result.stdout)
            print("STDERR:\n", result.stderr)
            return "Indeterminate"

        return decision

    except Exception as e:
        print(f"Error parsing PDP response: {e}")
        print("STDOUT:\n", result.stdout)
        print("STDERR:\n", result.stderr)
        return "Indeterminate"


# =========================================================
# MAIN
# =========================================================
def main():
    try:
        df = pd.read_excel(EXCEL_FILE)
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        return

    for i, row in df.iterrows():
        scenario = {
            "weight": normalize_value(row.get("weight")),
            "exposed_parts": normalize_value(row.get("exposed_parts")),
            "kinetic_energy": normalize_value(row.get("kinetic_energy")),
            "remote_id": normalize_value(row.get("remote_id")),
            "area_controlled": normalize_value(row.get("area_controlled")),
            "individuals_informed": normalize_value(row.get("individuals_informed")),
            "commercial_purpose": normalize_value(row.get("commercial_purpose")),
            "bvlos_certification": normalize_value(row.get("bvlos_certification")),

            # New night-operation columns expected in Excel
            "current_time": normalize_value(row.get("current_time")),
            "night_operation_knowledge_requirement": normalize_value(row.get("night_operation_knowledge_requirement")),
            "night_operation_lighting_requirement": normalize_value(row.get("night_operation_lighting_requirement")),
            "civil_twilight_operation_lighting": normalize_value(row.get("civil_twilight_operation_lighting")),
            "civil_twilight_time_definition": normalize_value(row.get("civil_twilight_time_definition")),
            "lighting_safety_adjustment": normalize_value(row.get("lighting_safety_adjustment")),
            "certificate_waiver_expiration": normalize_value(row.get("certificate_waiver_expiration")),
        }

        print(f"\nScenario {i + 1}:")
        print(f"Input: {scenario}")

        try:
            request_xml = generate_xacml_request(**scenario)
            decision = evaluate_request(request_xml)
            print(f"Decision: {decision}")
        except ValueError as e:
            print(f"Validation Error: {e}")


if __name__ == "__main__":
    main()