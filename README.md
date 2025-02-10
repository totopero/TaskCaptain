# Discord Classroom Bot

## Overview
This is a Discord bot designed to facilitate a virtual classroom environment. The bot provides features for role assignment, private student channels, assignment distribution, and checklists for students and teachers.

## Features
- **Role Management:** Assign `student` or `teacher` roles.
- **Private Channels:** Creates a private channel for each student and a shared teacher channel.
- **Assignments:**
  - Teachers can create assignments.
  - Assignments can be given to all students or specific students.
  - Students can submit completed assignments.
- **Checklists:**
  - Teachers can create checklists for students.
  - Students can mark checklist items as completed by reacting with emojis.

## Commands
| Command | Description |
|---------|-------------|
| `.start` | Initiates the role selection process. |
| `.student` | Assigns the `student` role. |
| `.teacher` | Assigns the `teacher` role. |
| `.mychannel` | Creates a private text channel for the user. |
| `.assign` | Starts the assignment creation process (teachers only). |
| `.create <ID> %%% <Title> %%% <Description> $$$ <Due Date>` | Creates an assignment with a unique ID (teachers only). |
| `.giveto @student <ID>` | Assigns a specific assignment to an individual student. |
| `.allassign <ID>` | Assigns an assignment to all students. |
| `.done <ID> <message>` | Marks an assignment as completed and notifies teachers. |
| `.checklist` | Creates a checklist for students (teachers only). |

## Setup
### Prerequisites
- Python 3.8+
- `discord.py` library
- `dotenv` for environment variables

### Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/discord-classroom-bot.git
   cd discord-classroom-bot
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Create a `.env` file and add your Discord bot token:
   ```sh
   TOKEN=your-bot-token
   ```
4. Run the bot:
   ```sh
   python bot.py
   ```

## Usage
1. Invite the bot to your Discord server.
2. Run `.start` to begin setting up roles and channels.
3. Teachers can create assignments using `.assign` and distribute them with `.giveto` or `.allassign`.
4. Students can submit assignments using `.done`.
5. Teachers can create checklists for students using `.checklist`.

## License
This project is open-source and available under the [MIT License](LICENSE).

## Contributions
Contributions are welcome! Please open an issue or submit a pull request.

---

### Notes
- The bot must have permission to manage roles and channels.
- Ensure the bot has the correct intents enabled in the Discord Developer Portal.

