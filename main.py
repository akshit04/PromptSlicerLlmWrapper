from config import API_KEY, REPO_URL
from github_processor import GitHubRepoProcessor
from openrouter_wrapper import OpenRouterWrapper

if __name__ == "__main__":
    wrapper = OpenRouterWrapper(API_KEY)    
    repo_processor = GitHubRepoProcessor(REPO_URL)
    content = repo_processor.get_combined_file_contents()
    response = wrapper.process_large_prompt(content)

    print("Individual Results:\n")
    index = 0
    for result in response["individual_results"]:
        print(f"Result {index}: {result}")
        index += 1
    print("\n\n")

    print("Indvidual context summaries:\n")
    index = 0
    for context in response["individual_context_summaries"]:
        print(f"Context summary {index}: {context}")
        index += 1
    print("\n\n")

    print("Final Summary:\n", response["final_summary"])
