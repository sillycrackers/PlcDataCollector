pyinstaller --onefile ^
--add-data=".\src\gui\imgs:.\src\gui\imgs" ^
--add-data=".\src\PLC Data Collector Manual.pdf:.\src" ^
--paths .\src:.\src\gui:.\src\gui\imgs ^
--icon .\src\gui\imgs\data_icon.ico ^
--name "PlcDataCollector"^
 .\src\main.py