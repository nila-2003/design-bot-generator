# Design Bot Generator
This project is a Streamlit-based web application that allows users to generate design images and corresponding React code based on textual prompts.
It uses Stability AI for image generation and Google's Gemini language model for generating React code.

1. Clone the repo
   ```ruby
   https://github.com/nila-2003/design-bot-generator.git
   cd design-bot-generator
   ```
2. Install the required Python packages
   ```ruby
   pip install -r requirements.txt
   ```
3. Replave the .env file contents with your API keys.
4. Run the streamlit application
   ```ruby
   streamlit run app.py
   ```

Check out the deployed application! 
https://design-bot-generator-fygyp6tuwezqzwu9odqbej.streamlit.app/



import yaml
import json
import os

def parse_swagger(swagger_path):
    with open(swagger_path, 'r') as file:
        swagger = yaml.safe_load(file)
    return swagger

def generate_pact(swagger):
    pact = {
        "consumer": {
            "name": "Consumer"
        },
        "provider": {
            "name": "Provider"
        },
        "interactions": []
    }
    
    for path, methods in swagger.get('paths', {}).items():
        for method, details in methods.items():
            interaction = {
                "description": details.get('summary', f"{method.upper()} {path}"),
                "request": {
                    "method": method.upper(),
                    "path": path,
                    "headers": {},
                    "body": {},
                    "query": ""
                },
                "response": {
                    "status": 200,
                    "headers": {},
                    "body": {}
                }
            }
            
            # Add request parameters
            if 'parameters' in details:
                for param in details['parameters']:
                    if param['in'] == 'query':
                        interaction['request']['query'] += f"{param['name']}={{}}&"
                    elif param['in'] == 'header':
                        interaction['request']['headers'][param['name']] = ""
                    elif param['in'] == 'body':
                        interaction['request']['body'] = param.get('schema', {})
            
            # Add response details
            responses = details.get('responses', {})
            for status, response in responses.items():
                interaction['response']['status'] = int(status)
                interaction['response']['body'] = response.get('schema', {})
                break  # Assume first response is the primary one for simplicity
            
            pact['interactions'].append(interaction)
    
    return pact

def save_pact(pact, output_path):
    with open(output_path, 'w') as file:
        json.dump(pact, file, indent=2)

def main(swagger_path, output_path):
    swagger = parse_swagger(swagger_path)
    pact = generate_pact(swagger)
    save_pact(pact, output_path)
    print(f"Pact file generated at {output_path}")

if __name__ == "__main__":
    swagger_path = "swagger.yaml"  # Change this to your Swagger file path
    output_path = "pact.json"      # Change this to your desired output file path
    main(swagger_path, output_path)






import yaml
from typing import Dict, List, Any

def parse_swagger(file_path: str) -> Dict[str, Any]:
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def extract_api_details(swagger_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    api_details = []

    for path, path_item in swagger_data['paths'].items():
        for method, operation in path_item.items():
            api_call = {
                'path': path,
                'method': method.upper(),
                'operation_id': operation.get('operationId', f"{method}_{path.replace('/', '_')}"),
                'summary': operation.get('summary', ''),
                'description': operation.get('description', ''),
                'parameters': extract_parameters(operation.get('parameters', [])),
                'request_body': extract_request_body(operation.get('requestBody', {})),
                'responses': extract_responses(operation.get('responses', {})),
            }
            api_details.append(api_call)

    return api_details

def extract_parameters(parameters: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    grouped_params = {
        'path': [],
        'query': [],
        'header': [],
        'cookie': []
    }

    for param in parameters:
        param_info = {
            'name': param['name'],
            'required': param.get('required', False),
            'schema': param.get('schema', {})
        }
        grouped_params[param['in']].append(param_info)

    return grouped_params

def extract_request_body(request_body: Dict[str, Any]) -> Dict[str, Any]:
    if not request_body:
        return {}

    content = request_body.get('content', {})
    for media_type, media_info in content.items():
        return {
            'media_type': media_type,
            'schema': media_info.get('schema', {}),
            'required': request_body.get('required', False)
        }

    return {}

def extract_responses(responses: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    extracted_responses = {}

    for status_code, response_info in responses.items():
        content = response_info.get('content', {})
        for media_type, media_info in content.items():
            extracted_responses[status_code] = {
                'description': response_info.get('description', ''),
                'media_type': media_type,
                'schema': media_info.get('schema', {})
            }
            break  # Assuming one media type per response

    return extracted_responses

def main(swagger_file: str):
    swagger_data = parse_swagger(swagger_file)
    api_details = extract_api_details(swagger_data)

    # Print extracted information (you can modify this to suit your needs)
    for api in api_details:
        print(f"Path: {api['path']}")
        print(f"Method: {api['method']}")
        print(f"Operation ID: {api['operation_id']}")
        print(f"Summary: {api['summary']}")
        print(f"Description: {api['description']}")
        print("Parameters:")
        for param_type, params in api['parameters'].items():
            print(f"  {param_type.capitalize()}:")
            for param in params:
                print(f"    - {param['name']} (Required: {param['required']})")
        print("Request Body:")
        if api['request_body']:
            print(f"  Media Type: {api['request_body']['media_type']}")
            print(f"  Required: {api['request_body']['required']}")
        print("Responses:")
        for status_code, response in api['responses'].items():
            print(f"  {status_code}:")
            print(f"    Description: {response['description']}")
            print(f"    Media Type: {response['media_type']}")
        print("\n")

if __name__ == "__main__":
    main("path/to/your/swagger.yaml")

    

import yaml
from typing import Dict, List, Any

# ... (previous code remains the same)

def generate_java_test_class(api_details: List[Dict[str, Any]], class_name: str) -> str:
    imports = set([
        "au.com.dius.pact.consumer.MockServer",
        "au.com.dius.pact.consumer.dsl.PactDslWithProvider",
        "au.com.dius.pact.consumer.junit5.PactConsumerTestExt",
        "au.com.dius.pact.consumer.junit5.PactTestFor",
        "au.com.dius.pact.core.model.RequestResponsePact",
        "au.com.dius.pact.core.model.annotations.Pact",
        "org.junit.jupiter.api.Test",
        "org.junit.jupiter.api.extension.ExtendWith",
        "org.springframework.http.HttpEntity",
        "org.springframework.http.HttpHeaders",
        "org.springframework.http.HttpMethod",
        "org.springframework.http.ResponseEntity",
        "org.springframework.web.client.RestTemplate",
        "org.springframework.web.client.HttpClientErrorException",
        "org.springframework.web.client.HttpServerErrorException",
        "java.util.HashMap",
        "java.util.Map",
        "org.junit.jupiter.api.Assertions",
        "com.fasterxml.jackson.databind.ObjectMapper"
    ])

    java_code = f"""
{generate_import_statements(imports)}

@ExtendWith(PactConsumerTestExt.class)
@PactTestFor(providerName = "{{{{PROVIDER_NAME}}}}")
public class {class_name} {{

    private static final String CONSUMER_NAME = "{{{{CONSUMER_NAME}}}}";
    private static final ObjectMapper objectMapper = new ObjectMapper();

    """

    for api in api_details:
        method_name = api['operation_id'].replace('-', '_')
        java_code += generate_pact_method(api, method_name)
        java_code += generate_test_method(api, method_name)

    java_code += "}\n"
    return java_code

def generate_import_statements(imports: set) -> str:
    return "\n".join(f"import {imp};" for imp in sorted(imports))

# ... (rest of the code remains the same)

def generate_test_method(api: Dict[str, Any], method_name: str) -> str:
    return f"""
    @Test
    @PactTestFor(pactMethod = "pactFor{method_name.capitalize()}")
    void test{method_name.capitalize()}(MockServer mockServer) {{
        RestTemplate restTemplate = new RestTemplate();
        String url = mockServer.getUrl() + "{api['path']}";
        {generate_path_params(api)}
        {generate_query_params_url(api)}

        HttpHeaders headers = new HttpHeaders();
        {generate_headers_test(api)}

        {generate_request_body_test(api)}

        try {{
            ResponseEntity<String> response = restTemplate.exchange(url, HttpMethod.{api['method']}, requestEntity, String.class);
            Assertions.assertEquals({next(iter(api['responses']))}, response.getStatusCodeValue());
            // Add more assertions here based on the expected response
        }} catch (HttpClientErrorException | HttpServerErrorException e) {{
            Assertions.fail("Unexpected error: " + e.getMessage());
        }}
    }}
    """

# ... (rest of the code remains the same)

 
