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

 
