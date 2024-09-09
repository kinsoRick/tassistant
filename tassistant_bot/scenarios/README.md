# Scenarios in Telegram Assistant

In Tassistant, scenarios are a flexible way to organize the logic of event handlers and state management. A scenario can be viewed as a sequence of actions that are executed in response to messages or other events in a chat, while also tracking progress through internal state management.

## Structure of a Scenario

1. **Starting the Scenario by Command:** A user sends a command to initiate the scenario.
2. **Initialization and Handler Setup:** After starting the scenario, it is assigned handlers to manage various events (e.g., commands, new messages, or chat members).
3. **State Tracking:** The internal state of the scenario changes based on progress (e.g., from "pending" to "in progress"). This allows for flexible management of scenario execution.
4. **Saving and Restoring State:** The scenario can save its current state to a file to allow for future restoration if needed.

## Example — Mafia Game Scenario

**Goal:** Managing the gameplay of "Mafia" in a chat.

1. **Command `/mafia`:** Starts the game creation process. The game begins by creating a new chat and binding handlers to manage game events.
2. **Creating Chat and Gathering Participants:** Upon running the command, a new chat is created, and participants specified in the command arguments are added.
3. **Command `/start`:** Changes the game state from "pending" to "in progress." The game transitions to an active state, and handlers for managing game phases are activated.
4. **Game Handlers:**
   - **Handler for Commands:** Handles player eliminations, night actions, and voting.
   - **Handler for Game End:** Ends the game and resets the state to "pending" after the game ends.
5. **Ending the Game:** After the game concludes, the scenario state is reset to "pending" or another appropriate state.

> **Note:** This approach simplifies the organization of complex sequences of actions, such as creating group playlists or running interactive games in a chat.

> **Warning:** Ensure to handle all states and transitions carefully to avoid inconsistencies in scenario execution.

---
### Example Scenario Code

```python
from typing import Optional
from pyrogram import Client
from pyrogram.types import Message
from pyrogram.handlers import MessageHandler
from tassistant_bot.scenarios import BaseScenario  # Import the BaseScenario class

class ExampleScenario(BaseScenario):
    class Meta:
        name = "Example Scenario"
        description = "An example scenario for demonstration."

    def __init__(self, filters, state: Optional[dict] = None) -> None:
        super().__init__(filters, state)
        self.internal_state = state or {}

    async def handle_join_member(self, client: Client, message: Message):
        for user in message.new_chat_members:
            client.send_message(message.chat.id, f"Hello {username}"

    async def handle_leave_member(self, client: Client, message: Message):
        username = message.left_chat_member.username
        client.send_message(message.chat.id, f"Bye {username}"

    async def configure(self, client: Client, message: Message) -> None:
        self.username = client.me.username

    async def init_all_handlers(self, client: Client) -> None:
        client.add_handler(MessageHandler(
            self.handle_join_member,
            pyro_filters.chat(self.chat.id)
            & pyro_filters.new_chat_members
        ))
        client.handle_leave_member(MessageHandler(
            self.handler,
            pyro_filters.chat(self.chat.id)
            & pyro_filters.left_chat_member
        ))

    async def post_configure(self, client: Client, message: Message) -> None:
        await message.reply("Example scenario is now active!")
