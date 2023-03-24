from .default import prompt_models
from .default import contents
from .default import renderers

niji_settings = {
    "prompt_models": prompt_models,
    "contents": contents,
    "renderers": renderers,
    "aspect_ratios": {
        "1:2": "--ar 1:2",
        "2:1": "--ar 2:1",
    },
}
