from pyrogram import filters
from tassistant.scenarios.partysound import PartySoundScenario


all_scenarios = [
    PartySoundScenario(filters.me & filters.command("partysound", prefixes="/"))
]
