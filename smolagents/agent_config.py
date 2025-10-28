import os
from smolagents import CodeAgent, OpenAIServerModel, DuckDuckGoSearchTool
from tools import go_back, close_popups, search_item_ctrl_f


def get_agent(driver):
    from tools import set_driver

    set_driver(driver)

    # model = OpenAIServerModel(
    #     model_id="gemma3:12b",
    #     api_base="http://localhost:11434/v1",
    #     api_key="ollama",
    #     flatten_messages_as_text=False,
    # )

    model = OpenAIServerModel(
        model_id="gemini-2.5-flash",
        api_base="https://generativelanguage.googleapis.com/v1beta/openai/",
        api_key=os.getenv("GOOGLE_API_KEY"),
    )

    agent = CodeAgent(
        tools=[
            go_back,
            close_popups,
            search_item_ctrl_f,
            DuckDuckGoSearchTool(max_results=5, rate_limit=2.0),
        ],
        model=model,
        additional_authorized_imports=[
            "helium",
        ],
        max_steps=20,
        verbosity_level=2,
    )

    agent.python_executor("from helium import *")

    return agent


helium_instructions = """
You can use helium to access websites. Don't bother about the helium driver, it's already managed.

You can go to pages using:
Code:
```py
helium.go_to('github.com/trending')
```<end_code>


You can directly click clickable elements by inputting the text that appears on them.
Code:
```py
helium.click("Top products")
```<end_code>

If it's a link:
Code:
```py
helium.click(helium.Link("Top products"))
```<end_code>

If you try to interact with an element and it's not found, you'll get a LookupError.
In general stop your action after each button click to see what happens on your screenshot.
Never try to login in a page.

To scroll up or down, use scroll_down or scroll_up with as an argument the number of pixels to scroll from.
Code:
```py
helium.scroll_down(num_pixels=1200) # This will scroll one viewport down
```<end_code>

When you have pop-ups with a cross icon to close, don't try to click the close icon by finding its element or targeting an 'X' element (this most often fails).
Just use your built-in tool `close_popups` to close them:
Code:
```py
close_popups()
```<end_code>

You can use .exists() to check for the existence of an element. For example:
Code:
```py
if helium.Text('Accept cookies?').exists():
    click('I accept')
```<end_code>
"""
