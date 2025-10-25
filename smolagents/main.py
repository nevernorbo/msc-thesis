from browser import get_chrome_driver
from agent_config import get_agent, helium_instructions

driver = get_chrome_driver()
agent = get_agent(driver)

search_request = """
    Start at the wikipedia page of Tom Brady and get to the page of the restaurant chain Wendy's
"""

agent_output = agent.run(search_request + helium_instructions)
print("Final output: ", agent_output)
