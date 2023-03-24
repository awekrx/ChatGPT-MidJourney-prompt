prompt_models = {
    "weights": "weights",
    "artistic": "artistic",
}

types = {
    "anime": "anime style::5 --upanime",
    "photorealistic": "high quality photo::5, soft light::2, sharp-focus::3, hyper realism::4",
    "avatar": "high quality avatar::5, circle::5, square::5, sharp-focus::5",
    "couple avatar": "anime::5, huge::4, kiss:4, high quality avatar::3, girl and boy::5, romantic::3",
}

contents: dict[str, str] = {
    "character": "character design::4",
    "landscape": "landscape design::4",
    "object": "object design::4, one object::5, high object details::3, --no background-details, --no background",
    "light": "light-design::4, shaders::3",
    "particles": "particle design::4, particles::3, smoke::2, neon::2, flash::2, spark::2",
}

renderers = {
    "octane": "octane render::4",
    "unreal engine": "unreal engine::4",
    "ray tracing": "ray tracing::4, v-ray::4",
    "mixed": "octane render::3 unreal engine::3, v-ray::3",
}

aspect_ratios = {
    "1:1": "--ar 1:1",
    "1:2": "--ar 1:2",
    "2:1": "--ar 2:1",
    "2:3": "--ar 2:3",
    "3:2": "--ar 3:2",
    "4:5": "--ar 4:5",
    "5:4": "--ar 5:4",
    "4:7": "--ar 4:7",
    "7:4": "--ar 7:4",
    "16:9": "--ar 16:9",
    "9:16": "--ar 9:16",
}
