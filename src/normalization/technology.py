TECHNOLOGY_ALIASES = {
    "python": "Python",
    "py": "Python",

    "aws": "AWS",
    "amazon web services": "AWS",

    "docker": "Docker",

    "tensorflow": "TensorFlow",
    "tf": "TensorFlow",

    "kubernetes": "Kubernetes",
    "k8s": "Kubernetes",

    "javascript": "JavaScript",
    "js": "JavaScript",

    "typescript": "TypeScript",
    "ts": "TypeScript",

    "react": "React",
    "reactjs": "React",

    "postgresql": "PostgreSQL",
    "postgres": "PostgreSQL"
}


# ======================================================================================
# Important: this isn't resume-format hardcoding.

# We're not saying:
# skills appear under SKILLS section.

# We're saying:
# These are known technology concepts and their aliases.

# Later we'll expand this using a proper technology taxonomy and model-assisted recognition.

"""
FILE PURPOSE:
Converts different names or aliases of the same technology into
one canonical value.

Examples:
AWS / Amazon Web Services -> AWS
K8s / Kubernetes -> Kubernetes
ReactJS / React -> React

Normalization prevents the matching system from treating aliases
as different skills.

LIMITATION:
The current implementation relies on known mappings and may miss
unknown aliases.
"""