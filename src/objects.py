from typing import Literal, cast

from screen_objects import ScreenObject, get_objects

from .paths import SAMPLES_DIR, REGIONS_DIR


ScreenObjectNames = Literal[
    "claim_daily",
    "blur",
    "x",
    "x_news",
    "x_new",
    "continue_game",
    "claim_healed",
    "hospital",
    "heal",
    "confirm_rss",
    "ask_help",
    "hospital_building",
    "speed_up",
    "speed_up_blue",
    "no_speed",
    "one-tap_speed_up",
    "confirm_speed_up",
    "sanctuary",
    "claim_holy_water",
    "confirm_claim_water",
    "holy_quest",
    "claim_holy_quest",
    "holy_revival",
    "revive",

    "lord",
    "recall_all",
    "harvest",
    "gather_speed_up",
    "use",

    "loading",
    "map_hand",
    "monster",
    "arrow",
    "attack",
    "quick_search",
    "use_stamina",
    "confirm_use_stamina",

    "castle_building",
    "tasks",
    "build_task",
    "hand",
    "upgrade",
    "upgrade_blue",
    "big_upgrade_blue",
    "go_upgrade",
    "get_now",
    "hammer_use",
    "hammer_200",
    "need_food",
    "need_wood",
    "need_stone",
    "need_iron",

    "recruit_task",
    "recruit",
    "cavalry",
    "previous",
    "second",
    "recruit_blue",
    "horse",

    "forge",
    "weapon",
    "helmet",
    "belt",
    "clothes",
    "accessory",
    "boots",
    "forge_green",
    "+",
    "select",
    "forge_blue",

    "college",
    "research",
    "resources",
    "military",
    "plow",
    "saw",
    "sickle",
    "axe",
    "load_boost",
    "draft",
    "expansion",
    "legion",
    "leadership",
    "horseshoes",
    "research_blue",
    "go_research",

    "claim",
    "alliance_bonuses",
    "join",
    "apply",
    "help",
    "alliance_donate",
    "donate_blue",
    "donate_confirm",

    "quest",
    "daily_quest_claim",
    "claim_daily_quest",
    "growth_quest",
    "claim_growth_quest",
    "another_growth_quest",
    "reward",

    "events",
    "event",
    "event_claim",
    "!",
    "event_arrow",

    "mail",
    "mail_reward",
    "read_claim_all",
    "confirm_read_all",

    "fortify",
    "one-tap_upgrade",
    "use_all",

    "sell",
    "buy",
    "shell",
    "confirm_shell",

    "switch_level",
    "green",

    "unlock_land",
    "shell",
    "map",

    "stragglers",
    "suppress",
    "search",
    "plus",
    "minus",
    "food_type",
    "wood_type",
    "stone_type",
    "iron_type",
    "go",
    "gather",
    "set_out",


    "lord_info",

    "check_details",
    "march_limit_3",
    "march_limit_2",
    "march_limit_1",
    "march_limit_0",

    "lord_skills",
    "development_skills",
    "lord_skill",
    "upgrade_to_max",
    "skill_points_0",

    "more_marches",
    "speed_up_march",
    "withdraw",
    "book",
    "elite_mines",
    "blue",
    "check",

    "leo",
    "haac",
    "hac",
    "VIChac",
    'farm,hacen',
    "kazuru_farm5",
    "kazuru_farm6",

    "avatar",
    "account",
    "bind",
    "change_name",
    "2-16_characters",
    "change_name_green",
    "switch",
    "new_game",
    "realm",
    "man",
    "blue_bonus",
    "confirm_bonus",
    "quit",
    "quest_complete",
    "bella",
    "level",
    "challenge",
    "bright_challenge",
    "backhand",
    "first_castle",
    "new_monster",
    "kingroad",
    "kingroad_claim",
    "kingroad_go",
    "kingroad_done",
    "start_upgrading",

    "heroic_evolution",
    "heroic_evoluation_blue",
    "go_blue",
    "evolve",
    "free",
    "unlock",
    "check_beast",
    "login",
    "gmail",
    "acc_list",
    "green_castle",
    "castle",
    "confirm",
    "no",
    "frozen_screen",

    "castle_level_4",
    "castle_level_5",
    "castle_level_6",
    "castle_level_7",
    "castle_level_8",
    "castle_level_9",
    "castle_level_10",
    "castle_level_11"
]



objects: dict[ScreenObjectNames, ScreenObject] = cast(
    dict[ScreenObjectNames, ScreenObject],
    get_objects(SAMPLES_DIR, REGIONS_DIR)
)

equipment = {
    objects['weapon'],
    objects['helmet'],
    objects['belt'],
    objects['accessory'],
    objects['clothes'],
    objects['boots'],
}

resources_technology = {
    objects['saw'],
    objects['plow'],
    objects['load_boost'],
    objects['sickle'],
    objects['axe'],
}

castle_levels = {
    int(name[13]): obj
    for name, obj in objects.items()
    if name.startswith(f'castle_level_')
}

resources_need = {
    name.removeprefix("need_"): obj
    for name, obj in objects.items()
    if name.startswith("need_")
}
