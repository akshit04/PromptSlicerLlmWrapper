from config import API_KEY, REPO_URL
from github_processor import GitHubRepoProcessor
from openrouter_wrapper import OpenRouterWrapper

if __name__ == "__main__":
    wrapper = OpenRouterWrapper(API_KEY)    
    repo_processor = GitHubRepoProcessor(REPO_URL)
    content = repo_processor.get_combined_file_contents()
    response = wrapper.process_large_prompt(content)

    print("## Individual Results:\n")
    index = 1
    for result in response["individual_results"]:
        print(f"### Result {index}:")
        print(f"{result}")
        index += 1

    print("## Indvidual context summaries:")
    index = 1
    for context in response["individual_context_summaries"]:
        print(f"### Context summary {index}:")
        print(f"{context}")
        index += 1

    print("## Final Summary:")
    print(f"{response['final_summary']}")
