from dataclasses import dataclass
import json

LANGUAGES_FILE_INDEX = "./lang/__index__.json"


@dataclass
class _langData:
    title: str = None
    subtitle: str = None
    mousePosition: str = None
    mouseColor: str = None
    mouseSpeed: str = None
    mouseSpeedDesc: str = None
    isMouseStopped: str = None
    false: str = None
    true: str = None
    mouseSensitivity: str = None
    medium: str = None
    colorIntensity: str = None
    redIntensity: str = None
    greenIntensity: str = None
    blueIntensity: str = None
    windowInformation: str = None
    windowTitle: str = None
    windowChanged: str = None


class _langManager:
    language: str
    langJson: dict
    _data: _langData

    def __init__(self, language: str = None) -> None:
        if language is None:
            self.language = self.getLanguageFromFile()
        else:
            self.language = language
        self._data = _langData()
        self.syncFromFile()

    def getData(self):
        return self._data

    def syncFromFile(self):
        with open(LANGUAGES_FILE_INDEX) as indexFile:
            langFilename = json.load(indexFile)[0][self.language]
            with open(f"./lang/{langFilename}.json", encoding="UTF-8") as langFile:
                self.langJson = json.load(langFile)

        for key, value in self.langJson.items():
            setattr(self._data, key, value)

    @staticmethod
    def getLanguageFromFile():
        with open(LANGUAGES_FILE_INDEX) as indexFile:
            langName = json.load(indexFile)[1]["language"]
            return langName


# 初始化语言管理器
langManager = _langManager()
lang = langManager.getData()
