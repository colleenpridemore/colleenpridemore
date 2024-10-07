import yaml

# Load the YAML file
with open('techstack.yml', 'r') as file:
    data = yaml.safe_load(file)

# Generate Markdown content
markdown_content = f"""
# {data['repo_name']}

**Report ID**: {data['report_id']}
**Version**: {data['version']}
**Repository Type**: {data['repo_type']}
**Timestamp**: {data['timestamp']}
**Requested By**: {data['requested_by']}
**Provider**: {data['provider']}
**Branch**: {data['branch']}
**Detected Tools Count**: {data['detected_tools_count']}

## Tools

"""

for tool in data['tools']:
    markdown_content += f"""
### {tool['name']}
- **Description**: {tool['description']}
- **Website**: [{tool['website_url']}]({tool['website_url']})
- **Open Source**: {'Yes' if tool['open_source'] else 'No'}
- **Hosted SaaS**: {'Yes' if tool['hosted_saas'] else 'No'}
- **Category**: {tool['category']}
"""

# Write the Markdown content to README.md
with open('README.md', 'w') as file:
    file.write(markdown_content)