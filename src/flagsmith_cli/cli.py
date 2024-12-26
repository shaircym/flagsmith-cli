import os
import sys
import yaml
import inquirer
from typing import Dict, Optional
from .flagsmith import Flagsmith

class CLI:
    def __init__(self):
        self.config = self.load_config()
        self.client: Optional[Flagsmith] = None
        self.page_size = 50
        
    def load_config(self) -> Dict:
        """Load config from ~/.flagsmith.yaml"""
        config_path = os.path.expanduser('~/.flagsmith.yaml')
        if not os.path.exists(config_path):
            print(f"Config file not found at {config_path}")
            print("Please copy config.example.yaml to ~/.flagsmith.yaml and add your API keys")
            sys.exit(1)
            
        with open(config_path) as f:
            return yaml.safe_load(f)
    
    def select_environment(self):
        """Select and initialize environment."""
        questions = [
            inquirer.List('environment',
                         message="Choose environment",
                         choices=['staging', 'production'])
        ]
        answers = inquirer.prompt(questions)
        env = answers['environment']
        api_key = self.config['environments'][env]['key']
        self.client = Flagsmith(api_key)
        print(f"\nUsing {env} environment")
        
    def list_flags(self):
        """List and manage feature flags."""
        page = 1
        while True:
            flags_data = self.client.get_feature_flags(page, self.page_size)
            flags = flags_data["results"]
            
            if not flags:
                print("No flags found")
                return

            choices = [f"{flag['name']} - Enabled: {flag['enabled']} - Value: {flag['value']}"
                      for flag in flags]
            choices.append("Next page" if page * self.page_size < flags_data["count"] 
                         else "Back")
            
            questions = [
                inquirer.List('flag',
                             message=f"Feature flags (Page {page})",
                             choices=choices)
            ]
            answer = inquirer.prompt(questions)
            
            if answer["flag"] == "Next page":
                page += 1
                continue
            elif answer["flag"] == "Back":
                break
            else:
                selected_flag = next(flag for flag in flags 
                    if f"{flag['name']} - Enabled: {flag['enabled']} - Value: {flag['value']}" == answer["flag"])
                self.modify_flag(selected_flag)

    def modify_flag(self, flag: Dict):
        """Modify a selected feature flag."""
        questions = [
            inquirer.List('action',
                         message=f"Modify flag: {flag['name']}",
                         choices=['Toggle', 'Set Value', 'Back'])
        ]
        answer = inquirer.prompt(questions)
        
        if answer["action"] == "Toggle":
            new_value = not flag["enabled"]
            if self.confirm_change(flag["name"], "enabled", new_value):
                self.client.update_flag(flag["id"], {"enabled": new_value})
                print(f"Successfully updated {flag['name']}")
                
        elif answer["action"] == "Set Value":
            questions = [
                inquirer.Text('value',
                             message=f"Enter new value for {flag['name']}")
            ]
            value_answer = inquirer.prompt(questions)
            
            if self.confirm_change(flag["name"], "value", value_answer["value"]):
                self.client.update_flag(flag["id"], {"value": value_answer["value"]})
                print(f"Successfully updated {flag['name']}")

    def confirm_change(self, flag_name: str, field: str, new_value: any) -> bool:
        """Confirm a flag modification."""
        questions = [
            inquirer.Confirm('confirm',
                           message=f"Confirm changing {flag_name} {field} to {new_value}?",
                           default=False)
        ]
        return inquirer.prompt(questions)["confirm"]

    def run(self):
        """Run the CLI main loop."""
        print("Flagsmith CLI")
        self.select_environment()
        
        while True:
            questions = [
                inquirer.List('action',
                             message="Choose action",
                             choices=['List Flags', 'Switch Environment', 'Exit'])
            ]
            answer = inquirer.prompt(questions)
            
            if answer["action"] == "List Flags":
                self.list_flags()
            elif answer["action"] == "Switch Environment":
                self.select_environment()
            elif answer["action"] == "Exit":
                sys.exit(0)

def main():
    CLI().run()

if __name__ == "__main__":
    main()