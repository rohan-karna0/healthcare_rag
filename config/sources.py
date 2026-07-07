from dataclasses import dataclass


@dataclass(frozen=True)
class SourceConfig:
    name: str
    base_url: str
    seed_urls: list[str]
    allowed_domains: list[str]


SOURCE_CONFIGS: dict[str, SourceConfig] = {
    "ADA": SourceConfig(
        name="ADA",
        base_url="https://diabetes.org",
        seed_urls=[
            "https://diabetes.org/about-diabetes",
            "https://diabetes.org/healthy-living",
        ],
        allowed_domains=["diabetes.org", "www.diabetes.org"],
    ),
    "WHO": SourceConfig(
        name="WHO",
        base_url="https://www.who.int",
        seed_urls=[
            "https://www.who.int/health-topics/diabetes",
            "https://www.who.int/news-room/fact-sheets/detail/diabetes",
        ],
        allowed_domains=["who.int", "www.who.int"],
    ),
    "CDC": SourceConfig(
        name="CDC",
        base_url="https://www.cdc.gov",
        seed_urls=[
            "https://www.cdc.gov/diabetes/about/index.html",
            "https://www.cdc.gov/diabetes/basics/index.html",
        ],
        allowed_domains=["cdc.gov", "www.cdc.gov"],
    ),
    "NIDDK": SourceConfig(
        name="NIDDK",
        base_url="https://www.niddk.nih.gov",
        seed_urls=[
            "https://www.niddk.nih.gov/health-information/diabetes",
            "https://www.niddk.nih.gov/health-information/diabetes/overview/what-is-diabetes",
        ],
        allowed_domains=["niddk.nih.gov", "www.niddk.nih.gov"],
    ),
    "FDA": SourceConfig(
        name="FDA",
        base_url="https://www.fda.gov",
        seed_urls=[
            "https://www.fda.gov/consumers/womens-health-topics/diabetes",
            "https://www.fda.gov/drugs/information-consumers-and-patients-drugs/diabetes-medicines",
        ],
        allowed_domains=["fda.gov", "www.fda.gov"],
    ),
}


def get_source_names() -> list[str]:
    return list(SOURCE_CONFIGS.keys())


def get_sources(names: list[str] | None = None) -> list[SourceConfig]:
    if not names:
        return list(SOURCE_CONFIGS.values())
    return [SOURCE_CONFIGS[name] for name in names if name in SOURCE_CONFIGS]
