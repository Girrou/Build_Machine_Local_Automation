@ECHO OFF
::SEtting Global Variables
:: Batch file location
set local=%~dp0
:: Build Machine file location
set BM_location=C:\src\beats_ip_mstp_buildmachine_flashloader\Build_Machine\
:: Binary file location and name
set BIN_location=C:\src\ip-vav\master\in4ps-firmware.build\in4ps-firmware.AL_IPVAV.IP.FreeRTOS.RelWithDebInfo.arm_gnu\
set BIN_name=in4ps-firmware
::ECC signing certificate info
set project_name=ALRIPVAV
set ecc_signing_certificate_file=C:\Code_Signing\ALRIPVAV.crt
set ecc_signing_worker_name="ALRIPVAV"
set ecc_signing_fixture_name="alr_fixture"
::CST certificate info
set SigningCertificate=C:\Code_Signing\ALRIPVAV_RSA.pem
set FixtureCertificate=CurrentUser\MY\497CDD877015CAC7D4372CC166E119A82AD3D585
set WorkerName=ALRIPVAV_RSA
::AppKicker
set AppKicker=app_kicker_IPVAV.out
set fwversion=v1.9.2.3
::Python - usar Python nativo Windows (no MSYS2) para evitar problemas con paths
set PYTHON=C:\Users\H298704\AppData\Local\Programs\Python\Python37-32\python.exe
::MFGTOOL file location
set MFGTOOL_location=C:\src\beats_ip_mstp_buildmachine_flashloader\Flashloader_RT1050_1.1\Tools\mfgtools-rel\Profiles\MXRT105X\OS Firmware\
::Setting and reviewing prerequisites
powershell -Command "& {Get-ChildItem -Path Cert:\CurrentUser\My; Set-ItemProperty -Path HKLM:\Software\Policies\Microsoft\Windows\PowerShell -Name ExecutionPolicy -Value ByPass; Get-ExecutionPolicy -List}"
::Updating info in the Build Machine
cd %local%
%PYTHON% check_FW_version.py %BM_location% %BIN_location% %BIN_name% %ecc_signing_certificate_file% %ecc_signing_worker_name% %ecc_signing_fixture_name% %SigningCertificate% %FixtureCertificate% %WorkerName% %AppKicker% %fwversion%
IF ERRORLEVEL 1 (
    echo [ERROR] check_FW_version.py fallo
    PAUSE
    EXIT /B 1
)
::Running Build Machine
cd %BM_location%
cd MainScript
%PYTHON% buildMachineTool.py IPVAV
IF ERRORLEVEL 1 (
    echo [ERROR] buildMachineTool.py fallo
    PAUSE
    EXIT /B 1
)
echo Script to delete files
del "%MFGTOOL_location%\*.sb" /f /q
del "%MFGTOOL_location%\*.imx" /f /q
del "C:\Alerton\Compass\2.0\System\app33.bin" /f /q
del "C:\Alerton\Compass\2.0\System\app33.info" /f /q
del "C:\Alerton\Compass\2.0\System\app34.bin" /f /q
del "C:\Alerton\Compass\2.0\System\app34.info" /f /q
del "C:\Alerton\Compass\2.0\System\app35.bin" /f /q
del "C:\Alerton\Compass\2.0\System\app35.info" /f /q
del "C:\Alerton\Compass\2.0\System\app36.bin" /f /q
del "C:\Alerton\Compass\2.0\System\app36.info" /f /q
echo Script to copy files
xcopy /Y "%BM_location%\MainScript\output\in4ps-firmware\FactoryImages\flash_Loader.imx" "%MFGTOOL_location%\"
xcopy /Y "%BM_location%\MainScript\output\in4ps-firmware\FactoryImages\factory_config.sb" "%MFGTOOL_location%\"
xcopy /Y "%BM_location%\MainScript\output\in4ps-firmware\FactoryImages\factory_image.sb" "%MFGTOOL_location%\"
xcopy /Y "%BM_location%\MainScript\output\in4ps-firmware\FactoryImages\hab_efuse.sb" "%MFGTOOL_location%\"
xcopy /Y "%BM_location%\MainScript\output\in4ps-firmware\FieldImage\app33.bin" "C:\Alerton\Compass\2.0\System\"
xcopy /Y "%BM_location%\MainScript\output\in4ps-firmware\FieldImage\app33.info" "C:\Alerton\Compass\2.0\System\"
echo Done!
PAUSE 