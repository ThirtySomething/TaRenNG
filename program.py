from zipfile import Path

from tarenng import Config, TaRenNG

if __name__ == "__main__":
    config: Config = Config()
    config_file: Path = config.get_app_config()
    if not config_file.exists():
        config.save()
    program: TaRenNG = TaRenNG(config)
    program.process()
