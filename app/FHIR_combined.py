import requests
import json
import ndjson
import os
import xmltodict

smart_defaults = {
    'app_id': 'my_web_app',
    'api_base': 'https://r4.smarthealthit.org/Patient',
}


def post_json(patient, path):
    try:
        if patient['resourceType'] == 'Patient':
            patient_json = json.dumps(patient)
            headers = {'Content-Type': 'application/json'}
            res = requests.post(url=smart_defaults['api_base'], headers=headers, data=patient_json).text
            res = json.loads(res)
            print(path + ": This validation was right, Patient: " + res['id'] + " created")
            return res
        else:
            print("Cannot handle this type yet")
            return
    except requests.HTTPError as e:
        if e.response.status_code == 400:
            print("FHIR server validation error")
    except Exception:
        print(path + ": This validation was wrong")


def post_xml(patient, path):
    try:
        xml_dict = xmltodict.parse(patient)
        if xml_dict['Patient']:
            headers = {'Content-Type': 'application/xml'}
            res = requests.post(url=smart_defaults['api_base'], headers=headers, data=patient).text
            res = xmltodict.parse(res)
            print(path + ": This validation was right, Patient: " + res['Patient']['id']['@value'] + " created")
            return res
        else:
            print("Cannot handle this type yet")
            return
    except requests.HTTPError as e:
        if e.response.status_code == 400:
            print("FHIR server validation error")
    except Exception:
        print(path + ": This validation was wrong")


def verify_fhir(path):
    try:
        filename, file_extension = os.path.splitext(path)

        if file_extension == '.ndjson':
            with open(path) as ndjson_file:
                patients_data = ndjson.load(ndjson_file)
            ndjson_file.close()
            for patient_data in patients_data:
                post_json(patient_data, path)

        elif file_extension == '.json':
            with open(path) as json_data:
                patient_data = json.load(json_data)
            json_data.close()
            post_json(patient_data, path)

        elif file_extension == '.xml':
            with open(path) as xml_file:
                patient_data = xml_file.read()
            xml_file.close()
            post_xml(patient_data, path)

        else:
            print('Cannot handle this file yet')
            return
    except FileNotFoundError:
        print("File path: " + path + " Does not exist")
        pass
    except Exception:
        print(path + ": This validation was wrong")


def main():
    while (1):
        file = input("Give file path or type exit to quit: ")
        if file == 'exit':
            break
        verify_fhir(file)


if __name__ == "__main__":
    main()