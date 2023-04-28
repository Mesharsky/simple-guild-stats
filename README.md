#### **Simple Guild Stats Bot for Discord made in Python**
Bot is working with sqlite database. Each db row has its own **guild_id** so bot can work on multiple servers without any issues.


------------

**Available commands:**

- **/add_admin_role (role)** - You can add any role you want that have permissions for bot commands (To add a role you need to have administrator priviliges on discord.)
- **/add_points (member, amount)** - Add points for discord member.
- **/remove_points (member, amount)** - Remove points for discord member.
- **/award_voice_members (title, amount)** - Give x amount of points to everyone that is currently on your voice channel. And generate embed message with outcome.
- **/check_points (member)** - Check how many points member have.
- **/total_rank** - Print embed message with total ranking for all members. From top to bottom.
- **/reset_points (member)** - Reset points for specific member.
- **/reset_all_points (security_code)** - Reset whole ranking, you need to use this command twice (security check in case you type command by mistake)

