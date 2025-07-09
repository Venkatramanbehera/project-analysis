import os
import httpx

def get_github_project_info(project_url: str) -> str:
    token = os.getenv("GITHUUB_TOKEN")
    if not token:
        return "Error: Missing GITHUUB_TOKEN"
    
    if project_url:
        return query_project_v2(project_url, token)
    else:
        return "Invalid Github project URL format."
    
def query_project_v2(project_url: str, token: str) -> str:
    try:
        parts = project_url.strip("/").split("/")
        username = parts[4]
        project_number = int(parts[6])
        print("\n query_project_v2", parts)
    except Exception:
        return "Failed to parse user-level GitHub Projects v2 URL."
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    query = """
        query($login: String!, $number: Int!) {
        user(login: $login) {
            projectV2(number: $number) {
            title
            shortDescription
            items(first: 5) {
                nodes {
                content {
                    ... on Issue {
                        title
                        state
                    }
                    ... on PullRequest {
                        title
                        state
                    }
                }
                }
            }
            }
        }
        }
    """
    variables = {
        "login": username,
        "number": project_number
    }
    response = httpx.post(
        "https://api.github.com/graphql",
        headers=headers,
        json={"query": query, "variables": variables}
    )

    if response.status_code != 200:
        return f"GraphQL Error: {response.text}"

    data = response.json()
    try: 
        project = data['data']['user']['projectV2']
        title = project['title']
        description = project.get("shortDescription") or "No description provided"
        items = project["items"]["nodes"]
        response_lines = [f"Project: {title}", f"Description: {description}", "Items:"]
        for item in items:
            content = item.get("content")
            if not content:
                continue
            entry = f"- [{content['state']}] {content['title']}"
            response_lines.append(entry)
        return "\n".join(response_lines)
    
    except Exception as e:
        return f"Error parsing project data: {e}"
