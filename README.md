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
